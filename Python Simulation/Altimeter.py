import random

class Altimeter():
    def getAltimeterData(self, initial_state_vector):
        return initial_state_vector["py"] + random.uniform(0, 0.5)
    def getTime(self, currentTime, dt):
        return currentTime + random.uniform(-dt, dt)
        