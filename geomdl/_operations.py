"""
.. module:: _operations
    :platform: Unix, Windows
    :synopsis: Helper functions for operations module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import copy
from . import linalg, helpers


# Initialize an empty __all__ for controlling imports
__all__ = []


def translate_single(obj, vec, **kwargs):
    # Input validity checks
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


def translate_multi(obj, vec, **kwargs):
    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    ret = obj.__class__()
    for o in obj:
        temp = translate_single(o, vec, **kwargs)
        ret.add(temp)

    if inplace:
        return obj
    else:
        return ret


def tangent_curve_single(obj, u, normalize):
    """ Evaluates the curve tangent vector at the given parameter value.

    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param obj: input curve
    :type obj: abstract.Curve
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
    vector = linalg.vector_normalize(ders[1]) if normalize else ders[1]

    return tuple(point), tuple(vector)


def tangent_curve_single_list(obj, param_list, normalize):
    """ Evaluates the curve tangent vectors at the given list of parameter values.

    :param obj: input curve
    :type obj: abstract.Curve
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = tangent_curve_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


def normal_curve_single(obj, u, normalize):
    """ Evaluates the curve normal vector at the input parameter, u.

    Curve normal is calculated from the 2nd derivative of the curve at the input parameter, u.
    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param obj: input curve
    :type obj: abstract.Curve
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
    vector = linalg.vector_normalize(ders[2]) if normalize else ders[2]

    return tuple(point), tuple(vector)


def normal_curve_single_list(obj, param_list, normalize):
    """ Evaluates the curve normal vectors at the given list of parameter values.

    :param obj: input curve
    :type obj: abstract.Curve
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = normal_curve_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


def binormal_curve_single(obj, u, normalize):
    """ Evaluates the curve binormal vector at the given u parameter.

    Curve binormal is the cross product of the normal and the tangent vectors.
    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param obj: input curve
    :type obj: abstract.Curve
    :param u: parameter
    :type u: float
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    # Cross product of tangent and normal vectors gives binormal vector
    tan_vector = tangent_curve_single(obj, u, normalize)
    norm_vector = normal_curve_single(obj, u, normalize)

    point = tan_vector[0]
    vector = linalg.vector_cross(tan_vector[1], norm_vector[1])
    vector = linalg.vector_normalize(vector) if normalize else vector

    return tuple(point), tuple(vector)


def binormal_curve_single_list(obj, param_list, normalize):
    """ Evaluates the curve binormal vectors at the given list of parameter values.

    :param obj: input curve
    :type obj: abstract.Curve
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = binormal_curve_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


def tangent_surface_single(obj, uv, normalize):
    """ Evaluates the surface tangent vector at the given (u,v) parameter pair.

    The output returns a list containing the starting point (i.e., origin) of the vector and the vectors themselves.

    :param obj: input surface
    :type obj: abstract.Surface
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
    vector_u = linalg.vector_normalize(skl[1][0]) if normalize else skl[1][0]
    vector_v = linalg.vector_normalize(skl[0][1]) if normalize else skl[0][1]

    return tuple(point), tuple(vector_u), tuple(vector_v)


def tangent_surface_single_list(obj, param_list, normalize):
    """ Evaluates the surface tangent vectors at the given list of parameter values.

    :param obj: input surface
    :type obj: abstract.Surface
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = tangent_surface_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


def normal_surface_single(obj, uv, normalize):
    """ Evaluates the surface normal vector at the given (u, v) parameter pair.

    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param obj: input surface
    :type obj: abstract.Surface
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
    vector = linalg.vector_cross(skl[1][0], skl[0][1])
    vector = linalg.vector_normalize(vector) if normalize else vector

    return tuple(point), tuple(vector)


def normal_surface_single_list(obj, param_list, normalize):
    """ Evaluates the surface normal vectors at the given list of parameter values.

    :param obj: input surface
    :type obj: abstract.Surface
    :param param_list: parameter list
    :type param_list: list or tuple
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    ret_vector = []
    for param in param_list:
        temp = normal_surface_single(obj, param, normalize)
        ret_vector.append(temp)
    return tuple(ret_vector)


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


def scale_single(obj, multiplier, **kwargs):
    # Get keyword arguments
    inplace = kwargs.get('inplace', False)

    # Scale control points
    new_ctrlpts = [[] for _ in range(obj.ctrlpts_size)]
    for idx, pts in enumerate(obj.ctrlpts):
        new_ctrlpts[idx] = [p * float(multiplier) for p in pts]

    # Return scaled shape
    if inplace:
        obj.ctrlpts = new_ctrlpts
        return obj
    else:
        nobj = copy.deepcopy(obj)
        nobj.ctrlpts = new_ctrlpts
        return nobj


def scale_multi(obj, multiplier, **kwargs):
    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    ret = obj.__class__()
    for o in obj:
        temp = scale_single(o, multiplier, **kwargs)
        ret.add(temp)

    if inplace:
        return obj
    else:
        return ret
