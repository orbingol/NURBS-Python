"""
.. module:: interpolate
    :platform: Unix, Windows
    :synopsis: Provides global interpolation functions for parametric shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import math
from . import BSpline
from . import utilities
from . import helpers


def interpolate_curve(points, degree, **kwargs):
    """ Curve interpolation through the data points.

    Please see Algorithm A9.1 on The NURBS Book (2nd Edition), pp.369-370 for details.

    Keyword Arguments:
        * ``clamped``: if True, a clamped curve is generated. *Default: True*
        * ``span_func``: Knot span finding function. *Default: linear search*
        * ``centripetal``: activates centripetal parametrization method. *Default: False*

    :param points: data points
    :type points: list, tuple
    :param degree: degree of the output parametric curve
    :type degree: int
    :return: interpolated B-Spline curve
    :rtype: BSpline.Curve
    """
    # Keyword arguments
    clamped = kwargs.get('clamped', True)
    span_func = kwargs.get('span_func', helpers.find_span_linear)
    use_centripetal = kwargs.get('centripetal', False)

    # Number of control points
    num_points = len(points)

    # Get uk
    uk = compute_params_curve(points, use_centripetal)

    # Compute knot vector
    kv = compute_knot_vector(degree, num_points, uk, clamped)

    # Do global interpolation
    ctrlpts = ginterp(degree, kv, points, uk, span_func)

    # Generate B-spline curve
    curve = BSpline.Curve()
    curve.degree = degree
    curve.ctrlpts = ctrlpts
    curve.knotvector = kv

    return curve


def interpolate_surface(points, size_u, size_v, degree_u, degree_v, **kwargs):
    """ Surface interpolation through the data points.

    Please see Algorithm A9.4 on The NURBS Book (2nd Edition), pp.380 for details.

    Keyword Arguments:
        * ``clamped_u``: if True, surface is clamped on the u-direction. *Default: True*
        * ``clamped_v``: if True, surface is clamped on the v-direction. *Default: True*
        * ``span_func``: knot span finding function. *Default: linear search*
        * ``centripetal``: activates centripetal parametrization method. *Default: False*

    :param points: data points
    :type points: list, tuple
    :param size_u: number of data points on the u-direction
    :type size_u: int
    :param size_v: number of data points on the v-direction
    :type size_v: int
    :param degree_u: degree of the output surface for the u-direction
    :type degree_u: int
    :param degree_v: degree of the output surface for the v-direction
    :type degree_v: int
    :return: interpolated B-Spline curve
    :rtype: BSpline.Curve
    """
    # Keyword arguments
    clamped_u = kwargs.get('clamped_u', True)
    clamped_v = kwargs.get('clamped_v', True)
    span_func = kwargs.get('span_func', helpers.find_span_linear)
    use_centripetal = kwargs.get('centripetal', False)

    # Get uk and vl
    uk, vl = compute_params_surface(points, size_u, size_v, use_centripetal)

    # Compute knot vectors
    kv_u = compute_knot_vector(degree_u, size_u, uk, clamped_u)
    kv_v = compute_knot_vector(degree_v, size_v, vl, clamped_v)

    # Do global interpolation on the u-direction
    ctrlpts_r = []
    for v in range(size_v):
        pts = [points[v + (size_v * u)] for u in range(size_u)]
        ctrlpts_r += ginterp(degree_u, kv_u, pts, uk, span_func)

    # Do global interpolation on the v-direction
    ctrlpts = []
    for u in range(size_u):
        pts = [ctrlpts_r[u + (size_u * v)] for v in range(size_v)]
        ctrlpts += ginterp(degree_v, kv_v, pts, vl, span_func)

    # Generate B-spline surface
    surf = BSpline.Surface()
    surf.degree_u = degree_u
    surf.degree_v = degree_v
    surf.ctrlpts_size_u = size_u
    surf.ctrlpts_size_v = size_v
    surf.ctrlpts = ctrlpts
    surf.knotvector_u = kv_u
    surf.knotvector_v = kv_v

    return surf


def compute_knot_vector(degree, num_points, params, clamped):
    """ Computes knot vector from the parameter list using averaging method.

    Please see Equation 9.8 on The NURBS Book (2nd Edition), pp.365 for details.

    :param degree: degree
    :type degree: int
    :param num_points: number of data points
    :type num_points: int
    :param params: list of parameters, :math:`\\overline{u}_{k}`
    :type params: list, tuple
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
            temp_kv = (1.0 / degree) * sum([params[j] for j in range(i + 1, i + degree + 1)])
            kv.append(temp_kv)

    # End knot vector
    kv += [1.0 for _ in range(m_ends)]

    return kv


