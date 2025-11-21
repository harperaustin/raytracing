import math
import numpy as np

from vector import Vector
from object import Sphere
from colour import Colour

class Intersection():

    @staticmethod
    def nearestIntersection(intersections):
        nearestIntersection = None
        for intersection in intersections:
            if intersection.intersects == True:
                if nearestIntersection == None:
                    nearestIntersection = intersection
                else:
                    if intersection.distance < nearestIntersection.distance:
                        nearestIntersection = intersection
        return nearestIntersection

    """
    Intersection bundles all information to determine how to shade a point
    """
    def __init__(self, intersects=False, distance=None, point=None, normal=None, object=None, bounces=0, through_count=0):
        self.intersects = intersects
        self.distance = distance
        self.point = point
        self.normal = normal
        self.object = object
        self.bounces = bounces
        self.through_count=through_count

    def directionRGB(self):
        # ray has not landed on anything, but might get light from light sources

        # test
        return Colour(0, 255,)
    
    """
    Computes the the final color from where the point landed.
    """
    def terminalRGB(self, spheres, background_colour=Colour(0, 0, 0), global_light_sources=[], point_light_sources=[], max_bounces=0):
        # colour of the thing landed on
        reflectivity, transparency, emitivity = self.object.material.reflective, self.object.material.transparent, self.object.material.emitive 
        
        illumination = self.object.colour.scaleRGB(emitivity)      # does not take distance from camera into account

        for light in global_light_sources:
            angle_to_light = self.normal.angleBetween(light.vector)
            illumination = illumination.addColour(light.relativeStrength(angle_to_light))
        
        for light in point_light_sources:
            if self.object.id != light.id:
                vector_to_light = light.position.subtractVector(self.point)
                ray_to_light = Ray(
                    origin=self.point,
                    D=vector_to_light
                )
                ray_to_light_terminus = ray_to_light.nearestSphereIntersect(spheres, suppress_ids=[self.object.id], max_bounces=max_bounces)

                if ray_to_light_terminus != None:
                    # clear line of sight
                    if ray_to_light_terminus.object.id == light.id:

                        angle_to_light = self.normal.angleBetween(vector_to_light)
                        distance_to_light = vector_to_light.magnitude()
                        illumination = illumination.addColour(light.relativeStrength(angl