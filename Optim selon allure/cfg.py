# -*- coding: utf-8 -*-
# Fichier où définir toutes les variables globales du problème
# En particulier : paramètres de l'aile, du vent, de l'air, les constantes physiques...
# pour utiliser ces variables dans d'autres modules :
#  -->  import cfg
from numpy import pi

# Constantes physiques :
# Physical constants:
g=9.81              # constante d'accélération de gravité (m/s2)

# Caractéristiques de l'air
rho=1.2         # masse volumique (kg/m3)

# Caractéristiques du vent :
U_wind=10.           # vitesse du vent (m/s)
Wind_direction=90*pi/180   # direction du vent (rad) par rapport au déplacement 
                    # du chariot (vent arrière --> 0)
                    
# Wind characteristics :
Uwind=10.           # vitesse du vent (m/s) a l'altitude Zref (m)
Zref=50.           # Reference altitude for wind measurements (m)
Zo=0.055            # longueur de rugosite du terrain (m)

#
R=50                 # Radius (m)
l=100                # Tether length (m)

