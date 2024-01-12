import numpy as np
from math import sin, cos, pi


A = [[0],[1]]

B = [[cos(pi/2), -sin(pi/2)], [sin(pi/2), cos(pi/2)]]
 
print(np.dot(B,A))