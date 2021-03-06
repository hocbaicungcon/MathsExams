import sympy


def probability_table(prob_table):

    try:
        values = ' & '.join([sympy.latex(float(value)) for value in prob_table.values()])
    except:
        values = ' & '.join([r'${0}$'.format(sympy.latex(value.together())) for value in prob_table.values()])

    return r'''
        \begin{{tabularx}}{{\textwidth}}{{ {0} }}
            \hline
            {1} & {2} \\
            \hline
            {3} & {4} \\
            \hline
        \end{{tabularx}}'''.format('|' + 'X|' * (len(prob_table) + 1),
                                    'x',
                                    ' & '.join([sympy.latex(key) for key in list(prob_table.keys())]),
                                    r'Pr(X = $x_{i}$)',
                                    values
                                )
