#!/usr/env python

"""SPEC.PY - Spectroscopy tools

"""

from __future__ import print_function

__authors__ = 'David Nidever <dnidever@montana.edu>'
__version__ = '20210605'  # yyyymmdd

# Imports

import os
import numpy as np
import copy
import time
import warnings
from astropy.io import fits
from astropy.table import Table
from dlnpyutils.minpack import curve_fit
from dlnpyutils import utils as dln, bindata, robust
from numpy.polynomial.polynomial import polyfit as npp_polyfit, polyval as npp_polyval
from scipy import ndimage
from scipy.signal import medfilt, argrelextrema
from scipy.ndimage.filters import median_filter,gaussian_filter1d
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit, least_squares
from scipy.special import erf, wofz
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.legend import Legend

try:
    import __builtin__ as builtins # Python 2
except ImportError:
    import builtins # Python 3

# Ignore these warnings, it's a bug
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

cspeed = 2.99792458e5  # speed of light in km/s

def gaussbin(x, amp, cen, sig, const=0, dx=1.0):
    """1-D gaussian with pixel binning
    
    This function returns a binned Gaussian
    par = [height, center, sigma]
    
    Parameters
    ----------
    x : array
       The array of X-values.
    amp : float
       The Gaussian height/amplitude.
    cen : float
       The central position of the Gaussian.
    sig : float
       The Gaussian sigma.
    const : float, optional, default=0.0
       A constant offset.
    dx : float, optional, default=1.0
      The width of each "pixel" (scalar).
    
    Returns
    -------
    geval : array
          The binned Gaussian in the pixel

    """

    xcen = np.array(x)-cen             # relative to the center
    x1cen = xcen - 0.5*dx  # left side of bin
    x2cen = xcen + 0.5*dx  # right side of bin

    t1cen = x1cen/(np.sqrt(2.0)*sig)  # scale to a unitless Gaussian
    t2cen = x2cen/(np.sqrt(2.0)*sig)

    # For each value we need to calculate two integrals
    #  one on the left side and one on the right side

    # Evaluate each point
    #   ERF = 2/sqrt(pi) * Integral(t=0-z) exp(-t^2) dt
    #   negative for negative z
    geval_lower = erf(t1cen)
    geval_upper = erf(t2cen)

    geval = amp*np.sqrt(2.0)*sig * np.sqrt(np.pi)/2.0 * ( geval_upper - geval_lower )
    geval += const   # add constant offset

    return geval


def gaussian(x, amp, cen, sig, const=0):
    """1-D gaussian: gaussian(x, amp, cen, sig)"""
    return amp * np.exp(-(x-cen)**2 / (2*sig**2)) + const


def gaussfit(x,y,initpar=None,sigma=None,bounds=(-np.inf,np.inf),binned=False):
    """Fit a Gaussian to data."""
    if initpar is None:
        initpar = [np.max(y),x[np.argmax(y)],1.0,np.median(y)]
    func = gaussian
    if binned is True: func=gaussbin
    return curve_fit(func, x, y, p0=initpar, sigma=sigma, bounds=bounds)



def wavesol(xpix,wave,order=3,xr=None):
    """
    Fit wavelength solution to X and Wavelength arrays.

    """

    n = len(xpix)
    if n<2:
        raise ValueError('Need at least two points.')
    if n<order+1:
        print('Warning: order='+str(order)+' but only '+str(n)+' points.  Reducing to order='+str(n-1))
        order = n-1

    # Robust polynomial fit
    coef = robust.polyfit(xpix,wave,order)

    # Generate output array of wavelength values
    if xr is None:
        xx = np.arange(np.floor(np.min(xpix)),np.ceil(np.max(xpix)))

    else:
        xx = np.arange(xr[0],xr[1])
    ww = npp_polyval(xx,coef)        

    return coef,ww
        

