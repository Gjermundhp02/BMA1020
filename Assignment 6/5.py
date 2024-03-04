import numpy as np

A = np.array([[1, -2], [4, 2]])
b = np.array([-6, 26])

print(np.linalg.solve(A, b))