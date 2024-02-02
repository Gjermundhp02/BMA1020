from sympy import pi, sin, cos, sqrt, symbols
from sympy.matrices import Matrix
a = symbols("a")
b = symbols("b")
c = symbols("c")

R = Matrix([[a/sqrt(a**2+b**2), -b/sqrt(a**2+b**2), 0], 
            [a/sqrt(a**2+b**2), b/sqrt(a**2+b**2), 0],
            [0, 0, 1]])

u = Matrix([[a], [b], [c]])
Ru = R*u
print(Ru)
print(Ru[0]/sqrt(Ru[0]**2+Ru[1]**2+Ru**[2]))