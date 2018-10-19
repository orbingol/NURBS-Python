"""
.. module:: operations
    :platform: Unix, Windows
    :synopsis: Provides various operations that can be applied to B-Spline and NURBS shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import copy
import warnings
from . import Abstract
from . import Multi
from . import helpers
from . import utilities
from . import evaluators


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
    if not isinstance(obj, Abstract.Curve):
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
    if not isinstance(obj, Abstract.Curve):
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
    """ Converts x-dimensional curve to a (x+1)-dimensional curve.

    If you pass ``inplace=True`` keyword argument, the input shape will be updated. Otherwise, this function does not
    change the input shape but returns the updated shape.

    Useful when converting a 2-dimensional curve to a 3-dimensional curve.

    :param obj: Curve
    :type obj: BSpline.Curve or NURBS.Curve
    :return: updated Curve
    :rtype: BSpline.Curve or NURBS.Curve
    """
    if not isinstance(obj, Abstract.Curve):
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


def derivative_curve(obj):
    """ Computes the hodograph (first derivative) curve of the input curve

    This function constructs the hodograph (first derivative) curve from the input curve by computing the degrees,
    knot vectors and the control points of the derivative curve.

    :param obj: input curve
    :type obj: Abstract.Curve
    :return: derivative curve
    :rtype: Abstract.Curve
    """
    if not isinstance(obj, Abstract.Curve):
        raise TypeError("Input shape must be an instance of Abstract.Curve class")

    # Unfortunately, rational curves do not have this property
    # Ref: https://pages.mtu.edu/~shene/COURSES/cs3621/LAB/curve/1st-2nd.html
    if obj.rational:
        warnings.warn("Cannot compute hodograph curve for a rational curve")
        return obj

    # Find the control points of the derivative curve
    pkl = evaluators.CurveEvaluator2.derivatives_ctrlpts(r1=0,
                                                         r2=len(obj.ctrlpts) - 1,  # n + 1 = num of control points
                                                         degree=obj.degree,
                                                         knotvector=obj.knotvector,
                                                         ctrlpts=obj.ctrlpts,
                                                         dimension=obj.dimension,
                                                         deriv_order=1)

    # Generate the derivative curve
    curve = obj.__class__()
    curve.degree = obj.degree - 1
    curve.ctrlpts = pkl[1][0:-1]
    curve.knotvector = obj.knotvector[1:-1]
    curve.delta = obj.delta

    return curve


def split_surface_u(obj, t, **kwargs):
    """ Splits the surface at the input parametric coordinate on the u-direction.

    This method splits the surface into two pieces at the given parametric coordinate on the u-direction,
    generates two different surface objects and returns them. It does not modify the input surface.

    :param obj: surface
    :type obj: BSpline.Surface or NURBS.Surface
    :param t: parametric coordinate on the u-direction
    :type t: float
    :return: a list of surface as the split pieces of the initial surface
    :rtype: Multi.MultiSurface
    """
    # Validate input
    if not isinstance(obj, Abstract.Surface):
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

    :param obj: surface
    :type obj: BSpline.Surface or NURBS.Surface
    :param t: parametric coordinate on the v-direction
    :type t: float
    :return: a list of surface as the split pieces of the initial surface
    :rtype: Multi.MultiSurface
    """
    # Validate input
    if not isinstance(obj, Abstract.Surface):
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

    :param obj: surface
    :type obj: BSpline.Surface or NURBS.Surface
    :return: a list of surface objects arranged as Bezier surface patches
    :rtype: Multi.MultiSurface
    """
    # Validate input
    if not isinstance(obj, Abstract.Surface):
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


def derivative_surface(obj):
    """ Computes the hodograph (first derivative) surface of the input surface

    This function constructs the hodograph (first derivative) surface from the input surface by computing the degrees,
    knot vectors and the control points of the derivative surface.

    The return value of this function is a tuple containing the following derivative surfaces in the given order:

    * U-derivative surface (derivative taken only on the u-direction)
    * V-derivative surface (derivative taken only on the v-direction)
    * UV-derivative surface (derivative taken on both the u- and the v-direction)

    :param obj: input surface
    :type obj: Abstract.Surface
    :return: derivative surfaces w.r.t. u, v and both u-v
    :rtype: tuple
    """
    if not isinstance(obj, Abstract.Surface):
        raise TypeError("Input shape must be an instance of Abstract.Surface class")

    if obj.rational:
        warnings.warn("Cannot compute hodograph surface for a rational surface")
        return obj

    # Find the control points of the derivative surface
    d = 2  # 0 <= k + l <= d, see pg. 114 of The NURBS Book, 2nd Ed.
    pkl = evaluators.SurfaceEvaluator2.derivatives_ctrlpts(r1=0, r2=obj.ctrlpts_size_u - 1,
                                                           s1=0, s2=obj.ctrlpts_size_v - 1,
                                                           degree_u=obj.degree_u, degree_v=obj.degree_v,
                                                           ctrlpts_size_u=obj.ctrlpts_size_u,
                                                           ctrlpts_size_v=obj.ctrlpts_size_v,
                                                           knotvector_u=obj.knotvector_u, knotvector_v=obj.knotvector_v,
                                                           ctrlpts=obj.ctrlpts2d,
                                                           dimension=obj.dimension,
                                                           deriv_order=d)

    ctrlpts2d_u = []
    for i in range(0, len(pkl[1][0]) - 1):
        ctrlpts2d_u.append(pkl[1][0][i])

    surf_u = copy.deepcopy(obj)
    surf_u.degree_u = obj.degree_u - 1
    surf_u.ctrlpts2d = ctrlpts2d_u
    surf_u.knotvector_u = obj.knotvector_u[1:-1]
    surf_u.delta = obj.delta

    ctrlpts2d_v = []
    for i in range(0, len(pkl[0][1])):
        ctrlpts2d_v.append(pkl[0][1][i][0:-1])

    surf_v = copy.deepcopy(obj)
    surf_v.degree_v = obj.degree_v - 1
    surf_v.ctrlpts2d = ctrlpts2d_v
    surf_v.knotvector_v = obj.knotvector_v[1:-1]
    surf_v.delta = obj.delta

    ctrlpts2d_uv = []
    for i in range(0, len(pkl[1][1]) - 1):
        ctrlpts2d_uv.append(pkl[1][1][i][0:-1])

    # Generate the derivative curve
    surf_uv = obj.__class__()
    surf_uv.degree_u = obj.degree_u - 1
    surf_uv.degree_v = obj.degree_v - 1
    surf_uv.ctrlpts2d = ctrlpts2d_uv
    surf_uv.knotvector_u = obj.knotvector_u[1:-1]
    surf_uv.knotvector_v = obj.knotvector_v[1:-1]
    surf_uv.delta = obj.delta

    return surf_u, surf_v, surf_uv


def translate(obj, vec, **kwargs):
    """ Translates a single curve or a surface by the input vector.

    If you pass ``inplace=True`` keyword argument, the input shape will be updated. Otherwise, this function does not
    change the input shape but returns the updated shape.

    :param obj: Curve or surface to be translated
    :type obj: Abstract.Curve or Abstract.Surface
    :param vec: translation vector
    :type vec: list, tuple
    """
    # Input validity checks
    if not isinstance(obj, (Abstract.Curve, Abstract.Surface)):
        raise TypeError("The input shape must be a single curve or a surface")

    if not vec or not isinstance(vec, (tuple, list)):
        raise TypeError("The input must be a list or a tuple")

    if len(vec) != obj.dimension:
        raise ValueError("The input must have " + str(obj.dimension) + " elements")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    # Translate control points
    new_ctrlpts = []
    for point in obj.ctrlpts:
        temp = [v + vec[i] for i, v in enumerate(point)]
        new_ctrlpts.append(temp)

    if inplace:
        obj.ctrlpts = new_ctrlpts
        return obj
    else:
        ret = copy.deepcopy(obj)
        ret.ctrlpts = new_ctrlpts
        return ret


def tangent(obj, params, **kwargs):
    """ Evaluates the tangent vector of the curves or surfaces at the input parameter values.

    This function is designed to evaluate tangent vectors of the B-Spline and NURBS shapes at single or
    multiple parameter positions.

    :param obj: input shape
    :type obj: Abstract.Curve or Abstract.Surface
    :param params: parameters
    :type params: float, list or tuple
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, Abstract.Curve):
        if isinstance(params, (list, tuple)):
            return _tangent_curve_single_list(obj, params, normalize)
        else:
            return _tangent_curve_single(obj, params, normalize)
    if isinstance(obj, Abstract.Surface):
        if isinstance(params[0], float):
            return _tangent_surface_single(obj, params, normalize)
        else:
            return _tangent_surface_single_list(obj, params, normalize)


