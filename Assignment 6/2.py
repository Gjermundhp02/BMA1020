# We create a random graph for you
import numpy as np
np.random.seed(1)
M = np.random.rand(10,10)
M = M + M.transpose()
M[M <= 1.2] = 0.0
M[M > 1.2] = 1.0


# a)

# Compute the list lenM using list comprehension and np.linalg.matrix_power
lenM = [np.linalg.matrix_power(M, i) for i in range(1, 10)]

# b)

# # i) Create a matrix B1 so that B1[i,j] is the number of paths of length 3 or 4 from j to i.
# B1 = lenM[3] + lenM[4]

# # ii) Create a matrix B2 so that B2[i,j] is the number of paths of length 5, 6 or 9 from j to i.
# B2 = lenM[5] + lenM[6] + lenM[9]

# # iii) Create a matrix B3 so that B3[i,j] is the number of paths of length 1..9 or less from j to i.
# b3 = [lenM[i] for i in range(10)]
# B3 = b3[1]
# for i in range(2, len(b3)): B3 += b3[i]


print(lenM)