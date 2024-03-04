# We create a random adjacency matrix for you to work with - don't change this code
import numpy as np
np.random.seed(0)
M = np.random.rand(30,30)  # a random matrix, entries are floats between 0..1
M[M > 0.9] = 1.0           # all entries > 0.9 become 1.0 and give arrows
M[M <= 0.9] = 0.0          # all entries <= 0.9 become 0.0, and give no arrows.

# a)

# Compute the vector av. We should have av[0]=1.0 and av[i] = 0.0 for other i.
# Hint: np.zeros will help
av = np.zeros(30)
av[0] = 1.0

# Compute the number of arrows from vertex 0 to vertex 5 and put it in the variable a5)
a5 = (M@av)[5]

# Compute the number of arrows from vertex 0 to vertex 11 and put the answer in the variable a11
a11 = (M@av)[11]

# Compute the number of loops at 0 and put the answer in the variable numloops.
numloops = (M@av)[0]


# b)

# Compute the number of paths from vertex 0 to vertex 8 of length 2.
num082 = (M@M@av)[8]

# Compute the number of paths from vertex 0 to vertex 10 of length 3.
num0103 = (M@M@M@av)[10]

# Compute the number of paths from vertex 0 to vertex 11 of length 5.
num0115 = (M@M@M@M@M@av)[11]

