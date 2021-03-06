import sympy
import random
from .. import all_functions, not_named_yet, simplify
from ..latex import solutions
from ..symbols import x
from . import relationships


@relationships.root
class SimpleInverse(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the derivative of an equation.


    Real-life instances
    ===================

    2008 10a: [6 lines] [2 marks]
    2009 3: [7 lines] [3 marks]
    2012 3: [5 lines] [2 marks]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 7, 3

        self._qp = {}

        self._qp['function_type'] = random.choice(['exp', 'hyperbola', 'log', 'cubic'])

        if self._qp['function_type'] == 'exp':
            func = all_functions.request_exp(difficulty=3)
            self._qp['domain'], self._qp['range'] = func.domain, func.range

            self._qp['equation'] = func.equation
            self._qp['inverse'] = simplify.canonise_log(all_functions.inverse(self._qp['equation']))

        elif self._qp['function_type'] == 'hyperbola':
            func = all_functions.request_hyperbola(difficulty=3)
            self._qp['domain'], self._qp['range'] = func.domain, func.range

            self._qp['equation'] = func.equation
            self._qp['inverse'] = sympy.apart(all_functions.inverse(self._qp['equation']))

        elif self._qp['function_type'] == 'log':
            func = all_functions.request_log(difficulty=3)
            self._qp['domain'], self._qp['range'] = func.domain, func.range

            self._qp['equation'] = func.equation
            self._qp['inverse'] = all_functions.inverse(self._qp['equation'])

        elif self._qp['function_type'] == 'cubic':  # no base class for cubics so I make it here
            m = not_named_yet.randint_no_zero(-3, 3)
            c = not_named_yet.randint_no_zero(-5, 5)
            self._qp['equation'] = m * x ** 3 + c
            self._qp['inverse'] = all_functions.inverse(self._qp['equation'])

            if random.choice([True, False]):
                self._qp['domain'] = sympy.Interval(-sympy.oo, 0)
                if m > 0:
                    self._qp['range'] = sympy.Interval(-sympy.oo, c)
                else:
                    self._qp['range'] = sympy.Interval(c, sympy.oo)
            else:
                self._qp['domain'] = sympy.Interval(0, sympy.oo)
                if m > 0:
                    self._qp['range'] = sympy.Interval(c, sympy.oo)
                else:
                    self._qp['range'] = sympy.Interval(-sympy.oo, c)

        self._qp['inverse_domain'] = self._qp['range']

    def question_statement(self):
        return r'''Let $f:{domain} \rightarrow R$, where $f(x) = {equation}$. Find $f^{{-1}}$,
            the inverse function of $f$.'''.format(
            **solutions.latexify_question_information(self._qp)
        )

    def solution_statement(self):
        lines = solutions.Lines()

        lines += r'$d_{{f^{{-1}}}} = r_{{f}} = {inverse_domain}$'.format(
            **solutions.latexify_question_information(self._qp)
        )

        lines += r'$f^{{-1}}(x) = {inverse}$'.format(
            **solutions.latexify_question_information(self._qp)
        )

        return lines.write()
