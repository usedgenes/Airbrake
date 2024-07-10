import turtle
import matplotlib.pyplot as plt
import numpy as np

COLORS = ['g','g','r','c','m','y','k']


class Rocket(turtle.Turtle):
    def __init__(self, screen_width, screen_height, mass, mmoi, targetAltitude):
        screen = turtle.Screen()
        screen.setup(screen_width, screen_height)
        rocket = turtle.Turtle()
        turtle.setworldcoordinates(0, 0, screen_width, screen_height)
        turtle.register_shape('rocket.gif')
        rocket.shape('rocket.gif')
        rocket.resizemode("user")
        rocket.penup();
        rocket.shapesize(0.5, 0.5, 0)
        rocket.goto(screen_width/2, 30)
        rocket.speed(0)
        self.mass = mass
        self.mmoi = mmoi
    def moveRocket(self, x, y):
        self.rocket.setx(x + 30)
        self.rocket.sety(y + 30)
    def rotateRocket(self, angle):
        self.rocket.setheading(np.rad2deg(angle))