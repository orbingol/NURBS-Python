"""
.. module:: interpolate
    :platform: Unix, Windows
    :synopsis: Provides global interpolation functions for parametric shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import utilities
from . import helpers


def interpolate_curve(points, degree, **kwargs):
    """ Applies global curve interpolation through the input points.

    :param points: points on the curve
    :type points: list, tuple
    :param degree: degree of the output parametric curve
    :type degree: int
    :return: interpolated B-Spline curve
    :rtype: BSpline.Curve
    """
    # Keyword arguments
    clamped = kwargs.get('clamped', True)
    span_func = kwargs.get('span_func', helpers.find_span_linear)

    # Number of control points
    num_cpts = len(points)

    # Number of knots
    m = num_cpts + degree + 1

    # Number of middle knots
    m_ends = degree + 1 if clamped else 1
    m_compute = m - (m_ends * 2)

    # Start knot vector
    kv = [0.0 for _ in range(m_ends)]

    # Chord length parametrization
    ubar = [0.0 for _ in range(num_cpts + 1)]
    ubar[-1] = 1.0
    for i in range(1, num_cpts):
        ubar[i] = utilities.point_distance(points[i], points[i - 1])
    # Find total chord length
    d = sum(ubar[1:-1])
    # Divide individual chord lengths by the total chord length
    uk = [0.0 for _ in range(num_cpts)]
    for i in range(num_cpts):
        uk[i] = sum(ubar[0:i + 1]) / d

    # Use averaging to compute middle knots in the knot vector
    if m_compute > 0:
        for i in range(m_compute):
            temp_kv = (1.0 / degree) * sum([uk[j] for j in range(i + 1, i + degree + 1)])
            kv.append(temp_kv)

    # End knot vector
    kv += [1.0 for _ in range(m_ends)]

    # Set up coefficient matrix
    matrix_a = [[0.0 for _ in range(num_cpts)] for _ in range(num_cpts)]
    for i in range(num_cpts):
        span = span_func(degree, kv, num_cpts, uk[i])
        bfuncs = helpers.basis_function(degree, kv, span, uk[i])
        matrix_a[i][span-degree:span+1] = bfuncs

    # Solve system of linear equations
    pass
