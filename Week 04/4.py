from sympy import sin, cos, sqrt, symbols
from sympy.matrices import Matrix
a = symbols("a")
b = symbols("b")
c = symbols("c")
α = symbols("α")

u = Matrix([a, b, c])

Rz = Matrix([[a/sqrt(a**2+b**2), +b/sqrt(a**2+b**2), 0], 
            [-b/sqrt(a**2+b**2), a/sqrt(a**2+b**2), 0],
            [0, 0, 1]])

Rzu = Rz*u

Ry = Matrix([[Rzu[0], 0, Rzu[2]], 
            [0, 1, 0],
            [-Rzu[2], 0, Rzu[0]]])

Ru=Ry*Rzu

print(Ru)
Rx = Matrix([[1, 0, 0],
            [0, cos(α), -sin(α)], 
            [0, sin(α),  cos(α)]])

Ru=Rx*Ru

Ry = Matrix([[-Rzu[0], 0, -Rzu[2]], 
            [0, 1, 0],
            [Rzu[2], 0, -Rzu[0]]])
Ru=Ry*Ru
Rz = Matrix([[-a/sqrt(a**2+b**2), -b/sqrt(a**2+b**2), 0], 
            [b/sqrt(a**2+b**2), -a/sqrt(a**2+b**2), 0],
            [0, 0, 1]])

Ru=Rz*Ru


# print(Ru)