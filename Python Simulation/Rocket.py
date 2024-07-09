import turtle
import matplotlib.pyplot as plt
import numpy as np

COLORS = ['g','g','r','c','m','y','k']


class RocketHandler(turtle.Turtle):
    def __init__(self, screen_width, screen_height):
        screen = turtle.Screen()
        screen.setup(screen_width, screen_height)
        rocket = turtle.Turtle()
        turtle.setworldcoordinates(0, 0, screen_width, screen_height)
        turtle.register_shape('rocket.gif')
        rocket.shape('rocket.gif')
        rocket.resizemode("user")
        rocket.penup();
        rocket.shapesize(0.5, 0.5, 0)
        rocket.goto(screen_width/2 + 30, 0)
        rocket.speed(0)
    def moveRocket(self, x, y):
        self.rocket.setx(x)
    def rotateRocket(self, angle):
        self.rocket.setheading(np,rad2deg(angle))