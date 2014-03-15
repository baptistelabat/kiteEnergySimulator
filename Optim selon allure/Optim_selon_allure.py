import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np
from numpy import pi
import Wind_Power2
import cfg

Polar=np.zeros((6,90))
Xo=(5.,0.5,0.)
bnds=((0.,None),(0.,pi/2),(-pi/2,pi/2))

for k in np.arange(90):
    windir=2*k*pi/180
    Xopt=minimize(Wind_Power2.Power,Xo,args=(cfg.U_wind,windir),method='L-BFGS-B',bounds=bnds,tol=10e-12,options={'maxiter':100, 'disp':True})
    Polar[0,k]=windir
    Polar[1:4,k]=Xopt.x
    Polar[4,k]=-Wind_Power2.Power(Xopt.x,cfg.U_wind,windir)
    Polar[5,k]=Xopt.success


plt.plot(Polar[0,:]*180/pi,Polar[1,:],'b')
plt.plot(Polar[0,:]*180/pi,Polar[2,:]*180/pi,'g')
plt.plot(Polar[0,:]*180/pi,Polar[3,:]*180/pi,'y')
plt.plot(Polar[0,:]*180/pi,np.log10(Polar[4,:])*10,'--')
plt.plot(Polar[0,:]*180/pi,Polar[5,:]*50,'r')
plt.show()
