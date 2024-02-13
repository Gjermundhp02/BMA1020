import math as m

def myDiff(f, t, dt):
    return (f(t + dt) - f(t-dt)) / (2.0*dt)

print(myDiff(lambda t : m.sin(t) + m.cos(t), 2, 0.1))