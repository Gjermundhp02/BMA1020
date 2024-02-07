from compositeBody import Circle
import pyglet
from pyglet.math import Vec2

window = pyglet.window.Window(960, 540)

circle = Circle(Vec2(window.width/2, window.height/2), 50, Vec2(1, 0), color=(255, 0, 0), components=[
    Circle(Vec2(0, -100), 50, color=(0, 255, 0))
])

pyglet.clock.schedule_interval(circle.updateComponents, 1)

@window.event
def on_draw():
    window.clear()
    circle.batch.draw()

pyglet.app.run()