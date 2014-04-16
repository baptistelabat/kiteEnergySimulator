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
import os

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
folder="."
os.chdir(folder)
filename="DU21_A17.dat"

#Input file reading  
fileId=open(filename)
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
        
filename=filename.replace('.dat','.npy')
np.save(filename,coefs)

def poly_trigo(a,x):
    p=0    
    for i in np.arange(0,15):
        p=p+a[2*i]*np.cos(i*x*pi/180)
    for i in np.arange(0,15):
        p=p+a[2*i+1]*np.sin((i+1)*x*pi/180)
    return p
    

def residual(a,y,x):
    err=y-poly_trigo(a,x)
    return err

a0=np.ones(30)
CL_poly=leastsq(residual,a0,args=(coefs[:,1],coefs[:,0]))
CL_poly=CL_poly[0]
filename=filename.replace('.npy','_CL.npy')
np.save(filename,CL_poly)
print(CL_poly)
CD_poly=leastsq(residual,a0,args=(coefs[:,2],coefs[:,0]))
CD_poly=CD_poly[0]
filename=filename.replace('CL','CD')
np.save(filename,CD_poly)
print(CD_poly)


plt.plot(coefs[:,0],coefs[:,1],'r')
plt.plot(coefs[:,0],poly_trigo(CL_poly,coefs[:,0]),'r+')
plt.plot(coefs[:,0],coefs[:,2],'b')
plt.plot(coefs[:,0],poly_trigo(CD_poly,coefs[:,0]),'b+')
plt.show()
