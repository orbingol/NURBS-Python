"""
.. module:: algorithms.split
    :platform: Unix, Windows
    :synopsis: Splitting algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import helpers
from ..base import GeomdlError
from .knot_insert import insert_knot

__all__ = []


def split_curve(obj, param, **kwargs):
    """ Splits the curve at the input parametric coordinate.

    This method splits the curve into two pieces at the given parametric coordinate, generates two different
    curve objects and returns them. It does not modify the input curve.

    Keyword Arguments:
        * ``find_span_func``: FindSpan implementation. *Default:* :func:`.helpers.find_span_linear`
        * ``insert_knot_func``: knot insertion algorithm implementation. *Default:* :func:`.operations.insert_knot`

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

    if param == obj.domain[0] or param == obj.domain[1]:
        raise GeomdlError("Cannot split from the domain edge")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)  # FindSpan implementation
    insert_knot_func = kwargs.get('insert_knot_func', insert_knot)  # Knot insertion algorithm

    # Find multiplicity of the knot and define how many times we need to add the knot
    ks = span_func(obj.degree, obj.knotvector.u, len(obj.ctrlpts), param) - obj.degree.u + 1
    s = helpers.find_multiplicity(param, obj.knotvector.u)
    r = obj.degree - s

    # Create backups of the original curve
    temp_obj = copy.deepcopy(obj)

    # Insert knot
    insert_knot_func(temp_obj, [param], num=[r], check_num=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree.u, temp_obj.knotvector.u, len(temp_obj.ctrlpts), param) + 1
    curve1_kv = list(temp_obj.knotvector.u[0:knot_span])
    curve1_kv.append(param)
    curve2_kv = list(temp_obj.knotvector.u[knot_span:])
    for _ in range(0, temp_obj.degree + 1):
        curve2_kv.insert(0, param)

    # Control points (use Pw if rational)
    cpts = temp_obj.ctrlptsw.points
    curve1_ctrlpts = cpts[0:ks + r]
    curve2_ctrlpts = cpts[ks + r - 1:]

    # Create a new curve for the first half
    curve1 = temp_obj.__class__()
    curve1.degree = temp_obj.degree
    curve1.set_ctrlpts(curve1_ctrlpts)
    curve1.knotvector = (curve1_kv,)

    # Create another curve fot the second half
    curve2 = temp_obj.__class__()
    curve2.degree = temp_obj.degree
    curve2.set_ctrlpts(curve2_ctrlpts)
    curve2.knotvector = (curve2_kv,)

    # Return the split curves
    ret_val = [curve1, curve2]
    return ret_val


def split_surface_u(obj, param, **kwargs):
    """ Splits the surface at the input parametric coordinate on the u-direction.

    This method splits the surface into two pieces at the given parametric coordinate on the u-direction,
    generates two different surface objects and returns them. It does not modify the input surface.

    Keyword Arguments:
        * ``find_span_func``: FindSpan implementation. *Default:* :func:`.helpers.find_span_linear`
        * ``insert_knot_func``: knot insertion algorithm implementation. *Default:* :func:`.operations.insert_knot`

    :param obj: surface
    :type obj: abstract.Surface
    :param param: parameter for the u-direction
    :type param: float
    :return: a list of surface patches
    :rtype: list
    """
    # Validate input
    if obj.pdimension != 2:
        raise GeomdlError("Input must be a B-Spline surface")

    if param == obj.domain[0][0] or param == obj.domain[0][1]:
        raise GeomdlError("Cannot split from the u-domain edge")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)  # FindSpan implementation
    insert_knot_func = kwargs.get('insert_knot_func', insert_knot)  # Knot insertion algorithm

    # Find multiplicity of the knot
    ks = span_func(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param) - obj.degree_u + 1
    s = helpers.find_multiplicity(param, obj.knotvector_u)
    r = obj.degree_u - s

    # Create backups of the original surface
    temp_obj = copy.deepcopy(obj)

    # Split the original surface
    insert_knot_func(temp_obj, [param, None], num=[r, 0], check_num=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree_u, temp_obj.knotvector_u, temp_obj.ctrlpts_size_u, param) + 1
    surf1_kv = list(temp_obj.knotvector_u[0:knot_span])
    surf1_kv.append(param)
    surf2_kv = list(temp_obj.knotvector_u[knot_span:])
    for _ in range(0, temp_obj.degree_u + 1):
        surf2_kv.insert(0, param)

    # Control points
    surf1_ctrlpts = temp_obj.ctrlpts2d[0:ks + r]
    surf2_ctrlpts = temp_obj.ctrlpts2d[ks + r - 1:]

    # Create a new surface for the first half
    surf1 = temp_obj.__class__()
    surf1.degree_u = temp_obj.degree_u
    surf1.degree_v = temp_obj.degree_v
    surf1.ctrlpts2d = surf1_ctrlpts
    surf1.knotvector_u = surf1_kv
    surf1.knotvector_v = temp_obj.knotvector_v

    # Create another surface fot the second half
    surf2 = temp_obj.__class__()
    surf2.degree_u = temp_obj.degree_u
    surf2.degree_v = temp_obj.degree_v
    surf2.ctrlpts2d = surf2_ctrlpts
    surf2.knotvector_u = surf2_kv
    surf2.knotvector_v = temp_obj.knotvector_v

    # Return the new surfaces
    ret_val = [surf1, surf2]
    return ret_val


