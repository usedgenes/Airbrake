import numpy as np
import time as Time
import Rocket 
import MotorThrustCurve as thrust
import Physics as phys
import PID
import Graphs as gh
import AirResistance as drag

motor = thrust.ThrustCurve("AeroTech_F67W.csv", 0.08, 0.03)

airResistance = drag.AirResistance(0.45, 1.2, 0.0034)

rocket = Rocket.Rocket(1600,1600, 0.65, 1, 260)

state_vector = {"ay" : 0 ,"vy" : 0,"py" : rocket.getY(),"ax" : 0 ,"vx" : 0,"px" : rocket.getX() ,"alpha" : 0.0,"omega" : 0.5,"theta" : 0.0}

rocket_phys = phys.Physics(state_vector, rocket.mass, rocket.mmoi)

pidController = PID.PID(0.07, 0.01, 0.01, 0)

sim_time = 0.0
time_lim = 12.0
delta_t = 0.05

time = []
vert_pos = []
vert_velocity = []

vertical_velocity = {"xlab" : "time(s)", "ylab" : "velocity Y", "title" : "Velocity Y"}

vertical_labels = {"xlab" : "time(s)", "ylab" : "Pos Y", "title" : "Position Y"}

graphs_dict = [vertical_velocity, vertical_labels]

graphics = gh.GraphHandler()
graphics.graphsHandler(2,graphs_dict)

Time.sleep(3)

while(sim_time < time_lim):
    vert_velocity.append(state_vector["vy"])
    vert_pos.append(rocket.getY()-30)
    graphs = [(time, vert_velocity), (time,vert_pos)]
    time.append(sim_time)
    a = motor.getThrust(sim_time)
    b = airResistance.getDrag(state_vector["vy"])
    netVerticalForce = a - b
    state_vector = rocket_phys.inputForces([netVerticalForce, 0, 0], delta_t)
    rocket.moveRocket(state_vector["px"], state_vector["py"])
    
    
    sim_time += delta_t
    
graphics.showGraphs(graphs)


