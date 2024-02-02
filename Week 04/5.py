from sympy import pi, sin, cos, sqrt, symbols, pprint
from sympy.matrices import Matrix
a = symbols("a")
b = symbols("b")
c = symbols("c")

α = symbols("α")

u = Matrix([a, b, c])
x = Matrix([1, 0, 0])
y = Matrix([0, 1, 0])
z = Matrix([0, 0, 1])
K = Matrix([[0, -c, b], [c, 0, -a], [-b, a, 0]])

I = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
R = Matrix(I+(1-cos(α))*K*K)

print(cos(α)*z+(1-cos(α))*u.dot(z)*u)