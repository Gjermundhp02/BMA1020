import numpy as np
import timeit

np.random.seed(5)
M = np.random.rand(20,20)
M[M <= 0.8] = 0.0
M[M > 0.8] = 1.0

# Compute the required matrix and store it in the variable answer
def my():
    lenM = [np.linalg.matrix_power(M,i) for i in range(20)]
    answer = np.zeros_like(M)
    for i in range(0,19):
        answer[answer == 0] = np.where(lenM[i][answer == 0] != 0, i, 0)

def mark():
    lenM = [np.linalg.matrix_power(M, i) for i in range(20)]
    answer = np.zeros((20,20))
    for i in range(0,19):
        answer = np.array([[i if lenM[i][j][k] != 0 and answer[j][k] == 0 else answer[j][k] for k in range(20)] for j in range(20)])
    answer[answer == 0] = 1

execs = 1000
print(timeit.timeit(his, number=execs)/timeit.timeit(my, number=execs))

