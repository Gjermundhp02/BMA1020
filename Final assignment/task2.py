from __future__ import annotations
from pyglet import shapes
import pyglet
import numpy as np
import sympy as sp

TASK = 0
WWidth = 800
WHeight = 800
window = pyglet.window.Window(WWidth, WHeight)
batch = pyglet.graphics.Batch()
group2 = pyglet.graphics.Group(1)
group1 = pyglet.graphics.Group(0)


def drawTriangle(points1, points2, color=(255, 255, 255)):
    triangles = [shapes.Triangle(*points1[i], *points1[(i+1)%len(points1)], *points2[i], color=color, batch=batch, group=group1) for i in range(len(points1))]
    triangles.append([shapes.Triangle(*points2[i], *points2[(i+1)%len(points1)], *points1[(i+1)%len(points1)], color=color, batch=batch, group=group1) for i in range(len(points1))])
    border = [shapes.Line(*points1[i], *points1[(i+1)%len(points1)], color=(0, 0, 0), batch=batch, group=group1) for i in range(len(points1))]
    border.append([shapes.Line(*points1[i], *points2[i], color=(0, 0, 0), batch=batch, group=group1) for i in range(len(points1)-1)])
    border.append([shapes.Line(*points1[i], *points2[(i+1)%len(points1)], color=(0, 0, 0), batch=batch, group=group1) for i in range(len(points1))])
    border.append([shapes.Line(*points2[i], *points2[(i+1)%len(points1)], color=(0, 0, 0), batch=batch, group=group1) for i in range(len(points1))])
    triangles.append(border)
    return triangles

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

def bezier(points, t):
    return (1-t)**3*points[0]+3*(1-t)**2*t*points[1]+3*(1-t)*t**2*points[2]+t**3*points[3]
        
def derived(p: np.ndarray, t: float) -> np.ndarray:
    """(4, 2) -> (2)"""
    return 3*(1-t)**2*(p[1]-p[0])+6*(1-t)*t*(p[2]-p[1])+3*t**2*(p[3]-p[2])

def gen_points(p1,p2,p3,p4):
    r = np.random.random()/4+0.3
    n1 = -r*p4+p1+r*p2
    m2 = r*p1+p2-r*p3
    n2 = -m2 + 2 * p2
    r = np.random.random()/4+0.3
    m3 = r*p2+p3-r*p4
    n3 = -m3 + 2 * p3
    r = np.random.random()/4+0.3
    m4 = r*p3+p4-r*p1
    n4 = -m4 + 2 * p4
    m1 = 2*p1 - n1
    return np.array([m1, p1,n1,m2,p2,n2,m3,p3,n3,m4,p4,n4])

def rotate(points: np.ndarray, rpoint: np.ndarray, angle: float):
    rotation = np.array([[np.cos(angle), -np.sin(angle), 0],
                        [np.sin(angle),  np.cos(angle), 0],
                        [0,          0,         1]])
    print(rotation)
    translation = np.identity(3)
    translation[:2, 2] = rpoint

    translationNeg = np.identity(3)
    translationNeg[:2, 2] = -rpoint

    rotatedPoints = np.zeros_like(points)
    for i in range(len(points)):
        rotatedPoints[i] = (translation @ rotation @ translationNeg @ np.append(points[i], 1).reshape(3,1)).flatten()[:2]

    print(rotatedPoints - points)
    return rotatedPoints
        
car = np.array([[20, 40], [0, 0]], dtype=np.float32)
carShapes = [shapes.Triangle(0, 0, 0, 0, 0, 0, color=(255, 0, 0), batch=batch, group=group2), shapes.Triangle(0, 0, 0, 0, 0, 0, color=(255, 0, 0), batch=batch, group=group2), *[shapes.Line(0, 0, 0, 0, color=(0, 0, 0), batch=batch, group=group2) for i in range(5)]]
track = []

