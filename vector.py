import math
import numpy as np
from numpy import sin, cos, tan, arccos

class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    """
    Converts an NPArray to a Vector
    """
    @staticmethod
    def fromNpArray(array):
        return Vector(x=array[0], y=array[1], z=array[2])
    
    def getXYZ(self):
        return self.x, self.y, self.z
    
    """
    Converts a vector to an np array
    """
    def toNpArray(self):
        return np.array([self.x, self.y, self.z])
    

    """
    Below are a collection of linear algebra operations to make 3D vector operations simpler
    """
    def addVector(self, B, inplace=False):
        if inplace:
            self.x += B.x
            self.y += B.y
            self.z += B.z
            return self
        return Vector(self.x + B.x, self.y + B.y, self.z + B.z)
    
    def subtractVector(self, B, inplace=False):
        if inplace == True:
            self.x -= B.x
            self.y -= B.y
            self.z -= B.z
            return self
        return Vector(self.x - B.x, self.y - B.y, self.z - B.z)

    def invert(self, inplace=False):
        if inplace == True:
            self.x = -self.x
            self.y = -self.y
            self.z = -self.z
            return self
        return Vector(-self.x, -self.y, -self.z)
    
    def scaleByLength(self, l, inplace=False):
        if inplace == True:
            self.x *= l
            self.y *= l
            self.z *= l
            return self
        else:
            return Vector(self.x * l, self.y * l, self.z * l)
    
