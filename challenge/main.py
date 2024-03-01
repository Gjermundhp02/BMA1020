import pyglet
from pyglet import shapes
from pyglet.window import key
import numpy as np

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

# --- Globals ---
backgroundColor = (0, 0, 0, 255)
createTrack = False
points = [(914, 495), (840, 391), (622, 460), (519, 425), (400, 450), (289, 466), (95, 245), (214, 71), (382, 213), (476, 327), (710, 336), (883, 321), (876, 167), (828, 106), (646, 143), (379, 94), (175, 111)]
t=0
# ----------------

class Cart:
    def __init__(self, pos, size, origin=(), r=0, batch=None):
        # Uses sliced pos to support both length 2 and 3
        self.pos = np.array([*pos[:2], 1])+[*origin[:2], 0]
        self.size = np.array(size)
        self.shape = shapes.Rectangle(*pos[:2], *size, color=(255, 0, 0), batch=batch)
        self.origin = np.array([*origin[:2], 1]) # Point to rotate around
        if len(origin): self.rotate(r)
        print(self.pos, self.origin)
    
    def setPos(self, pos):
        self.pos = np.array([*pos, 1])

    def update(self):
        self.shape.x, self.shape.y = self.pos[:2]-self.size/2

    def rotate(self, t):
        if len(self.origin)==1:
            raise ValueError("Origin not set")
        else:
            rotation = np.array([[np.cos(t), -np.sin(t), 0],
                                [np.sin(t),  np.cos(t), 0],
                                [0,          0,         1]])
            
            translation = np.identity(3)
            translation[:2, 2] = self.origin[:2]

            translationNeg = np.identity(3)
            translationNeg[:2, 2] = -self.origin[:2]

            self.pos = (translation @ rotation @ translationNeg @ self.pos)
        

class FerrisWheel:
    def __init__(self, pos, r, thikness=5, batch=None):
        self.pos = np.array([*pos, 1])
        self.thikness = thikness
        # Two circles are used because Arc does not support thickness
        self.shape = shapes.Circle(*pos, r, color=(255, 255, 255), batch=batch)
        self.shape2 = shapes.Circle(*pos, r-self.thikness, color=backgroundColor, batch=batch)

        self.carts = [Cart((r-thikness/2, 0), (20, 10), self.pos, 2*np.pi/8*i, batch) for i in range(8)]
        self.spokes = [shapes.Line(*pos, r*np.cos(2*np.pi/8*i)+pos[0], r*np.sin(2*np.pi/8*i)+pos[1], 2, color=(255, 255, 255), batch=batch) for i in range(8)]

    def update(self):
        for cart in self.carts:
            cart.rotate(0.01)
            cart.update()


def translate(p1, p2, t):
    return ((1-t)*p1[0]+t*p2[0], (1-t)*p1[1]+t*p2[1])

def translateList(points, t):
        return [translate(points[i], points[i+1], t) for i in range(len(points)-1)]

# --- Globals instances ---
track = shapes.BezierCurve(*points, color=(255, 255, 255), batch=batch)
cart = Cart(points[0], (10, 5), batch=batch)
wheel = FerrisWheel((100, 100), 50, batch=batch)
# --------------------------

# --- Curve creation ---
if createTrack:
    track.delete()
    points.clear()
# ----------------------

@window.event
def on_mouse_release(x, y, button, modifiers):
    # --- Curve creation ---
    if createTrack:
        global track
        points.append((x, y))
        print(points)
        if len(points) > 2:
            track = shapes.BezierCurve(*points, color=(255, 255, 255), batch=batch)
    # ----------------------

@window.event
def on_key_press(symbol, modifiers):
    # --- Curve creation ---
    if createTrack:
        if symbol == key.C:
            points.clear()
            track.delete()
    # ----------------------

def update(dt):
    global t
    t += 0.05*dt
    t%=1
    plist = points.copy()
    while len(plist)>1:
        plist = translateList(plist, t)
    cart.setPos(plist[0])
    cart.update()
    wheel.update()


pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()