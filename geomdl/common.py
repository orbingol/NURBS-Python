"""
.. module:: common
    :platform: Unix, Windows
    :synopsis: Common utility functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""


def linspace(start, stop, num, decimals=6):
    """ Returns a list of evenly spaced numbers over a specified interval.

    Inspired from Numpy's linspace function: https://github.com/numpy/numpy/blob/master/numpy/core/function_base.py

    :param start: starting value
    :type start: float
    :param stop: end value
    :type stop: float
    :param num: number of samples to generate
    :type num: int
    :param decimals: number of significands
    :type decimals: int
    :return: a list of equally spaced numbers
    :rtype: list
    """
    start = float(start)
    stop = float(stop)
    num = int(num)
    div = num - 1
    delta = stop - start
    return [float(("%0." + str(decimals) + "f") % (float(x) * delta / div)) for x in range(num)]


def find_span(knot_vector, num_ctrlpts, knot):
    """ Finds the span of the knot over the input knot vector.

    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: int
    :param knot: knot
    :type knot: float
    :return: span of the knot over the knot vector
    :rtype: int
    """
    span = 0  # Knot span index starts from zero
    while span < num_ctrlpts and knot_vector[span] <= knot:
        span += 1

    return span - 1


def find_spans(knot_vector, num_ctrlpts, knots):
    """ Find spans of a knot list over the input knot vector.

    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: int
    :param knots: list of knots
    :type knots: list, tuple
    :return: list of spans
    :rtype: list
    """
    spans = []
    for knot in knots:
        spans.append(find_span(knot_vector, num_ctrlpts, knot))
    return spans


def basis_function(degree, knot_vector, span, knot):
    """ Computes the non-vanishing basis functions for a single knot.

    Implementation of Algorithm A2.2 in The NURBS Book by Piegl & Tiller.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param span: span of the knot
    :type span: int
    :param knot: knot
    :type knot: float
    :return: basis functions
    :rtype: list
    """
    left = [0.0 for _ in range(degree + 1)]
    right = [0.0 for _ in range(degree + 1)]
    N = [1.0 for _ in range(degree + 1)]  # N[0] = 1.0 by definition

    for j in range(1, degree + 1):
        left[j] = knot - knot_vector[span + 1 - j]
        right[j] = knot_vector[span + j] - knot
        saved = 0.0
        for r in range(0, j):
            temp = N[r] / (right[r + 1] + left[j - r])
            N[r] = saved + right[r + 1] * temp
            saved = left[j - r] * temp
        N[j] = saved

    return N


def basis_functions(degree, knot_vector, spans, knots):
    """ Computes the non-vanishing basis functions.

    Implementation of Algorithm A2.2 in The NURBS Book by Piegl & Tiller.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param spans: spans
    :type spans:  list, tuple
    :param knots: knots
    :type knots: list, float
    :return: basis functions
    :rtype: list
    """
    basis = []
    for span, knot in zip(spans, knots):
        basis.append(basis_function(degree, knot_vector, span, knot))
    return basis
