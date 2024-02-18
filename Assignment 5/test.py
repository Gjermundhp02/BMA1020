import numpy as np

m1 = np.zeros((10, 5))
m2 = np.zeros((5, 3))
m3 = m1 @ m2
print(m3.shape)