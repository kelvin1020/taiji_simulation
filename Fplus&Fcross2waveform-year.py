#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import time                     #python 自带
from astropy.time import Time   #astropy 
from astropy import units as u 
from astropy import constants as const #import constants 
from astropy.coordinates import cartesian_to_spherical
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS
import ligo.skymap.plot

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from moviepy.video.io.bindings import mplfig_to_npimage#动图生成
import moviepy.editor as mpy

####teukolsky
from lib.waveform import teukolsky
from lib.waveform import get_td_waveform

from scipy.interpolate import interp1d


# Constants
G = (const.G).value # gravitational constant
C = (const.c).value # the speed of light


def randUnitVec(number):
    phi      = np.random.rand(number,1) * 2 * np.pi  #方位角
    costheta = np.random.rand(number,1) * 2 - 1
    x = np.sqrt(1 - costheta**2) * np.cos(phi)
    y = np.sqrt(1 - costheta**2) * np.sin(phi)
    z = costheta
    r = np.concatenate([x, y, z], axis = 1)
    return r #(x,y,z)

def vecCross(a, b):
    e = np.zeros((3, 3, 3))
    e[0, 1, 2] = e[1, 2, 0] = e[2, 0, 1] = 1
    e[0, 2, 1] = e[2, 1, 0] = e[1, 0, 2] = -1

    c = [np.einsum("i,j,ijk->k", a[i,:],b[i,:], e) for i in range(0, len(a))]
    return np.vstack(c) #(x,y,z)

def vecDot(a, b):
    c = [np.inner(a[i],b[i]) for i in range(0, len(a))]
    return np.vstack(c) #(x,y,z)


def cart2spher(r):
    ans   =  cartesian_to_spherical(r[:,0], r[:,1], r[:,2])
    theta = ((np.pi/2 * u.radian - ans[1][0]) ).to('deg').value
    phi   = ans[2][0].to('deg').value
    return theta, phi


def transMat(ex, ey, ez):
    c = [np.vstack([ex[i], ey[i], ez[i]]) for i in range(0, len(ex))]
    return c


def W2ThetaPhi(trans, NVec):
    wt      = np.vstack([(np.inner(trans[i], NVec)).T for i in range(0, len(trans))])
    ewt     = wt / np.linalg.norm(wt, axis=1, keepdims=True)
    rLatLon = cartesian_to_spherical(ewt[:,0], ewt[:,1], ewt[:,2])
    theta   = np.pi/ 2 - rLatLon[1].value  #theta
    phi     = rLatLon[2].value # phi
    thetaPhi= np.vstack([theta, phi]).T
    return thetaPhi

def LNZ2Psi(LVec, NVec, ezd):
    psi = [np.arctan((vecDot(LVec, np.array([ezd[i]]) ) - vecDot(LVec, NVec) * vecDot(np.array([ezd[i]]), NVec))                           / vecDot(NVec, vecCross(LVec, np.array([ezd[i]])))) for i in range(0, len(ezd))]
    return np.vstack(psi)


def Fplus1(theta, phi, psi):
    return 1/2 * (1 + (np.cos(theta))**2) * np.cos(2 * phi) * np.cos(2 * psi) - np.cos(theta)* np.sin(2 * phi) * np.sin(2 * psi) 

def Fcross1(theta, phi, psi):
    return 1/2 * (1 + (np.cos(theta))**2) * np.cos(2 * phi) * np.sin(2 * psi) + np.cos(theta)* np.sin(2 * phi) * np.cos(2 * psi) 


def Fplus2(theta, phi, psi):
    return 1/2 * (1 + (np.cos(theta))**2) * np.sin(2 * phi) * np.cos(2 * psi) + np.cos(theta)* np.cos(2 * phi) * np.sin(2 * psi) 

def Fcross2(theta, phi, psi):
    return 1/2 * (1 + (np.cos(theta))**2) * np.sin(2 * phi) * np.sin(2 * psi) - np.cos(theta)* np.cos(2 * phi) * np.cos(2 * psi) 



def WaveDataOut(**kwargs):
    #   Parameters
    duration = 86400 * 365          #信号持续时间(duration of signal) 2^16, 0.75d, 2^25 ,1.06yr
    step = 4

    atilde = np.sqrt(kwargs['SpinxBH']**2 + kwargs['SpinyBH']**2 + kwargs['SpinzBH']**2)  # 自旋参量
    nu = kwargs['MassCO'] / kwargs['MassBH'] # 质量比? 对称质量比
    M = ((kwargs['MassBH'] + kwargs['MassCO']) * const.M_sun).to(u.kg).value  #the mass of system, kilogram
    # m = (1e1 * const.M_sun).to(u.kg).value  #the mass of small compact body, kilogram

    l = np.arange(2,3)      
    # m = 2
    k = np.arange(-2,12,1)                   #the nth harmonic

    ########################
    R_unit = (G * M / C**2)#                #the unit length in G = C = 1 system, metre
    # t_unit = R_unit / C    #                #the unit time in G = C = 1 system, second
    ########################

    e = kwargs['ECC']                                 #eccentricity of orbit
    p = kwargs['PM']  * R_unit                         #semi-latus rectum

    a = p / (1 - e**2)                      #the semi-major axis of orbit, metre

    D = (1.00 * u.Gpc).to('m').value

    wave = teukolsky(atilde = atilde, nu = nu, M = M, l = l, k = k, e = e, a = a, D = D)
    wave.ecalculate(duration = duration, delta_t = step)
    hp, hc = get_td_waveform(template=wave)

    timeVec = (np.array(hp.sample_times)).reshape(-1, 1)
    hpVec =  (np.array(hp)).reshape(-1, 1)
    hcVec =  (np.array(hc)).reshape(-1, 1)
    waveMat = np.concatenate((timeVec, hpVec, hcVec), axis = 1)
    waveData = pd.DataFrame(waveMat, columns = ['timeSecond', 'hp', 'hc'])
#     waveData.to_csv('waveDataEMRI.dat')# columns=['JDTimeTCB']  #导出csv文件
    return waveData


# In[ ]:


MassBH    = 1e6
SpinxBH   = 0
SpinyBH   = 0
SpinzBH   = 0.9
MassCO    = 1e1
SpinxCO   = 0 
SpinyCO   = 0
SpinzCO   = 90
ECC       = 0.5
PM        = 20
IOTA      = 0.25


kwargs = dict(MassBH=MassBH, SpinxBH=SpinxBH, SpinyBH=SpinyBH, SpinzBH=SpinzBH,     MassCO=MassCO, SpinxCO=SpinxCO, SpinyCO=SpinyCO, SpinzCO=SpinzCO, ECC=ECC, PM=PM, IOTA=IOTA)

wave = WaveDataOut(**kwargs)
wave.to_csv('waveDataEMRIyear.dat')# columns=['JDTimeTCB']  #导出csv文件

