from __future__ import annotations
from pyglet import shapes
import pyglet
import numpy as np
import sympy as sp

TASK = 0
WWidth = 800
WHeight = 800
window = pyglet.window.Window(WWidth, WHeight)
batchTrack = pyglet.graphics.Batch()
batchCar = pyglet.graphics.Batch()
group2 = pyglet.graphics.Group(1)
group1 = pyglet.graphics.Group(0)


def drawTriangle(points1: np.ndarray, points2: np.ndarray, color=(255, 255, 255)):
    triangles = [shapes.Triangle(*points1[i], *points1[(i+1)%len(points1)], *points2[i], color=color, batch=batchTrack) for i in range(len(points1))]
    triangles.append([shapes.Triangle(*points2[i], *points2[(i+1)%len(points1)], *points1[(i+1)%len(points1)], color=color, batch=batchTrack) for i in range(len(points1))])
    border = [shapes.Line(*points1[i], *points1[(i+1)%len(points1)], color=(0, 0, 0), batch=batchTrack) for i in range(len(points1))]
    border.append([shapes.Line(*points1[i], *points2[i], color=(0, 0, 0), batch=batchTrack) for i in range(len(points1)-1)])
    border.append([shapes.Line(*points1[(i+1)%len(points1)], *points2[i], color=(0, 0, 0), batch=batchTrack) for i in range(len(points1))])
    border.append([shapes.Line(*points2[i], *points2[(i+1)%len(points1)], color=(0, 0, 0), batch=batchTrack) for i in range(len(points1))])
    triangles.append(border)
    return triangles

def bezierQubic(points, t):
    return (1-t)**3*points[0]+3*(1-t)**2*t*points[1]+3*(1-t)*t**2*points[2]+t**3*points[3]
        
def bezierQuadratic(p: np.ndarray, t: float) -> np.ndarray:
    """(4, 2) -> (2)"""
    return (1-t)**2*3*(p[1]-p[0])+2*(1-t)*t*3*(p[2]-p[1])+t**2*3*(p[3]-p[2])

def bezierLinear(p: np.ndarray, t: float) -> np.ndarray:
    """(4, 2) -> (2)"""
    return -6*(-p[0]*(1-t)+p[1]*(2-3*t)+3*p[2]*t-p[2]-p[3]*t)

def carSetPos(pos: np.ndarray):
    carShapes[0].x, carShapes[0].y = pos[0]
    carShapes[0].x2, carShapes[0].y2 = pos[1]
    carShapes[0].x3, carShapes[0].y3 = pos[2]
    carShapes[1].x, carShapes[1].y = pos[1]
    carShapes[1].x2, carShapes[1].y2 = pos[2]
    carShapes[1].x3, carShapes[1].y3 = pos[3]

    carShapes[2].x, carShapes[2].y = pos[0]
    carShapes[2].x2, carShapes[2].y2 = pos[2]
    carShapes[3].x, carShapes[3].y = pos[1]
    carShapes[3].x2, carShapes[3].y2 = pos[3]
    carShapes[4].x, carShapes[4].y = pos[0]
    carShapes[4].x2, carShapes[4].y2 = pos[1]
    carShapes[5].x, carShapes[5].y = pos[2]
    carShapes[5].x2, carShapes[5].y2 = pos[3]
    carShapes[6].x, carShapes[6].y = pos[1]
    carShapes[6].x2, carShapes[6].y2 = pos[2]

def carMakePos(pos: np.ndarray, size: np.ndarray):
    return np.array([pos+[-size[0]/2, -size[1]/2],
                     pos+[size[0]/2, -size[1]/2],
                     pos+[-size[0]/2, size[1]/2],
                     pos+[size[0]/2, size[1]/2]])

