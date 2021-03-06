from .relations.polynomials import absolute_value, quadratic, linear, hyperbola
from .relations.trigonometry import trig
from .relations.logarithms import log
from .relations.exponentials import exp
from .symbols import *
import random


def random_function(linear_difficulty=None,
                    quadratic_difficulty=None,
                    log_difficulty=None,
                    trig_difficulty=None,
                    exp_difficulty=None,
                    exclude=None):

    if linear_difficulty is None:
        linear_difficulty = random.randint(1, 2)
    if quadratic_difficulty is None:
        quadratic_difficulty = random.randint(1, 3)
    if log_difficulty is None:
        log_difficulty = random.randint(1, 2)
    if trig_difficulty is None:
        trig_difficulty = random.randint(1, 2)
    if exp_difficulty is None:
        exp_difficulty = random.randint(1, 3)
    if exclude is None:
        exclude = []

    ''' linear_difficulty:
                1: y = m * x (m != 0)
                2: y = x + c
                3: y = m * x + c (m not in [0, 1])

        quadratic_difficulty:
                1: discriminant = 0
                2: discriminant > 0 and is a square number and the squared term coefficient is positive
                3: discriminant > 0 and is not a square number and the squared term coefficient is positive
                4: discriminant < 0 and is a square number
                5: discriminant < 0 and is not a square number

        log_difficulty:
                1: y = a * ln(b * x) + c, b > 0
                2: y = a * ln(b * x) + c, b < 0

        trig_difficulty: (we can use any of sin, cos or tan but we will use sin)
                1: y = sin([pi * ]*q*x)
                2: y = sin([pi * ]*q*x + k)


        exp_difficulty:
                1: y = e^(k * x)
                2: y = e^(k * x) + c
                3: y = a * e^(k * x) + c
    '''

    while True:
        function = random.sample(['linear', 'quadratic', 'log', 'trig', 'exp'], 1)[0]
        if function not in exclude:
            break

    if function == 'trig':
        function = random.choice(['sin', 'cos', 'tan'])

    return {
        'linear': linear.Linear(linear_difficulty),
        'quadratic': quadratic.Quadratic(quadratic_difficulty),
        'log': log.Log(log_difficulty),
        'sin': trig.Sin(trig_difficulty),
        'cos': trig.Cos(trig_difficulty),
        'tan': trig.Tan(trig_difficulty),
        'exp': exp.Exp(exp_difficulty)}[function]


def random_function_type():
    return random.choice([
        sympy.sin, sympy.cos, sympy.tan,
        sympy.log,  # it's the natural log, ln
        sympy.exp,
        sympy.sqrt])


def inverse(function):  # requires future work as more things are included

    symbols = function.free_symbols

    if len(symbols) == 1:
        var = symbols.pop()
    else:
        raise ValueError('The function needs to have only one parameter, instead it had these: {0}'.format(symbols))

    solutions = sympy.solve(function - y, var)

    if function.as_poly().degree() == 3:
        for solution in solutions:
            if sympy.ask(sympy.Q.extended_real(solution), sympy.Q.real(y)):
                return solution.replace(y, var)

    if len(solutions) > 1:
        return solutions[1].replace(y, var)
    else:
        return solutions[0].replace(y, var)


def request_linear(difficulty, var=x):
    return linear.request_linear(difficulty, var)


def request_quadratic(difficulty):
    return quadratic.Quadratic(difficulty)


def request_exp(difficulty):
    return exp.Exp(difficulty)


def request_log(difficulty):
    return log.Log(difficulty)


def request_absolute_value(difficulty):
    return absolute_value.AbsoluteValue(difficulty)


def request_hyperbola(difficulty):
    return hyperbola.Hyperbola(difficulty)


def request_sin(difficulty):
    return trig.Sin(difficulty)


def request_cos(difficulty):
    return trig.Cos(difficulty)


def request_tan(difficulty):
    return trig.Tan(difficulty)


def request_trig(difficulty=None):
    function_type = random.choice(['sin', 'cos', 'tan'])

    if difficulty is None:
        difficulty = random.randint(1, 2)

    if function_type == 'sin':
        return request_sin(difficulty)
    if function_type == 'cos':
        return request_cos(difficulty)
    if function_type == 'tan':
        return request_tan(difficulty)


# for use when matching - e.g. say we have y = tan(2*x), we have to do y.match(a*tan(b) + c) - what if we don't know what the trig function is?
# that's what this function is for
def detect_expr_type(expr):
    sympy_types = [sympy.cos, sympy.sin, sympy.tan, sympy.cot, sympy.sec, sympy.csc, sympy.log, sympy.exp]

    found_types = 0
    for sympy_type in sympy_types:
        if expr.find(sympy_type):
            found_types += 1

    if found_types > 1:
        raise ValueError('This expression has more than one type: {0}'.format(expr))

    for sympy_type in sympy_types:
        if expr.has(sympy_type):
            return sympy_type

    if expr.is_polynomial():
        degree = expr.as_poly().degree()
        return sympy.poly(x ** degree, x)


# takes an ordered list of x-values, and selects two values to return as a lower/upper bound pair
def choose_bounds(x_values):
    def test_is_list(x_values):
        assert isinstance(x_values, list)

    def test_is_sorted(x_values):  # my first ever test
        assert x_values == sorted(x_values)

    # remember that len(list) - 1 (not len(list)) gives the final index of a list
    l_index = random.randint(0, len(x_values) - 2)  # choose any index except the last
    u_index = random.randint(l_index + 1, len(x_values) - 1)

    def test_indices_order(l_index, u_index):
        assert l_index < u_index

    return (x_values[l_index], x_values[u_index])


# returns a principal domain of x values that compute nicely in a trig function
def sensible_trig_x_values(function):
    # assume inner_function is a linear function - it always is in questions

    if function.has(sympy.sin):
        trig_type = sympy.sin
    elif function.has(sympy.cos):
        trig_type = sympy.cos
    elif function.has(sympy.tan):
        trig_type = sympy.tan

    inner_function = function.find(trig_type).pop().args[0]

    if trig_type in [sympy.sin, sympy.cos]:
        primary_x_values = [sympy.pi / 6 * i for i in range(-5, 7)]
    elif trig_type == sympy.tan:
        primary_x_values = [sympy.pi / 6 * i for i in range(-5, 7) if i not in [-3, 3]]  # tan(-pi/2) and tan(pi/2) are undefined, so exclude those x-values

    secondary_x_values = [sympy.solve(inner_function - i)[0] for i in primary_x_values]

    return secondary_x_values
