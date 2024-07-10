class AirResistance():
    def __init__(self, dragCoefficient, airDensity, crossSectionalArea):
        self.dragCoefficient = dragCoefficient
        self.airDensity = airDensity
        self.crossSectionalArea = crossSectionalArea
        
    def getDrag(self, velocity):
        return 0.5*self.dragCoefficient*self.airDensity*self.crossSectionalArea*velocity*velocity