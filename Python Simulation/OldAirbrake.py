class OldAirbrake():
    firstLoop = True;
    timeConstant = None;
    alpha = None;
    currentAltitude = None;
    currentTime = None;
    filteredProjectedAltitude = None;
    
    def __init__(self, closedDragCoefficient, openDragCoefficient, airDensity, area, mass, cutoffFrequency, initialAlpha, targetAltitude, maxEfficiency, motorDelay):
        timeConstant = 1/(6.283 * cutoffFrequency)
        alpha = initialAlpha / (initialAlpha + timeConstant)
        currentAltitude = 30
        currentTime = 0
        self.closedDragCoefficient = closedDragCoefficient
        self.openDragCoefficient = openDragCoefficient
        self.airDensity = airDensity
        self.area = area
        self.mass = mass
        self.targetAltitude = targetAltitude
        self.maxEfficiency = maxEfficiency 
        self.motorDelay = motorDelay
        
    def getDrag(self, altitude, time):
        global firstLoop
        global alpha
        global currentAltitude
        global currentTime
        global filteredProjectedAltitude
        
        if(firstLoop == True):
            firstLoop = False
            filteredProjectedAltitude = currentAltitude
            return 0
        previousTime = currentTime
        currentTime = time
        previousAltitude = currentAltitude
        currentAltitude = altitude
        velocity = 1000*(currentAltitude - previousAltitude)/(currentTime - previousTime)
        projectedAltitude = currentAltitude + (velocity * velocity / (19.6 + ((self.dragCoefficient * self.airDensity * velocity * velocity * self.area* 0.5) / self.mass)))
        previousFilteredProjectedAltitude = filteredProjectedAltitude;
        filteredProjectedAltitude = (projectedAltitude*alpha)+(previousFilteredProjectedAltitude*(1-alpha))
        
        if(currentTime > self.motorDelay):
            altitudeDifference = filteredProjectedAltitude - self.targetAltitude
            if(altitudeDifference > 0):
                if(altitudeDifference > self.maxEfficiency):
                    return self.openDragCoefficient
      
                else:
                    return (altitudeDifference / self.maxEfficiency) * (self.openDragCoefficient - self.closedDragCoefficient)
            else:
                return 0

        
 