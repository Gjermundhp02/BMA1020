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
import pyglet.shapes

WWIDTH = 960
WHEIGHT = 540

window = pyglet.window.Window(WWIDTH, WHEIGHT)
batch = pyglet.graphics.Batch()

K = 2
MAXSPEED = 40

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
        other.outOfBounds()

        if not sum(self.pos-other.pos):
            return
        dist = np.linalg.norm(self.pos-other.pos)
        

        if dist < self.r+other.r:
            normal = (self.pos-other.pos)/dist
            self.pos += normal*(self.r+other.r-dist)/2
            other.pos -= normal*(self.r+other.r-dist)/2
            p = 2*(self.vel-other.vel)/(self.r+other.r)
            self.vel = self.vel-p*other.r
            other.vel = other.vel+p*self.r
        
        self.pos += self.vel*dt
        self.shape.x, self.shape.y = self.pos
        other.pos += other.vel*dt
        other.shape.x, other.shape.y = other.pos


circles = np.array([[[np.random.uniform(0, WWIDTH), np.random.uniform(0, WHEIGHT)], 
                     [np.random.uniform(-MAXSPEED, MAXSPEED), np.random.uniform(-MAXSPEED, MAXSPEED)], 
                     [np.random.randint(10, 22), 0]] for _ in range(10)]) # replace zero with newaxies
circles = np.array([[[50+_*100, 50+_*20], 
                     [20*(-1)**_, 0], 
                     [15, 0]] for _ in range(3)], dtype=float)
shapes = np.array([pyglet.shapes.Circle(i[0, 0], i[0, 1], i[2, 0], color=(255, 255, 255), batch=batch) for i in circles])

# circles = np.array([Circle() for _ in range(100)], dtype=tuple)

def update(dt):
    # Fix them appearing inside the screen
    circles[circles[:, 0, 0] < 0, 0, 0] = circles[circles[:, 0, 0] < 0, 0, 0]+WWIDTH
    circles[circles[:, 0, 0] > WWIDTH, 0, 0] = circles[circles[:, 0, 0] > WWIDTH, 0, 0]-WWIDTH
    circles[circles[:, 0, 1] < 0, 0, 1] = circles[circles[:, 0, 1] < 0, 0, 1]+WHEIGHT
    circles[circles[:, 0, 1] > WHEIGHT, 0, 1] = circles[circles[:, 0, 1] > WHEIGHT, 0, 1]-WHEIGHT
    for i in range(1, len(circles)):
        roll = np.roll(circles, -i, axis=0)
        tes = np.linalg.norm(circles[:, 0]-roll[:, 0], axis=1)<(circles[:, 2, 0]+roll[:, 2, 0])
        r2 = (circles[tes, 2, 0]+roll[tes, 2, 0])[:, np.newaxis]
        rm2 = (circles[tes, 2, 0]-roll[tes, 2, 0])[:, np.newaxis]
        dist = np.linalg.norm(circles[tes, 0]-roll[tes, 0], axis=1)[:, np.newaxis]
        norm = (circles[tes, 0]-roll[tes, 0])/dist
        # Move out of collision
        if tes.any(): print((r2-dist)*norm/2+np.roll((r2-dist)*norm/2, i))
        circles[tes, 0] += (r2-dist)*norm/2
        if tes.any(): print(np.linalg.norm(circles[tes, 0]-roll[tes, 0], axis=1)[:, np.newaxis], r2)
        circles[np.roll(tes, i), 0] -= np.roll((r2-dist)*norm/2, i)
        if tes.any(): print(np.linalg.norm(circles[tes, 0]-np.roll(circles, -i, axis=0)[tes, 0], axis=1)[:, np.newaxis], r2)
        # Collisions
        circles[tes, 1] = rm2/r2*circles[tes, 1]+2*roll[tes, 2, 0][:, np.newaxis]/r2*roll[tes, 1]
        if tes.any(): print(circles[:, 1])
        circles[np.roll(tes, i), 1] = np.roll(2*circles[tes, 2, 0][:, np.newaxis]/r2*circles[tes, 1]-rm2/r2*roll[tes, 1], i)
        if tes.any(): print(circles[:, 1])
        if tes.any(): print(np.linalg.norm(circles[tes, 0]-roll[tes, 0], axis=1)[:, np.newaxis], r2)

    # Update positions
    circles[:, 0] += circles[:, 1]*dt
    for i in range(len(shapes)):
        shapes[i].x, shapes[i].y = circles[i, 0]

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()