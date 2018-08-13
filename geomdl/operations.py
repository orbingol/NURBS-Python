"""
.. module:: operations
    :platform: Unix, Windows
    :synopsis: Provides various operations that can be applied to B-Spline and NURBS shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import copy
from . import BSpline
from . import Multi
from . import helpers
from . import utilities


def split_curve(obj, u, **kwargs):
    """ Splits the curve at the input parametric coordinate.

    This method splits the curve into two pieces at the given parametric coordinate, generates two different
    curve objects and returns them. It does not modify the input curve.

    :param obj: Curve to be split
    :type obj: BSpline.Curve or NURBS.Curve
    :param u: parametric coordinate
    :type u: float
    :return: a list of curves as the split pieces of the initial curve
    :rtype: Multi.MultiCurve
    """
    if not isinstance(obj, BSpline.Curve):
        raise TypeError("Input shape must be an instance of any Curve class")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Validate input data
    if u == 0.0 or u == 1.0:
        raise ValueError("Cannot split on the corner points")
    utilities.check_uv(u)

    # Find multiplicity of the knot and define how many times we need to add the knot
    ks = span_func(obj.degree, obj.knotvector, len(obj.ctrlpts), u) - obj.degree + 1
    s = helpers.find_multiplicity(u, obj.knotvector)
    r = obj.degree - s

    # Create backups of the original curve
    temp_obj = copy.deepcopy(obj)

    # Insert knot
    temp_obj.insert_knot(u, r, check_r=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree, temp_obj.knotvector, len(temp_obj.ctrlpts), u) + 1
    curve1_kv = list(temp_obj.knotvector[0:knot_span])
    curve1_kv.append(u)
    curve2_kv = list(temp_obj.knotvector[knot_span:])
    for _ in range(0, temp_obj.degree + 1):
        curve2_kv.insert(0, u)

    # Control points (use private variable due to differences between rational and non-rational curve)
    curve1_ctrlpts = temp_obj._control_points[0:ks + r]
    curve2_ctrlpts = temp_obj._control_points[ks + r - 1:]

    # Create a new curve for the first half
    curve1 = temp_obj.__class__()
    curve1.degree = temp_obj.degree
    curve1.set_ctrlpts(curve1_ctrlpts)
    curve1.knotvector = curve1_kv

    # Create another curve fot the second half
    curve2 = temp_obj.__class__()
    curve2.degree = temp_obj.degree
    curve2.set_ctrlpts(curve2_ctrlpts)
    curve2.knotvector = curve2_kv

    # Create a MultiCurve
    ret_val = Multi.MultiCurve()
    ret_val.add(curve1)
    ret_val.add(curve2)

    # Return the new curves as a MultiCurve object
    return ret_val


def decompose_curve(obj, **kwargs):
    """ Decomposes the curve into Bezier curve segments of the same degree.

    This operation does not modify the input curve, instead it returns the split curve segments.

    :param obj: Curve to be decomposed
    :type obj: BSpline.Curve or NURBS.Curve
    :return: a list of curve objects arranged in Bezier curve segments
    :rtype: Multi.MultiCurve
    """
    if not isinstance(obj, BSpline.Curve):
        raise TypeError("Input shape must be an instance of any Curve class")

    curve_list = Multi.MultiCurve()
    curve = copy.deepcopy(obj)
    knots = curve.knotvector[curve.degree + 1:-(curve.degree + 1)]
    while knots:
        knot = knots[0]
        curves = split_curve(curve, u=knot, **kwargs)
        curve_list.add(curves[0])
        curve = curves[1]
        knots = curve.knotvector[curve.degree + 1:-(curve.degree + 1)]
    curve_list.add(curve)

    return curve_list


def add_dimension(obj, **kwargs):
    """ Converts x-D curve to a (x+1)-D curve.

    Useful when converting a 2-D curve to a 3-D curve.

    :param obj: Curve
    :type obj: BSpline.Curve or NURBS.Curve
    :return: updated Curve
    :rtype: BSpline.Curve or NURBS.Curve
    """
    if not isinstance(obj, BSpline.Curve):
        raise TypeError("Input shape must be an instance of any Curve class")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)
    array_init = kwargs.get('array_init', [[] for _ in range(len(obj.ctrlpts))])

    # Update control points
    new_ctrlpts = array_init
    for idx, point in enumerate(obj.ctrlpts):
        temp = [float(p) for p in point[0:obj.dimension]]
        temp.append(0.0)
        new_ctrlpts[idx] = temp

    if inplace:
        obj.ctrlpts = new_ctrlpts
        return obj
    else:
        ret = copy.deepcopy(obj)
        ret.ctrlpts = new_ctrlpts
        return ret


def split_surface_u(obj, t, **kwargs):
    """ Splits the surface at the input parametric coordinate on the u-direction.

    This method splits the surface into two pieces at the given parametric coordinate on the u-direction,
    generates two different surface objects and returns them. It does not modify the input surface.

    :param obj: Surface
    :type obj: BSpline.Surface or NURBS.Surface
    :param t: parametric coordinate on the u-direction
    :type t: float
    :return: a list of surface as the split pieces of the initial surface
    :rtype: Multi.MultiSurface
    """
    # Validate input
    if not isinstance(obj, BSpline.Surface):
        raise TypeError("Input shape must be an instance of any Surface class")

    if t == 0.0 or t == 1.0:
        raise ValueError("Cannot split on the corner points")
    utilities.check_uv(t)

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Find multiplicity of the knot
    ks = span_func(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, t) - obj.degree_u + 1
    s = helpers.find_multiplicity(t, obj.knotvector_u)
    r = obj.degree_u - s

    # Create backups of the original surface
    temp_obj = copy.deepcopy(obj)

    # Split the original surface
    temp_obj.insert_knot(u=t, ru=r, check_r=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree_u, temp_obj.knotvector_u, temp_obj.ctrlpts_size_u, t) + 1
    surf1_kv = list(temp_obj.knotvector_u[0:knot_span])
    surf1_kv.append(t)
    surf2_kv = list(temp_obj.knotvector_u[knot_span:])
    for _ in range(0, temp_obj.degree_u + 1):
        surf2_kv.insert(0, t)

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

    # Create a MultiSurface
    ret_val = Multi.MultiSurface()
    ret_val.add(surf1)
    ret_val.add(surf2)

    # Return the new surfaces
    return ret_val


def split_surface_v(obj, t, **kwargs):
    """ Splits the surface at the input parametric coordinate on the v-direction.

    This method splits the surface into two pieces at the given parametric coordinate on the v-direction,
    generates two different surface objects and returns them. It does not modify the input surface.

    :param obj: Surface
    :type obj: BSpline.Surface or NURBS.Surface
    :param t: parametric coordinate on the v-direction
    :type t: float
    :return: a list of surface as the split pieces of the initial surface
    :rtype: Multi.MultiSurface
    """
    # Validate input
    if not isinstance(obj, BSpline.Surface):
        raise TypeError("Input shape must be an instance of any Surface class")

    if t == 0.0 or t == 1.0:
        raise ValueError("Cannot split on the corner points")
    utilities.check_uv(t)

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Find multiplicity of the knot
    ks = span_func(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, t) - obj.degree_v + 1
    s = helpers.find_multiplicity(t, obj.knotvector_v)
    r = obj.degree_v - s

    # Create backups of the original surface
    temp_obj = copy.deepcopy(obj)

    # Split the original surface
    temp_obj.insert_knot(v=t, rv=r, check_r=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree_v, temp_obj.knotvector_v, temp_obj.ctrlpts_size_v, t) + 1
    surf1_kv = list(temp_obj.knotvector_v[0:knot_span])
    surf1_kv.append(t)
    surf2_kv = list(temp_obj.knotvector_v[knot_span:])
    for _ in range(0, temp_obj.degree_v + 1):
        surf2_kv.insert(0, t)

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

    # Create a MultiSurface
    ret_val = Multi.MultiSurface()
    ret_val.add(surf1)
    ret_val.add(surf2)

    # Return the new surfaces
    return ret_val


def decompose_surface(obj, **kwargs):
    """ Decomposes the surface into Bezier surface patches of the same degree.

    This operation does not modify the input surface, instead it returns the surface patches.

    :param obj: Surface
    :type obj: BSpline.Surface or NURBS.Surface
    :return: a list of surface objects arranged as Bezier surface patches
    :rtype: Multi.MultiSurface
    """
    # Validate input
    if not isinstance(obj, BSpline.Surface):
        raise TypeError("Input shape must be an instance of any Surface class")

    # Work with an identical copy
    surf = copy.deepcopy(obj)

    surf_list = []

    # Process u-direction
    knots_u = surf.knotvector_u[surf.degree_u + 1:-(surf.degree_u + 1)]
    while knots_u:
        knot = knots_u[0]
        surfs = split_surface_u(surf, t=knot, **kwargs)
        surf_list.append(surfs[0])
        surf = surfs[1]
        knots_u = surf.knotvector_u[surf.degree_u + 1:-(surf.degree_u + 1)]
    surf_list.append(surf)

    # Process v-direction
    multi_surf = Multi.MultiSurface()
    for surf in surf_list:
        knots_v = surf.knotvector_v[surf.degree_v + 1:-(surf.degree_v + 1)]
        while knots_v:
            knot = knots_v[0]
            surfs = split_surface_v(surf, t=knot, **kwargs)
            multi_surf.add(surfs[0])
            surf = surfs[1]
            knots_v = surf.knotvector_v[surf.degree_v + 1:-(surf.degree_v + 1)]
        multi_surf.add(surf)

    return multi_surf
