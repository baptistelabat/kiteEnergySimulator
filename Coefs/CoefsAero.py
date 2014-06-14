#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Load Aerodynamic coefficients CLift (CL) et CDraft (CD) from our files.dat
"""
from numpy import load
from numpy import pi
from scipy import interp
import wing_cfg
import matplotlib.pyplot as plt
import numpy as np

filename    = wing_cfg.Wing # The profil is chosen in wing_cfg.py
coefs       = load(filename)

AoA_index, CL_index, CD_index  = range(3)

# Lift coefficient
def CL(alpha):
    return interp(alpha, coefs[:, AoA_index], coefs[:, CL_index])
    
# Drag coefficient
def CD(alpha):
    return interp(alpha, coefs[:, AoA_index], coefs[:, CD_index])

def CLoverCD(alpha):
    return CL(alpha)/CD(alpha)

# Plot Aerodynamic glide ratio of our profil
angles = np.linspace(0, np.pi, num = 500)

glide_ratio = [CLoverCD(angle) for angle in angles]

if False: 
    plt.plot(180./(np.pi)*angles, glide_ratio,'bx', label='Profil chosen') 
    plt.xlabel('Angle of attack (deg)')
    plt.ylabel('Cl/Cd') 
    plt.legend()
    plt.show()
