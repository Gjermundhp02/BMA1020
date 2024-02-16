import numpy as np


#
# Answer to question a)
#
A = np.array([[3, 3, 1], [1, -3, 2], [1, 1, -5]])
b = np.array([1, 2, 3])
solA = np.linalg.solve(A, b)

#
# Answer to question b)
#
A = np.array([[3, 3, 1], [1, -3, 2], [1, 1, -5]])
b = np.array([8, 2, 6])
solB = np.linalg.solve(A, b)


#
# Answer to question c)
#
A = A
Ainv = np.linalg.inv(A)
b = b
solC =  Ainv@b
