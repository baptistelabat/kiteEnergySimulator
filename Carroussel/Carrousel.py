#!/usr/bin/env python
# -*- coding: utf8 -*-
# Licensed under the MIT License,
# https://github.com/baptistelabat/kiteEnergySimulator
# @author: Charles Spraul
# Created on Fri Mar 14 16:04:44 2014

from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

import sys
sys.path.append('../Optim')

import Wind_Power_Car as WPC

cmptKA = 0
cmptPower = 0
global n

def Kite_Attitude(U, WD):# Define loads exerced on the kite according to the Wind direction WD. U is the trolley speed
    global cmptKA, cmptPower, n
    cmptKA      += 1
    AnglesOpti  = (0., 0.)
    Pmax        = -1e15
    
    # Alpha angle
    amin        = -pi/20.
    amax        = pi/2.
    da          = amax-amin
    
    # Beta angle
    bmin        = -pi/2.
    bmax        = pi/2.
    db          = bmax-bmin
    
    while db > 0.001: # Convergence criterion
        # Loop on alpha and beta angles and find maxima
        for a in np.linspace(amin + da/(n+1), amax - da/(n+1), n):
                for b in np.linspace(bmin + db/(n+1), bmax - db/(n+1), n):
                    Angles = (a, b)
                    [Fx, Fy, Fz, X, Y, Z] = WPC.ComputeEquilibrium(Angles, U, WD)
                    P = WPC.Power(Fx, U)
                    cmptPower += 1
                    if (P>Pmax and Z>25): # Do not allow solution where kite is too close to the ground
                        AnglesOpti = Angles
                        Pmax = P
                        Polar = (Angles[0], Angles[1], X, Y, Z, Fx, Fy, Fz, P)
        # Compute the new range where to find optimum                
        amin    = AnglesOpti[0] - da/(n+1)
        amax    = AnglesOpti[0] + da/(n+1)
        da      = amax - amin
        bmin    = AnglesOpti[1] - db/(n+1)
        bmax    = AnglesOpti[1] + db/(n+1)
        db      = bmax-bmin
    return Polar # Polar contains all the information about loads, position, and angles

def f(U): # f is the function used in the optimisation of the trolley speed.
    global npt
    P = 0.
    Polar = np.zeros((9, npt))
    for wd in np.arange(npt):
        Polar[:, wd] = Kite_Attitude(U, 360/npt*wd*pi/180.)
        P = P + Polar[8, wd]/npt
    return(-P)

n = 15.
npt = 60 # number of discretization points for the carrousel circle
Uopt = minimize_scalar(f, bounds=[1., 500.], method='Bounded') #optimisation of
print'Uopt', Uopt.x
print'La fonction Kite_Allure a ete lancee', cmptKA,'fois (', cmptKA/npt, 'vitesses testees)'
print'La fonction Power a ete lancee', cmptPower,'fois, soit', cmptPower/cmptKA, 'fois en moyenne'


P = 0. #P is the Power
Polar = np.zeros((9, npt))
for wd in np.arange(npt):
    Polar[:, wd] = Kite_Attitude(Uopt.x, 360/npt*wd*pi/180.)
    P = P + Polar[8, wd]/npt
print'Average power (W) =', P
    
plt.figure(1)
plt.subplot(1,3,1)
plt.plot(360/npt*np.arange(npt), Polar[0,:]*180/pi, 'bx', label='alpha') # alpha
plt.plot(360/npt*np.arange(npt), Polar[1,:]*180/pi, 'rx', label='beta') # beta
plt.xlabel('Wind Direction (deg)')
plt.ylabel('Optimal Kite Angles (deg)')
plt.axis([0, 360, -90, 90])
plt.legend()
plt.subplot(1,3,2)
plt.plot(360/npt*np.arange(npt), Polar[4,:], 'y')        # altitude du kite
plt.xlabel('Wind Direction (deg)')
plt.ylabel('Altitude of the Kite (m)')
plt.xlim(0, 360)
plt.subplot(1, 3, 3)
plt.plot(360/npt*np.arange(npt), Polar[8, :], 'go')   # Power
plt.xlabel('Wind Direction (deg)')
plt.ylabel('Power (W)')
plt.xlim(0, 360)
plt.show()




