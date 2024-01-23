import sympy as sp
x = sp.symbols("x")
# print(sp.solve(x**2 - 2*x - 3, x))

# scalar product of u and v
def dot(u, v):
      return u[0]*v[0] + u[1]*v[1]

# length of u
def absv(u):
      return  sp.sqrt(u[0]**2+u[1]**2)

# unit vector in the direction of u
def normalise(u):
      return [u[0]/absv(u), u[1]/absv(u)]

# Example vector
v1 = [sp.sqrt(2)/2, sp.S(2)] # Use sp.S to force numbers to be symbols 
v2 = [sp.S(3), sp.sqrt(5)]
print(normalise(v1))