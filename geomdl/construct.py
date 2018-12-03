"""
.. module:: construct
    :platform: Unix, Windows
    :synopsis: Contains functions for constructing parametric surfaces and volumes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline
from . import NURBS
from . import utilities
from . import convert


def construct_surface(*args, **kwargs):
    """ Generates NURBS surfaces from parametric curves.

    :return: NURBS surface
    :rtype: NURBS.Surface
    """
    # Get keyword arguments
    degree_v = kwargs.get('degree', 2)

    size_v = len(args)
    if size_v < 2:
        raise ValueError("You need to input at least 2 curves")

    # Construct the control points of the new surface
    degree_u = args[0].degree
    size_u = args[0].ctrlpts_size
    new_ctrlptsw = []
    for arg in args:
        if degree_u != arg.degree:
            raise ValueError("Input curves must have the same degrees")
        if size_u != arg.ctrlpts_size:
            raise ValueError("Input curves must have the same number of control points")
        nc = convert.bspline_to_nurbs(arg) if isinstance(arg, BSpline.Curve) else arg
        new_ctrlptsw += list(nc.ctrlptsw)

    # Generate the surface
    ns = NURBS.Surface()
    ns.degree_u = degree_u
    ns.degree_v = degree_v
    ns.ctrlpts_size_u = size_u
    ns.ctrlpts_size_v = size_v
    ns.ctrlptsw = new_ctrlptsw
    ns.knotvector_u = args[0].knotvector
    ns.knotvector_v = utilities.generate_knot_vector(degree_v, size_v)

    return ns


def construct_volume(*args, **kwargs):
    """ Generates NURBS volumes from parametric surfaces.

    :return: NURBS volume
    :rtype: NURBS.Volume
    """
    # Get keyword arguments
    degree_w = kwargs.get('degree', 2)

    size_w = len(args)
    if size_w < 2:
        raise ValueError("You need to input at least 2 surfaces")

    # Construct the control points of the new volume
    degree_u, degree_v = args[0].degree_u, args[0].degree_v
    size_u, size_v = args[0].ctrlpts_size_u, args[0].ctrlpts_size_v
    new_ctrlptsw = []
    for arg in args:
        if degree_u != arg.degree_u or degree_v != arg.degree_v:
            raise ValueError("Input surfaces must have the same degrees")
        if size_u != arg.ctrlpts_size_u or size_v != arg.ctrlpts_size_v:
            raise ValueError("Input surfaces must have the same number of control points")
        ns = convert.bspline_to_nurbs(arg) if isinstance(arg, BSpline.Surface) else arg
        new_ctrlptsw += list(ns.ctrlptsw)

    # Generate the volume
    nv = NURBS.Volume()
    nv.degree_u = degree_u
    nv.degree_v = degree_v
    nv.degree_w = degree_w
    nv.ctrlpts_size_u = size_u
    nv.ctrlpts_size_v = size_v
    nv.ctrlpts_size_w = size_w
    nv.ctrlptsw = new_ctrlptsw
    nv.knotvector_u = args[0].knotvector_u
    nv.knotvector_v = args[0].knotvector_v
    nv.knotvector_w = utilities.generate_knot_vector(degree_w, size_w)

    return nv
