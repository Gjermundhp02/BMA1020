import numpy as np
import math as m

# a)

def integrate_ex1(f, start, stop, dt):
    return np.sum(np.vectorize(f)(np.arange(start, stop, dt))*dt)
print(integrate_ex1(m.sin, 0, 5, 0.01))
# b) 

def integrate_ex2(f, start, stop, dt):
    return np.sum(np.vectorize(lambda x1, x2: (f(x1)+f(x2))/2)(np.arange(start, stop-dt, dt), np.arange(start+dt, stop, dt))*dt)
print(int(100*integrate_ex2(m.sin, 1, 6, 0.02))/100)
# c)
# Simpson's 1/3 rule
def integrate_ex3(f, start, stop, dt):
    n = 2
    x = np.arange(start, stop, dt)
    return (1/3)*((stop-start)/n)*(f(start)+4*np.sum(x[]))+2*np.sum(np.vectorize(f)(np.arange(start, n/2, 1)))+f(stop))
print(integrate_ex3(m.sin, 2, 7, 0.03))