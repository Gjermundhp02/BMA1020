from __future__ import annotations
from math import sin, cos, sqrt
from numpy import array

class Vector:
    def __init__(self, x: int|float, y: int|float, z=None) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __name__(self) -> str:
        return "Vector"

    def __repr__(self) -> str:
        return f"<Vector {self.x, self.y, self.z} {id(self)}>"
    
    def __str__(self) -> str:
        return f"[{self.x}, {self.y}{', '+str(self.z) if self.z!=None else ''}]"
    
    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z if self.z!=None and other.z!=None else None)
    
    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z if self.z!=None and other.z!=None else None)
    
    def __mul__(self, other: Vector|float|int) -> Vector|float|int:
        match type(other).__name__:
            case 'int'|'float':
                return Vector(self.x*other, self.y*other, self.z*other if self.z!=None else None)
            case 'Vector':
                if self.z==None and other.z==None:
                    return self.x*other.x+self.y*other.y
                else:
                    return self.x*other.x+self.y*other.y+self.z*other.z
    
    def __rmul__(self, other: Vector|float|int) -> Vector|float|int:
        match type(other).__name__:
            case 'int'|'float':
                return Vector(self.x*other, self.y*other, self.z*other if self.z!=None else None)
            case 'Vector':
                if self.z==None and other.z==None:
                    return self.x*other.x+self.y*other.y
                else:
                    return self.x*other.x+self.y*other.y+self.z*other.z
    
    # TODO: Add support for y component
    def __truediv__(self, other: int|float) -> Vector:
        return Vector(self.x/other, self.y/other)
    
    def __rtruediv__(self, other: int|float) -> Vector:
        return Vector(self.x/other, self.y/other)

    # TODO: Throw error if len < 3     
    def __matmul__(self, other: Vector) -> Vector:
        print(self, other)
        return Vector(self.y*other.z-self.z*other.y, self.z*other.x-self.x*other.z, self.x*other.y-self.y*other.x)
    
    def __abs__(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2 if self.z else 0)

    def __len__(self):
        return 3 if self.z!= None else 2
    
    def __getitem__(self, key: int):
        match key:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.z if self.z else self.__missing__(key)
            case _:
                self.__missing__(key)
    
    def __setitem__(self, key, val):
        match key:
            case 0:
                self.x = val
            case 1:
                self.y = val
            case 2:
                self.z = val
            case _:
                self.__missing__(key)
    
    def __iter__(self):
        yield self.x
        yield self.y
        if self.z: yield self.z
    
    def __missing__(self, key: int):
        raise IndexError(f"index {key} out of range")

    def rotate(self, rad: float) -> None:
        """@param rad < pi/2 - radians to rotate the vector"""
        if self.z!=None: raise NotImplementedError

        self.x, self.y = self.x*cos(rad)-self.y*sin(rad), self.x*sin(rad)+self.y*cos(rad)
        return self
    
    @staticmethod
    def proj(v: Vector, u: Vector):
        """Projects v onto u"""
        return ((u*v)/(u*u))*u
    
    @staticmethod
    def angBetween(v: Vector, u: Vector):
        pass
    
v1 = Vector(3, 4, 2)
v2 = Vector(55, 61, 55)
print(abs(v2))