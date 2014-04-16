'''
File whith useful functions for Carrousel_optim

'''

# Optimiser l'angle d'incidence et la vitesse du chariot pour maximiser la puissance
# Renvoyer l'angle d'incidence, la vitesse chariot, les efforts aero et la puissance recuperable

import numpy as np
import cfg

import sys
sys.path.append('../Coefs')
import CoefsAero
import wing_cfg

#
def Apparent_Wind(U,Uwind,WDir):# Definition of the Apparent Wind. U = Speed of the trolley supposed equal to the kite speed
    Uapp=np.sqrt((np.cos(WDir)*Uwind-U)**2+(np.sin(WDir)*Uwind)**2)
    if WDir==0.:
        delta=(U>Uwind)*np.pi
    else:
        delta=2.*np.arctan((np.sin(WDir)*Uwind)/((np.cos(WDir)*Uwind-U)+Uapp))
    return (Uapp,delta)

#
def Forces(Angles,U,WDir):# Define loads applied to the kite wing
    alpha=Angles[0]
    beta=Angles[1]
    Uwind=cfg.Uwind
    Umem=0.
   # k=0
    while np.abs(Uwind-Umem)>10e-4: #Looking for the balance position
        [Uapp,delta]=Apparent_Wind(U,Uwind,WDir)
        Cl=CoeffAero.CL(alpha)
        Cd=CoeffAero.CD(alpha)
        Lift=1./2.*cfg.rho*cfg.Area*Cl*Uapp**2
        Draft=1./2.*cfg.rho*cfg.Area*Cd*Uapp**2
        Fx=np.cos(delta)*Draft+np.sin(delta)*np.sin(beta)*Lift
        Fy=np.sin(delta)*Draft+np.cos(delta)*np.sin(beta)*Lift
        Fz=np.cos(beta)*Lift
        Z=cfg.l*np.sin(np.arctan(Fz/np.sqrt(Fx**2+Fy**2)))
        Umem=Uwind
        Uwind=cfg.Uwind*np.log(Z/cfg.Zo)/np.log(cfg.Zref/cfg.Zo) # Log wind profil
       
    X=cfg.l*np.sin(np.arctan(Fx/np.sqrt(Fz**2+Fy**2)))
    Y=cfg.l*np.sin(np.arctan(Fy/np.sqrt(Fx**2+Fz**2)))
    return (Fx,Fy,Fz,X,Y,Z)

#
def Power(Fx,U):
    f=0.5*U**2    #loss on the electrical engine
    P=(Fx-f)*U
    return(P)


