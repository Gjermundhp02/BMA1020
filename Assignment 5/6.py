import numpy as np

#
# position, color index, circle radius and possible colors for circles
#
circlePos = np.array([[51.18216247, 95.04636963], [14.41596127, 94.86494471], 
                      [31.1831452,  42.3326449 ], [82.77025938, 40.91991364],
                      [54.95936877,  2.75591132]])
numCircles = circlePos.shape[0]
maxRadius = 40  # a number greater than any radius
circleRad = np.array([30.14052435, 21.52573253, 13.18926866, 31.53714814, 12.12779317])
colors = np.array([[1.0, 1.0, 0.0, 1.0],[1.0, 0.0, 0.0, 1.0]])


# a)
# Compute
posX = circlePos[:,0]
posY = circlePos[:,1]
#


# b)
#
posPairs = np.meshgrid(posX, posX)
dx = posPairs[0]-posPairs[1]
# You compute
dy = np.meshgrid(posY, posY)[0]-np.meshgrid(posY, posY)[1]
rad = np.meshgrid(circleRad, circleRad)[0]+np.meshgrid(circleRad, circleRad)[1]
# in a similar way. 


# c)
#
dist = rad - np.sqrt(dx*dx+dy*dy)

# subtract 2*maxRadius*IdentityMatrix from dist to avoid self-collision
dist -= 2*maxRadius*np.eye(numCircles)

# clamp values in dist between 0 and 1
dist = np.clip(dist, 0, 1)

# Check your answer before you continue.


# Finishing setting the colors
#
circleCol = colors[np.int32(np.max(dist,1))]
