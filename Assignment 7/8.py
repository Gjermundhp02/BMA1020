from __future__ import annotations
import pyglet
import pyglet.shapes as shapes
import numpy as np

WWIDTH = 960
WHEIGHT = 540
window = pyglet.window.Window(WWIDTH, WHEIGHT)
batch = pyglet.graphics.Batch()

K = 2

class Circle:
    def __init__(self) -> None:
        self.r = np.random.randint(1, 9)
        self.pos = np.array([np.random.randint(0, WWIDTH), np.random.randint(0, WHEIGHT)])
        self.vel = np.array([0, 0])
        self.shape = shapes.Circle(self.pos[0], self.pos[1], self.r)
    
    def collides(self, other: Circle):
        return np.linalg.norm(self.pos-other.pos) < self.r+other.r
    
    def gravity(self, other: Circle, dt: float):
        if not self.collides(other):
            force = 1/(np.linalg.norm(self.pos-other.pos)**2)*self.r*other.r*(self.pos-other.pos)
            self.vel = np.clip((force/self.r)*dt+self.vel, -300, 300)

    def update(self, dt: float):
        self.pos += self.vel*dt
        self.shape.x, self.shape.y = self.pos

def gravity(circles: np.ndarray[tuple], dt: float):
    pass

def update(dt):
    circles[:, 2] = (1/(np.linalg.norm(circles[:-1, 1]-circles[1:, 1])**2)*circles[:-1, 0]*circles[1:, 0]*K*(circles[:-1, 1]-circles[:1, 1]))/circles[:-1, 0]*dt+circles[:-1, 2]
    circles[:, 1] += circles[:, 2]*dt
    circles[:, 3].x, circles[:, 3].y = circles[:, 1]

# (r, pos, vel, shape)
circles = np.array([((r:=np.random.randint(1, 9)), (pos:=np.array([np.random.randint(0, WWIDTH), np.random.randint(0, WHEIGHT)])), shapes.Circle(pos[0], pos[1], r)) for _ in range(10)], dtype=tuple)

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()