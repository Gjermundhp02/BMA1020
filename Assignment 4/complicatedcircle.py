#
# Drawing some shapes
#
import pyglet as pg

width = 500
height = 500
window = pg.window.Window(width, height)

# you need to change coordinates y  ->  height - y.  
# pyglet has a very unusual coordinate system

import math as m
batch = pg.graphics.Batch()
myShape = []
numTriangles = 10
radius = 100
for i in range(numTriangles):
    myShape.append(  
        pg.shapes.Triangle(250,250, 
                           250 + radius*m.cos(2*m.pi*i / numTriangles), 250 + radius*m.sin(2*m.pi*i / numTriangles), 
                           250 + radius*m.cos(2*m.pi*(i+1) / numTriangles), 250 + radius*m.sin(2*m.pi*(i+1) / numTriangles),
                           batch = batch))
    

# circle is a bunch of triangles
# square is a bunch of triangles


@window.event
def on_draw():
    window.clear()
    batch.draw()

def update(dt):
    pass
    

pg.clock.schedule_interval(update, 1/60)

pg.app.run()



