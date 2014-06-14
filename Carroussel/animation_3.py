# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 15:08:35 2014

@author: Quentin_perso
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import os

R       = 4000  # Radius (m)
l       = 100   # Tether length
Vext    = 1     # Speed of a car
omega   = Vext/float(R)
n       = 5     # Number of kites

angle=np.pi/180*np.linspace(0,356,90)

# Load polar curve
folder = "../Polar"
filename = 'Polar_DU21_30ms.npy'
kitePos = np.load(os.path.join(folder,filename))

# Animation parameters
tmax = 2*np.pi/omega # Time to do one turn
nbFrames = 1000*int(tmax) # 1000 fps
incr = tmax/nbFrames

# Initialize the figure
bnd = R + l
fig = plt.figure()
ax = plt.axes(xlim=(-bnd, bnd), ylim=(-bnd, bnd))
kite, = ax.plot([], [], 'go')
for i in np.arange(0, n):
    exec(''.join(['line', str(i+1), ',=ax.plot([], [], lw=1)']))
circle,     = ax.plot([], [], lw=2)
windArrow,  = ax.plot([], [], lw=1)

# Initialization function (plot the background of each frame)
def init():
    # Kites
    kite.set_data([], [])
    
    # Lines    
    for i in np.arange(0,n):
        exec(''.join(['line', str(i+1), '.set_data([], [])']))
    
    # Circle
    angle = np.linspace(0, 2*np.pi, 50)
    x = R*np.cos(angle)
    y = R*np.sin(angle)
    circle.set_data(x, y)
    
    # Kite path
    path, = ax.plot([], [], lw=1)
    theta = np.pi/180*np.linspace(-180, 176, 90)
    xL = kitePos[2, :]
    yL = kitePos[3, :]
    X = -xL*np.sin(theta) + (R-yL)*np.cos(theta)
    Y = xL*np.cos(theta) + (R-yL)*np.sin(theta)
    X = np.append(X, X[0])
    Y = np.append(Y, Y[0])
    path.set_data(X, Y)
    
    # Wind direction
    ArrL = 50
    top = ArrL/6
    ArrX = [        -top,        0,   0,        0,          top]
    ArrY = [bnd-ArrL+top, bnd-ArrL, bnd, bnd-ArrL, bnd-ArrL+top]
    windArrow.set_data(ArrX,ArrY)
    
# Animation function
def animate(t):
    theta = np.linspace(0, 2*np.pi*(n-1)/n, n) + omega*t
    thetaV = np.mod(theta + np.pi, 2*np.pi)
    
    x = R*np.cos(theta)
    y = R*np.sin(theta)
    kite.set_data(x, y)
    
    # Local kite position
    ret = 'kite'
    for i in np.arange(0,n):
        xL = np.interp(thetaV[i], angle,kitePos[2,:])
        yL = np.interp(thetaV[i], angle,kitePos[3,:])
        X  = -xL*np.sin(theta[i]) + (R-yL)*np.cos(theta[i])
        Y  = xL*np.cos(theta[i]) + (R-yL)*np.sin(theta[i])
        exec(''.join(['line', str(i+1), '.set_data([x[i], X], [y[i], Y])']))
        ret =''.join([ret, ', line', str(i+1)])
        
    return eval(ret)

#Animator  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=nbFrames, interval=incr, blit=True)
#anim = animation.TimedAnimation(fig, interval=200)

plt.show()
