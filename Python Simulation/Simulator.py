import numpy as np
import time as Time
import Rocket 
import MotorThrustCurve as thrust
import Physics as phys
import Graphs as gh
import AirResistance as drag
import OldAirbrake
import Airbrake
import Altimeter

mass = 0.65
dragCoefficient = 0.45
openDragCoefficient = 0.8
airDensity = 1.2
area = 0.0034
cutoffFrequency = 0.9
initialAlpha = 0.03
targetAltitude = 900
maxEfficiency = 3
motorDelay = 1.5

motor = thrust.ThrustCurve("AeroTech_F42T_L.csv", 0.08, 0.03)

airResistance = drag.AirResistance(airDensity, area)

rocket = Rocket.Rocket(1600,1600, mass, 1)

altimeter = Altimeter.Altimeter()

oldAirbrake = OldAirbrake.OldAirbrake(dragCoefficient, openDragCoefficient, airDensity, area, mass, cutoffFrequency, initialAlpha, targetAltitude, maxEfficiency, motorDelay)

airbrake = Airbrake.Airbrake(0.07, 0.01, 0.01, 0)

state_vector = {"ay" : 0 ,"vy" : 0,"py" : 0,"ax" : 0 ,"vx" : 0,"px" : rocket.getX() ,"alpha" : 0.0,"omega" : 0.5,"theta" : 0.0}

rocket_phys = phys.Physics(state_vector, rocket.mass, rocket.mmoi)


sim_time = 0.0
time_lim = 10
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
    altitude = altimeter.getAltimeterData(state_vector)
    time = altimeter.getTime(sim_time, delta_t)
    airbrakeDrag = oldAirbrake.getDrag(altitude, time)
    netVerticalForce = motor.getThrust(sim_time) - airResistance.getDrag(dragCoefficient + airbrakeDrag, state_vector["vy"])
    state_vector = rocket_phys.inputForces([netVerticalForce, 0, 0], delta_t)
    rocket.moveRocket(state_vector["px"], state_vector["py"])
    
    vert_velocity.append(state_vector["vy"])
    vert_pos.append(rocket.getY()-30)
    graphs = [(time, vert_velocity), (time,vert_pos)]
    time.append(sim_time)
    sim_time += delta_t
    
graphics.showGraphs(graphs)


