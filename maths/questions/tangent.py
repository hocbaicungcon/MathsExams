import sympy
import random
from ..symbols import x
from .. import all_functions, not_named_yet
from ..latex import solutions
from . import relationships
import itertools
import os
import pickle


question_not_complete = True


def enumerate_quadratics():
    """Generate all quadratics for a certain range of coefficients.

    e.g. y = x**2 + 1, y = x**2 + 2, and so on
    """
    leading_coefficients = [i for i in range(-5, 6) if i != 0]
    coefficients = [leading_coefficients, range(-10, 11), range(-10, 11)]

    quadratic_coefficients = itertools.product(*coefficients)

    for coeffs in quadratic_coefficients:
        yield coeffs[0]*x**2 + coeffs[1]*x + coeffs[2]


def enumerate_cubics():
    """Generate all cubics for a certain range of coefficients.

    e.g. y = x**3 + 1, y = x**3 + 2, and so on
    """
    leading_coefficients = [i for i in range(-5, 6) if i != 0]
    coefficients = [leading_coefficients, range(-10, 11), range(-10, 11), range(-10, 11)]

    cubic_coefficients = itertools.product(*coefficients)

    for coeffs in cubic_coefficients:
        yield coeffs[0]*x**3 + coeffs[1]*x**2 + coeffs[2]*x + coeffs[3]


def enumerate_curves():
    """Combine multiple generators into one to allow easy calling.
    """
    yield from enumerate_quadratics()
    yield from enumerate_cubics()


def enumerate_tangents(curve, domain=list(range(-5, 6))):
    """Generate all tangents over a domain for a given curve.
    """

    for x_coordinate in domain:
        y_coordinate_at_point_of_tangency = curve.subs({x: x_coordinate})
        curve_gradient_at_point_of_tangency = curve.diff().subs({x: x_coordinate})

        tangent_y_intercept = y_coordinate_at_point_of_tangency - curve_gradient_at_point_of_tangency * x_coordinate

        enumerate_tangents.current_x = x_coordinate
        yield curve_gradient_at_point_of_tangency * x + tangent_y_intercept


def is_reasonable_point(coordinates):
    """Check if the point of tangency has student-friendly coordinates.

    We don't need to check the x-coordinate since we set it in
    enumerate_tangents.
    """

    if not isinstance(coordinates[1], sympy.Integer):
        return False
    elif coordinates[1] not in sympy.Interval(-20, 20):
        return False
    return True


def is_reasonable_tangent(tangent):
    """Check if the tangent has student-friendly coefficients.
    """

    gradient = tangent.coeff(x, 1)
    if not isinstance(gradient, sympy.Integer):
        return False
    elif gradient not in sympy.Interval(-5, 5):
        return False
    elif gradient == 0:
        return False

    y_intercept = tangent.coeff(x, 0)
    if not isinstance(y_intercept, sympy.Integer):
        return False
    elif y_intercept not in sympy.Interval(-10, 10):
        return False

    return True


def polynomial_coefficients(polynomial):
    """Return the coefficients of a polynomial in descending order of degree.

    >>> polynomial_coefficients(2*x**2 + 5*x - 3)
    [2, 5, -3]
    """
    degree = polynomial.as_poly().degree()

    return [polynomial.coeff(x, i) for i in range(degree, -1, -1)]


@relationships.root
class Tangent(relationships.QuestionPart):
    """ A question on tangents!
    """


    @classmethod
    def enumerate_questions(cls):
        """Generate all possible question numbers that have student-friendly values.
        """

        for curve in enumerate_curves():
            for tangent in enumerate_tangents(curve):
                point_of_tangency = (enumerate_tangents.current_x, tangent.subs({x: enumerate_tangents.current_x}))
                if is_reasonable_point(point_of_tangency) and is_reasonable_tangent(tangent):
                    yield {'tangent': tangent, 'curve': curve}


    def __init__(self):
        self.num_lines, self.num_marks = -1, -1
        self._qp = Tangent.scan_random_question()



    def question_statement(self):
        self._qi = {}



        return r'''$$'''




    def solution_statement(self):
        lines = solutions.Lines()



        return lines.write()