def genTrack():
    bezierPoints = np.array([[np.random.randint(WWidth/8, WWidth/4), np.random.randint(WWidth/8, WHeight/4)], [np.random.randint(WWidth/8, WWidth/4), np.random.randint(WHeight/4*3, WHeight/8*7)], [np.random.randint(WWidth/4*3, WWidth/8*7), np.random.randint(WHeight/4*3, WHeight/8*7)], [np.random.randint(WWidth/4*3, WWidth/8*7), np.random.randint(WWidth/8, WHeight/4)]])
    bezierPointsShape = [shapes.Circle(bezierPoints[i][0], bezierPoints[i][1], 5, color=(int(255), int(255/(i+1)), int(255/(i+1))), batch=batch) for i in range(len(bezierPoints))]

    WEIGHT = 0.1
    kpoints = np.array([(bezierPoints[i]+(bezierPoints[(i+1)%len(bezierPoints)]-(bezierPoints[(i-1)%len(bezierPoints)]))*WEIGHT, bezierPoints[i]-(bezierPoints[(i+1)%len(bezierPoints)]-(bezierPoints[(i-1)%len(bezierPoints)]))*WEIGHT) for i in range(len(bezierPoints))]).flatten().reshape(-1, 2)
    kpointsShape = [shapes.Circle(kpoints[i][0], kpoints[i][1], 5, color=(255, 255, 0), batch=batch, group=group1) for i in range(len(kpoints))]

    allPoints = np.flip(np.insert(kpoints.reshape(len(bezierPoints), 2, 2), 1, bezierPoints, axis=1), axis=1).reshape(-1, 2)
    # allPoints = gen_points(*bezierPoints)
    print(allPoints)

    curves = np.array([[bezier(np.concatenate((allPoints[1+i:5+i], allPoints[:i%12*i//12])), j) for i in range(4)] for j in range(100)])
    norms = np.array([[bezier(np.concatenate((allPoints[1+i:5+i], allPoints[:i%12*i//12])), j) for i in range(4)] for j in range(20)])+np.array([(v:=derived(np.concatenate((allPoints[1+i:5+i], allPoints[:i%12*i//12]), axis=0), car[1, 1]))/np.linalg.norm(v)*10 for i in range(4)])
    print(np.array([(v:=derived(np.concatenate((allPoints[1+i:5+i], allPoints[:i%12*i//12]), axis=0), j))/np.linalg.norm(v)*10 for i in range(4) for j in range(20)]).shape)
    curveShapes = [shapes.Line(*curves[j, i], *norms[j, i], 3, color=(255, 0, 100), batch=batch, group=group2) for i in range(4) for j in range(20)]
    # curveShape = [[shapes.Circle(i[0], i[1], 5, color=(255, 0, 255), batch=batch) for i in j] for j in curves]

    der = np.array([[derived(allPoints[1:5], i/100) for i in range(0, 100, 5)],
        [derived(allPoints[4:8], i/100) for i in range(0, 100, 5)],
        [derived(allPoints[7:11], i/100) for i in range(0, 100, 5)],
        [derived(np.concatenate((allPoints[10:], allPoints[:2]), axis=0), i/100) for i in range(0, 100, 5)]])

    derPoints = [[translateList(allPoints[1:5], i/100) for i in range(0, 100, 5)],
                [translateList(allPoints[4:8], i/100) for i in range(0, 100, 5)],
                [translateList(allPoints[7:11], i/100) for i in range(0, 100, 5)],
                [translateList(np.concatenate((allPoints[10:], allPoints[:2]), axis=0), i/100) for i in range(0, 100, 5)]]
    norm = np.flip(der/np.linalg.norm(der, axis=2)[:, :, None], axis=2)
    norm[:, :, 0] = -norm[:, :, 0]
    outer = (np.array(derPoints)+norm*25).reshape(-1, 2)
    inner = (np.array(derPoints)-norm*25).reshape(-1, 2)

    derShape = [shapes.Circle(i[0], i[1], 5, color=(0, 255, 255), batch=batch) for i in inner]
    derShape2 = [shapes.Circle(i[0], i[1], 5, color=(0, 255, 255), batch=batch) for i in outer]

    triangels = drawTriangle(inner, outer, color=(255, 255, 255))
    return allPoints, triangels, curveShapes

def updateCar(dt):
    global track
    car[1, 1] += 0.1*dt
    if car[1, 1] >= 1:
        car[1, 0] = (car[1, 0]+1)%4
        car[1, 1] = 0
    pos = np.array(translateList(track[0][(1+int(car[1, 0])*3):(5+int(car[1, 0])*3)], car[1, 1]))
    norm = (v:=derived(track[0][(1+int(car[1, 0])*3):(5+int(car[1, 0])*3)], car[1, 1]))/np.linalg.norm(v)
    cos = np.dot(norm, [1, 0])
    points =[pos+[-car[0, 0]/2, -car[0, 1]/2],
             pos+[car[0, 0]/2, -car[0, 1]/2],
             pos+[-car[0, 0]/2, car[0, 0]/2],
             pos+[car[0, 0]/2, car[0, 0]/2],]
    rpoints = rotate(points, pos, np.arccos(cos))

    carShapes[0].x, carShapes[0].y = rpoints[0]
    carShapes[0].x2, carShapes[0].y2 = rpoints[1]
    carShapes[0].x3, carShapes[0].y3 = rpoints[2]
    carShapes[1].x, carShapes[1].y = rpoints[1]
    carShapes[1].x2, carShapes[1].y2 = rpoints[2]
    carShapes[1].x3, carShapes[1].y3 = rpoints[3]


@window.event
def on_key_press(symbol, modifiers):
    global TASK
    if symbol == pyglet.window.key.SPACE:
        TASK = (TASK+1)%3

def update(dt):
    global track
    if TASK == 0:
        track = genTrack()
    if TASK == 1:
       updateCar(dt)

pyglet.clock.schedule_interval(update, 2)
update(0)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()