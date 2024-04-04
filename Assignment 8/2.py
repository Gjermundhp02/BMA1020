from __future__ import annotations
import numpy as np
import pyglet
import pyglet.shapes

WWIDTH = 960
WHEIGHT = 540

WINDVEL = 30

window = pyglet.window.Window(WWIDTH, WHEIGHT)
batch = pyglet.graphics.Batch()

particles = np.empty((0, 3))
shapes = np.array([], dtype=pyglet.shapes.Circle)

t = 0.5
dir = 1

def update(dt):
    global particles, shapes, dir, t
    if t>1 or t<0:
       t = np.clip(t, 0, 1)
       dir = -dir
    t += 0.2*dir*dt
    new = np.array([[np.random.randint(200, 300), np.random.uniform(np.pi/4, 3*np.pi/4), np.random.randint(10, 15)] for i in range(5)])
    particles = np.vstack((particles, new))
    shapes = np.hstack((shapes, [pyglet.shapes.Circle(WWIDTH/2, WHEIGHT/2, i[2], color=(255, 255, 255), batch=batch) for i in new]))
    xVel = np.cos(particles[:, 1])*particles[:, 0]-(((1-t)*-WINDVEL+t*WINDVEL)*2*particles[:, 2]-np.cos(particles[:, 1])*particles[:, 0])*dt
    yVel = np.sin(particles[:, 1])*particles[:, 0]-200*dt
    particles[:, 0] = np.linalg.norm(np.vstack((xVel, yVel)), axis=0)
    particles[:, 1] = np.arctan2(yVel, xVel)
    inBounds = []
    for i in range(len(shapes)):
        if shapes[i].y > 0 and shapes[i].y < WHEIGHT and shapes[i].x > 0 and shapes[i].x < WWIDTH:
            shapes[i].y += np.sin(particles[i, 1])*particles[i, 0]*dt
            shapes[i].x += np.cos(particles[i, 1])*particles[i, 0]*dt
            inBounds.append(i)
    particles = particles[inBounds]
    shapes = shapes[inBounds]

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()