import numpy as np
import time
import Rocket 
import MotorThrustCurve
import Physics as phys
import PID

motor = MotorThrustCurve.ThrustCurve("AeroTech_F67W.csv", 0.08, 0.03)

rocket = Rocket.Rocket(1600,1600, 0.65, 0, 260)

state_vector = {"ax" : 0 ,"vx" : 0,"px" : 0,"az" : 0 ,"vz" : 1,"pz" : 0 ,"alpha" : 0.0,"omega" : 0.5,"theta" : 0.0}

rocket_phys = phys.Physics(state_vector, rocket.mass, rocket.mmoi)

pidController = PID.PID(0.07, 0.01, 0.01, 0)

sim_time = 0.0
time_lim = 10.0
delta_t = 0.1

