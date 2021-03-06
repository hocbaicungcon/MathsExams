import sympy
import random
import gmpy
from ... import not_named_yet
from ...symbols import *

coefficients_bound = 5


class Quadratic(object):
    """ Return a quadratic polynomial in one variable.

    Keyword arguments:
    difficulty: influences the type of equation generated

    Public attributes:
    equation -- the actual equation of the polynomial
    discriminant -- the discriminant of the quadratic
    domain -- which is always the reals for a quadratic
    range -- the range of the quadratic

    """

    def __init__(self, difficulty):

        if difficulty not in [1, 2, 3]:
            raise ValueError('You gave an invalid difficulty of %d!' % difficulty)

        while True:
            a = not_named_yet.randint_no_zero(-coefficients_bound + 2, coefficients_bound - 2)
            b = random.randint(-coefficients_bound * 4, coefficients_bound * 4)
            c = random.randint(-coefficients_bound * 4, coefficients_bound * 4)
            discriminant = b ** 2 - 4 * a * c
            if difficulty == 1 and discriminant == 0 and (b == 0 or c == 0):
                break
            elif difficulty == 2 and discriminant > 0 and gmpy.is_square(discriminant):
                break
            elif difficulty == 3 and discriminant > 0 and not gmpy.is_square(discriminant):
                break

        self.equation = a * x ** 2 + b * x + c
        self.discriminant = b ** 2 - 4 * a * c

        self.domain = sympy.Interval(-sympy.oo, sympy.oo, True, True)
        vertex_x = -sympy.Rational(b, 2*a)
        vertex_y = self.equation.subs({x: vertex_x})

        if a > 0:
            self.range = sympy.Interval(vertex_y, sympy.oo, False, True)
        else:
            self.range = sympy.Interval(-sympy.oo, vertex_y, True, False)
