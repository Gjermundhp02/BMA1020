import numpy as np

np.random.seed(5)
M = np.random.rand(20,20)
M[M <= 0.8] = 0.0
M[M > 0.8] = 1.0

# Compute the required matrix and store it in the variable answer
lenM = [np.linalg.matrix_power(M,i) for i in range(20)]
answer = np.zeros_like(M)+999
for i in range(0, 20):
    sume = sum([lenM[j] for j in range(i+1)])
    sume[sume>0] = i+1
    sume[sume==0] = 999
    answer = np.minimum(answer, sume)

answer[answer==999] = 20

