import pyglet
from pyglet import shapes

window = pyglet.window.Window(500, 500)
batch = pyglet.graphics.Batch()

red=(255, 0, 0) # Color1
green=(0, 255, 0) # Color2
blue=(0, 0, 255) # Color3
yellow=(255, 255, 0) # Color4
magenta=(255, 0, 255) # Color5

movingCircles = [[shapes.Circle(10, window.height-(30+i), 20, color=red, batch=batch), 
                  20,                   # startposx
                  230,                  # endposx
                  window.height-(30+i), # startposy
                  window.height-(30+i), # endposy
                  1/5,                  # velocity
                  0,                    # tpos  
                  1,                    # dir
                  0,                    # posparam
                  ] for i in range(0, 200, 50)]

movingCircles[1][0].color = yellow
movingCircles[2][0].color = green
movingCircles[3][0].color = blue
movingCircles[1][5] = 1/2
movingCircles[2][5] = 1/2

colorCircles = [[shapes.Circle(50+i, window.height-300, 50, color=red, batch=batch),
                50,   # startsize
                50,   # endsize
                red,  # startcolor
                red,  # endcolor
                1/2,  # velocity
                0,    # t
                1,    # dir
                0     # param
                ] for i in range(0, 300, 100)]

colorCircles[0][1] = 0
colorCircles[1][4] = green
colorCircles[2][1] = 25
colorCircles[2][3] = green
colorCircles[2][4] = yellow

bezierCircles = [[shapes.Circle(0, 0, 10, color=magenta, batch=batch),
                  500,  # p1x
                  250,  # p2x
                  20,   # p3x
                  100,  # p1y
                  500,  # p2y
                  350,  # p3y
                  1/2,  # velocity
                  i*0.2/2,    # t
                  0     # param
                  ] for i in range(10)]

def translate(points, t):
    return [(1-t)*points[i]+t*points[i+1] for i in range(0, len(points), 2)]

def translateColor(color1, color2, t):
    return [translate([color1[i], color2[i]], t) for i in range(3)]

def translateBezier(points, t):
    return translate([*translate([points[0], points[1]], t), *translate([points[1], points[2]], t)], t)

def update(dt):
    for i in range(len(movingCircles)):
        if i == 0:
            movingCircles[i][6] += movingCircles[i][5]*dt
            if movingCircles[i][6] >= 1 or movingCircles[i][6] < 0:
                movingCircles[i][6] = 0
            movingCircles[i][0].x, movingCircles[i][0].y = translate(movingCircles[i][1:5], movingCircles[i][6])
        else:
            movingCircles[i][6] += movingCircles[i][5]*dt*movingCircles[i][7]
            if movingCircles[i][6] >= 1 or movingCircles[i][6] < 0:
                movingCircles[i][7] = -movingCircles[i][7]
            if i == 1:
                # set the param to be the same as the t to make the same code work on both circles
                movingCircles[i][8] = movingCircles[i][6]
            elif i == 2:
                movingCircles[i][8] = movingCircles[i][6]**2*(3-2*movingCircles[i][6])
            else:
                if movingCircles[i][7] == 1:
                    movingCircles[i][8] = movingCircles[i][6]**3
                else:
                    movingCircles[i][8] = 1-(1-movingCircles[i][6])**3
            movingCircles[i][0].x, movingCircles[i][0].y = translate(movingCircles[i][1:5], movingCircles[i][8])

    for i in range(len(colorCircles)):
        colorCircles[i][6] += colorCircles[i][5]*dt*colorCircles[i][7]
        if colorCircles[i][6] >= 1 or colorCircles[i][6] <= 0:
            colorCircles[i][7] = -colorCircles[i][7]
        if i == 0 or i == 2:
            colorCircles[i][0].radius = translate(colorCircles[i][1:3], colorCircles[i][6])[0]
        if i == 1 or i == 2:
            color = []
            for j in range(3):
                color.append(int(*translate([colorCircles[i][3][j], colorCircles[i][4][j]], colorCircles[i][6])))
            colorCircles[i][0].color = color
    
    for i in range(len(bezierCircles)):
        bezierCircles[i][8] += bezierCircles[i][7]*dt
        if bezierCircles[i][8] >= 1:
            bezierCircles[i][8] = 0
        bezierCircles[i][0].x = translateBezier(bezierCircles[i][1:4], bezierCircles[i][8])[0]
        bezierCircles[i][0].y = window.height-translateBezier(bezierCircles[i][4:7], bezierCircles[i][8])[0]

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()