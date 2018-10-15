from math import sqrt, acos, pi
from decimal import Decimal, getcontext
getcontext().prec = 30
class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG ='Cannot normalize the sero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG ='No unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG ='No unique orthogonal component'
    ONLY_DEFINED_IN_2_3_DIMS_MSG = """Cross product of two numbers is only defined
                                    in 2 or 3 dimensional space"""
    def __init__(self,coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates=tuple(Decimal(x) for x in coordinates)
            self.dimension=len(self.coordinates)
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector:{}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def add(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def s_multiply(self, s):
        new_coordinates = [Decimal(s)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        new_coordinates = [x**2 for x in self.coordinates]
        return Decimal(sqrt(sum(new_coordinates)))

    def normalize(self):
        try:
            mag = self.magnitude()
            return self.s_multiply(Decimal('1.0')/mag)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dotPdt(self,v):
        new_coordinates = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(new_coordinates)

    def angle(self, v, in_rad=False):
        try:
            u1=self.normalize()
            u2=v.normalize()
            angle_in_rad=acos(u1.dotPdt(u2))
            if in_rad == False:
                angle_in_deg = angle_in_rad * (180/pi)
                return angle_in_deg
            else:
                return angle_in_rad
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot compute an angle with the zero vector")
            else:
                raise e

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_orthogonal(self, v, tolerance=1e-10):
        return abs(self.dotPdt(v)) < tolerance

    def is_parallel(self,v):
        return (self.is_zero() or v.is_zero() or
                self.angle(v) == 0 or
                self.angle(v) == pi)

    def projection(self,base):
        try:
            unitBase= base.normalize()
            dotbase = self.dotPdt(unitBase)
            return unitBase.s_multiply(dotbase)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal(self,base):
        try:
            projection = self.projection(base)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def convert3D(self):
        try:
            new_coordinates=[x for x in self.coordinates]
            if self.dimension == 2:
                new_vector=new_coordinates.append(0)
                return (new_vector)
            elif self.dimension == 3:
                return new_coordinates
            else:
                raise ValueError
        except ValueError as e:
            if self.dimension < 2 or self.dimension > 3:
                raise Exception(self.ONLY_DEFINED_IN_2_3_DIMS_MSG)
            else:
                raise e

    def crossPdt(self,v):
        u1=self.convert3D()
        u2=v.convert3D()
        x1,y1,z1=u1
        x2,y2,z2=u2
        crossP=[y1*z2 - y2*z1,
                x2*z1 - x1*z2,
                x1*y2 - x2*y1]
        return Vector(crossP)

    def areaPara(self,v):
        para=self.crossPdt(v)
        return para.magnitude()

    def areaTriangle(self,v):
        triangle=self.areaPara(v)
        return (triangle/Decimal('2.0'))
