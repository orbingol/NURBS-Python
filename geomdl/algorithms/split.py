"""
.. module:: algorithms.split
    :platform: Unix, Windows
    :synopsis: Splitting algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import helpers
from ..base import GeomdlError
from .knot import insert_knot

__all__ = []


def split_curve(obj, param, **kwargs):
    """ Splits the curve at the input parametric coordinate.

    This method splits the curve into two pieces at the given parametric coordinate, generates two different
    curve objects and returns them. It does not modify the input curve.

    :param obj: Curve to be split
    :type obj: abstract.Curve
    :param param: parameter
    :type param: float
    :return: a list of curve segments
    :rtype: list
    """
    # Validate input
    if obj.pdimension != 1:
        raise GeomdlError("Input must be a B-Spline curve")

    if param == obj.domain[0][0] or param == obj.domain[0][1]:
        raise GeomdlError("Cannot split from the domain edge")

    # Find multiplicity of the knot and define how many times we need to add the knot
    ks = helpers.find_span_linear(obj.degree, obj.knotvector.u, obj.ctrlpts.count, param) - obj.degree.u + 1
    s = helpers.find_multiplicity(param, obj.knotvector.u)
    r = obj.degree.u - s

    # Create backups of the original curve
    objc = copy.deepcopy(obj)

    # Insert knot
    objc = insert_knot(objc, [param], num=[r], check_num=False)

    # Knot vectors
    knot_span = helpers.find_span_linear(objc.degree.u, objc.knotvector.u, objc.ctrlpts.count, param) + 1
    curve1_kv = list(objc.knotvector.u[0:knot_span])
    curve1_kv.append(param)
    curve2_kv = list(objc.knotvector.u[knot_span:])
    for _ in range(0, objc.degree.u + 1):
        curve2_kv.insert(0, param)

    # Control points (use Pw if rational)
    cpts = objc.ctrlptsw.points
    curve1_ctrlpts = cpts[0:ks + r]
    curve2_ctrlpts = cpts[ks + r - 1:]

    # Create a new curve for the first half
    curve1 = objc.__class__()
    curve1.degree.u = objc.degree.u
    curve1.set_ctrlpts(curve1_ctrlpts)
    curve1.knotvector.u = curve1_kv
    curve1.check_variables()

    # Create another curve fot the second half
    curve2 = objc.__class__()
    curve2.degree.u = objc.degree.u
    curve2.set_ctrlpts(curve2_ctrlpts)
    curve2.knotvector.u = curve2_kv
    curve2.check_variables()

    # Return the split curves
    return curve1, curve2


def split_surface(obj, param, pdir, **kwargs):
    """ Splits the surface at the input parametric coordinate.

    This method splits the surface into two pieces at the given parametric coordinate on the input parametric direction,
    generates two different surface objects and returns them. It does not modify the input surface.

    :param obj: surface
    :type obj: abstract.Surface
    :param param: parameter
    :type param: float
    :param pdir: parametric direction
    :type pdir: str
    :return: a list of surface patches
    :rtype: list
    """
    # Validate input
    if obj.pdimension != 2:
        raise GeomdlError("Input must be a B-Spline surface")

    # Create backup of the original surface
    objc = copy.deepcopy(obj)

    if pdir == "u":
        if param == obj.domain[0][0] or param == obj.domain[0][1]:
            raise GeomdlError("Cannot split from the u-domain edge")

        # Find multiplicity of the knot
        ks = helpers.find_span_linear(obj.degree.u, obj.knotvector.u, obj.ctrlpts_size.u, param) - obj.degree.u + 1
        s = helpers.find_multiplicity(param, obj.knotvector.u)
        r = obj.degree.u - s

        # Split the original surface
        objc = insert_knot(objc, [param, None], num=[r, 0], check_num=False)

        # Knot vectors
        knot_span = helpers.find_span_linear(objc.degree.u, objc.knotvector.u, objc.ctrlpts_size.u, param) + 1
        surf1_kv_u = list(objc.knotvector.u[0:knot_span])
        surf1_kv_u.append(param)
        surf2_kv_u = list(objc.knotvector.u[knot_span:])
        for _ in range(0, objc.degree.u + 1):
            surf2_kv_u.insert(0, param)
        surf1_kv_v = surf2_kv_v = objc.knotvector.v

        # Control points
        surf1_ctrlpts = [objc.ctrlptsw[u, v] for v in range(0, objc.ctrlpts_size.v) for u in range(0, ks + r)]
        surf2_ctrlpts = [objc.ctrlptsw[u, v] for v in range(0, objc.ctrlpts_size.v) for u in range(ks + r - 1, objc.ctrlpts_size.u)]
        surf1_size_u = ks + r
        surf2_size_u = objc.ctrlpts_size.u - (ks + r - 1)
        surf1_size_v = surf2_size_v = objc.ctrlpts_size.v

    elif pdir == "v":
        if param == obj.domain[1][0] or param == obj.domain[1][1]:
            raise GeomdlError("Cannot split from the v-domain edge")

        # Find multiplicity of the knot
        ks = helpers.find_span_linear(obj.degree.v, obj.knotvector.v, obj.ctrlpts_size.v, param) - obj.degree.v + 1
        s = helpers.find_multiplicity(param, obj.knotvector.v)
        r = obj.degree.v - s

        # Split the original surface
        objc = insert_knot(objc, [None, param], num=[0, r], check_num=False)

        # Knot vectors
        knot_span = helpers.find_span_linear(objc.degree.v, objc.knotvector.v, objc.ctrlpts_size.v, param) + 1
        surf1_kv_v = list(objc.knotvector.v[0:knot_span])
        surf1_kv_v.append(param)
        surf2_kv_v = list(objc.knotvector.v[knot_span:])
        for _ in range(0, objc.degree.v + 1):
            surf2_kv_v.insert(0, param)
        surf1_kv_u = surf2_kv_u = objc.knotvector.u

        # Control points
        surf1_ctrlpts = [objc.ctrlptsw[u, v] for v in range(0, ks + r) for u in range(0, objc.ctrlpts_size.u)]
        surf2_ctrlpts = [objc.ctrlptsw[u, v] for v in range(ks + r - 1, objc.ctrlpts_size.v) for u in range(0, objc.ctrlpts_size.u)]
        surf1_size_v = ks + r
        surf2_size_v = objc.ctrlpts_size.v - (ks + r - 1)
        surf1_size_u = surf2_size_u = objc.ctrlpts_size.u
    else:
        raise GeomdlError("Supported parametric directions: u or v")

    # Create a new surface for the first half
    surf1 = objc.__class__()
    surf1.degree.u = objc.degree.u
    surf1.degree.v = objc.degree.v
    surf1.knotvector.u = surf1_kv_u
    surf1.knotvector.v = surf1_kv_v
    surf1.set_ctrlpts(surf1_ctrlpts, surf1_size_u, surf1_size_v)
    surf1.check_variables()

    # Create another surface for the second half
    surf2 = objc.__class__()
    surf2.degree.u = objc.degree.u
    surf2.degree.v = objc.degree.v
    surf2.knotvector.u = surf2_kv_u
    surf2.knotvector.v = surf2_kv_v
    surf2.set_ctrlpts(surf2_ctrlpts, surf2_size_u, surf2_size_v)
    surf2.check_variables()

    # Return the new surfaces
    return surf1, surf2
