import csv

class ThrustCurve():
    def __init__(self, motorFile, weight, propellantWeight):
        with open(motorFile, mode = 'r') as file:
            csvFile = csv.reader(file)
            for row in csvFile:
                print(row)
        self.weight = weight-propellantWeight
        self.propellantWeight = propellantWeight
        print(5)