"""
.. module:: convert
    :platform: Unix, Windows
    :synopsis: Provides BSpline to NURBS conversion functionality

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline, NURBS
from . import _convert


def bspline_to_nurbs(obj):
    """ Converts non-rational parametric shapes to rational ones.

    :param obj: B-Spline shape
    :type obj: BSpline.Curve, BSpline.Surface or BSpline.Volume
    :return: NURBS shape
    :rtype: NURBS.Curve, NURBS.Surface or NURBS.Volume
    :raises: TypeError
    """
    # B-Spline -> NURBS
    if isinstance(obj, BSpline.Curve):
        return _convert.convert_curve(obj, NURBS)
    elif isinstance(obj, BSpline.Surface):
        return _convert.convert_surface(obj, NURBS)
    elif isinstance(obj, BSpline.Volume):
        return _convert.convert_volume(obj, NURBS)
    else:
        raise TypeError("Input must be an instance of B-Spline curve, surface or volume")


def nurbs_to_bspline(obj, **kwargs):
    """ Extracts the non-rational components from rational parametric shapes, if possible.

    The possibility of converting a rational shape to a non-rational one depends on the weights vector.

    :param obj: NURBS shape
    :type obj: NURBS.Curve, NURBS.Surface or NURBS.Volume
    :return: B-Spline shape
    :rtype: BSpline.Curve, BSpline.Surface or BSpline.Volume
    :raises: TypeError
    """
    if not obj.rational:
        raise TypeError("The input must be a rational shape")

    # Get keyword arguments
    tol = kwargs.get('tol', 10e-8)

    # Test for non-rational component extraction
    for w in obj.weights:
        if abs(w - 1.0) > tol:
            print("Cannot extract non-rational components")
            return obj

    # NURBS -> B-Spline
    if isinstance(obj, NURBS.Curve):
        return _convert.convert_curve(obj, BSpline)
    elif isinstance(obj, NURBS.Surface):
        return _convert.convert_surface(obj, BSpline)
    elif isinstance(obj, NURBS.Volume):
        return _convert.convert_volume(obj, BSpline)
    else:
        raise TypeError("Input must be an instance of NURBS curve, surface or volume")