def trace(im,yestimate=None,yorder=2,sigorder=4,step=10):
    """ Trace the spectrum.  Spectral dimension is assumed to be on the horizontal axis."""
    ny,nx = im.shape
    if yestimate is None:
        ytot = np.sum(im,axis=1)
        yestimate = np.argmax(ytot)
    # Smooth in spectral dimension
    # a uniform (boxcar) filter with a width of 50
    smim = ndimage.uniform_filter1d(im, 50, 1)
    nstep = nx//step
    # Loop over the columns in steps and fit Gaussians
    tcat = np.zeros(nstep,dtype=np.dtype([('x',float),('pars',float,4)]))
    for i in range(nstep):
        pars,cov = dln.gaussfit(y[yestimate-10:yestimate+10],im[yestimate-10:yestimate+10,step*i+step//2])
        tcat['x'][i] = step*i+step//2
        tcat['pars'][i] = pars
    # Fit polynomail to y vs. x and gaussian sigma vs. x
    ypars = np.polyfit(tcat['x'],tcat['pars'][:,1],yorder)
    sigpars = np.polyfit(tcat['x'],tcat['pars'][:,2],sigorder)
    # Model
    mcat = np.zeros(nx,dtype=np.dtype([('x',float),('y',float),('sigma',float)]))
    xx = np.arange(nx)
    mcat['x'] = xx
    mcat['y'] = np.poly1d(ypars)(xx)
    mcat['sigma'] = np.poly1d(sigpars)(xx)
    return tcat, ypars, sigpars,mcat

def boxcar(im):
    """ Boxcar extract the spectrum"""
    ny,nx = im.shape
    ytot = np.sum(im,axis=1)
    yest = np.argmax(ytot)
    # Background subtract
    yblo = int(np.maximum(yest-50,0))
    ybhi = int(np.minimum(yest+50,ny))
    med = np.median(im[yblo:ybhi,:],axis=0)
    medim = np.repeat(med,ny).reshape(ny,nx)
    subim = im.copy()-medim
    # Sum up the flux
    ylo = int(np.maximum(yest-20,0))
    yhi = int(np.minimum(yest+20,ny))
    flux = np.sum(subim[ylo:yhi,:],axis=0)
    return flux

def gaussline(x, amp, cen, sigma, const=0):
    """1-D gaussian: gaussian(x, amp, cen, sig)"""
    return amp * np.exp(-(x-cen)**2 / (2*sigma**2)) + const

def fitlines(x,y,err=None,nsig=5):
    """ Automatically detect emission lines and fit Gaussians to them."""

    n = len(x)
    sm = 101
    
    # Detect peaks
    med = medfilt(y,sm)
    sig = dln.mad(y-med,zero=True)
    peaks, = argrelextrema(y,np.greater)
    good, = np.where((y[peaks]-med[peaks] > nsig*sig) & (y[peaks]>0))
    ngood = len(good)
    if ngood==0:
        print('No peaks found')
        return None
    peaks = peaks[good]
    
    # Loop over peaks and fit Gaussians
    dt = np.dtype([('id',int),('xpeak',int),('amp',float),('xcen',float),('sigma',float),('const',float),
                   ('gpar',(float,4)),('gparerr',(float,4)),('flux',float),('success',bool)])
    out = np.zeros(ngood,dtype=dt)
    out['id'] = np.arange(ngood)+1
    for i in range(ngood):
        x0 = np.maximum(peaks[i]-15,0)
        x1 = np.minimum(peaks[i]+15,n-1)
        if err is not None:
            err1 = err[x0:x1+1]
        else:
            err1 = None
        initpar = [y[peaks[i]]-med[peaks[i]],peaks[i],5.0,med[peaks[i]]]
        lbounds = np.zeros(4,float)
        lbounds[1] = peaks[i]-2
        lbounds[3] = np.min(y)
        ubounds = np.zeros(4,float)
        ubounds[0] = np.inf
        ubounds[1] = peaks[i]+2
        ubounds[2] = np.inf
        ubounds[3] = np.max(y)
        bounds = (lbounds,ubounds)
        out['xpeak'][i] = peaks[i]
        try:
            par1, cov1 = curve_fit(gaussline, x[x0:x1+1], y[x0:x1+1], p0=initpar, bounds=bounds, sigma=err1)
            perror1 = np.sqrt(np.diag(cov1))
            flux1 = par1[0]*par1[2]*np.sqrt(2*np.pi)
            out['gpar'][i] = par1
            out['gparerr'][i] = perror1
            out['amp'][i] = par1[0]
            out['xcen'][i] = par1[1]
            out['sigma'][i] = par1[2]
            out['const'][i] = par1[3]            
            out['flux'][i] = flux1
            out['success'][i] = True
        except:
            out['amp'][i] = initpar[0]
            out['xcen'][i] = initpar[1]
            out['sigma'][i] = initpar[2]
            out['const'][i] = initpar[3]  
            out['success'][i] = False        
        
    return out
        
    
def linefit(x,y,initpar,bounds,err=None):
    # Fit Gaussian profile to data with center and sigma fixed.
    # for extracting spectra
    # initpar = [height, center, sigma, constant offset]
    cen = initpar[1]
    sigma = initpar[2]
    def gline(x, amp, const=0):
        """1-D gaussian: gaussian(x, amp, cen, sig)"""
        return amp * np.exp(-(x-cen)**2 / (2*sigma**2)) + const
    line_initpar = [initpar[0],initpar[3]]
    lbounds, ubounds = bounds
    line_bounds = ([lbounds[0],lbounds[3]],[ubounds[0],ubounds[3]])
    return curve_fit(gline, x, y, p0=line_initpar, bounds=line_bounds, sigma=err)


def extract(im,imerr=None,mcat=None,nobackground=False):
    """ Extract a spectrum"""
    ny,nx = im.shape
    x = np.arange(nx)
    y = np.arange(ny)
    # No trace information input, get it
    if mcat is None:
        tcat,ypars,sigpars,mcat=trace(im)
    # Loop over the columns and get the flux using the trace information
    cat = np.zeros(nx,dtype=np.dtype([('x',int),('pars',float,2),('perr',float,2),
                                      ('flux',float),('fluxerr',float)]))
    for i in range(nx):
        line = im[:,i].flatten()
        if imerr is not None:
            lineerr = imerr[:,i].flatten()
        else:
            lineerr = np.ones(len(line))   # unweighted
        # Fit the constant offset and the height of the Gaussian
        #  fix the central position and sigma
        ycen = mcat['y'][i]
        ysigma = mcat['sigma'][i]
        ht0 = np.maximum(line[int(np.round(ycen))],0.01)
        initpar = [ht0,ycen,ysigma,np.median(line)]
        if nobackground is True:
            initpar = [ht0,ycen,ysigma,0]
        # Only fit the region right around the peak
        y0 = int(np.maximum(ycen-50,0))
        y1 = int(np.minimum(ycen+50,ny))
        bnds = ([0,ycen-1e-4,ysigma-1e-4,0],[1.5*ht0,ycen,ysigma,1.5*initpar[3]])
        if nobackground is True:
            bnds = ([0,ycen-1e-4,ysigma-1e-4,0],[1.5*ht0,ycen,ysigma,0.1])
        pars,cov = linefit(y[y0:y1],line[y0:y1],initpar=initpar,bounds=bnds,err=lineerr[y0:y1])
        perr = np.sqrt(np.diag(cov))
        # Gaussian area = ht*wid*sqrt(2*pi)
        flux = pars[0]*ysigma*np.sqrt(2*np.pi)
        fluxerr = perr[0]*ysigma*np.sqrt(2*np.pi)
        cat['x'][i] = i
        cat['pars'][i] = pars
        cat['perr'][i] = perr
        cat['flux'][i] = flux
        cat['fluxerr'][i] = fluxerr
    return cat

def emissionlines(spec,thresh=None):
    """Measure the emission lines in an arc lamp spectrum. """
    nx = len(spec)
    x = np.arange(nx)
    
    # Threshold
    if thresh is None:
        thresh = np.min(spec) + (np.max(spec)-np.min(spec))*0.05
    
    # Detect the peaks
    sleft = np.hstack((0,spec[0:-1]))
    sright = np.hstack((spec[1:],0))
    peaks, = np.where((spec>sleft) & (spec>sright) & (spec>thresh))
    npeaks = len(peaks)
    print(str(npeaks)+' peaks found')
    
    # Loop over the peaks and fit them with Gaussians
    gcat = np.zeros(npeaks,dtype=np.dtype([('x0',int),('x',float),('xerr',float),('pars',float,4),('perr',float,4),
                                           ('flux',float),('fluxerr',float)]))
    resid = spec.copy()
    gmodel = np.zeros(nx)
    for i in range(npeaks):
        x0 = peaks[i]
        xlo = np.maximum(x0-6,0)
        xhi = np.minimum(x0+6,nx)
        initpar = [spec[x0],x0,1,0]
        bnds = ([0,x0-3,0.1,0],[1.5*initpar[0],x0+3,10,1e4])
        pars,cov = dln.gaussfit(x[xlo:xhi],spec[xlo:xhi],initpar,bounds=bnds,binned=True)
        perr = np.sqrt(np.diag(cov))
        gmodel1 = dln.gaussian(x[xlo:xhi],*pars)
        gmodel[xlo:xhi] += (gmodel1-pars[3])
        resid[xlo:xhi] -= (gmodel1-pars[3])
        # Gaussian area = ht*wid*sqrt(2*pi)
        flux = pars[0]*pars[2]*np.sqrt(2*np.pi)
        fluxerr = perr[0]*pars[2]*np.sqrt(2*np.pi)
        gcat['x0'][i] = x0
        gcat['x'][i] = pars[1]
        gcat['xerr'][i] = perr[1]
        gcat['pars'][i] = pars
        gcat['perr'][i] = perr
        gcat['flux'][i] = flux
        gcat['fluxerr'][i] = fluxerr
        
    return gcat, gmodel


def continuum(spec,bin=50,perc=60,norder=4):
    """ Derive the continuum of a spectrum."""
    nx = len(spec)
    x = np.arange(nx)
    # Loop over bins and find the maximum
    nbins = nx//bin
    xbin1 = np.zeros(nbins,float)
    ybin1 = np.zeros(nbins,float)
    for i in range(nbins):
        xbin1[i] = np.mean(x[i*bin:i*bin+bin])
        ybin1[i] = np.percentile(spec[i*bin:i*bin+bin],perc)
    # Fit polynomial to the binned values
    coef1 = np.polyfit(xbin1,ybin1,norder)
    cont1 = np.poly1d(coef1)(x)
    
    # Now remove large negative outliers and refit
    gdmask = np.zeros(nx,bool)
    gdmask[(spec/cont1)>0.8] = True
    xbin = np.zeros(nbins,float)
    ybin = np.zeros(nbins,float)
    for i in range(nbins):
        xbin[i] = np.mean(x[i*bin:i*bin+bin][gdmask[i*bin:i*bin+bin]])
        ybin[i] = np.percentile(spec[i*bin:i*bin+bin][gdmask[i*bin:i*bin+bin]],perc)
    # Fit polynomial to the binned values
    coef = np.polyfit(xbin,ybin,norder)
    cont = np.poly1d(coef)(x)
    
    return cont,coef
