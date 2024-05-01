from __future__ import annotations
from pyglet import shapes
import pyglet
import numpy as np

WWidth = 800
WHeight = 800
window = pyglet.window.Window(WWidth, WHeight)
batch = pyglet.graphics.Batch()

def translate(p1, p2, t):
    if len(p1)==4 and len(p2)==4:
        return((1-t)*p1[0]+t*p2[0], (1-t)*p1[1]+t*p2[1], (1-t)*p1[2]+t*p2[2], (1-t)*p1[3]+t*p2[3])
    else:
        return ((1-t)*p1[0]+t*p2[0], (1-t)*p1[1]+t*p2[1])

def translateList(points, t):
        if len(points)<2:
            return points[0]
        else:
            return translateList([translate(points[i], points[i+1], t) for i in range(len(points)-1)], t=t)

bezierPoints = np.array([[np.random.randint(WWidth/8, WWidth/4), np.random.randint(WWidth/8, WHeight/4)], [np.random.randint(WWidth/8, WWidth/4), np.random.randint(WHeight/4*3, WHeight/8*7)], [np.random.randint(WWidth/4*3, WWidth/8*7), np.random.randint(WHeight/4*3, WHeight/8*7)], [np.random.randint(WWidth/4*3, WWidth/8*7), np.random.randint(WWidth/8, WHeight/4)]])
points = [shapes.Circle(bezierPoints[i][0], bezierPoints[i][1], 5, color=(int(255), int(255/(i+1)), int(255/(i+1))), batch=batch) for i in range(len(bezierPoints))]

WEIGHT = 0.1
kpoints = np.array([(bezierPoints[i]+(bezierPoints[(i+1)%len(bezierPoints)]-(bezierPoints[(i-1)%len(bezierPoints)]))*WEIGHT, bezierPoints[i]-(bezierPoints[(i+1)%len(bezierPoints)]-(bezierPoints[(i-1)%len(bezierPoints)]))*WEIGHT) for i in range(len(bezierPoints))]).flatten().reshape(-1, 2)
d = [shapes.Circle(kpoints[i][0], kpoints[i][1], 5, color=(255, 255, 0), batch=batch) for i in range(len(kpoints))]

# print(np.insert(kpoints.reshape(len(bezierPoints), 2, 2), 1, bezierPoints, axis=1).reshape(-1, 2))
poin = np.insert(kpoints.reshape(len(bezierPoints), 2, 2), 1, bezierPoints, axis=1).reshape(-1, 2)
p = [translateList(poin[(j+1)%len(poin):(j+5)%len(poin)], i/100) for i in range(100) for j in range(0, len(kpoints)-1, 1)]
# p = [print(poin[(j+1)%len(poin):(j+5)%len(poin)]) for j in range(0, len(kpoints)-1, 1)]
print(poin)
q = [shapes.Circle(p[i][0], p[i][1], 5, color=(255, 0, 255), batch=batch) for i in range(len(p))]

def update(dt):
    pass

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()