def normal(obj, params, **kwargs):
    """ Evaluates the normal vector of the curves or surfaces at the input parameter values.

    This function is designed to evaluate normal vectors of the B-Spline and NURBS shapes at single or
    multiple parameter positions.

    :param obj: input shape
    :type obj: Abstract.Curve or Abstract.Surface
    :param params: parameters
    :type params: float, list or tuple
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, Abstract.Curve):
        if isinstance(params, (list, tuple)):
            return _normal_curve_single_list(obj, params, normalize)
        else:
            return _normal_curve_single(obj, params, normalize)
    if isinstance(obj, Abstract.Surface):
        if isinstance(params[0], float):
            return _normal_surface_single(obj, params, normalize)
        else:
            return _normal_surface_single_list(obj, params, normalize)


def binormal(obj, params, **kwargs):
    """ Evaluates the binormal vector of the curves or surfaces at the input parameter values.

    This function is designed to evaluate binormal vectors of the B-Spline and NURBS shapes at single or
    multiple parameter positions.

    :param obj: input shape
    :type obj: Abstract.Curve or Abstract.Surface
    :param params: parameters
    :type params: float, list or tuple
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, Abstract.Curve):
        if isinstance(params, (list, tuple)):
            return _binormal_curve_single_list(obj, params, normalize)
        else:
            return _binormal_curve_single(obj, params, normalize)
    if isinstance(obj, Abstract.Surface):
        raise NotImplementedError("Binormal vector evaluation for the surfaces is not implemented!")


