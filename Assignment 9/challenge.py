# Softbody collision between two squares
import numpy as np
import pyglet
import pyglet.shapes as shapes

WWIDTH = 960
WHEIGHT = 540

window = pyglet.window.Window(WWIDTH, WHEIGHT)
batch = pyglet.graphics.Batch()

SPEED = 0.01
K = 9
g = 10

def genVec(n):
    vec = np.array([], dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            vec = np.append(vec, [i, j])
    return vec.reshape(-1, 2)

def listDot(a, b):
    return np.sum(a*b, axis=1)

def listSub(a):
    return a[:, 0]-a[:, 1]
class SoftBody:
    def __init__(self, pos, vel, size):
        self.size = size
        self.points = {
            "points": (p:=np.array([[pos, vel, [0, 0]], [pos+np.array([size, 0]), vel, [0, 0]], [pos+np.array([size, size]), vel, [0, 0]], [pos+np.array([0, size]), vel, [0, 0]]], dtype=np.float64)),
            "shapes": np.array([shapes.Circle(i[0], i[1], 5, color=(255, 255, 255), batch=batch) for i in p[:, 0]])
        }
        self.lines = {
            "lines": (l:=np.hstack((v:=genVec(4), np.linalg.norm(p[v[:, 0], 0]-p[v[:, 1], 0], axis=1)[:, np.newaxis]))),
            "shapes": np.array([shapes.Line(*p[int(i), 0], *p[int(j), 0], color=(255, 255, 255), batch=batch) for i, j, _ in l])
        }

    def update(self, dt):
        self.points["points"][self.points["points"][:, 0, 1] < 5, 2, 1] += g*SPEED*dt # Prevent buildup of speed while on the ground
        self.points["points"][self.points["points"][:, 0, 1] < 5, 0, 1] = 5 # Keep in bounds y
        vecs = self.points["points"][self.lines["lines"][:, 0].astype(np.int64), 0]-self.points["points"][self.lines["lines"][:, 1].astype(np.int64), 0] # Vectors between all the points
        dist = np.linalg.norm(vecs, axis=1) # Distance between all the points
        distDiff = (self.lines["lines"][:, 2]-dist)[:, np.newaxis] # Distance differance between what it should be and what it is
        for i in range(len(distDiff)):
            if distDiff[i]>0.001:
                self.lines["shapes"][i].color = (255, 0, 0)
            elif distDiff[i]<-0.001:
                self.lines["shapes"][i].color = (0, 255, 0)
            else:
                self.lines["shapes"][i].color = (255, 255, 255)
        if (distDiff>0.001).any() or (distDiff<-0.001).any(): # Needed because of floating point errors
            norm = vecs/dist[:, np.newaxis] # Normalized vectors between all the points
            Fs = distDiff*K # Spring force
            Fd = listDot(norm, listSub(self.points["points"][self.lines["lines"][:, 0:2].astype(np.int64), 1]))*8 # Damping force
            acc = (Fs+Fd.reshape(-1, 1))*norm/2 # Acceleration
            # acc = ((distDiff*K)+(listDot(norm, listSub(self.points["points"][self.lines["lines"][:, 0:2].astype(np.int64), 1]))*8).reshape(-1, 1))*norm/2
            self.points["points"][self.lines["lines"][:, 0].astype(np.int64), 2] += acc # Add acceleration to the first point
            self.points["points"][self.lines["lines"][:, 1].astype(np.int64), 2] -= acc # Subtract acceleration from the second point

        self.points["points"][:, 1] = self.points["points"][:, 1]+self.points["points"][:, 2]*SPEED*dt+np.array([0, -g])*SPEED*dt # Update velocity
        self.points["points"][:, 0] = self.points["points"][:, 0]+self.points["points"][:, 1]*SPEED*dt # Update position

        # Update shapes
        for i in range(len(self.points["shapes"])):
            self.points["shapes"][i].x, self.points["shapes"][i].y = self.points["points"][i, 0]
        for i in range(len(self.lines["shapes"])):
            i = int(i)
            self.lines["shapes"][i].x, self.lines["shapes"][i].y = self.points["points"][int(self.lines["lines"][i, 0]), 0]
            self.lines["shapes"][i].x2, self.lines["shapes"][i].y2 = self.points["points"][int(self.lines["lines"][i, 1]), 0]

s1 = SoftBody(np.array([100, 5]), np.array([0, 0]), 100)
pyglet.clock.schedule_interval(s1.update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()