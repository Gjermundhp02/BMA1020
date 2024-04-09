# Softbody collision between two squares
import numpy as np
import pyglet
import pyglet.shapes as shapes

WWIDTH = 960
WHEIGHT = 540

window = pyglet.window.Window(WWIDTH, WHEIGHT)
batch = pyglet.graphics.Batch()

K = 2
g = 10

def genVec(n):
    vec = np.array([], dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            vec = np.append(vec, [i, j])
    return vec.reshape(-1, 2)

class SoftBody:
    def __init__(self, pos, vel, size):
        self.pos = pos
        self.vel = vel
        self.size = size
        self.points = {
            "points": (p:=np.array([pos, pos+np.array([size, 0]), pos+np.array([size, size]), pos+np.array([0, size])])),
            "shapes": np.array([shapes.Circle(i[0], i[1], 5, color=(255, 255, 255), batch=batch) for i in p])
        }
        self.lines = {
            "lines": (l:=np.hstack((v:=genVec(4), np.linalg.norm(p[v[:, 0]]-p[v[:, 1]], axis=1)[:, np.newaxis]))),
            "shapes": np.array([shapes.Line(*p[int(i)], *p[int(j)], color=(255, 255, 255), batch=batch) for i, j, _ in l])
        }

    def update(self, dt):
        self.points["points"][self.points["points"][:, 1] < 0, 1] = 0
        vecs = self.points["points"][self.lines["lines"][:, 0].astype(np.int64)]-self.points["points"][self.lines["lines"][:, 1].astype(np.int64)]
        dist = np.linalg.norm(vecs, axis=1)
        norm = vecs/dist[:, np.newaxis]
        distDiff = (self.lines["lines"][:, 2]-np.linalg.norm(vecs, axis=1))[:, np.newaxis]
        if (distDiff>0.001).any() or (distDiff<-0.001).any(): # Needed because of floating point errors
            acc = distDiff*K*dt*norm/2
            print(acc, norm)

        self.vel = self.vel-[0, g*dt]
        self.points["points"] = self.points["points"]+self.vel*dt
        for i in range(len(self.points["shapes"])):
            self.points["shapes"][i].x, self.points["shapes"][i].y = self.points["points"][i]
        for i in range(len(self.lines["shapes"])):
            i = int(i)
            self.lines["shapes"][i].x, self.lines["shapes"][i].y = self.points["points"][int(self.lines["lines"][i, 0])]
            self.lines["shapes"][i].x2, self.lines["shapes"][i].y2 = self.points["points"][int(self.lines["lines"][i, 1])]

s1 = SoftBody(np.array([100, 100]), np.array([10, 0]), 100)
pyglet.clock.schedule_interval(s1.update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()