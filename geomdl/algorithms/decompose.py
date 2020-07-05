"""
.. module:: algorithms.decompose
    :platform: Unix, Windows
    :synopsis: Decomposition algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import helpers
from ..base import GeomdlError
from .split import split_curve, split_surface


def decompose_curve(obj, **kwargs):
    """ Decomposes the curve into Bezier curve segments of the same degree.

    This operation does not modify the input curve, instead it returns the split curve segments.

    Keyword Arguments:
        * ``find_span_func``: FindSpan implementation. *Default:* :func:`.helpers.find_span_linear`
        * ``insert_knot_func``: knot insertion algorithm implementation. *Default:* :func:`.operations.insert_knot`

    :param obj: Curve to be decomposed
    :type obj: abstract.Curve
    :return: a list of Bezier segments
    :rtype: list
    """
    if obj.pdimension != 1:
        raise GeomdlError("Input shape must be an instance of abstract.Curve class")

    multi_curve = []
    curve = copy.deepcopy(obj)
    knots = curve.knotvector.u[curve.degree.u + 1:-(curve.degree.u + 1)]
    while knots:
        knot = knots[0]
        curves = split_curve(curve, param=knot, **kwargs)
        multi_curve.append(curves[0])
        curve = curves[1]
        knots = curve.knotvector.u[curve.degree.u + 1:-(curve.degree.u + 1)]
    multi_curve.append(curve)

    return multi_curve


def decompose_surface(obj, **kwargs):
    """ Decomposes the surface into Bezier surface patches of the same degree.

    This operation does not modify the input surface, instead it returns the surface patches.

    Keyword Arguments:
        * ``find_span_func``: FindSpan implementation. *Default:* :func:`.helpers.find_span_linear`
        * ``insert_knot_func``: knot insertion algorithm implementation. *Default:* :func:`.operations.insert_knot`

    :param obj: surface
    :type obj: abstract.Surface
    :return: a list of Bezier patches
    :rtype: list
    """
    def decompose(srf, idx, sdir, **kws):
        srf_list = []
        knots = srf.knotvector[idx][srf.degree[idx] + 1:-(srf.degree[idx] + 1)]
        while knots:
            knot = knots[0]
            srfs = split_surface(srf, knot, sdir, **kws)
            srf_list.append(srfs[0])
            srf = srfs[1]
            knots = srf.knotvector[idx][srf.degree[idx] + 1:-(srf.degree[idx] + 1)]
        srf_list.append(srf)
        return srf_list

    # Validate input
    if obj.pdimension != 2:
        raise GeomdlError("Input must be a surface")

    # Get keyword arguments
    decompose_dir = kwargs.get('decompose_dir', 'uv')  # possible directions: u, v, uv
    if "decompose_dir" in kwargs:
        kwargs.pop("decompose_dir")

    # Work with an identical copy
    surf = copy.deepcopy(obj)

    # Only u-direction
    if decompose_dir == 'u':
        return decompose(surf, 0, decompose_dir, **kwargs)

    # Only v-direction
    if decompose_dir == 'v':
        return decompose(surf, 1, decompose_dir, **kwargs)

    # Both u- and v-directions
    if decompose_dir == 'uv':
        multi_surf = []
        # Process u-direction
        surfs_u = decompose(surf, 0, "u", **kwargs)
        # Process v-direction
        for sfu in surfs_u:
            multi_surf += decompose(sfu, 1, "v", **kwargs)
        return multi_surf
    else:
        raise GeomdlError("Cannot decompose in " + str(decompose_dir) + " direction. Acceptable values: u, v, uv")
