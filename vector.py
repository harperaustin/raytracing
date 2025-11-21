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

    # adding a vector
    def addVector(self, B, inplace=False):
        if inplace:
            self.x += B.x
            self.y += B.y
            self.z += B.z
            return self
        return Vector(self.x + B.x, self.y + B.y, self.z + B.z)
    
    # subtracting a vector
    def subtractVector(self, B, inplace=False):
        if inplace == True:
            self.x -= B.x
            self.y -= B.y
            self.z -= B.z
            return self
        return Vector(self.x - B.x, self.y - B.y, self.z - B.z)


    # inverting a vector
    def invert(self, inplace=False):
        if inplace == True:
            self.x = -self.x
            self.y = -self.y
            self.z = -self.z
            return self
        return Vector(-self.x, -self.y, -self.z)
    
    # scaling a vector by a factor of l
    def scaleByLength(self, l, inplace=False):
        if inplace == True:
            self.x *= l
            self.y *= l
            self.z *= l
            return self
        else:
            return Vector(self.x * l, self.y * l, self.z * l)

    # find the distance from this vector and vector B 
    def distanceFrom(self, B):
        return math.sqrt((B.x - self.x)**2 + (B.y - self.y)**2 + (B.z - self.z)**2)

    # find thge angle between this vector and vector B using the dot product identity
    def angleBetween(self, B):
        return arccos(self.dotProduct(B) / (self.magnitude() * B.magnitude()))


    # calculates the reflection vector from A over B. Reflect A over B
    def reflectInVector(self, B):
        v = self.normalise()
        normal = B.normalise()
        return v.subtractVector(normal.scaleByLength(2 * v.dotProduct(normal))).normalise()

    # perform the dot product between this vector and vector B
    def dotProduct(self, B):
        return self.x * B.x + self.y * B.y + self.z * B.z

    # computes a vector that is orthognal/perpendicular to both this vector and B.
    def crossProduct(self, B):
        return Vector(
            x=self.y*B.z - self.z*B.y,
            y=self.z*B.x - self.x*B.z,
            z=self.x*B.y - self.y*B.x
        )

    # computes the length of the vector 
    def magnitude(self):
        dotProduct = self.dotProduct(self)
        return math.sqrt(dotProduct)

    # computes a vector that points in same direction but has a length of 1.
    def normalise(self):
        magnitude = self.magnitude()
        return Vector(x=self.x/magnitude, y=self.y/magnitude, z=self.z/magnitude)

    # multiplies this vector by a matrix
    def multiplyByMatrix(self, T):
        return self.fromNpArray(np.matmul(self.toNpArray(), T))

    # rotates the vector by this angle
    def rotate(self, angle, inplace=False):
        a, b, c = angle.x, angle.y, angle.z
        R = np.array([
            [cos(c)*cos(b)*cos(a) - sin(c)*sin(a), cos(c)*cos(b)*sin(a) + sin(c)*cos(a), -cos(c)*sin(b)],
            [-sin(c)*cos(b)*cos(a) - cos(c)*sin(a), -sin(c)*cos(b)*sin(a) + cos(c)*cos(a), sin(c)*sin(b)],
            [sin(b)*cos(a), sin(b)*sin(a), cos(b)]
        ])
        V = np.matmul(