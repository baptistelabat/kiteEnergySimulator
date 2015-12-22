# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 21:38:12 2014

@author: Quentin Renaud
"""
# Read the data file
import numpy as np
from numpy import pi
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import os

# Input file [Angle_deg Cl Cd Cm]
folder = "."
os.chdir(folder)
filename = "DU21_A17.dat"

coefs = np.genfromtxt(filename, dtype=float, skip_header=14)
# Convert first column to radians
coefs[:, 0] = pi/180*coefs[:, 0]
angles  = coefs[:, 0]
CL      = coefs[:, 1]
CD      = coefs[:, 2]

filename=filename.replace('.dat', '.npy')
np.save(filename, coefs)

def poly_trigo(a, theta, N=5):
    p = a[0]    
    for i in range(1, N+1):
        p = p + a[2*i-1]*np.cos(i*theta)
    for i in range(1, N+1):
        p = p + a[2*i]*np.sin(i*theta)
    return p
    

def residual(a, y, theta, N):
    err = y - poly_trigo(a, theta, N=N)
    return err

N = 15
a = np.ones(2*N+1)
CL_poly = leastsq(residual, a, args=(CL, angles, N))
CL_poly = CL_poly[0]
filename = filename.replace('.npy', '_CL.npy')
np.save(filename, CL_poly)
print(CL_poly)

CD_poly = leastsq(residual, a, args=(CD, angles, N))
CD_poly = CD_poly[0]
filename = filename.replace('CL', 'CD')
np.save(filename, CD_poly)
print(CD_poly)


p1, = plt.plot(angles*180/pi, CL, 'r+')
p2, = plt.plot(angles*180/pi, poly_trigo(CL_poly, angles, N), 'r')
p3, = plt.plot(angles*180/pi, CD, 'b+')
p4, = plt.plot(angles*180/pi, poly_trigo(CD_poly, angles, N), 'b')
plt.title("Coefficients de l'aile en fonction de AoA")
plt.legend([p1,p2,p3,p4],["Clift", "Poly_Clift", "Cdrag", "Poly_Cdrag"])
plt.show()
