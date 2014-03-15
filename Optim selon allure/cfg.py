# -*- coding: utf-8 -*-
# Fichier où définir toutes les variables globales du problème
# En particulier : paramètres de l'aile, du vent, de l'air, les constantes physiques...
# pour utiliser ces variables dans d'autres modules :
#  -->  import cfg
from numpy import pi

# Constantes physiques :
g=9.81              # constante d'accélération de gravité (m/s2)

# Caractéristiques de l'air
rho=1.2         # masse volumique (kg/m3)

# Caractéristiques de l'aile :
Area=5              # surface (m2)
Thickness=0.01      # épaisseur (m)
Cord=0.5            # corde (m)
Camber=0            # cambrure
L=10                # envergure (m)
Weight=2.5          # masse (kg)

# Caractéristiques du vent :
U_wind=10.           # vitesse du vent (m/s)
Wind_direction=90*pi/180   # direction du vent (rad) par rapport au déplacement 
                    # du chariot (vent arrière --> 0)

