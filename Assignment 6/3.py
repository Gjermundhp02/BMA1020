import numpy as np

np.random.seed(5)
M = np.random.rand(20,20)
M[M <= 0.8] = 0.0
M[M > 0.8] = 1.0

# Compute the required matrix and store it in the variable answer
lenM = [np.linalg.matrix_power(M,i) for i in range(20)]
answer = np.zeros_like(M)
#lenM[j]@(np.zeros(30)[:, :] := 1)
for x in range(0, 2):
    for y in range(0, 2):
            av = np.zeros(20)
            av[y] = 1
            l = lenM[x]@av
            print(l)
            answer[y, l>0] =x
#
# for i in range(0, 2):
#     sume = sum([lenM[j] for j in range(i+1)])
#     print(sume)
#     sume[sume>0] = i+1
#     sume[sume==0] = 999
#     answer = np.minimum(answer, sume)

# answer[answer==999] = 20

print(M)
print(answer)