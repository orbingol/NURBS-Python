"""
.. module:: _operations
    :platform: Unix, Windows
    :synopsis: Helper functions for operations module

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import linalg, helpers
from .base import GeomdlError

# Initialize an empty __all__ for controlling imports
__all__ = []


def find_ctrlpts_curve(t, curve, **kwargs):
    """ Finds the control points involved in the evaluation of the curve point defined by the input parameter.

    This function uses a modified version of the algorithm *A3.1 CurvePoint* from The NURBS Book by Piegl & Tiller.

    :param t: parameter
    :type t: float
    :param curve: input curve object
    :type curve: abstract.Curve
    :return: 1-dimensional control points array
    :rtype: list
    """
    # Get keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Find spans and the constant index
    span = span_func(curve.degree, curve.knotvector, len(curve.ctrlpts), t)
    idx = span - curve.degree

    # Find control points involved in evaluation of the curve point at the input parameter
    curve_ctrlpts = [() for _ in range(curve.degree + 1)]
    for i in range(0, curve.degree + 1):
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
    :type surf: abstract.Surface
    :return: 2-dimensional control points array
    :rtype: list
    """
    # Get keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Find spans
    span_u = span_func(surf.degree_u, surf.knotvector_u, surf.ctrlpts_size_u, t_u)
    span_v = span_func(surf.degree_v, surf.knotvector_v, surf.ctrlpts_size_v, t_v)

    # Constant indices
    idx_u = span_u - surf.degree_u
    idx_v = span_v - surf.degree_v

    # Find control points involved in evaluation of the surface point at the input parameter pair (u, v)
    surf_ctrlpts = [[] for _ in range(surf.degree_u + 1)]
    for k in range(surf.degree_u + 1):
        temp = [() for _ in range(surf.degree_v + 1)]
        for l in range(surf.degree_v + 1):
            temp[l] = surf.ctrlpts2d[idx_u + k][idx_v + l]
        surf_ctrlpts[k] = temp

    # Return 2-dimensional control points array
    return surf_ctrlpts


def link_curves(*args, **kwargs):
    """ Links the input curves together.

    The end control point of the curve k has to be the same with the start control point of the curve k + 1.

    Keyword Arguments:
        * ``tol``: tolerance value for checking equality. *Default: 10e-8*
        * ``validate``: flag to enable input validation. *Default: False*

    :return: a tuple containing knot vector, control points, weights vector and knots
    """
    # Get keyword arguments
    tol = kwargs.get('tol', 10e-8)
    validate = kwargs.get('validate', False)

    # Validate input
    if validate:
        for idx in range(len(args) - 1):
            if linalg.point_distance(args[idx].ctrlpts[-1], args[idx + 1].ctrlpts[0]) > tol:
                raise GeomdlError("Curve #" + str(idx) + " and Curve #" + str(idx + 1) + " don't touch each other")

    kv = []  # new knot vector
    cpts = []  # new control points array
    wgts = []  # new weights array
    kv_connected = []  # superfluous knots to be removed
    pdomain_end = 0

    # Loop though the curves
    for arg in args:
        # Process knot vectors
        if not kv:
            kv += list(arg.knotvector[:-(arg.degree + 1)])  # get rid of the last superfluous knot to maintain split curve notation
            cpts += list(arg.ctrlpts)
            # Process control points
            if arg.rational:
                wgts += list(arg.weights)
            else:
                tmp_w = [1.0 for _ in range(arg.ctrlpts_size)]
                wgts += tmp_w
        else:
            tmp_kv = [pdomain_end + k for k in arg.knotvector[1:-(arg.degree + 1)]]
            kv += tmp_kv
            cpts += list(arg.ctrlpts[1:])
            # Process control points
            if arg.rational:
                wgts += list(arg.weights[1:])
            else:
                tmp_w = [1.0 for _ in range(arg.ctrlpts_size - 1)]
                wgts += tmp_w

        pdomain_end += arg.knotvector[-1]
        kv_connected.append(pdomain_end)

    # Fix curve by appending the last knot to the end
    kv += [pdomain_end for _ in range(arg.degree + 1)]
    # Remove the last knot from knot insertion list
    kv_connected.pop()

    return kv, cpts, wgts, kv_connected