def split_surface_v(obj, param, **kwargs):
    """ Splits the surface at the input parametric coordinate on the v-direction.

    This method splits the surface into two pieces at the given parametric coordinate on the v-direction,
    generates two different surface objects and returns them. It does not modify the input surface.

    Keyword Arguments:
        * ``find_span_func``: FindSpan implementation. *Default:* :func:`.helpers.find_span_linear`
        * ``insert_knot_func``: knot insertion algorithm implementation. *Default:* :func:`.operations.insert_knot`

    :param obj: surface
    :type obj: abstract.Surface
    :param param: parameter for the v-direction
    :type param: float
    :return: a list of surface patches
    :rtype: list
    """
    # Validate input
    if obj.pdimension != 2:
        raise GeomdlError("Input must be a B-Spline surface")

    if param == obj.domain[1][0] or param == obj.domain[1][1]:
        raise GeomdlError("Cannot split from the v-domain edge")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)  # FindSpan implementation
    insert_knot_func = kwargs.get('insert_knot_func', insert_knot)  # Knot insertion algorithm

    # Find multiplicity of the knot
    ks = span_func(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param) - obj.degree_v + 1
    s = helpers.find_multiplicity(param, obj.knotvector_v)
    r = obj.degree_v - s

    # Create backups of the original surface
    temp_obj = copy.deepcopy(obj)

    # Split the original surface
    insert_knot_func(temp_obj, [None, param], num=[0, r], check_num=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree_v, temp_obj.knotvector_v, temp_obj.ctrlpts_size_v, param) + 1
    surf1_kv = list(temp_obj.knotvector_v[0:knot_span])
    surf1_kv.append(param)
    surf2_kv = list(temp_obj.knotvector_v[knot_span:])
    for _ in range(0, temp_obj.degree_v + 1):
        surf2_kv.insert(0, param)

    # Control points
    surf1_ctrlpts = []
    for v_row in temp_obj.ctrlpts2d:
        temp = v_row[0:ks + r]
        surf1_ctrlpts.append(temp)
    surf2_ctrlpts = []
    for v_row in temp_obj.ctrlpts2d:
        temp = v_row[ks + r - 1:]
        surf2_ctrlpts.append(temp)

    # Create a new surface for the first half
    surf1 = temp_obj.__class__()
    surf1.degree_u = temp_obj.degree_u
    surf1.degree_v = temp_obj.degree_v
    surf1.ctrlpts2d = surf1_ctrlpts
    surf1.knotvector_v = surf1_kv
    surf1.knotvector_u = temp_obj.knotvector_u

    # Create another surface fot the second half
    surf2 = temp_obj.__class__()
    surf2.degree_u = temp_obj.degree_u
    surf2.degree_v = temp_obj.degree_v
    surf2.ctrlpts2d = surf2_ctrlpts
    surf2.knotvector_v = surf2_kv
    surf2.knotvector_u = temp_obj.knotvector_u

    # Return the new surfaces
    ret_val = [surf1, surf2]
    return ret_val
