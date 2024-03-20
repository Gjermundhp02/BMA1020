from __future__ import annotations
import pyglet
import pyglet.shapes as shapes
import numpy as np

WWIDTH = 960
WHEIGHT = 540
window = pyglet.window.Window(WWIDTH, WHEIGHT)
batch = pyglet.graphics.Batch()

K = 1000

antall = 100
r = (np.random.random((antall)))*8+1
pos = np.random.random((antall, 2))*np.array([WWIDTH, WHEIGHT])
vel = np.zeros((antall, 2))
shape = np.array([shapes.Circle(pos[i, 0], pos[i, 1], r[i], batch=batch) for i in range(antall)])

def update(dt):
    global r, pos, vel, shape
    for i in range(len(pos)-1):
        vec = pos[i]-pos[i+1:]
        dist = np.tile(np.linalg.norm(vec, axis=1), (2, 1)).T
        disp = vec/dist # use where to avoid division by zero
        rn = np.tile(r[i+1:], (2, 1)).T
        f = 1/(dist**2)*r[i]*rn*K*disp
        vel[i] = np.clip(vel[i]-sum(np.where(dist>r[i]+r[i+1], f/r[i]*dt, 0)), -300, 300)
        vel[i+1:] = np.clip(vel[i+1:]+np.where(dist>r[i]+r[i+1], f/rn*dt, 0),  -300, 300)
        
        # print(vel)
        pos[i] += vel[i]*dt
        shape[i].position = pos[i]
    pos[-1] += vel[-1]*dt
    shape[-1].position = pos[-1]

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()