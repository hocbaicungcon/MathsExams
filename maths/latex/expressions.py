from ..symbols import x0, x1, x2, x
from . import latex, solutions
from ..utils import functions
import sympy


def integral(lb, ub, expr, var=x):
    """Return LaTeX that displays a definite integral.
    """

    if expr.has(sympy.log):
        expr = expr.replace(sympy.log(x0), sympy.log(x0, evaluate=False))

    return r'\displaystyle\int^{{{0}}}_{{{1}}} {2}\ d{3}'.format(sympy.latex(ub), sympy.latex(lb), sympy.latex(expr), sympy.latex(var))


def integral_intermediate(lb, ub, expr, var=x):
    """Return LaTeX for the 'square bracket' intermediate form used for
    evaluating a definite integral.
    """

    antideriv = expr.integrate(var)

    if antideriv.has(sympy.log):
        antideriv = antideriv.replace(sympy.log(x0), sympy.log(sympy.Abs(x0), evaluate=False))

    return r'\left[{0}\right]^{{{1}}}_{{{2}}}'.format(sympy.latex(antideriv), sympy.latex(ub), sympy.latex(lb))


def integral_intermediate_eval(lb, ub, expr, var=x):
    """Return LaTex that displays both evaluated bounds of the integral.

    >>> k = sympy.Symbol('k')
    >>> y = -k + 1
    >>> integral_intermediate_eval(lb=-5, ub=5, expr=y)
    '- 5 k + 5 - (5 k - 5)'
    """

    antideriv = expr.integrate(var)

    if antideriv.has(sympy.log):
        antideriv = antideriv.replace(sympy.log(x0), sympy.log(sympy.Abs(x0), evaluate=False))

    left = antideriv.subs({var: ub})
    right = antideriv.subs({var: lb})

    if isinstance(right, sympy.Add):  # an expression like (-1 + sqrt(3)/2) or (k + 1)
        return r'{0} - ({1})'.format(sympy.latex(left), sympy.latex(right))
    elif right.could_extract_minus_sign():
        return r'{0} - ({1})'.format(sympy.latex(left), sympy.latex(right))
    else:
        return r'{0} - {1}'.format(sympy.latex(left), sympy.latex(right))


def integral_trifecta(lb, ub, expr, var=x):
    """A wrapper for returning the multiple forms an integral takes when it
    gets evaluated.
    """

    return (
        integral(lb, ub, expr, var),
        integral_intermediate(lb, ub, expr, var),
        integral_intermediate_eval(lb, ub, expr, var)
    )


def derivative(upper_variable, lower_variable, degree=1):
    """Return LaTeX to display a derivative in the form dy/dx or du/dt.
    """

    if degree != 1:
        numerator = 'd^{degree}{upper_variable}'.format(degree=degree, upper_variable=upper_variable)
        denominator = 'd{lower_variable}^{degree}'.format(degree=degree, lower_variable=lower_variable)
    else:
        numerator = 'd{upper_variable}'.format(upper_variable=upper_variable)
        denominator = 'd{lower_variable}'.format(lower_variable=lower_variable)

    return r'\frac{{{numerator}}}{{{denominator}}}'.format(
        numerator=numerator,
        denominator=denominator
    )


def piecewise(func):
    """Return LaTeX to display a piecewise expression.
    """

    line_begin = '\n' + r'\begin{cases}' + '\n'
    line_end = r'\end{cases}' + '\n'

    lines = []
    for expr in func.args:
        if isinstance(expr[1], (sympy.StrictLessThan, sympy.LessThan, sympy.StrictGreaterThan, sympy.GreaterThan, sympy.And, sympy.Or)):
            interval = sympy.latex(functions.relation_to_interval(expr[1]))
            lines.append('\t' + r'{0} & \text{{for}}\: {1} \in {2}'.format(sympy.latex(expr[0]), func.free_symbols.pop(), interval) + '\n')
        else:
            lines.append('\t' + r'{0} & \: \text{{otherwise}}'.format(sympy.latex(expr[0])) + '\n')

        lines.append(latex.latex_newline())

    return line_begin + ''.join(lines) + line_end


def symbolic_discrete_expectation_x(degree=1):
    """Return LaTeX to display the symbolic expectation of a variable.

    i.e. Using sigma notation and without any specific number values.
    """

    if degree != 1:
        return r'\sum\limits_{{i=1}}^{{n}} x_{{i}}^{degree} \times Pr(X = x_{{i}})'.format(degree=degree)
    else:
        return r'\sum\limits_{{i=1}}^{{n}} x_{{i}} \times Pr(X = x_{{i}})'


def discrete_expectation_x_squared(prob_table):
    """Return LaTeX to display the summation of data points used to calculate
    the expectation of a variable squared.
    """

    return ' + '.join([r'{0}^2 \times {1}'.format(k, sympy.latex(v)) for k, v in prob_table.items()])


def discrete_expectation_x(prob_table):
    """Return LaTeX to display the summation of data points used to calculate
    the expectation of a variable.
    """

    return ' + '.join([r'{0} \times {1}'.format(k, sympy.latex(v)) for k, v in prob_table.items()])


