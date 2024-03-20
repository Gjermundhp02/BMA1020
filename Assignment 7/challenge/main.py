import pyglet
from pyglet import shapes
from pyglet.window import key
import numpy as np

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

# --- Globals ---
backgroundColor = (0.7, 0.7, 0.7, 1)
colorInTunnel = (0, 0, 0, 1)
colorOutTunnel = backgroundColor
createTrack = False
trackPoints = np.array([(914, 495), (840, 391), (622, 460), (519, 425), (400, 450), (289, 466), (95, 245), (214, 71), (382, 213), (476, 327), (710, 336), (883, 321), (876, 167), (828, 106), (646, 143), (379, 94), (175, 111)])
tunnelPoints = np.array([(0.01, 0.1), (0.3, 0.4), (0.6, 0.7), (0.9, 0.99)])
t=0
speed=0.05
# ----------------

pyglet.gl.glClearColor(*backgroundColor)

class Cart:
    def __init__(self, pos, size, origin=(), r=0, batch=None):
        # Uses sliced pos to support both length 2 and 3
        self.pos = np.array([*pos[:2], 1])
        self.size = np.array(size)
        self.shape = shapes.Rectangle(*pos[:2], *size, color=(255, 0, 0), batch=batch)
        self.origin = np.array([*origin[:2], 1]) # Point to rotate around
        if len(origin): self.rotate(r)
        
    
    def setPos(self, pos):
        self.pos = np.array([*pos, 1])
        rotOffset = np.array([-np.cos(np.radians(self.shape.rotation))*self.size[0]/2, np.sin(np.radians(self.shape.rotation))*self.size[0]/2])
        self.shape.x, self.shape.y = self.pos[:2]+rotOffset
        self.shape.anchor_y = self.size[1]/2

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
        self.color = (0, 0, 0)
        # Two circles are used because Arc does not support thickness
        self.shape = shapes.Circle(*pos, r, color=self.color, batch=batch)
        self.shape2 = shapes.Circle(*pos, r-self.thikness, color=[int(i*255) for i in backgroundColor], batch=batch)
        self.legs = [shapes.Line(*pos, *(self.pos[:2]+[r/2, -r-10]), 5, color=self.color, batch=batch),
                     shapes.Line(*pos, *(self.pos[:2]+[-r/2, -r-10]), 5, color=self.color, batch=batch)]

        self.spokes = [shapes.Line(*pos, r*np.cos(2*np.pi/8*i)+pos[0], r*np.sin(2*np.pi/8*i)+pos[1], 2, color=self.color, batch=batch) for i in range(8)]
        self.carts = [Cart(self.pos+[r-thikness/2, 0, 0], (20, 10), self.pos, 2*np.pi/8*i, batch) for i in range(8)]

    def update(self):
        for cart in self.carts:
            cart.rotate(0.01)
            cart.update()
        for spoke in self.spokes:
            spoke.x2, spoke.y2 = rotate((spoke.x2, spoke.y2, 1), self.pos, 0.01)[:2]
        self.shape2.color = [int(i*255) for i in backgroundColor]

class Tunnel:
    def __init__(self, t, width=1, batch=None):
        self.tpos = np.array(t)
        self.dir = 1
        self.tmid = (t[1]-t[0])/2+t[0]
        self.tprev = 0
        self.width = width
        self.shape = BezierCurve(trackPoints, self.width, t[0], t[1], 100, color=(255, 0, 0), batch=batch)
        self.t = 0

    def update(self, dt):
        global t, backgroundColor, speed
        # store previous t to check if t has crossed tmid
        if t>self.tpos[0] and t<self.tpos[1]:
            if self.t>1:
                self.dir = -1
            self.t += 1/(self.tpos[1]-self.tpos[0])*speed*2*self.dir*dt
            backgroundColor = translate(colorOutTunnel, colorInTunnel, self.t**2*(3-2*self.t))
            self.tprev = t
        if t>self.tpos[1]:
            self.t=0
            self.dir = 1
        

class BezierCurve:
    def __init__(self, points, width, tFrom=0, tTo=1, segments=300, color=(255, 255, 255), batch=None) -> None:
        self.tpoints = [translateList(points, i)[0] for i in np.arange(tFrom, tTo, (tTo-tFrom)/segments)]
        self.lines = [shapes.Line(*self.tpoints[i], *self.tpoints[i+1], width, color, batch) for i in range(len(self.tpoints)-1)]

class Track:
    def __init__(self, points, width, color, batch=None):
        self.points = points
        self.width = width
        self.color = color
        self.line = BezierCurve(points, width, color=color, batch=batch)
        self.cart = Cart(points[0], (20, 5), batch=batch)

    def update(self, dt):
        global t, speed
        p1 = translateList(trackPoints, t)[0]
        p2 = translateList(trackPoints, t+dt*speed)[0] # Assumes that dt is the same next frame
        self.cart.setPos(p1)
        self.cart.shape.rotation = np.degrees(np.arccos((p2[0]-p1[0])/np.linalg.norm((p2[0]-p1[0], p2[1]-p1[1]))))
        

def rotate(pos, origin, t):
    rotation = np.array([[np.cos(t), -np.sin(t), 0],
                        [np.sin(t),  np.cos(t), 0],
                        [0,          0,         1]])
    
    translation = np.identity(3)
    translation[:2, 2] = origin[:2]

    translationNeg = np.identity(3)
    translationNeg[:2, 2] = -origin[:2]

    return (translation @ rotation @ translationNeg @ pos)

def translate(p1, p2, t):
    if len(p1)==4 and len(p2)==4:
        return((1-t)*p1[0]+t*p2[0], (1-t)*p1[1]+t*p2[1], (1-t)*p1[2]+t*p2[2], (1-t)*p1[3]+t*p2[3])
    else:
        return ((1-t)*p1[0]+t*p2[0], (1-t)*p1[1]+t*p2[1])

def translateList(points, t):
        if len(points)<2:
            return points
        else:
            return translateList([translate(points[i], points[i+1], t) for i in range(len(points)-1)], t=t)

# --- Globals instances ---
track = Track(trackPoints, 10, (25, 25, 25), batch)
wheel = FerrisWheel((100, 100), 50, batch=batch)
tunnels = [Tunnel(tunnelPoints[i], 15, batch) for i in range(len(tunnelPoints))]
# --------------------------

# --- Curve creation ---
if createTrack:
    track.delete()
    trackPoints.clear()
# ----------------------

@window.event
def on_mouse_release(x, y, button, modifiers):
    # --- Curve creation ---
    if createTrack:
        global track
        trackPoints.append((x, y))
        if len(trackPoints) > 2:
            track = shapes.BezierCurve(*trackPoints, color=(0, 0, 0), batch=batch)
    # ----------------------

@window.event
def on_key_press(symbol, modifiers):
    # --- Curve creation ---
    if createTrack:
        if symbol == key.C:
            trackPoints.clear()
            track.delete()
    # ----------------------

def update(dt):
    global t
    t += speed*dt
    t%=1
    plist = trackPoints.copy()
    track.update(dt)
    wheel.update()
    for tunnel in tunnels:
        tunnel.update(dt)
    pyglet.gl.glClearColor(*backgroundColor)


pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()

# TODO:
# - Add tunnels
# - Support speed of ferriswheel
