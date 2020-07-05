"""
.. module:: algorithms.derivative
    :platform: Unix, Windows
    :synopsis: Hodograph computation algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import helpers
from ..base import GeomdlError, GeomdlWarning

__all__ = []


def derivative_curve(obj):
    """ Computes the hodograph (first derivative) curve of the input curve.

    This function constructs the hodograph (first derivative) curve from the input curve by computing the degrees,
    knot vectors and the control points of the derivative curve.

    :param obj: input curve
    :type obj: abstract.Curve
    :return: derivative curve
    """
    if obj.pdimension != 1:
        raise GeomdlError("Input shape must be an instance of abstract.Curve class")

    # Unfortunately, rational curves do NOT have this property
    # Ref: https://pages.mtu.edu/~shene/COURSES/cs3621/LAB/curve/1st-2nd.html
    if obj.rational:
        GeomdlWarning("Cannot compute hodograph curve for a rational curve")
        return obj

    # Find the control points of the derivative curve
    pkl = helpers.curve_deriv_cpts(obj.dimension, obj.degree.u, obj.knotvector.u, obj.ctrlpts.points,
                                          rs=(0, obj.ctrlpts_size.u - 1), deriv_order=1)

    # Generate the derivative curve
    curve = obj.__class__()
    curve.degree.u = obj.degree.u - 1
    curve.set_ctrlpts(pkl[1][0:-1])
    curve.knotvector.u = obj.knotvector.u[1:-1]

    return curve


def derivative_surface(obj):
    """ Computes the hodograph (first derivative) surface of the input surface.

    This function constructs the hodograph (first derivative) surface from the input surface by computing the degrees,
    knot vectors and the control points of the derivative surface.

    The return value of this function is a tuple containing the following derivative surfaces in the given order:

    * U-derivative surface (derivative taken only on the u-direction)
    * V-derivative surface (derivative taken only on the v-direction)
    * UV-derivative surface (derivative taken on both the u- and the v-direction)

    :param obj: input surface
    :type obj: abstract.Surface
    :return: derivative surfaces w.r.t. u, v and both u-v
    :rtype: tuple
    """
    if obj.pdimension != 2:
        raise GeomdlError("Input shape must be an instance of abstract.Surface class")

    if obj.rational:
        GeomdlWarning("Cannot compute hodograph surface for a rational surface")
        return obj

    # Find the control points of the derivative surface
    d = 2  # 0 <= k + l <= d, see pg. 114 of The NURBS Book, 2nd Ed.
    pkl = helpers.surface_deriv_cpts(obj.dimension, obj.degree, obj.knotvector, obj.ctrlpts, obj.ctrlpts_size,
                                            rs=(0, obj.ctrlpts_size.u - 1), ss=(0, obj.ctrlpts_size.v - 1), deriv_order=d)

    # u-derivative surface
    ctrlpts_u = []
    size_u = len(pkl[1][0]) - 1
    size_v = len(pkl[1][0][0])
    for j in range(0, size_v):
        for i in range(0, size_u):
            ctrlpts_u.append(pkl[1][0][i][j])

    surf_u = copy.deepcopy(obj)
    surf_u.degree.u = obj.degree.u - 1
    surf_u.knotvector.u = obj.knotvector.u[1:-1]
    surf_u.set_ctrlpts(ctrlpts_u, size_u, size_v)

    # v-derivative surface
    ctrlpts_v = []
    size_u = len(pkl[0][1])
    size_v = len(pkl[0][1][0]) - 1
    for j in range(0, size_v):
        for i in range(0, size_u):
            ctrlpts_v.append(pkl[0][1][i][j])

    surf_v = copy.deepcopy(obj)
    surf_v.degree.v = obj.degree.v - 1
    surf_v.knotvector.v = obj.knotvector.v[1:-1]
    surf_v.set_ctrlpts(ctrlpts_v, size_u, size_v)

    ctrlpts_uv = []
    size_u = len(pkl[1][1]) - 1
    size_v = len(pkl[1][1][0]) - 1
    for j in range(0, size_v):
        for i in range(0, size_u):
            ctrlpts_uv.append(pkl[1][1][i][j])

    # uv-derivative surface
    surf_uv = obj.__class__()
    surf_uv.degree.u = obj.degree.u - 1
    surf_uv.degree.v = obj.degree.v - 1
    surf_uv.knotvector.u = obj.knotvector.u[1:-1]
    surf_uv.knotvector.v = obj.knotvector.v[1:-1]
    surf_uv.set_ctrlpts(ctrlpts_uv, size_u, size_v)

    return surf_u, surf_v, surf_uv
