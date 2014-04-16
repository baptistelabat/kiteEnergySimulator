"""
Load Aerodynamic coefficients CLift (CL) et CDraft (CD) from our files.dat
"""
from numpy import load
from numpy import pi
from scipy import interp
import wing_cfg
import matplotlib.pyplot as plt
import numpy as np

filename=wing_cfg.Wing # the profil is chosen in cfg.py
coefs=load(filename)


# Lift coefficient
def CL(alpha):
    return interp(alpha*180/pi,coefs[:,0],coefs[:,1])
    
# Drag coefficient
def CD(alpha):
    return interp(alpha*180/pi,coefs[:,0],coefs[:,2])

def CLoverCD(alpha):
    return CL(alpha)/CD(alpha)

# Plot Aerodynamic Finess of our profil
angle=np.pi/180*np.linspace(0,180,500)

finesse=np.empty(len(angle))
for i in np.arange(0,len(angle)):
    finesse[i] =CLoverCD(angle[i])
    
plt.plot(180./(np.pi)*angle,finesse,'bx',label='Profil chosen') 
plt.xlabel('Angle d''incidence (deg)')
plt.ylabel('Cl/Cd') 
plt.legend()
plt.show()
