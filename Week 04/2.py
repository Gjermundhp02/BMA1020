from sympy import pi, sin, cos
from sympy.matrices import Matrix

u = Matrix([4, 3])
v = Matrix([1, 0])
w = Matrix([0, 1])
uv = u.dot(v)/u.dot(u)*u
uw = u.dot(w)/u.dot(u)*u
M = Matrix([[uv[0], uw[0]], [uv[1], uw[1]]])

a = pi/4
r = Matrix([[cos(a), -sin(a)], [sin(a), cos(a)]])
t = Matrix([[1, 0], [0, -1]])
rm = Matrix([[cos(-pi/4), -sin(-pi/4)], [sin(-pi/4), cos(-pi/4)]])
v = Matrix([3, 4])

print(r*t*rm*v)
print(M*Matrix([-4, 5]))