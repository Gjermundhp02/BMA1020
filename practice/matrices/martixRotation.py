from numpy import array
from numpy.typing import ArrayLike
from math import sin, cos, pi

def rotate(matrix: ArrayLike, rad: float, axis: str):
    match axis:
        case 'x'|'X':
            return array([[1, 0,         0       ],
                          [0, cos(rad), -sin(rad)], 
                          [0, sin(rad),  cos(rad)]]) @ matrix
        case 'y'|'Y':
            return array([[ cos(rad), 0, sin(rad)],
                          [ 0,         1, 0,     ], 
                          [-sin(rad), 0, cos(rad)]]) @ matrix
        case 'z'|'Z':
            return array([[cos(rad), -sin(rad), 0], 
                          [sin(rad),  cos(rad), 0],
                          [0,         0,        1]]) @ matrix
