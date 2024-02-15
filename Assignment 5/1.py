import numpy as np

#
# Answer to question a)
#
matA = np.zeros((10, 10))
matA[:, 4] = 1
matA[3:5, :] = 1



#
# Answer to question b)
#
matB = np.zeros((10, 10))
matB[1:9, 1:9] = 1


#
# Answer to question c)
#
matC = matA + matB


#
# Answer to question d)
#
matD = np.array([[True if i>1 else False for i in j] for j in matC])

