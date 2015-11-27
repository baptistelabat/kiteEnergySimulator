# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 15:08:35 2014

@author: Quentin_perso
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3
import os

R       = 500  # Radius (m)
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
ax = p3.Axes3D(fig)

# Create the object to draw
kite, = ax.plot([], [], [], 'go')
lines = [ax.plot([], [], [], lw=1)[0] for i in range(n)]
lines.append(kite)
circle,     = ax.plot([], [], [], lw=2)
windArrow,  = ax.plot([], [], [], lw=1)
path, = ax.plot([], [], lw=1)

# Setting the axes properties
ax.set_xlim3d([-bnd, bnd])
ax.set_xlabel('X')

ax.set_ylim3d([-bnd, bnd])
ax.set_ylabel('Y')

ax.set_zlim3d([0, 2*bnd])
ax.set_zlabel('Z')
ax.set_title('3D Test')


# Initialization function (plot the background of each frame)
def init():
    kite = lines[-1]
    # Kites
    kite.set_data([], [])
    kite.set_3d_properties([])
    
    # Lines    
    for line in lines[0:-1]:
        line.set_data([], [])
        line.set_3d_properties([])
        
    lines[-1] = kite
    # Circle
    angle = np.linspace(0, 2*np.pi, 50)
    x = R*np.cos(angle)
    y = R*np.sin(angle)
    circle.set_data(x, y)
    circle.set_3d_properties(0*x)
    
    # Kite path
    theta = np.pi/180*np.linspace(-180, 176, 90)
    xL = kitePos[2, :]
    yL = kitePos[3, :]
    zL = kitePos[4, :]
    X = -xL*np.sin(theta) + (R-yL)*np.cos(theta)
    Y = xL*np.cos(theta) + (R-yL)*np.sin(theta)
    Z = zL
    X = np.append(X, X[0])
    Y = np.append(Y, Y[0])
    Z = np.append(Z, Z[0])
    path.set_data(X, Y)
    path.set_3d_properties(Z)
    
    # Wind direction
    ArrL = R # Arrow length
    top = ArrL/6.0
    ArrX = [        -top,        0,   0,        0,          top]
    ArrY = [-ArrL/2.+top, -ArrL/2., ArrL/2., -ArrL/2.0, -ArrL/2.+top]
    
    windArrow.set_data(ArrX, ArrY)
    
    windArrow.set_3d_properties(0*np.array(ArrX))
    print "Init done"
    
# Animation function
def animate(t):
    
    theta = np.linspace(0, 2*np.pi*(n-1)/n, n) + omega*t
    thetaV = np.mod(theta + np.pi, 2*np.pi)
    
    x = R*np.cos(theta)
    y = R*np.sin(theta)
    kite.set_data(x, y)
    kite.set_3d_properties(0*x)
    
    # Local kite position
    i = 0
    for l in lines[0:-1]:
        xL = np.interp(thetaV[i], angle, kitePos[2, :])
        yL = np.interp(thetaV[i], angle, kitePos[3, :])
        zL = np.interp(thetaV[i], angle, kitePos[4, :])
        X  = -xL*np.sin(theta[i]) + (R-yL)*np.cos(theta[i])
        Y  = xL*np.cos(theta[i]) + (R-yL)*np.sin(theta[i])
        Z  = zL 
        l.set_data([x[i], X], [y[i], Y])
        l.set_3d_properties([0, Z])
        i += 1  
    lines[-1] = kite
    return lines
    
init()
# Animator  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, frames=nbFrames, interval=incr, blit=True)
# anim = animation.TimedAnimation(fig, interval=200)

plt.show()
