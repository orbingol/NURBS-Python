"""
.. module:: fitting.interpolate_global
    :platform: Unix, Windows
    :synopsis: Global interpolation functions

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import linalg, BSpline
from . import common

__all__ = []


def interpolate_curve(points, degree, **kwargs):
    """ Curve interpolation through the data points.

    Please refer to Algorithm A9.1 on The NURBS Book (2nd Edition), pp.369-370 for details.

    Keyword Arguments:
        * ``centripetal``: activates centripetal parametrization method. *Default: False*

    :param points: data points
    :type points: list, tuple
    :param degree: degree of the output parametric curve
    :type degree: int
    :return: interpolated B-Spline curve
    :rtype: BSpline.Curve
    """
    # Keyword arguments
    use_centripetal = kwargs.get('centripetal', False)

    # Number of control points
    num_points = len(points)

    # Get uk
    uk = common.compute_params_curve(points, use_centripetal)

    # Compute knot vector
    kv = common.compute_knot_vector(degree, num_points, uk)

    # Do global interpolation
    matrix_a = common.build_coeff_matrix(degree, kv, uk, points)
    ctrlpts = linalg.lu_solve(matrix_a, points)

    # Generate B-spline curve
    curve = BSpline.Curve()
    curve.degree.u = degree
    curve.set_ctrlpts(ctrlpts)
    curve.knotvector.u = kv

    return curve


def interpolate_surface(points, size_u, size_v, degree_u, degree_v, **kwargs):
    """ Surface interpolation through the data points.

    Please refer to the Algorithm A9.4 on The NURBS Book (2nd Edition), pp.380 for details.

    Keyword Arguments:
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
    :return: interpolated B-Spline surface
    :rtype: BSpline.Surface
    """
    # Keyword arguments
    use_centripetal = kwargs.get('centripetal', False)

    # Get uk and vl
    uk, vl = common.compute_params_surface(points, size_u, size_v, use_centripetal)

    # Compute knot vectors
    kv_u = common.compute_knot_vector(degree_u, size_u, uk)
    kv_v = common.compute_knot_vector(degree_v, size_v, vl)

    # Do global interpolation on the v-direction
    ctrlpts_r = []
    for u in range(size_u):
        pts = [points[u + (size_u * v)] for v in range(size_v)]
        matrix_a = common.build_coeff_matrix(degree_v, kv_v, vl, pts)
        ctrlpts_r += linalg.lu_solve(matrix_a, pts)

    # Do global interpolation on the u-direction
    ctrlpts = []
    for v in range(size_v):
        pts = [ctrlpts_r[v + (size_v * u)] for u in range(size_u)]
        matrix_a = common.build_coeff_matrix(degree_u, kv_u, uk, pts)
        ctrlpts += linalg.lu_solve(matrix_a, pts)

    # Generate B-spline surface
    surf = BSpline.Surface()
    surf.degree.u = degree_u
    surf.degree.v = degree_v
    surf.set_ctrlpts(ctrlpts, size_u, size_v)
    surf.knotvector.u = kv_u
    surf.knotvector.v = kv_v

    return surf
