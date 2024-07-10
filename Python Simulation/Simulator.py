import numpy as np
import time as Time
import Rocket 
import MotorThrustCurve as thrust
import Physics as phys
import PID
import Graphs as gh

motor = thrust.ThrustCurve("AeroTech_F67W.csv", 0.08, 0.03)

rocket = Rocket.Rocket(1600,1600, 0.65, 1, 260)

state_vector = {"ay" : 0 ,"vy" : 0,"py" : rocket.getY(),"ax" : 0 ,"vx" : 0,"px" : rocket.getX() ,"alpha" : 0.0,"omega" : 0.5,"theta" : 0.0}

rocket_phys = phys.Physics(state_vector, rocket.mass, rocket.mmoi)

pidController = PID.PID(0.07, 0.01, 0.01, 0)

sim_time = 0.0
time_lim = 12.0
delta_t = 0.1

time = []
vert_pos = []
hori_pos = []

horizontal_labels = {"xlab" : "time(s)", "ylab" : "Pos X", "title" : "Position X"}

vertical_labels = {"xlab" : "time(s)", "ylab" : "Pos Y", "title" : "Position Y"}

graphs_dict = [horizontal_labels, vertical_labels]

graphics = gh.GraphHandler()
graphics.graphsHandler(2,graphs_dict)

Time.sleep(3)

while(sim_time < time_lim):
    hori_pos.append(rocket.getX())
    vert_pos.append(rocket.getY()-30)
    graphs = [(time, hori_pos), (time,vert_pos)]
    time.append(sim_time)
    
    state_vector = rocket_phys.inputForces([motor.getThrust(sim_time), 0, 0], delta_t)
    rocket.moveRocket(state_vector["px"], state_vector["py"])
    
    
    sim_time += delta_t
    
graphics.showGraphs(graphs)


