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
                     [np.random.randint(10, 22), 0]] for _ in range(100)]) # replace zero with newaxies

shapes = np.array([pyglet.shapes.Circle(i[0, 0], i[0, 1], i[2, 0], color=(255, 255, 255), batch=batch) for i in circles])

def update(dt):
    # Fix them appearing inside the screen
    circles[circles[:, 0, 0] < 0, 0, 0] = circles[circles[:, 0, 0] < 0, 0, 0]+WWIDTH
    circles[circles[:, 0, 0] > WWIDTH, 0, 0] = circles[circles[:, 0, 0] > WWIDTH, 0, 0]-WWIDTH
    circles[circles[:, 0, 1] < 0, 0, 1] = circles[circles[:, 0, 1] < 0, 0, 1]+WHEIGHT
    circles[circles[:, 0, 1] > WHEIGHT, 0, 1] = circles[circles[:, 0, 1] > WHEIGHT, 0, 1]-WHEIGHT
    for i in range(1, len(circles)-1):
        roll = np.roll(circles, -i, axis=0)
        collides = np.linalg.norm(circles[:, 0]-roll[:, 0], axis=1)<(circles[:, 2, 0]+roll[:, 2, 0])
        r2 = (circles[collides, 2, 0]+roll[collides, 2, 0])[:, np.newaxis]
        rm2 = (circles[collides, 2, 0]-roll[collides, 2, 0])[:, np.newaxis]
        dist = np.linalg.norm(circles[collides, 0]-roll[collides, 0], axis=1)[:, np.newaxis]
        vec = (circles[collides, 0]-roll[collides, 0])/dist
        norm = np.vstack((vec[:, 0]*-1, vec[:, 1])).T
        # Move out of collision
        circles[collides, 0] += (r2-dist)*vec/2
        circles[np.roll(collides, i), 0] -= (r2-dist)*vec/2
        # Collisions
        rVel = np.linalg.norm(roll[collides, 1], axis=1)
        cVel = np.linalg.norm(circles[collides, 1], axis=1)
        c1 = ((rm2/r2)[:, 0]*cVel+2*roll[collides, 2, 0]/r2[:, 0]*rVel)[:, np.newaxis]
        c2 = (2*circles[collides, 2, 0]/r2[:, 0]*cVel-(rm2/r2)[:, 0]*rVel)[:, np.newaxis]
        circles[collides, 1] = c1*norm
        circles[np.roll(collides, i), 1] = c2*-norm

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