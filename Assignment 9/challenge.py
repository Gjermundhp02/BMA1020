# Softbody collision between two squares
# I wanted to add collision response to but i couldn't figure it out in time
# The code only checks for collison if only one corner collides
from __future__ import annotations
import numpy as np
import pyglet
import pyglet.shapes as shapes

WWIDTH = 960
WHEIGHT = 540

window = pyglet.window.Window(WWIDTH, WHEIGHT)
batch = pyglet.graphics.Batch()

DEBUG = True
SPEED = 1
Ks = 2
Kd = 40
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
    b = [a[i, 0]-a[i, 1] for i in range(len(a))]
    b = a[:, 0]-a[:, 1]
    return b
class SoftBody:
    def __init__(self, pos, vel, size):
        self.size = size
        self.points = {
            "points": (p:=np.array([[pos, vel, [0, 0]], [pos+np.array([size, 0]), vel, [0, 0]], [pos+np.array([0, size]), vel, [0, 0]], [pos+np.array([size, size]), vel, [0, 0]]], dtype=np.float64)),
            "shapes": np.array([shapes.Circle(i[0], i[1], 5, color=(255, 255, 255), batch=batch) for i in p[:, 0]])
        }
        self.lines = {
            "lines": (l:=np.hstack((v:=genVec(4), np.linalg.norm(p[v[:, 0], 0]-p[v[:, 1], 0], axis=1)[:, np.newaxis]))),
            "shapes": np.array([shapes.Line(*p[int(i), 0], *p[int(j), 0], 3, color=(255, 255, 255), batch=batch) for i, j, _ in l])
        }

    def update(self, dt):
        oBounds = self.points["points"][:, 0, 1] < 5
        if oBounds.any():
            np.add.at(self.points["points"][:, 2, 1], oBounds, g*SPEED*dt) # Prevent buildup of speed while on the ground
            self.points["points"][oBounds, 0, 1] = 5 # Keep in bounds y
            self.points["points"][oBounds, 1] = 0 # Keep in bounds y
        vecs = self.points["points"][self.lines["lines"][:, 0].astype(np.int64), 0]-self.points["points"][self.lines["lines"][:, 1].astype(np.int64), 0] # Vectors between all the points
        dist = np.linalg.norm(vecs, axis=1) # Distance between all the points
        distDiff = (dist-self.lines["lines"][:, 2])[:, np.newaxis] # Distance differance between what it should be and what it is
        if DEBUG:
            for i in range(len(distDiff)):
                if distDiff[i]>0.001:
                    self.lines["shapes"][i].color = (0, 255, 0) # Expands
                elif distDiff[i]<-0.001:
                    self.lines["shapes"][i].color = (255, 0, 0) # Contracts
                else:
                    self.lines["shapes"][i].color = (255, 255, 255)
        norm = vecs/dist[:, np.newaxis] # Normalized vectors between all the points
        Fs = distDiff*Ks # Spring force
        Fd = listDot(norm, listSub(self.points["points"][self.lines["lines"][:, 0:2].astype(np.int64), 1]))*Kd # Damping force
        acc = (Fs+Fd.reshape(-1, 1))*norm/2 # Acceleration
        np.add.at(self.points["points"][:, 2], self.lines["lines"][:, 1].astype(np.int64), acc) # Add acceleration to the first point
        np.subtract.at(self.points["points"][:, 2], self.lines["lines"][:, 0].astype(np.int64), acc) # Subtract acceleration from the second point
        self.points["points"][:, 2] = self.points["points"][:, 2]+np.array([0, -g])*SPEED*dt # Add gravity
        self.points["points"][:, 1] = self.points["points"][:, 1]+self.points["points"][:, 2]*SPEED*dt # Update velocity
        self.points["points"][:, 0] = self.points["points"][:, 0]+self.points["points"][:, 1]*SPEED*dt # Update position

        # Update shapes
        for i in range(len(self.points["shapes"])):
            self.points["shapes"][i].x, self.points["shapes"][i].y = self.points["points"][i, 0]
        for i in range(len(self.lines["shapes"])):
            i = int(i)
            self.lines["shapes"][i].x, self.lines["shapes"][i].y = self.points["points"][int(self.lines["lines"][i, 0]), 0]
            self.lines["shapes"][i].x2, self.lines["shapes"][i].y2 = self.points["points"][int(self.lines["lines"][i, 1]), 0]

    def collides(self, other: SoftBody, dt: float):
        # Requires the objects to have the same amount of points
        # Rough check
        nextPos = self.points["points"][:, 0]+self.points["points"][:, 1]*SPEED*dt
        minXY = other.points["points"][:, 0].min(axis=0)
        maxXY = other.points["points"][:, 0].max(axis=0)
        cY = (nextPos[:, 1] > minXY[1]) & (nextPos[:, 1] < maxXY[1]) # True for corner that collides in y
        cX = (nextPos[:, 0] > minXY[0]) & (nextPos[:, 0] < maxXY[0]) # True for corner that collides in x
        c = cX & cY
        # Fine check
        if len(c[c==True])==1:
            # Self = p+r, other = q+s
            q = other.points["points"][other.lines["lines"][:, 0].astype(np.int64), 0]
            p = np.full_like(q, self.points["points"][c, 0])
            s = other.points["points"][other.lines["lines"][:, 1].astype(np.int64), 0]-q # Vectors between all the points
            r = np.full_like(s, self.points["points"][c, 1])*SPEED*dt
            rXs = np.cross(r, s, axis=1)
            t = np.cross((q[rXs!=0]-p[rXs!=0]), s[rXs!=0], axis=1)/rXs[rXs!=0]
            u = np.cross((q[rXs!=0]-p[rXs!=0]), r[rXs!=0], axis=1)/rXs[rXs!=0]
            mask = (t<=1) & (t>=0) & (u<=1) & (u>=0)
            if mask[1]:
                pass
            if (mask).any():
                self.points["shapes"][np.arange(len(c))[c]][0].color = (0, 0, 255)
                # p = self.points["points"][c, 0]+self.points["points"][c, 1]*t[mask]
                # u2 = 1-u[mask]
                # norm = np.linalg.norm(self.points["points"][c, 1], axis=1)
                # other.points["points"][other.lines["lines"][mask, 0:2].astype(np.int64), 0]
                

            
            


s1 = SoftBody(np.array([110, 274]), np.array([0, 0]), 100)
s2 = SoftBody(np.array([120, 240]), np.array([0, 0]), 100)

def update(dt):
    s1.update(dt)
    s2.update(dt)
    s1.collides(s2, dt)
    s2.collides(s1, dt)

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()