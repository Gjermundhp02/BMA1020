import pyglet
from pyglet import shapes
from random import randint

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()
batch2 = pyglet.graphics.Batch()

circle = shapes.Circle(700, 150, 100, color=(50, 225, 30), batch=batch)
rectangle = shapes.Rectangle(250, 300, 400, 200, color=(255, 22, 20), batch=batch)
line = shapes.Line(100, 100, 100, 200, width=19, batch=batch)
star = shapes.Star(800, 400, 60, 40, num_spikes=20, color=(255, 255, 0), batch=batch)
ellipse = shapes.Ellipse(100, 200, 200, 100, color=(200, 20, 20), batch=batch)
triangle = shapes.Triangle(700, 500, 800, 525, 700, 550, color=(255, 22, 20), batch=batch)
box = shapes.Box(0, 0, 50, 51, color=(32, 211, 22), batch=batch)
sector = shapes.Sector(50+40, 51+40, 80, angle=209, start_angle=1, color=(33, 22, 200), batch=batch)
arc = shapes.Arc(200, 200, 20, angle=2, color=(222, 222, 0), batch=batch)
borderRectangle = shapes.BorderedRectangle(350, 100, 100, 100, border=10, color=(255, 0, 255), batch=batch)

circleArr = []
for i in range(1000):
    circleArr.append(shapes.Circle(randint(0, 960), randint(0, 540), 10, color=(randint(0, 255), randint(0, 255), randint(0, 255)), batch=batch2))

@window.event
def on_draw():
    window.clear()
    batch.draw()
    batch2.draw()

pyglet.app.run()