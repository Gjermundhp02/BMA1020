import numpy as np

circlePos = np.array([[1.0,0.0],[3.0,3.0],[4.0,6.0]], dtype = float)
circleVel = np.array([[4.0, 2.0],[3.0,11.0], [21.0, 40.0]], dtype = float)


# a)
# position = position + dt * velocity
#
def updateA(dt):
    global circlePos
    circlePos += dt * circleVel


# b)
#
#
def move(xv, yv):
    global circlePos
    circlePos += np.array([xv, yv])


# c)
#
#
circleColor = np.zeros((3, 4)) # all circles are black to begin with

def turnRed():
    global circleColor
    circleColor = np.array([[1.0, 0.0, 0.0, 1.0] for _ in range(3)])


# d)
#
#
def brighten():
    global circleColor
    circleColor[:, :3] /= 2 


    