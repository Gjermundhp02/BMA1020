#
# u, v are lists of the form [a,b,c].
#

import math as m

# the cross product of u and v
def cross(u,v):
    return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    
# the unit vector in the same direction of u
def normalise(u):
    len = m.sqrt(u[0]**2+u[1]**2+u[2]**2)
    return [u[0]/len, u[1]/len, u[2]/len]
    
# projection of u onto v
def project(u, v):
    dotUV = u[0]*v[0]+ u[1]*v[1] +u[2]*v[2]
    dotVV = v[0]*v[0]+ v[1]*v[1] +v[2]*v[2]
    scalar = dotUV/dotVV
    return [u[0]*scalar, u[1]*scalar, u[2]*scalar]

u = [[50, 55, 50], [54, 64, 56], [68, 55, 53]]
answer2 = [[int(100*c) for  c in normalise(u[i])] for i in range(3)]
print(answer2)