def compute_params_curve(points, centripetal):
    """ Computes :math:`\\overline{u}_{k}` for curves.

    Please see Equations 9.4 and 9.5 for chord length parametrization, and Equation 9.6 for centripetal method on
    The NURBS Book (2nd Edition), pp.364-365.

    :param points: data points
    :type points: list, tuple
    :param centripetal: activates centripetal parametrization method
    :type centripetal: bool
    :return: parameter array, :math:`\\overline{u}_{k}`
    :rtype: list
    """
    # Length of the points array
    num_points = len(points)

    # Calculate chord lengths
    cds = [0.0 for _ in range(num_points + 1)]
    cds[-1] = 1.0
    for i in range(1, num_points):
        distance = utilities.point_distance(points[i], points[i - 1])
        cds[i] = math.sqrt(distance) if centripetal else distance

    # Find the total chord length
    d = sum(cds[1:-1])

    # Divide individual chord lengths by the total chord length
    uk = [0.0 for _ in range(num_points)]
    for i in range(num_points):
        uk[i] = sum(cds[0:i + 1]) / d

    return uk


def compute_params_surface(points, size_u, size_v, centripetal):
    """ Computes :math:`\\overline{u}_{k}` and :math:`\\overline{u}_{l}` for surfaces.

    The data points array has a row size of ``size_v`` and column size of ``size_u`` and it is 1-dimensional. Please
    see The NURBS Book (2nd Edition), pp.366-367 for details on how to compute :math:`\\overline{u}_{k}` and
    :math:`\\overline{u}_{l}` arrays for global surface interpolation.

    Please note that this function is not a direct implementation of Algorithm A9.3 which can be found on The NURBS Book
    (2nd Edition), pp.377-378. However, the output is the same.

    :param points: data points
    :type points: list, tuple
    :param size_u: number of points on the u-direction
    :type size_u: int
    :param size_v: number of points on the v-direction
    :type size_v: int
    :param centripetal: activates centripetal parametrization method
    :type centripetal: bool
    :return: :math:`\\overline{u}_{k}` and :math:`\\overline{u}_{l}` parameter arrays as a tuple
    :rtype: tuple
    """
    # Compute uk
    uk = [0.0 for _ in range(size_u)]

    # Compute for each curve on the v-direction
    uk_temp = []
    for v in range(size_v):
        pts_u = [points[v + (size_v * u)] for u in range(size_u)]
        uk_temp += compute_params_curve(pts_u, centripetal)

    # Do averaging on the u-direction
    for u in range(size_u):
        knots_v = [uk_temp[u + (size_u * v)] for v in range(size_v)]
        uk[u] = sum(knots_v) / size_v

    # Compute vl
    vl = [0.0 for _ in range(size_v)]

    # Compute for each curve on the u-direction
    vl_temp = []
    for u in range(size_u):
        pts_v = [points[v + (size_v * u)] for v in range(size_v)]
        vl_temp += compute_params_curve(pts_v, centripetal)

    # Do averaging on the v-direction
    for v in range(size_v):
        knots_u = [vl_temp[v + (size_v * u)] for u in range(size_u)]
        vl[v] = sum(knots_u) / size_u

    return uk, vl


def ginterp(degree, knotvector, points, params, span_func):
    """ Global interpolation.

    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param points: data points
    :type points: list, tuple
    :param params: list of parameters
    :type params: list, tuple
    :param span_func: reference to the knot span finding function
    :type span_func: function
    :return: control points
    :rtype: list
    """
    # Dimension
    dim = len(points[0])

    # Number of data points
    num_points = len(points)

    # Set up coefficient matrix
    matrix_a = [[0.0 for _ in range(num_points)] for _ in range(num_points)]
    for i in range(num_points):
        span = span_func(degree, knotvector, num_points, params[i])
        matrix_a[i][span-degree:span+1] = helpers.basis_function(degree, knotvector, span, params[i])

    # Solve system of linear equations
    matrix_l, matrix_u = utilities.lu_decomposition(matrix_a)
    ctrlpts = [[0.0 for _ in range(dim)] for _ in range(num_points)]
    for i in range(dim):
        b = [pt[i] for pt in points]
        y = utilities.forward_substitution(matrix_l, b)
        x = utilities.backward_substitution(matrix_u, y)
        for j in range(num_points):
            ctrlpts[j][i] = x[j]

    # Return control points
    return ctrlpts