def quadratic_formula(quadratic, var=x):
    """Return LaTeX to display the quadratic formula used to find a
    quadratic's solutions.
    """
    match = quadratic.match(x0 * var ** 2 + x1 * var + x2)

    a = r'({0})'.format(sympy.latex(match[x0])) if match[x0].could_extract_minus_sign() else sympy.latex(match[x0])
    b = r'({0})'.format(sympy.latex(match[x1])) if match[x1].could_extract_minus_sign() else sympy.latex(match[x1])
    c = r'({0})'.format(sympy.latex(match[x2])) if match[x2].could_extract_minus_sign() else sympy.latex(match[x2])

    return r'\dfrac{{-{1} \pm \sqrt{{{1}^2 - 4 \times {0} \times {2}}}}}{{2 \times{0}}}'.format(a, b, c)


def conditional_probability(givee, given):
    """Return LaTeX to display a conditional probability.
    """
    return r'\frac{{ Pr({0} \cap {1}) }}{{ Pr({1}) }}'.format(givee, given)


def shrink_solution_set(expr, domain, expr_equal_to=0, var=x):
    """Return LaTeX to state values that are invalid due to being outside of
    the domain.

    e.g. c = 5/3, 7/3
    but c is in the domain [1, 2], so c = 5/3
    """

    var_solutions = sympy.solve(expr - expr_equal_to)

    lines = solutions.Lines()

    var_solutions_text = ', '.join([sympy.latex(i) for i in var_solutions])
    # HERE IS WHERE I WAS WORKING UP TO
    lines += r'${0} = {1}$'.format(sympy.latex(var), var_solutions_text)

    smaller_set_text = ', '.join([sympy.latex(i) for i in var_solutions if i in domain])

    if isinstance(domain, sympy.Interval) and domain.left == -sympy.oo:
        domain_text = r'{0} {1} {2}'.format(sympy.latex(var), r'\le' if domain.right_open else r'\lte', sympy.latex(domain.right))
    elif isinstance(domain, sympy.Interval) and domain.right == sympy.oo:
        domain_text = r'{0} {1} {2}'.format(sympy.latex(var), r'\ge' if domain.right_open else r'\gte', sympy.latex(domain.left))
    else:
        domain_text = r'{0} \in {1}'.format(sympy.latex(var), sympy.latex(domain))

    lines += r'but ${0}$, so ${1} = {2}$'.format(domain_text, sympy.latex(var), smaller_set_text)

    return lines


def relation(interval_or_relation, var=x):
    """Return LaTeX that represents an interval or a relation as a chained inequality.

    e.g. [1, 5] --> 1 < x < 5
    """
    if isinstance(interval_or_relation, (sympy.StrictLessThan, sympy.LessThan, sympy.StrictGreaterThan, sympy.GreaterThan)):
        interval = functions.relation_to_interval(interval_or_relation)
    else:
        interval = interval_or_relation

    if isinstance(interval_or_relation, sympy.Union):
        raise NotImplementedError('unions are not yet supported')

    if interval.left == -sympy.oo and interval.right == sympy.oo:
        return r'{0} < {1} < {2}'.format(sympy.latex(-sympy.oo), sympy.latex(var), sympy.latex(sympy.oo))
    elif interval.left == -sympy.oo:
        operator = r'<' if interval.right_open else r'\le'
        return r'{0} {1} {2}'.format(sympy.latex(var), operator, sympy.latex(interval.right))
    elif interval.right == sympy.oo:
        operator = r'>' if interval.left_open else r'\ge'
        return r'{0} {1} {2}'.format(sympy.latex(var), operator, sympy.latex(interval.left))
    else:
        left_operator = r'<' if interval.left_open else r'\le'
        right_operator = r'<' if interval.right_open else r'\le'
        return r'{0} {1} {2} {3} {4}'.format(
            sympy.latex(interval.left),
            left_operator,
            sympy.latex(var),
            right_operator,
            sympy.latex(interval.right)
        )


def union_of_probabilities(probabilities):
    """Return LaTeX to represent a union of probabilities.
    """

    return r' \cap '.join(probabilities)


def sum_combination_probabilities(combinations):
    """Return LaTeX to represent the sum of the probabilities of selecting particular
    combinations of items.
    """

    probabilities = []
    n_selections = len(combinations[0])
    for combination in combinations:
        event = union_of_probabilities(['ball_{ball_number} = {ball_value}'.format(
            ball_number=index + 1, ball_value=item_value) for index, item_value in enumerate(combination)])

        probability = r'{n_selections}! \times Pr({event})'.format(
            n_selections=n_selections,
            event=event
        )

        probabilities.append(probability)

    return ' + '.join(probabilities)


def sum_permutation_probabilities(permutations):
    """Return LaTeX to represent the sum of the probabilities of selecting particular
    permutations of items.
    """

    probabilities = []
    for permutation in permutations:
        event = union_of_probabilities(['ball_{ball_number} = {ball_value}'.format(
            ball_number=index + 1, ball_value=item_value) for index, item_value in enumerate(permutation)])

        probabilities.append(
            r'Pr({event})'.format(event=event)
        )

    return ' + '.join(probabilities)