# Evaluates the curve tangent at the given u parameter
def _tangent_curve_single(obj, u, normalize):
    """ Evaluates the curve tangent vector at the given parameter value.

    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param obj: input curve
    :type obj: Abstract.Curve
    :param u: parameter
    :type u: float
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    # 1st derivative of the curve gives the tangent
    ders = obj.derivatives(u, 1)

    point = ders[0]
    vector = utilities.vector_normalize(ders[1]) if normalize else ders[1]

    return tuple(point), tuple(vector)


def _tangent_curve_single_list(obj, param_list, normalize):
    """ Evaluates the curve tangent vectors at the given list of parameter values.

    :param obj: input curve
    :type obj: Abstract.Curve
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = _tangent_curve_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


def _normal_curve_single(obj, u, normalize):
    """ Evaluates the curve normal vector at the input parameter, u.

    Curve normal is calculated from the 2nd derivative of the curve at the input parameter, u.
    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param obj: input curve
    :type obj: Abstract.Curve
    :param u: parameter
    :type u: float
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    # 2nd derivative of the curve gives the normal
    ders = obj.derivatives(u, 2)

    point = ders[0]
    vector = utilities.vector_normalize(ders[2]) if normalize else ders[2]

    return tuple(point), tuple(vector)


def _normal_curve_single_list(obj, param_list, normalize):
    """ Evaluates the curve normal vectors at the given list of parameter values.

    :param obj: input curve
    :type obj: Abstract.Curve
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = _normal_curve_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


# Evaluates the curve binormal at the given u parameter
def _binormal_curve_single(obj, u, normalize):
    """ Evaluates the curve binormal vector at the given u parameter.

    Curve binormal is the cross product of the normal and the tangent vectors.
    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param obj: input curve
    :type obj: Abstract.Curve
    :param u: parameter
    :type u: float
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    # Cross product of tangent and normal vectors gives binormal vector
    tan_vector = _tangent_curve_single(obj, u, normalize)
    norm_vector = _normal_curve_single(obj, u, normalize)

    point = tan_vector[0]
    vector = utilities.vector_cross(tan_vector[1], norm_vector[1])
    vector = utilities.vector_normalize(vector) if normalize else vector

    return tuple(point), tuple(vector)


def _binormal_curve_single_list(obj, param_list, normalize):
    """ Evaluates the curve binormal vectors at the given list of parameter values.

    :param obj: input curve
    :type obj: Abstract.Curve
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = _binormal_curve_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


