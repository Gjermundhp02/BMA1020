# The pseudo code for collision detection and response is:

# - check all possible pairs of circles for collision.

# - where a collision happens, compute the normal and tangent direction of collision, and perform 1d collision in the normal direction

# - move objects out of collision before continuing

# The mathematical details for the calculations were given in class.


# Some more details you should follow

# - there are 100 circles with random radii between 2 and 22.

# - at the start circles have random positions in the window

# - at the start circles have random velocity (-MAXSPEED...MAXSPEED for x and y).

# - the mass of a disk is equal to its radius


# Implement the program. For full score you should make effective use of numpy.

# Include a log where you detail all the help you have gotten from people/websites and ai. Include complete conversations with ai. Comment in code where you have used outside sources.

from __future__ import annotations
import numpy as np
import pyglet
import pyglet.shapes as shapes

WWIDTH = 960
WHEIGHT = 540

window = pyglet.window.Window(WWIDTH, WHEIGHT)
batch = pyglet.graphics.Batch()

K = 2
MAXSPEED = 20

class Circle:
    def __init__(self) -> None:
        self.r = np.random.randint(10, 22)
        self.pos = np.array([np.random.uniform(0, WWIDTH), np.random.uniform(0, WHEIGHT)])
        self.vel = np.array([np.random.uniform(-MAXSPEED, MAXSPEED), np.random.uniform(-MAXSPEED, MAXSPEED)])
        self.shape = shapes.Circle(self.pos[0], self.pos[1], self.r, color=(255, 255, 255), batch=batch)
    
    def collides(self, other: Circle):
        return np.linalg.norm(self.pos-other.pos) < self.r+other.r
    
    def outOfBounds(self):
        if self.pos[0] < 0:
          self.pos[0] = WWIDTH  
        if self.pos[0] > WWIDTH:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = WHEIGHT
        if self.pos[1] > WHEIGHT:
            self.pos[1] = 0

    def update(self, other: Circle, dt: float):
        self.outOfBounds()

        if not sum(self.pos-other.pos):
            return
        dist = np.linalg.norm(self.pos-other.pos)
        

        if dist < self.r+other.r:
            normal = (self.pos-other.pos)/dist
            self.pos += normal*(self.r+other.r-dist)/2
            other.pos -= normal*(self.r+other.r-dist)/2
            # self.vel = tangent*np.clip(np.dot(self.vel, tangent), -MAXSPEED, MAXSPEED)
            # other.vel = tangent*np.clip(np.dot(other.vel, tangent), -MAXSPEED, MAXSPEED)
            # include r in the calculation
            print(sum(self.vel*self.r+other.vel*other.r))
            self.vel = (self.r-other.r)/(self.r+other.r)*self.vel+2*other.r/(self.r+other.r)*other.vel
            other.vel = 2*self.r/(self.r+other.r)*self.vel-(self.r-other.r)/(self.r+other.r)*other.vel
            print(sum(self.vel*self.r+other.vel*other.r))
        
        self.pos += self.vel*dt
        self.shape.x, self.shape.y = self.pos
        other.pos += other.vel*dt
        other.shape.x, other.shape.y = other.pos

circles = np.array([Circle() for _ in range(5)], dtype=tuple)

def update(dt):
    for i in range(len(circles)):
        for j in range(len(circles)):
            circles[i].update(circles[j], dt)

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()