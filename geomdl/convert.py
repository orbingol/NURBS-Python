"""
.. module:: convert
    :platform: Unix, Windows
    :synopsis: Provides BSpline - NURBS conversion functionality

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline
from . import NURBS
from . import compatibility


def bspline_to_nurbs(obj):
    """ Converts B-Spline objects to NURBS objects.

    The intended functionality is converting B-Spline curves and surfaces to NURBS curves and surfaces, respectively.
    Therefore, the inputs should be :py:class:`.BSpline.Curve` or :py:class:`.BSpline.Surface`.
    Otherwise, the function will raise a TypeError.

    :param obj: B-Spline object
    :type obj: BSpline.Curve, BSpline.Surface
    :return: NURBS object
    :rtype: NURBS.Curve, NURBS.Surface
    :raises: TypeError
    """
    if isinstance(obj, BSpline.Curve):
        return bspline_to_nurbs_curve(obj)
    elif isinstance(obj, BSpline.Surface):
        return bspline_to_nurbs_surface(obj)
    else:
        raise TypeError("Input must be an instance of B-Spline curve or surface")


def bspline_to_nurbs_curve(bs_curve):
    nurbs_curve = NURBS.Curve()
    nurbs_curve.degree = bs_curve.degree
    nurbs_curve.ctrlpts = bs_curve.ctrlpts
    nurbs_curve.knotvector = bs_curve.knotvector
    return nurbs_curve


def bspline_to_nurbs_surface(bs_surface):
    nurbs_surface = NURBS.Surface()
    nurbs_surface.degree_u = bs_surface.degree_u
    nurbs_surface.degree_v = bs_surface.degree_v
    nurbs_surface.ctrlpts_size_u = bs_surface.ctrlpts_size_u
    nurbs_surface.ctrlpts_size_v = bs_surface.ctrlpts_size_v
    nurbs_surface.ctrlpts = bs_surface.ctrlpts
    nurbs_surface.knotvector_u = bs_surface.knotvector_u
    nurbs_surface.knotvector_v = bs_surface.knotvector_v
    return nurbs_surface
