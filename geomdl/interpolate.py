"""
.. module:: interpolate
    :platform: Unix, Windows
    :synopsis: Provides global interpolation functions for parametric shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline
from . import utilities
from . import helpers


def interpolate_curve(points, degree, **kwargs):
    """ Applies global curve interpolation through the data points.

    Please see Algorithm A9.1 on The NURBS Book (2nd Edition), pp.369-370 for details.

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

    # Dimension
    dim = len(points[0])

    # Number of control points
    num_points = len(points)

    # Get uk
    uk = compute_knots_curve(points)

    # Get knot vector
    kv = compute_knot_vector(degree, num_points, uk, clamped)

    # Set up coefficient matrix
    matrix_a = [[0.0 for _ in range(num_points)] for _ in range(num_points)]
    for i in range(num_points):
        span = span_func(degree, kv, num_points, uk[i])
        matrix_a[i][span-degree:span+1] = helpers.basis_function(degree, kv, span, uk[i])

    # Solve system of linear equations
    matrix_l, matrix_u = utilities.lu_decomposition(matrix_a)
    ctrlpts = [[0.0 for _ in range(dim)] for _ in range(num_points)]
    for i in range(dim):
        b = [pt[i] for pt in points]
        y = utilities.forward_substitution(matrix_l, b)
        x = utilities.backward_substitution(matrix_u, y)
        for j in range(num_points):
            ctrlpts[j][i] = x[j]

    # Generate B-spline curve
    curve = BSpline.Curve()
    curve.degree = degree
    curve.ctrlpts = ctrlpts
    curve.knotvector = kv

    return curve


def compute_knot_vector(degree, num_points, param_list, clamped):
    """ Computes knot vector from the parameter list using averaging method.

    Please see Equation 9.8 on The NURBS Book (2nd Edition), pp.365 for details.

    :param degree: degree
    :type degree: int
    :param num_points: number of data points
    :type num_points: int
    :param param_list: list of parameters, :math:`\\overline{u}_{k}`
    :type param_list: list, tuple
    :param clamped: flag to generate clamped or unclamped knot vector
    :type clamped: bool
    :return: knot vector
    :rtype: list
    """
    # Number of knots
    m = num_points + degree + 1

    # Number of middle knots
    m_ends = degree + 1 if clamped else 1
    m_compute = m - (m_ends * 2)

    # Start knot vector
    kv = [0.0 for _ in range(m_ends)]

    # Use averaging method (Eqn 9.8) to compute middle knots in the knot vector
    if m_compute > 0:
        for i in range(m_compute):
            temp_kv = (1.0 / degree) * sum([param_list[j] for j in range(i + 1, i + degree + 1)])
            kv.append(temp_kv)

    # End knot vector
    kv += [1.0 for _ in range(m_ends)]

    return kv


def compute_knots_curve(points):
    """ Computes :math:`\\overline{u}_{k}` for curves using chord length parametrization.

    Please see Equations 9.4 and 9.5 on The NURBS Book (2nd Edition), pp.364-365 for details.

    :param points: data points
    :type points: list, tuple
    :return: knots array, :math:`\\overline{u}_{k}`
    :rtype: list
    """
    # Length of the points array
    num_points = len(points)

    # Calculate chord lengths
    cds = [0.0 for _ in range(num_points + 1)]
    cds[-1] = 1.0
    for i in range(1, num_points):
        cds[i] = utilities.point_distance(points[i], points[i - 1])

    # Find the total chord length
    d = sum(cds[1:-1])

    # Divide individual chord lengths by the total chord length
    uk = [0.0 for _ in range(num_points)]
    for i in range(num_points):
        uk[i] = sum(cds[0:i + 1]) / d

    return uk
