"""
.. module:: convert
    :platform: Unix, Windows
    :synopsis: Provides BSpline to NURBS conversion functionality

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline
from . import NURBS


def bspline_to_nurbs(obj):
    """ Converts B-Spline parametric shapes to NURBS parametric shapes.

    :param obj: B-Spline shape
    :type obj: BSpline.Curve, BSpline.Surface or BSpline.Volume
    :return: NURBS shape
    :rtype: NURBS.Curve, NURBS.Surface or BSpline.Volume
    :raises: TypeError
    """
    if isinstance(obj, BSpline.Curve):
        return bspline_to_nurbs_curve(obj)
    elif isinstance(obj, BSpline.Surface):
        return bspline_to_nurbs_surface(obj)
    elif isinstance(obj, BSpline.Volume):
        return bspline_to_nurbs_volume(obj)
    else:
        raise TypeError("Input must be an instance of B-Spline curve, surface or volume")


def bspline_to_nurbs_curve(bcrv):
    ncrv = NURBS.Curve()
    ncrv.degree = bcrv.degree
    ncrv.ctrlpts = bcrv.ctrlpts
    ncrv.knotvector = bcrv.knotvector
    return ncrv


def bspline_to_nurbs_surface(bsurf):
    nsurf = NURBS.Surface()
    nsurf.degree_u = bsurf.degree_u
    nsurf.degree_v = bsurf.degree_v
    nsurf.ctrlpts_size_u = bsurf.ctrlpts_size_u
    nsurf.ctrlpts_size_v = bsurf.ctrlpts_size_v
    nsurf.ctrlpts = bsurf.ctrlpts
    nsurf.knotvector_u = bsurf.knotvector_u
    nsurf.knotvector_v = bsurf.knotvector_v
    return nsurf


def bspline_to_nurbs_volume(bvol):
    nvol = NURBS.Volume()
    nvol.degree_u = bvol.degree_u
    nvol.degree_v = bvol.degree_v
    nvol.degree_w = bvol.degree_w
    nvol.ctrlpts_size_u = bvol.ctrlpts_size_u
    nvol.ctrlpts_size_v = bvol.ctrlpts_size_v
    nvol.ctrlpts_size_w = bvol.ctrlpts_size_w
    nvol.ctrlpts = bvol.ctrlpts
    nvol.knotvector_u = bvol.knotvector_u
    nvol.knotvector_v = bvol.knotvector_v
    nvol.knotvector_w = bvol.knotvector_w
    return nvol
