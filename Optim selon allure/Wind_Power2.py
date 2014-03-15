# -*- coding: utf-8 -*-
# Fixer les paramètres de l'aile et du wind
# Optimiser l'angle d'incidence et la vitesse du chariot pour maximiser la puissance
# Renvoyer l'angle d'incidence, la vitesse chariot, les efforts aéro et la puissance récupérable

import numpy as np
import cfg
import CoeffAero

#
def Apparent_Wind(U,Uwind,Wind_direction):
    Uapp=np.sqrt((np.cos(Wind_direction)*Uwind-U)**2+(np.sin(Wind_direction)*Uwind)**2)
    delta=2*np.arctan((np.sin(Wind_direction)*Uwind)/((np.cos(Wind_direction)*Uwind-U)+Uapp))
    #print('Uapp =',Uapp)
    #print('delta (deg) = ',delta*180/pi,'\n')
    return (Uapp,delta)

#
def Forces(Xpar,Uwind,Wind_direction):
    U=Xpar[0]
    alpha=Xpar[1]
    beta=Xpar[2]
    [Uapp,delta]=Apparent_Wind(U,Uwind,Wind_direction)
    Cl=CoeffAero.CL(alpha)
    Cd=CoeffAero.CD(alpha)
    Lift=1/2*cfg.rho*cfg.Area*Cl*Uapp**2
    Draft=1/2*cfg.rho*cfg.Area*Cd*Uapp**2
    Fx=np.cos(delta)*Draft+np.sin(delta)*np.sin(beta)*Lift
    Fy=np.sin(delta)*Draft+np.cos(delta)*np.sin(beta)*Lift
    Fz=np.cos(beta)*Lift
    return (Fx,Fy,Fz)

#
def Power(Xpar,Uwind,Wind_direction):
    U=Xpar[0]
    f=0.5*U**2
    Fx=Forces(Xpar,Uwind,Wind_direction)[0]
    Fy=Forces(Xpar,Uwind,Wind_direction)[1]
    Fz=Forces(Xpar,Uwind,Wind_direction)[2]
    Z=100*np.sin(np.arctan(Fz/np.sqrt(Fx**2+Fy**2)))
    if Z<50:
        Fx=Fx*(-2*(Z/50)**3+3*(Z/50)**2)
    P=(Fx-f)*U
    return(-P)