# Evaluates the surface tangent vectors at the given (u,v) parameter
def _tangent_surface_single(obj, uv, normalize):
    """ Evaluates the surface tangent vector at the given (u,v) parameter pair.

    The output returns a list containing the starting point (i.e., origin) of the vector and the vectors themselves.

    :param obj: input surface
    :type obj: Abstract.Surface
    :param uv: (u,v) parameter pair
    :type uv: list or tuple
    :param normalize: if True, the returned tangent vector is converted to a unit vector
    :type normalize: bool
    :return: A list in the order of "surface point", "derivative w.r.t. u" and "derivative w.r.t. v"
    :rtype: list
    """
    # Tangent is the 1st derivative of the surface
    skl = obj.derivatives(uv[0], uv[1], 1)

    point = skl[0][0]
    vector_u = utilities.vector_normalize(skl[1][0]) if normalize else skl[1][0]
    vector_v = utilities.vector_normalize(skl[0][1]) if normalize else skl[0][1]

    return tuple(point), tuple(vector_u), tuple(vector_v)


def _tangent_surface_single_list(obj, param_list, normalize):
    """ Evaluates the surface tangent vectors at the given list of parameter values.

    :param obj: input surface
    :type obj: Abstract.Surface
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = _tangent_surface_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


# Evaluates the surface normal vector at the given (u, v) parameter
def _normal_surface_single(obj, uv, normalize):
    """ Evaluates the surface normal vector at the given (u, v) parameter pair.

    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param obj: input surface
    :type obj: Abstract.Surface
    :param uv: (u,v) parameter pair
    :type uv: list or tuple
    :param normalize: if True, the returned normal vector is converted to a unit vector
    :type normalize: bool
    :return: a list in the order of "surface point" and "normal vector"
    :rtype: list
    """
    # Take the 1st derivative of the surface
    skl = obj.derivatives(uv[0], uv[1], 1)

    point = skl[0][0]
    vector = utilities.vector_cross(skl[1][0], skl[0][1])
    vector = utilities.vector_normalize(vector) if normalize else vector

    return tuple(point), tuple(vector)


def _normal_surface_single_list(obj, param_list, normalize):
    """ Evaluates the surface normal vectors at the given list of parameter values.

    :param obj: input surface
    :type obj: Abstract.Surface
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = _normal_surface_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


def find_ctrlpts(obj, u, v=None, **kwargs):
    """ Finds the control points involved in the evaluation of the curve/surface point defined by the input parameter(s).

    :param obj: curve or surface
    :type obj: Abstract.Curve or Abstract.Surface
    :param u: parameter (for curve), parameter on the u-direction (for surface)
    :type u: float
    :param v: parameter on the v-direction (for surface only)
    :type v: float
    :return: control points; 1-dimensional array for curve, 2-dimensional array for surface
    :rtype: list
    """
    utilities.check_uv(u, v)
    if isinstance(obj, Abstract.Curve):
        return _find_ctrlpts_curve(u, obj, **kwargs)
    elif isinstance(obj, Abstract.Surface):
        if v is None:
            raise ValueError("Parameter value for the v-direction must be set for operating on surfaces")
        return _find_ctrlpts_surface(u, v, obj, **kwargs)
    else:
        raise NotImplementedError("The input must be an instance of Abstract.Curve or Abstract.Surface")


def _find_ctrlpts_curve(t, curve, **kwargs):
    """ Finds the control points involved in the evaluation of the curve point defined by the input parameter.

    This function uses a modified version of the algorithm *A3.1 CurvePoint* from The NURBS Book by Piegl & Tiller.

    :param t: parameter
    :type t: float
    :param curve: input curve object
    :type curve: Abstract.Curve
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


def _find_ctrlpts_surface(t_u, t_v, surf, **kwargs):
    """ Finds the control points involved in the evaluation of the surface point defined by the input parameter pair.

    This function uses a modified version of the algorithm *A3.5 SurfacePoint* from The NURBS Book by Piegl & Tiller.

    :param t_u: parameter on the u-direction
    :type t_u: float
    :param t_v: parameter on the v-direction
    :type t_v: float
    :param surf: input surface
    :type surf: Abstract.Surface
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
