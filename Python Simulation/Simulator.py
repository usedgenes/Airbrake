import numpy as np
import time
import Graphics as gh

time_ret = []
angles_ret = []
vert_pos_ret = []
hori_pos_ret = []

ori_labels = {"xlab" : "time(s)", "ylab" : "angle(theta)", "title" : "Theta"}
translate_labels = {"xlab" : "time(s)", "ylab" : "Pos Z", "title" : "Position Z"}
vertical_labels = {"xlab" : "time(s)", "ylab" : "Pos X", "title" : "Position X"}

graphs_dict = [ori_labels,translate_labels,vertical_labels]
graphics = gh.GraphicHandler()
graphics.graphsHandler(3,graphs_dict)

graphics = gh.GraphicHandler()
graphics.graphsHandler(3,graphs_dict) #number of graphs and their labels

rocket = graphics.createAgent('black')
targe = graphics.createAgent('red')

