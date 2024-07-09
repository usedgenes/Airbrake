import matplotlib.pyplot as plt
import numpy as np

class GraphHandler():
    def graphsHandler(self,num_graphs,graphs_dict):
		self.fig, self.axs = plt.subplots(num_graphs, sharex=True)
		i = 0
		for a in self.axs:
			a.set(xlabel= graphs_dict[i]['xlab'],ylabel= graphs_dict[i]['ylab'])
			i += 1
	def setGraphRate(self,dt):
		self.graph_rate = dt
	def setGraphColors(self):
		pass
	def updateGraphs(self,graph_values):
		i = 0
		for a in self.axs:
			a.plot(graph_values[i][0],graph_values[i][1],'tab:red')
			i += 1
			plt.pause(self.graph_rate)
	def showGraphs(self,graph_values,batch_num = 0):
		i = 0
		for a in self.axs:
			a.plot(graph_values[i][0],graph_values[i][1],'tab:red')
			i += 1
		plt.show()