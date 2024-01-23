import pyglet
from pyglet import shapes
from random import randint

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

color=(255, 0, 0)

# [[x, y, with, height, rot, parent]]
cat = [
    [window.width/2, window.height/2, 100, 50, None],
    [-80, 50, 50, 50, 0],
    [-30, 55, 25, 25, 1],
    [30, 55, 25, 25, 1],
    [-40, -40, ]
]

def posX(start):
    return cat[start][0]+(posX(cat[start][-1]) if start>0 else 0)
def posY(start):
    return cat[start][1]+(posY(cat[start][-1]) if start>0 else 0)

catShapes=[shapes.Ellipse(posX(index), posY(index), i[2], i[3], color=color, batch=batch) for index, i in enumerate(cat)]

# catShapes.append(shapes.Ellipse(*cat[0][:-1], color=color, batch=batch))

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()