def rotate(points: np.ndarray, rpoint: np.ndarray, angle: float):
    rotation = np.array([[np.cos(angle), -np.sin(angle), 0],
                        [np.sin(angle),  np.cos(angle), 0],
                        [0,          0,         1]])
    
    translation = np.identity(3)
    translation[:2, 2] = rpoint

    translationNeg = np.identity(3)
    translationNeg[:2, 2] = -rpoint

    rotatedPoints = np.zeros_like(points)
    for i in range(len(points)):
        rotatedPoints[i] = (translation @ rotation @ translationNeg @ np.append(points[i], 1).reshape(3,1)).flatten()[:2]

    return rotatedPoints

# (Height, Width), (Segment, t), pos, vel, acc, (rot, 0), (w, s), (a, d)
car = np.array([[20, 40], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], dtype=np.float32)
carShapes = [shapes.Triangle(0, 0, 0, 0, 0, 0, color=(255, 0, 0), batch=batchCar), shapes.Triangle(0, 0, 0, 0, 0, 0, color=(255, 0, 0), batch=batchCar), *[shapes.Line(0, 0, 0, 0, color=(0, 0, 0), batch=batchCar) for i in range(5)]]
carAcc = shapes.Line(0, 0, 0, 0, 4, color=(0, 255, 0), batch=batchCar)
track = []

