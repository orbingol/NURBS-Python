"""
.. module:: algorithms.derivative
    :platform: Unix, Windows
    :synopsis: Hodograph computation algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import helpers
from ..base import GeomdlError, GeomdlWarning
from .knot_insert import insert_knot

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
    pkl = helpers.curve_deriv_cpts(obj.dimension, obj.degree, obj.knotvector, obj.ctrlpts,
                                          rs=(0, obj.ctrlpts_size - 1), deriv_order=1)

    # Generate the derivative curve
    curve = obj.__class__()
    curve.degree = obj.degree - 1
    curve.ctrlpts = pkl[1][0:-1]
    curve.knotvector = obj.knotvector[1:-1]
    curve.delta = obj.delta

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
    pkl = helpers.surface_deriv_cpts(obj.dimension, obj.degree, obj.knotvector, obj.ctrlpts, obj.cpsize,
                                            rs=(0, obj.ctrlpts_size_u - 1), ss=(0, obj.ctrlpts_size_v - 1), deriv_order=d)

    ctrlpts2d_u = []
    for i in range(0, len(pkl[1][0]) - 1):
        ctrlpts2d_u.append(pkl[1][0][i])

    surf_u = copy.deepcopy(obj)
    surf_u.degree_u = obj.degree_u - 1
    surf_u.ctrlpts2d = ctrlpts2d_u
    surf_u.knotvector_u = obj.knotvector_u[1:-1]
    surf_u.delta = obj.delta

    ctrlpts2d_v = []
    for i in range(0, len(pkl[0][1])):
        ctrlpts2d_v.append(pkl[0][1][i][0:-1])

    surf_v = copy.deepcopy(obj)
    surf_v.degree_v = obj.degree_v - 1
    surf_v.ctrlpts2d = ctrlpts2d_v
    surf_v.knotvector_v = obj.knotvector_v[1:-1]
    surf_v.delta = obj.delta

    ctrlpts2d_uv = []
    for i in range(0, len(pkl[1][1]) - 1):
        ctrlpts2d_uv.append(pkl[1][1][i][0:-1])

    # Generate the derivative curve
    surf_uv = obj.__class__()
    surf_uv.degree_u = obj.degree_u - 1
    surf_uv.degree_v = obj.degree_v - 1
    surf_uv.ctrlpts2d = ctrlpts2d_uv
    surf_uv.knotvector_u = obj.knotvector_u[1:-1]
    surf_uv.knotvector_v = obj.knotvector_v[1:-1]
    surf_uv.delta = obj.delta

    return surf_u, surf_v, surf_uv
