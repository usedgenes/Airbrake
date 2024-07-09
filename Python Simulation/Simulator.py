import numpy as np
import time
import Rocket 
import MotorThrustCurve

motor = MotorThrustCurve.ThrustCurve("AeroTech_F67W.csv", 0.08, 0.03)

graphics = Rocket.Rocket(1600,1600, 0.65, 0)

