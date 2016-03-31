# Python Art - Multiple Turtles, Random Shapes
#
# This code generates Python Turtle images using six turtles drawing randomly coloured linked shapes.
#
# CC0 Ian Simpson, 30th March 2016 @familysimpson

import turtle
import random

# Square draws a square of pre-defined colour using the passed parameter item (the current turtle instance)

def square(item, size):
    for x in range(4):
        item.forward(size)
        item.right(90)
    item.forward(size)
    item.left(random.randrange(-180, 180))

# Circle draws a circle of pre-defined colour using the passed parameter item (the current turtle instance)

def circle(item, size):
    item.circle(size)
    item.forward(size)
    item.left(random.randrange(-180, 180))

# Zag draws a randomly sized zigzag in a pre-defined direction using the passed parameter item (the current turtle instance)

def zag(item, size, heading):
    item.setheading(heading)
    for x in range(3):
        item.forward(size)
        item.right(165)
        item.forward(size)
        item.left(165)

# Main program
# Set up the turtle screen, the six turtle instances, and then create the image using random colours and screen locations

wn = turtle.Screen()
w = wn.window_width()
h = wn.window_height()

t1 = turtle.Turtle()
t2 = turtle.Turtle()
t3 = turtle.Turtle()
t4 = turtle.Turtle()
t5 = turtle.Turtle()
t6 = turtle.Turtle()

turtles = [t1, t2, t3, t4, t5, t6]

wn.tracer(False)
angle = random.randrange(0,360)
for iteration in range(15):
    for item in turtles:
            item.penup()
            item.goto(random.randrange(-w,w),random.randrange(-h,h))
            item.color(random.randrange(0,255)/255.,random.randrange(0,255)/255.,random.randrange(0,255)/255.)
            item.pendown()
    wn.tracer(False)
    for move in range(2500):
        for item in turtles:
            item.speed(0)
            zag(item,random.randrange(5,25), angle)
    wn.tracer(True)

wn.exitonclick()

