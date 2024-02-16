import numpy as np

#
# Answer to question a)
#
zeros = np.zeros((2, 2))
ones = np.ones((2, 3))
twos = 2*np.ones((3, 3))
threes = 3*np.ones((3, 2))
# Write your one line of code using vstack and hstack below
matA = np.vstack((np.hstack((zeros, ones)), np.hstack((threes, twos))))



#
# Answer to question b)
#
matB = matA.flatten()
# Write your one line of code here.


#
# Answer to question c)
#
matC = matA[2:6, :]




#
# Answer to question d)
#
matD = matC.T

