# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 21:38:12 2014

@author: Quentin Renaud
"""
#Lecture du fichier de données
import numpy as np
from numpy import pi
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def el1(lineStr,symb):
    elFind=False
    for c in lineStr:
        if c!=symb:
            if not elFind:
                el=c
                elFind=True
            else:
                el=''.join([el,c])
        elif elFind:
            break
    return el

#Input file [Angle Cl Cd]
filename="DU21_A17.dat"

#Input file reading  
fileId=open(filename, "r")
data=fileId.readlines()
fileId.close()

line1=14 #1st line of the data file
s=np.size(data)
coefs=np.zeros((s-line1,3))

for line in np.arange(line1,s):
    dline=str(data[line])
    for i in np.arange(0,3):
        coefs[line-14,i]=el1(dline,' ')
        dline=dline.replace(el1(dline,' '),'',1)
        
filename='CoefsAero.npy'
np.save(filename,coefs)

def poly_even(a,x):
    p=0    
    for i in np.arange(0,10):
        p=p+a[i]*cos(i*x*pi/180)
    return p

def residual_even(a,y,x):
    err=y-poly_even(a,x)
    return err

def poly_odd(a,x):
    p=0    
    for i in np.arange(0,10):
        p=p+a[i]*sin((i+1)*x*pi/180)
    return p    

def residual_odd(a,y,x):
    err=y-poly_odd(a,x)
    return err

a0=np.ones(10)
CL_poly=leastsq(residual_odd,a0,args=(coefs[:,1],coefs[:,0]))
print(CL_poly[0])
CD_poly=leastsq(residual_even,a0,args=(coefs[:,2],coefs[:,0]))
print(CD_poly[0])


plt.plot(coefs[:,0],coefs[:,1],'r')
plt.plot(coefs[:,0],poly_odd(CL_poly[0],coefs[:,0]),'r+')
plt.plot(coefs[:,0],coefs[:,2],'b')
plt.plot(coefs[:,0],poly_even(CD_poly[0],coefs[:,0]),'b+')
plt.show()
