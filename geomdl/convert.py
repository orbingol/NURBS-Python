"""
.. module:: convert
    :platform: Unix, Windows
    :synopsis: Helper module for converting rational and non-rational geometries to each other

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline, NURBS
from . import _convert as cvt


def bspline_to_nurbs(obj, **kwargs):
    """ Converts non-rational splines to rational ones.

    :param obj: non-rational spline geometry
    :type obj: BSpline.Curve, BSpline.Surface or BSpline.Volume
    :return: rational spline geometry
    :rtype: NURBS.Curve, NURBS.Surface or NURBS.Volume
    :raises: TypeError
    """
    # B-Spline -> NURBS
    if isinstance(obj, BSpline.Curve):
        ret = cvt.convert_curve(obj, NURBS)
    elif isinstance(obj, BSpline.Surface):
        ret = cvt.convert_surface(obj, NURBS)
    elif isinstance(obj, BSpline.Volume):
        ret = cvt.convert_volume(obj, NURBS)
    else:
        raise TypeError("Input must be an instance of B-Spline curve, surface or volume")
    
    return ret


def nurbs_to_bspline(obj, **kwargs):
    """ Converts rational splines to non-rational ones (if possible).

    The possibility of converting a rational spline geometry to
    a non-rational one depends on the weights vector.

    :param obj: rational spline geometry
    :type obj: NURBS.Curve, NURBS.Surface or NURBS.Volume
    :return: non-rational spline geometry
    :rtype: BSpline.Curve, BSpline.Surface or BSpline.Volume
    :raises: TypeError
    """
    if not obj.rational:
        raise TypeError("The input must be a rational geometry")

    # Get keyword arguments
    tol = kwargs.get('tol', 10e-8)

    # Test for non-rational component extraction
    for w in obj.weights:
        if abs(w - 1.0) > tol:
            print("Cannot extract non-rational components")
            return obj

    # NURBS -> B-Spline
    if isinstance(obj, NURBS.Curve):
        ret = cvt.convert_curve(obj, BSpline)
    elif isinstance(obj, NURBS.Surface):
        ret = cvt.convert_surface(obj, BSpline)
    elif isinstance(obj, NURBS.Volume):
        ret = cvt.convert_volume(obj, BSpline)
    else:
        raise TypeError("Input must be an instance of NURBS curve, surface or volume")

    return ret
