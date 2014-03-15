#import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

# Lift coefficient
def CL(alpha):
    if alpha < pi*15/180:
        return 1.5*np.sin(alpha*90/15)
    else:
        return 1.5*(-2*((alpha-90*pi/180)/(-75*pi/180))**3+3*((alpha-90*pi/180)/(-75*pi/180))**2)
        
    #table=[ 0., 2., 3., 2.5, 2., 1.8, 1.5, 1., 0.]    #1.5*np.cos((alpha-pi*15/180)*90/(90-15))
    #return sp.interp(alpha, pi/16*np.arange(0,9), table)
	
# Drag coefficient
def CD(alpha):
    return 1.5*(alpha/90/pi*180)**2 + 0.02
    #table=[ 0., 0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4.]
    #return sp.interp(alpha, pi/16*np.arange(0,9), table)
	
def dCLdalpha(alpha):
    if alpha < pi*15/180:
        return 1.5*90/15*np.cos(alpha*90/15)
    else:
        return -1.5*90/(90-15)*np.sin((alpha-pi*15/180)*90/(90-15))

def CLoverCD(alpha):
    return CL(alpha)/CD(alpha)


#nn=180
## Define the angle of attack
#alpha_deg = np.linspace(0., 90.,nn)
#
#F=np.zeros((nn,4))
#for i in np.arange(nn):
#    F[i,0]=CL(pi*alpha_deg[i]/180)
#    F[i,1]=CD(pi*alpha_deg[i]/180)
#    F[i,2]=CLoverCD(pi*alpha_deg[i]/180)
#    F[i,3]=dCLdalpha(pi*alpha_deg[i]/180)
#
#plt.plot(alpha_deg, F[:,0],'b')
#plt.plot(alpha_deg, F[:,1],'r')
##plt.plot(alpha_deg, F[:,2],'g')
##plt.plot(alpha_deg, F[:,3],'y--')
#plt.show()


