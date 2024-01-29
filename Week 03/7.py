from __future__ import annotations
import pyglet
from pyglet import shapes, text
from pyglet.window import key
from random import randint
from math import sqrt

window = pyglet.window.Window(960, 540)
batchA = pyglet.graphics.Batch()
batchB = pyglet.graphics.Batch()

red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
orange=(255,140,0)

# Task A
def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]

class Circle:
    def __init__(self, x, y, velx=10, vely=10, index=None) -> None:
        self.shape = shapes.Circle(x, y, 50, color=red, batch=batchA)
        self.velx = velx
        self.vely = vely
        self.label = text.Label(str(index), x=x, y=y, batch=batchA) if index!=None else None
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
        if self.label:
            self.label.x = self.shape.x
            self.label.y = self.shape.y
        if self.intersectC:
            self.shape.color = green
        elif self.intersectL:
            self.shape.color = blue
        else:
            self.shape.color = red
        self.outOfBounds()
        self.intersectC = False
        self.intersectL = False

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
    def __init__(self, x, y, x2, y2, velx=10, vely=10, index=None) -> None:
        self.shape = shapes.Line(x, y, x2, y2, 10, color=red, batch=batchA)
        self.velx = velx
        self.vely = vely
        self.label = text.Label(str(index), x=x, y=y, batch=batchA) if index!=None else None
        self.intersectC = False
    
    def __name__(self) -> str:
        return "Line"
    
    def outOfBounds(self):
        diffx = abs(self.shape.x2-self.shape.x)
        diffy = abs(self.shape.y2-self.shape.y)
        if max(self.shape.x, self.shape.x2) < 0:
            self.shape.x += window.width+diffx
            self.shape.x2 += window.width+diffx
        elif min(self.shape.x, self.shape.x2) > window.width:
            self.shape.x -= window.width+diffx; 
            self.shape.x2 -= window.width+diffx
        if max(self.shape.y, self.shape.y2) < 0:
            self.shape.y += window.height+diffy
            self.shape.y2 += window.height+diffy
        elif min(self.shape.y, self.shape.y2) > window.height:
            self.shape.y -= window.height+diffy
            self.shape.y2 -= window.height+diffy

    def update(self, dt):
        self.shape.x += self.velx*dt
        self.shape.y += self.vely*dt
        self.shape.x2 += self.velx*dt
        self.shape.y2 += self.vely*dt
        if self.label:
            self.label.x = self.shape.x
            self.label.y = self.shape.y
        if self.intersectC:
            self.shape.color = orange
        else:
            self.shape.color = red
        self.outOfBounds()
        self.intersectC = False

class Ellipse:
    def __init__(self, x, y, width, height, parentIndex, color=(100, 100, 100)) -> None:
        self.shape = shapes.Ellipse(x, y, width, height, color=color, batch=batchB) if parentIndex==-1 else None
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.parentIndex = parentIndex
        self.color = color
    
    def update(self) -> None:
        x = self.x
        y = self.y
        if self.parentIndex>-1:
            parent = cat[self.parentIndex]
            while parent.parentIndex>-1:
                x += parent.x
                y += parent.y
                parent = cat[parent.parentIndex]
            x += parent.x
            y += parent.y
        if self.shape == None:
            self.shape = shapes.Ellipse(x, y, self.width, self.height, color=self.color, batch=batchB)
        else:
            self.shape.x = x
            self.shape.y = y

lines = [Line(randint(0, window.width), 
              randint(0, window.height), 
              randint(0, window.width//2), 
              randint(0, window.height//2), 
              randint(-100, 100), 
              randint(-100, 100)
              ) for _ in range(11)]

circles = [Circle(randint(0, window.width), 
                  randint(0, window.height), 
                  randint(-100, 100), 
                  randint(-100, 100)
                  ) for _ in range(8)]

def intersects() -> None:
    """Checks for intersections"""
    for i in range(len(circles)):
        for j in range(i+1, len(circles)):
            if circles[i].intersects(circles[j]):
                circles[i].intersectC = True
                circles[j].intersectC = True
    for i in range(len(circles)):
        for j in range(len(lines)):
            if circles[i].intersects(lines[j]):
                circles[i].intersectL = True
                lines[j].intersectC = True

# Task B
cat = [Ellipse(window.width/6, window.height/2, 100, 50, -1), #Body
       Ellipse(-70, 40, 50, 50, 0), #Head
       Ellipse(-20, 40, 25, 25, 1), #Ear
       Ellipse(20, 40, 25, 25, 1), #Ear
       Ellipse(-80, -40, 10, 20, 0), #Thigh
       Ellipse(0, -20, 10, 20, 4), #Leg
       Ellipse(0, -20, 15, 10, 5), #Paw
       Ellipse(-60, -40, 10, 20, 0), #Thigh
       Ellipse(0, -20, 10, 20, 7), #Leg
       Ellipse(0, -20, 15, 10, 8), #Paw
       Ellipse(60, -40, 10, 20, 0), #Thigh
       Ellipse(0, -20, 10, 20, 10), #Leg
       Ellipse(0, -20, 15, 10, 11), #Paw
       Ellipse(80, -40, 10, 20, 0), #Thigh
       Ellipse(0, -20, 10, 20, 13), #Leg
       Ellipse(0, -20, 15, 10, 14), #Paw
       Ellipse(100, 20, 20, 10, 0), #Tail
       Ellipse(20, 0, 20, 10, 16), #Tail
       Ellipse(20, 0, 20, 10, 17), #Tail
       Ellipse(-20, 20, 10, 10, 1, color=(0, 0, 0)), #Eye
       Ellipse(20, 20, 10, 10, 1, color=(0, 0, 0)) #Eye
]

def update(dt) -> None:
    if task:
        intersects()
        for i in circles:
            i.update(dt)
        for i in lines:
            i.update(dt)
    else:
        for i in cat:
            i.update()
        cat[0].x += 100*dt

# True = A False = B
task = True

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_key_press(symbol, modifiers):
    global task
    if symbol==key.SPACE:
        task = not task
    

@window.event
def on_draw():
    window.clear()
    if task:
        batchA.draw()
    else:
        batchB.draw()

pyglet.app.run()