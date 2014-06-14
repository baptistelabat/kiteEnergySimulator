kiteEnergySimulator
===================

This piece of software aims at computing the power that can be retrieved from a kite, pulling a craft or an electrical generator. This simulator was developed by Quentin RENAUD, Vincent ARNAL, Charles SPRAUL during a student project at Ecole Centrale de Nantes, based on a proposal by Baptiste LABAT.

To run the code you need to install python and a few libraries  
-Numpy  
-Matplotlib  
-Scipy  

Some results files where saved in Polar directory

You can get a 3D simulation of the Carousel by going into Carroussel directory and typing:  
python animation_3.py

The wing parameters are stored in Coefs/wing_cfg.py and in the .dat files (Lift and drag coefficients)

The fluid parameters are stored in Optim/cfg.py. Density can be changed to get results in water instead of air

The carousel parameters (radius, line length) are stored in Carroussel/animation_3.Py
