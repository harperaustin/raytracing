import math
import numpy as np

from vector import Vector, Angle
from object import Sphere
from colour import Colour

print("Ray module reloaded")

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

    def __init__(self, intersects=False, distance=None, point=None, normal=None, object=None, bounces=0, through_count=0):
        self.intersects = intersects
        self.distance = distance
        self.point = point
        self.normal = normal
        self.object = object
        self.bounces = bounces
        self.through_count=through_count



    """
    Given a ray that hit an object, what is the final color of that pixel considering all light sources?
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
                        illumination = illumination.addColour(light.relativeStrength(angle_to_light, distance_to_light))

        # resolve final total of illumination
        return background_colour.addColour(self.object.colour.illuminate(illumination))


class Ray():
    def __init__(self, origin, D):
        self.origin = origin
        self.D = D.normalise()  # direction in vector


    """
    Find where a ray intersects a given sphere
    """
    def sphereDiscriminant(self, sphere, point=0):      # set point to 1 when you want the second intersection
        # ray origin and direction
        O = self.origin
        D = self.D
        C = sphere.centre
        r = sphere.radius

        L = C.subtractVector(O)
        tca = L.dotProduct(D)
        
        d2 = L.dotProduct(L) - tca*tca
        if d2 > r*r:
            return Intersection()

        thc = math.sqrt(max(0, r*r - d2))
        t0 = tca - thc
        t1 = tca + thc

        # pick smallest positive t
        t = None
        if t0 > 1e-6:
            t = t0
        elif t1 > 1e-6:
            t = t1
        else:
            return Intersection()

        phit = O.addVector(D.scaleByLength(t))
        nhit = phit.subtractVector(C).normalise()
        return Intersection(True, t, phit, nhit, sphere)


    # calculates the ray that exits a transparent sphere after traveling through it.
    def sphereExitRay(self, sphere, intersection):

        # refract at first intersection
        refracted_ray_D = self.D.refractInVector(intersection.normal, 1, sphere.material.refractive_index)

        # get internal ray
        internal_ray = Ray(
            origin=intersection.point,
            D=refracted_ray_D
        )

        # get second intersection
        exit_intersection = internal_ray.sphereDiscriminant(sphere=sphere, point=1)

        exit_ray_D = None
        exit = False

        n = 0
        while (exit == False) & (n < 10):
            n+=1

            # refract exit ray
            exit_ray_D = refracted_ray_D.refractInVector(exit_intersection.normal.invert(), sphere.material.refractive_index, 1)

            if exit_ray_D != False:
                exit = True
            else:
                # Total internal reflection, ray gets trapped inside
                refracted_ray_D = refracted_ray_D.reflectInVector(exit_intersection.normal)
                # find next exit point
                exit_ray = Ray(
                    origin=exit_intersection.point,
                    D=refracted_ray_D
                )
                exit_intersection = exit_ray.sphereDiscriminant(sphere=sphere, point=1)
            
        if exit == True:

            return Ray(
                exit_intersection.point,
                exit_ray_D
            )

        # TRAPPED RAY:
        print("TRAPPED RAY:")
        self.origin.describe()
        self.D.describe()

        return None

    # returns the nearest sphere intersection associated with a ray. Accounts for reflections and refractions.
    def nearestSphereIntersect(self, spheres, suppress_ids=[], bounces=0, max_bounces=1, through_count=0):

        intersections = []

        for i, sphere in enumerate(spheres):
            if sphere.id not in suppress_ids:
                intersections.append(self.sphereDiscriminant(sphere))

        nearestIntersection = Intersection.nearestIntersection(intersections)
        
        if nearestIntersection == None:
            return None

        if bounces > max_bounces:
            return None

        nearestIntersection.bounces = bounces
        nearestIntersection.through_count = through_count

        # NB - reflective objects return background colour if no reflections found
        if nearestIntersection.object.material.reflective == True:
            reflected_ray_D = self.D.reflectInVector(nearestIntersection.normal)
            
            reflected_ray = Ray(
                origin=nearestIntersection.point,
                D=reflected_ray_D
            )
            bounces += 1
            suppress_ids = [nearestIntersection.object.id]
            reflected_terminus = reflected_ray.nearestSphereIntersect(
                spheres=spheres,
                suppress_ids=suppress_ids,
                bounces=bounces,
                max_bounces=max_bounces,
                through_count=through_count
            )

            if reflected_terminus != None:
                return reflected_terminus
            
            return nearestIntersection

        # check for refraction
        if nearestIntersection.object.material.transparent == True:

            sphere_exit_ray = self.sphereExitRay(
                sphere=nearestIntersection.object,
                intersection=nearestIntersection
            )

            if sphere_exit_ray == None:
                return None
            
            bounces += 1
            through_count += 1
            suppress_ids = [nearestIntersection.object.id]

            reflected_terminus = sphere_exit_ray.nearestSphereIntersect(
                spheres=spheres,
                suppress_ids=suppress_ids,
                bounces=bounces,
                max_bounces=max_bounces,
                through_count=through_count
            )

            if reflected_terminus != None:
                return reflected_terminus

            return None

        return nearestIntersection

