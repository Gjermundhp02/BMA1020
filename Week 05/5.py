import pyglet
from pyglet import shapes, text
from math import sqrt

window = pyglet.window.Window(500, 500)
batch = pyglet.graphics.Batch()

red=(255, 0, 0) # Color1
green=(0, 255, 0) # Color2
blue=(0, 0, 255) # Color3
yellow=(255, 255, 0) # Color4

movingCircles = [[shapes.Circle(10, 10, 10, color=red, batch=batch), 
                  20,                   # startposx
                  window.height-(30+i), # startposy
                  230,                  # endposx
                  window.height-(30+i), # endposy
                  1/5,                  # velocity
                  0,                    # tpos  
                  0,                    # dir
                  0,                    # posparam
                  lambda i: movingCircles[i][6] = 0,
                  ] for i in range(0, 150, 50)]

movingCircles[1][5] = 1/2
movingCircles[2][5] = 1/2

def translate(start, end, t):
    return (1-t)*start + t*end

circle1 = {
    "shape": shapes.Circle(10, 10, 10, color=red, batch=batch),
    "startposx": 20,
    "startposy": window.height-30,
    "endposx": 230,
    "endposy": window.height-30,
    "tpos": 0
}
circle2 = {
    "shape": shapes.Circle(10, 20, 10, color=yellow, batch=batch),
    "startposx": 20,
    "startposy": window.height-80,
    "endposx": 230,
    "endposy": window.height-80,
    "tpos": 0,
    "dir": 1
}
circle3 = {
    "shape": shapes.Circle(10, 20, 10, color=blue, batch=batch),
    "startposx": 130,
    "startposy": window.height-130,
    "endposx": 230,
    "endposy": window.height-80,
    "tpos": 0,
    "dir": 1,
    "posparam": 0
}
circle4 = {
    "shape": shapes.Circle(10, 10, 10, color=red, batch=batch),
    "startposx": 20,
    "startposy": window.height-180,
    "endposx": 230,
    "endposy": window.height-80,
    "tpos": 0,
    "dir": 1,
    "posparam": 0
}
circle5 = {
    "shape": shapes.Circle(50, 50, 50, color=red, batch=batch),
    "startsize": 0,
    "endsize": 50,
    "sizeparam": 0,
    "tsize": 0,
    "dir": 1
}
circle6 = {
    "shape": shapes.Circle(150, 50, 50, color=red, batch=batch),
    "startcolor": red,
    "endcolor": green,
    "tcolor": 0,
    "dir": 1
}
circle7 = {
    "shape": shapes.Circle(250, 50, 50, color=red, batch=batch),
    "startcolor": green,
    "endcolor": yellow,
    "startsize": 0,
    "endsize": 50,
    "t": 0,
    "dir": 1
}


tpos = 0

def update(dt):
    circle1["tpos"] += (1/5)*dt
    if circle1["tpos"] >= 1:
        circle1["tpos"] = 0
    circle1["shape"].x = (1-circle1["tpos"])*circle1['startposx'] + circle1["tpos"]*circle1["endposx"]
    circle1["shape"].y = (1-circle1["tpos"])*circle1['startposy'] + circle1["tpos"]*circle1["endposy"]

    circle2["tpos"] += (1/2)*dt*circle2["dir"]
    if circle2["tpos"] >= 1 or circle2["tpos"] < 0:
        circle2["dir"] = -circle2["dir"]
    circle2["shape"].x = (1-circle2["tpos"])*circle2['startposx'] + circle2["tpos"]*circle2["endposx"]
    circle2["shape"].y = (1-circle2["tpos"])*circle2['startposy'] + circle2["tpos"]*circle2["endposy"]

    circle3["tpos"] += (1/2)*dt*circle3["dir"]
    circle3["posparam"] = circle3["tpos"]**2*(3-2*circle3["tpos"])
    if circle3["tpos"] >= 1 or circle3["tpos"] < 0:
        circle3["dir"] = -circle3["dir"]
    circle3["shape"].x = (1-circle3["posparam"])*circle3['startposx'] + circle3["posparam"]*circle3["endposx"]
    circle3["shape"].y = (1-circle3["posparam"])*circle3['startposy'] + circle3["posparam"]*circle3["endposy"]

    circle4["tpos"] += (1/5)*dt*circle4["dir"]
    if dir == 1:
        circle4["posparam"] = circle4["tpos"]**3
    else:
        circle4["posparam"] = 1-(1-circle4["tpos"])**3
    if circle4["tpos"] >= 1 or circle4["tpos"] <= 0:
        circle4["dir"] = -circle4["dir"]
    circle4["shape"].x = circle4["startposx"]+circle4["posparam"]*(circle4["endposx"]-circle4["startposx"])
    circle4["shape"].y = circle4["startposy"]+circle4["posparam"]*(circle4["endposy"]-circle4["startposy"])

    circle5["tsize"] += (1/2)*dt*circle5["dir"]
    circle5["sizeparam"] = circle5["tsize"]**2*(3-2*circle5["tsize"])
    if circle5["tsize"] >= 1 or circle5["tsize"] <= 0:
        circle5["dir"] = -circle5["dir"]
    circle5["shape"].radius = (1-circle5["sizeparam"])*circle5["startsize"] + circle5["sizeparam"]*circle5["endsize"]

    circle6["tcolor"] += (1/2)*dt*circle6["dir"]
    if circle6["tcolor"] >= 1 or circle6["tcolor"] <= 0:
        circle6["dir"] = -circle6["dir"]
    circle6["shape"].color = (int((1-circle6["tcolor"])*circle6["startcolor"][0] + circle6["tcolor"]*circle6["endcolor"][0]),
                               int((1-circle6["tcolor"])*circle6["startcolor"][1] + circle6["tcolor"]*circle6["endcolor"][1]),
                               int((1-circle6["tcolor"])*circle6["startcolor"][2] + circle6["tcolor"]*circle6["endcolor"][2]))
    
    circle7["t"] += (1/2)*dt*circle7["dir"]
    circle7["param"] = circle7["t"]**2*(3-2*circle7["t"])
    if circle7["t"] >= 1 or circle7["t"] <= 0:
        circle7["dir"] = -circle7["dir"]
    circle7["shape"].radius = (1-circle7["param"])*circle7["startsize"] + circle7["param"]*circle7["endsize"]
    circle7["shape"].color = (int((1-circle7["param"])*circle7["startcolor"][0] + circle7["param"]*circle7["endcolor"][0]),
                               int((1-circle7["param"])*circle7["startcolor"][1] + circle7["param"]*circle7["endcolor"][1]),
                               int((1-circle7["param"])*circle7["startcolor"][2] + circle7["param"]*circle7["endcolor"][2]))



pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()