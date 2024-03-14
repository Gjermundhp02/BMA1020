import numpy as np
import math as m

# a)

def integrate_ex1(f, start, stop, dt):
    return np.sum(np.vectorize(f)(np.arange(start, stop, dt))*dt)

# b) 

def integrate_ex2(f, start, stop, dt):
    np.sum(np.vectorize(lambda x1, x2: f(x1)+f(x2)/2)(np.arange(start, stop, dt), np.arange(start+1, stop+1, dt))*dt)
print(int(100*integrate_ex2(m.sin, 1, 6, 0.02))/100)
# c)

def integrate_ex3(f, start, stop, dt):
    pass # delete this line before starting
