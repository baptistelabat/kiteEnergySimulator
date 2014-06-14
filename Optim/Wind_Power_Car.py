#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
File whith useful functions for Carrousel_optim

'''

# Optimiser l'angle d'incidence et la vitesse du chariot pour maximiser la puissance
# Renvoyer l'angle d'incidence, la vitesse chariot, les efforts aero et la puissance recuperable
# Find angle of attack and cart speed to optimize the power extraction
# Refer to "Rapport_v3_3-2.pdf" for documentation

import numpy as np
import cfg

import sys
sys.path.append('../Coefs')
from CoefsAero import CD, CL
from wing_cfg import Area as S
from cfg import rho

#
def Apparent_Wind(U, Uwind, WDir):
    """Definition of the Apparent Wind.
     U = Speed of the trolley supposed equal to the kite speed
     0deg is wind from behind
     180deg is facing wind"""
    Uapp  = np.hypot(  np.sin(WDir)*Uwind, np.cos(WDir)*Uwind - U)   
    delta = np.arctan2(np.sin(WDir)*Uwind, np.cos(WDir)*Uwind - U)
    return (Uapp, delta)
    
def AerodynamicForces(Uapp, alpha):
    """Computes lift and drag in frame defined by wind
     direction and body orientation.
     It assumes body is stabilised in "yaw" to face wind"""
    Lift = 1./2*rho*S*Uapp**2*CL(alpha)
    Drag = 1./2*rho*S*Uapp**2*CD(alpha)
    return (Lift, Drag)
    
def Forces(Angles, U, Uwind, WDir):
    """Computes forces projected in ground reference frame"""
    alpha = Angles[0]
    beta  = Angles[1]
    
    # Compute apparent wind at given wind speed
    [Uapp, delta] = Apparent_Wind(U, Uwind, WDir)
    
    # Compute corresponding lift and drag
    Lift, Drag = AerodynamicForces(Uapp, alpha)
    
    # Project in ground reference frame
    Fx = np.cos(delta)*Drag + np.sin(delta)*np.sin(beta)*Lift
    Fy = np.sin(delta)*Drag + np.cos(delta)*np.sin(beta)*Lift
    Fz = np.cos(beta) *Lift
    return (Fx, Fy, Fz)

#
def ComputeEquilibrium(Angles, U, WDir):
    """Computes the position at which the kite is at equilibrium
     for a given orientation"""
    Uwind = cfg.Uwind
    Umem  = 0. # Temporary variable to track convergence
    
    # Iterate to find the balance position
    while np.abs(Uwind - Umem) > 10e-4: 
        Fx, Fy, Fz = Forces(Angles, U, Uwind, WDir)
        
        # Assuming massless kite and string, compute kite attitude
        Z = cfg.line_length*np.sin(np.arctan2(Fz, np.hypot(Fx, Fy)))
        
        # Compute the effective wind at this altitude using log wind profil
        # http://en.wikipedia.org/wiki/Log_wind_profile
        Umem = Uwind
        Uwind = cfg.Uwind*np.log(Z/cfg.Zo)/np.log(cfg.Zref/cfg.Zo) # Log wind profil
        
    # Compute the kite position in ground reference frame   
    X = cfg.line_length*np.sin(np.arctan2(Fx, np.hypot(Fz, Fy)))
    Y = cfg.line_length*np.sin(np.arctan2(Fy, np.hypot(Fx, Fz)))
    return (Fx, Fy, Fz, X, Y, Z)

#
def Power(Fx, U):
    f = 0.5*U**2    #loss on the electrical engine
    P = (Fx - f)*U
    return(P)


