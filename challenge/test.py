
import pyglet
from pyglet import shapes

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

curve = shapes.BezierCurve(*[[300, 300], [200, 200], [300, 400]], thickness=50, color=(255, 0, 0), batch=batch)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()