def genTrack():
    bezierPoints = np.array([[np.random.randint(WWidth/8, WWidth/4), np.random.randint(WWidth/8, WHeight/4)], [np.random.randint(WWidth/8, WWidth/4), np.random.randint(WHeight/4*3, WHeight/8*7)], [np.random.randint(WWidth/4*3, WWidth/8*7), np.random.randint(WHeight/4*3, WHeight/8*7)], [np.random.randint(WWidth/4*3, WWidth/8*7), np.random.randint(WWidth/8, WHeight/4)]])

    WEIGHT = 0.1
    kpoints = np.array([(bezierPoints[i]+(bezierPoints[(i+1)%len(bezierPoints)]-(bezierPoints[(i-1)%len(bezierPoints)]))*WEIGHT, bezierPoints[i]-(bezierPoints[(i+1)%len(bezierPoints)]-(bezierPoints[(i-1)%len(bezierPoints)]))*WEIGHT) for i in range(len(bezierPoints))]).flatten().reshape(-1, 2)

    allPoints = np.flip(np.insert(kpoints.reshape(len(bezierPoints), 2, 2), 1, bezierPoints, axis=1), axis=1).reshape(-1, 2)
    allPoints = np.array([np.concatenate((allPoints[1+i*3:5+i*3], allPoints[:(i%4-1)*(i//3)])) for i in range(4)])

    der = np.array([[bezierQuadratic(i, j/20) for i in allPoints] for j in range(20)])

    derPoints = np.array([[bezierQubic(i, j/20) for i in allPoints] for j in range(20)])

    norm = np.flip(der/np.linalg.norm(der, axis=2)[:, :, None], axis=2)
    norm[:, :, 0] = -norm[:, :, 0]

    outer = np.flip(np.rot90(derPoints+norm*25, axes=(1, 0)), axis=1).reshape(-1, 2)
    inner = np.flip(np.rot90(derPoints-norm*25, axes=(1, 0)), axis=1).reshape(-1, 2)

    triangels = drawTriangle(outer, inner, color=(255, 255, 255))
    return allPoints, outer, inner, triangels

def updateCarAuto(dt):
    global track
    v1 = -3*track[0][int(car[1, 0]), 0]+9*track[0][int(car[1, 0]), 1]-9*track[0][int(car[1, 0]), 2]+3*track[0][int(car[1, 0]), 3]
    v2 = 6*track[0][int(car[1, 0]), 0]-12*track[0][int(car[1, 0]), 1]+6*track[0][int(car[1, 0]), 2]
    v3 = -3*track[0][int(car[1, 0]), 0]+3*track[0][int(car[1, 0]), 1]
    car[1, 1] += 160*dt/np.linalg.norm(car[1, 1]**2*v1+car[1, 1]*v2+v3)
    if car[1, 1] >= 1:
        car[1, 0] = (car[1, 0]+1)%4
        car[1, 1] = 0
    pos = bezierQubic(track[0][int(car[1, 0])], car[1, 1])
    car[2] = pos
    norm = (v:=bezierQuadratic(track[0][int(car[1, 0])], car[1, 1]))/np.linalg.norm(v)
    angle = np.arctan2(-norm[0], norm[1])
    car[5, 0] = angle
    points = carMakePos(pos, car[0])
    rpoints = rotate(points, pos, angle)

    carSetPos(rpoints)

def updateCarManual(dt):
    car[4] = np.array([0, 0])
    if car[7, 0]:
        car[5, 0] += 1*dt
    if car[7, 1]:
        car[5, 0] -= 1*dt
    if not car[3].any():
        car[4] = np.array([0, 0])
    if car[6, 0]:
        car[4] = car[4] + rotate(np.array([[0, 40]], dtype=float), np.array([0, 0]), car[5, 0])[0]
    elif car[6, 1]:
        norm = car[3]/np.linalg.norm(car[3])
        car[4] = car[4]-min(np.linalg.norm(car[3]), 40)*norm
    car[3] = car[3]+car[4]*dt
    if car[3].any() and not car[6, 0]:
        norm = car[3]/np.linalg.norm(car[3])
        car[4] = car[4]-min(np.linalg.norm(car[3]), 10)*norm
        car[3] = car[3]+car[4]*dt
        norm = car[3]/np.linalg.norm(car[3])
        car[3] = min(np.linalg.norm(car[3]+car[4]*dt), 50)*norm
    car[2] = car[2]+car[3]*dt

    carPoints = rotate(carMakePos(car[2], car[0]), car[2], car[5, 0])
    carSetPos(carPoints)
    
    oLines = np.roll(track[1], 1, axis=0)-track[1]
    iLines = np.roll(track[2], 1, axis=0)-track[2]

    carLines = np.roll(carPoints, 1, axis=0)-carPoints
    for i in range(len(carLines)):
        q = carPoints[i]
        s = carLines[i]
        for j in range(len(oLines)):
            p = track[1][j]
            r = oLines[j]
            sXr = np.cross(s, r)
            t = np.cross((p-q), r)/sXr
            u = np.cross((p-q), s)/sXr
            if sXr!=0 and 0<=t<=1 and 0<=u<=1:
                print("GAME OVER")
                pyglet.app.exit()
        for j in range(len(iLines)):
            p = track[2][j]
            r = iLines[j]
            sXr = np.cross(s, r)
            t = np.cross((p-q), r)/sXr
            u = np.cross((p-q), s)/sXr
            if sXr!=0 and 0<=t<=1 and 0<=u<=1:
                print("GAME OVER")
                pyglet.app.exit()
        


@window.event
def on_key_press(symbol, modifiers):
    global TASK
    match symbol:
        case pyglet.window.key.SPACE:
            TASK = (TASK+1)%3
            match TASK:
                case 0:
                    pyglet.clock.unschedule(updateCarManual)
                    pyglet.clock.schedule_interval(update, 1.5)
                case 1:
                    pyglet.clock.unschedule(update)
                    pyglet.clock.schedule_interval(updateCarAuto, 1/60)
                case 2:
                    pyglet.clock.unschedule(updateCarAuto)
                    pyglet.clock.schedule_interval(updateCarManual, 1/60)
        case pyglet.window.key.W:
            car[6, 0] = 1
        case pyglet.window.key.S:
            car[6, 1] = 1
        case pyglet.window.key.A:
            car[7, 0] = 1
        case pyglet.window.key.D:
            car[7, 1] = 1
    

@window.event
def on_key_release(symbol, modifiers):
    match symbol:
        case pyglet.window.key.W:
            car[6, 0] = 0
        case pyglet.window.key.S:
            car[6, 1] = 0
        case pyglet.window.key.A:
            car[7, 0] = 0
        case pyglet.window.key.D:
            car[7, 1] = 0

def update(dt):
    global track
    track = genTrack()

pyglet.clock.schedule_interval(update, 1.5)
update(0)

@window.event
def on_draw():
    window.clear()
    batchTrack.draw()
    if TASK == 1 or TASK == 2:
        batchCar.draw()

pyglet.app.run()