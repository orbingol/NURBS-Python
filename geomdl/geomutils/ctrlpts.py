"""
.. module:: geomutils.ctrlpts
    :platform: Unix, Windows
    :synopsis: Provides utility functions related to control points

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import helpers
from ..base import export, GeomdlError


@export
def find_ctrlpts(obj, u, v=None, **kwargs):
    """ Finds the control points involved in the evaluation of the curve/surface point defined by the input parameter(s).

    :param obj: curve or surface
    :type obj: abstract.Curve or abstract.Surface
    :param u: parameter (for curve), parameter on the u-direction (for surface)
    :type u: float
    :param v: parameter on the v-direction (for surface only)
    :type v: float
    :return: control points; 1-dimensional array for curve, 2-dimensional array for surface
    :rtype: list
    """
    if obj.pdimension == 1:  # curve
        return find_ctrlpts_curve(u, obj, **kwargs)
    elif obj.pdimension == 2:  # surface
        if v is None:
            raise GeomdlError("Parameter value for the v-direction must be set for operating on surfaces")
        return find_ctrlpts_surface(u, v, obj, **kwargs)
    else:
        raise GeomdlError("The input must be an instance of abstract.Curve or abstract.Surface")


def find_ctrlpts_curve(t, curve, **kwargs):
    """ Finds the control points involved in the evaluation of the curve point defined by the input parameter.

    This function uses a modified version of the algorithm *A3.1 CurvePoint* from The NURBS Book by Piegl & Tiller.

    :param t: parameter
    :type t: float
    :param curve: input curve object
    :type curve: BSpline.Curve
    :return: 1-dimensional control points array
    :rtype: list
    """
    # Find spans and the constant index
    span = helpers.find_span_linear(curve.degree.u, curve.knotvector.u, curve.ctrlpts.count, t)
    idx = span - curve.degree.u

    # Find control points involved in evaluation of the curve point at the input parameter
    curve_ctrlpts = [[] for _ in range(curve.degree.u + 1)]
    for i in range(0, curve.degree.u + 1):
        curve_ctrlpts[i] = curve.ctrlpts[idx + i]

    # Return control points array
    return curve_ctrlpts


def find_ctrlpts_surface(t_u, t_v, surf, **kwargs):
    """ Finds the control points involved in the evaluation of the surface point defined by the input parameter pair.

    This function uses a modified version of the algorithm *A3.5 SurfacePoint* from The NURBS Book by Piegl & Tiller.

    :param t_u: parameter on the u-direction
    :type t_u: float
    :param t_v: parameter on the v-direction
    :type t_v: float
    :param surf: input surface
    :type surf: BSpline.Surface
    :return: 1-dimensional control points array, u-dimension comes the first
    :rtype: list
    """
    # Find spans
    span_u = helpers.find_span_linear(surf.degree.u, surf.knotvector.u, surf.ctrlpts_size.u, t_u)
    span_v = helpers.find_span_linear(surf.degree.v, surf.knotvector.v, surf.ctrlpts_size.v, t_v)

    # Constant indices
    idx_u = span_u - surf.degree.u
    idx_v = span_v - surf.degree.v

    # Find control points involved in evaluation of the surface point at the input parameter pair (u, v)
    surf_ctrlpts = [[] for _ in range((surf.degree.u + 1) * (surf.degree.v + 1))]
    for l in range(surf.degree.v + 1):
        for k in range(surf.degree.u + 1):
            surf_ctrlpts[l] = surf.ctrlpts[idx_u + k, idx_v + l]

    # Return 1-dimensional control points array
    return surf_ctrlpts
