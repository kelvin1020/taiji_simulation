# gravitational wave source EMRI/IMRI parameters
# !/usr/bin/python
# -*- coding: UTF-8 -*-

import sympy as sp #导入sympy包中的函数
import gravipy as gp #导入gravipy包的函数
import numpy as np  #导入numpy包的函数
import math
#if sourcetype = 'EMRI' or 'IMRI' 
# intrinstic parameters
MassBH     = 1e6    # mass of central MBH, in unit of sun 
SpinxBH    = 0      # spin of central MBH in x direction, dimensionless
SpinyBH    = 0      # spin of central MBH in y direction, dimensionless
SpinzBH    = 0.5    # spin of central MBH in z direction, dimensionless                                            
MassCO     = 1e2    # mass of small compact object, in unit of sun     
SpinxCO    = 0      # spin of small compact object in x direction, dimensionless  
SpinyCO    = 0      # spin of small compact object in y direction, dimensionless
SpinzCO    = 0      # spin of small compact object in z direction, dimensionless
massratio  = MassCO/MassBH # mass ratio of system
ECC        = 0.5    # eccentricity of orbit
PM         = 8.0    # semi-latus of orbit
IOTA       = np.pi/4 # orbital inclination                                                             
