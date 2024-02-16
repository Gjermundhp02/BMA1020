import numpy as np

# Work with these matrices
M1 = np.array([[1,2,3], [4,5,6], [7,8,9]])
M2 = np.array([[1,1,1], [1,0,1], [1,1,1]])


#
# Answer to question a)
#
matA = M1*M2

#
# Answer to question b)
#
matB = M1@M2

#
# Answer to question c)
#
matC = 2*np.linalg.matrix_power(matA, 3)+np.eye(3)
print(matC)

