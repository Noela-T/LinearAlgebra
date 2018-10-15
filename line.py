from decimal import Decimal, getcontext
from vector import  Vector
getcontext().prec = 30

class Line(object):
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'
    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension=2
        if not normal_vector:
            all_zeros=['0']*self.dimension
            normal_vector=Vector(all_zeros)
        self.normal_vector=normal_vector

        if not constant_term:
            constant_term=Decimal('0')
        self.constant_term=Decimal(constant_term)

        self.set_basepoint()

    def set_basepoint(self):
        try:
            n=self.normal_vector
            c=self.constant_term
            basepoint_coords = ['0']*self.dimension
            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]
            basepoint_coords[initial_index] = c/Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)
        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __str__(self):
        num_decimal_places = 3
        def write_coefficient(coefficient,is_initial_term=False):
            coefficient=round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)
            output = ''
            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'
            if not is_initial_term:
                output += " "
            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))
            return output
        n = self.normal_vector
        try:
            initial_index= Line.first_nonzero_index(n)
            terms=[write_coefficient(n[i], is_initial_term=(i==initial_index))
                    + 'x_{}'.format(i+1) for i in range(self.dimension)
                    if round(n[i],num_decimal_places) != 0]
            output = ' '.join(terms)
        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)
        return output

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def is_parallel_to(self,l):
        v1=Vector(self.normal_vector)
        v2=Vector(l.normal_vector)
        return v1.is_parallel(v2)

    def __eq__(self,l):
        if not self.is_parallel_to(l):
            return False
        x0=self.basepoint
        y0=l.basepoint
        basepoint_diff = x0.minus(y0)
        n=Vector(self.normal_vector)
        return basepoint_diff.is_orthogonal(n)

    def intersect_at(self, l):
        if self.is_parallel_to(l):
            return "The Lines do not intersect because they are parallel to each other"
        elif self==l:
            return "Infinitely many intersection points because the lines are equal"
        else:
            n1=self.normal_vector
            n2=l.normal_vector
            deno = Decimal((n1[0]*n2[1])-(n1[1]*n2[0]))
            x_point=((Decimal(n2[1])*self.constant_term)-(Decimal(n1[1])*l.constant_term))/deno
            y_point=((Decimal(n1[0])*l.constant_term)-(Decimal(n2[0])*self.constant_term))/deno
            return Vector([x_point,y_point])


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
