from math import sin, cos, pi, sqrt
import pyglet

def rotate(vec, rad):
    return [vec[0]*cos(rad)-vec[1]*sin(rad), vec[0]*sin(rad)+vec[1]*cos(rad)]

def vecLen(vec):
    return sqrt(vec[0]**2+vec1[1]**2)

def update():
    global vec2
    vec2 = rotate(vec2, pi/4)
    line2.x2 = 960/2+vec2[0]
    line2.y2 = 540/2+vec2[1]

vec1 = [100, 0]
vec2 = rotate(vec1, pi-1)
print(vec2)

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

line = pyglet.shapes.Line(960/2, 540/2, 960/2+vec1[0], 540/2+vec1[1], width=10, batch=batch, color=(50, 225, 30))
line2 = pyglet.shapes.Line(960/2, 540/2, 960/2+vec2[0], 540/2+vec2[1], width=10, batch=batch, color=(250, 225, 30))
arc = pyglet.shapes.Arc(960/2, 540/2, vecLen(vec1), color=(222, 222, 0), batch=batch)


@window.event
def on_draw():
    window.clear()
    batch.draw()
    # update() # Use custom schedule_inerval to make it independant of framerate pyglet.clock.shedule_interval

pyglet.clock.schedule_interval(update(), 1)

pyglet.app.run()