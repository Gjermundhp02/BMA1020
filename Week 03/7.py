from __future__ import annotations
import pyglet
from pyglet import shapes
from random import randint
from math import sqrt

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
orange=(255,140,0)

def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]

def project(u, v):
    scalar = dot(u, v)/dot(v, v)
    print(scalar)
    return [v[0]*scalar, v[1]*scalar]
class Circle:
    def __init__(self, x, y, velx=10, vely=10) -> None:
        self.shape = shapes.Circle(x, y, 50, color=red, batch=batch)
        self.velx = velx
        self.vely = vely
        self.intersectC = False
        self.intersectL = False

    def __name__(self) -> str:
        return "Circle"
    
    def intersects(self, other: Circle|Line) -> bool:
        match type(other).__name__:
            case 'Circle':
                return sqrt((self.shape.x-other.shape.x)**2+(self.shape.y-other.shape.y)**2) <= 100
            case 'Line':
                v = [other.shape.x2-other.shape.x, other.shape.y2-other.shape.y]
                u = [self.shape.x-other.shape.x, self.shape.y-other.shape.y]
                scalar = dot(v, u)/dot(v, v)
                if scalar<0:
                    return sqrt(u[0]**2+u[1]**2) <= 50
                elif scalar>1:
                    return sqrt((self.shape.x+other.shape.x2)**2+(self.shape.y+other.shape.y2)**2) <= 50
                else:
                    return sqrt((u[0]-scalar*v[0])**2+(u[1]-scalar*v[1])**2) <= 50
    
    def update(self, dt):
        self.shape.x += self.velx*dt
        self.shape.y += self.vely*dt
        if self.intersectC:
            self.shape.color = green
        elif self.intersectL:
            self.shape.color = blue
        else:
            self.shape.color = red
        self.outOfBounds()

    def outOfBounds(self):
        if self.shape.x < -50:
            self.shape.x = window.width+50
        elif self.shape.x > window.width+50:
            self.shape.x = -50
        if self.shape.y < -50:
            self.shape.y = window.height+50
        elif self.shape.y > window.height+50:
            self.shape.y = -50

class Line:
    def __init__(self, x, y, x2, y2, velx=10, vely=10) -> None:
        self.shape = shapes.Line(x, y, x2, y2, 10, color=red, batch=batch)
        self.velx = velx
        self.vely = vely
        self.intersectC = False
        self.intersectL = False
    
    def __name__(self) -> str:
        return "Line"

# [[x, y, x2, y2, velx, vely, [circleInter, lineInter]]]
lines = [Line(randint(0, window.width), randint(0, window.height), randint(0, window.width), randint(0, window.height), randint(20, 40), randint(20, 40)) for _ in range(5)]
# [[x, y, velx, vely, [circleInter, lineInter]]]
circles = [Circle(randint(0, window.width), randint(0, window.height), randint(-200, 200), randint(-200, 200)) for _ in range(5)]

def intersects() -> None:
    """Checks for intersections"""
    
    for i in range(len(circles)):
        for j in range(i+1, len(circles)):
            if circles[i].intersects(circles[j]):
                circles[i].intersectC = True
                circles[j].intersectC = True
                break
            else:
                circles[i].intersectC = False
                circles[j].intersectC = False
    for i in range(len(circles)):
        for j in range(len(lines)):
            if circles[i].intersects(lines[j]):
                circles[i].intersectL = True
                break
            else:
                circles[i].intersectL = False
            

def update(dt) -> None:
    for i in circles:
        i.update(dt)
    

# # [[x, y, with, height, rot, parent]]
# cat = [
#     [window.width/2, window.height/2, 100, 50, None],
#     [-80, 50, 50, 50, 0],
#     [-30, 55, 25, 25, 1],
#     [30, 55, 25, 25, 1],
#     [-40, -40, ]
# ]

# def posX(start):
#     return cat[start][0]+(posX(cat[start][-1]) if start>0 else 0)
# def posY(start):
#     return cat[start][1]+(posY(cat[start][-1]) if start>0 else 0)

# catShapes=[shapes.Ellipse(posX(index), posY(index), i[2], i[3], color=color, batch=batch) for index, i in enumerate(cat)]

# # catShapes.append(shapes.Ellipse(*cat[0][:-1], color=color, batch=batch))

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    intersects()
    window.clear()
    batch.draw()

pyglet.app.run()