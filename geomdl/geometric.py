"""
.. module:: operations
    :platform: Unix, Windows
    :synopsis: Provides geometric operations that can be applied to all types of shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import copy
from . import Abstract
from . import utilities


def translate(obj, vec, **kwargs):
    """ Translates a single curve or a surface by the input vector.

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
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, Abstract.Curve):
        return _tangent_curve(obj, params, normalize)
    if isinstance(obj, Abstract.Surface):
        return _tangent_surface(obj, params[0], params[1], normalize)


def normal(obj, params, **kwargs):
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, Abstract.Curve):
        return _normal_curve(obj, params, normalize)
    if isinstance(obj, Abstract.Surface):
        return _normal_surface(obj, params[0], params[1], normalize)


def binormal(obj, params, **kwargs):
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, Abstract.Curve):
        return _binormal_curve(obj, params, normalize)
    if isinstance(obj, Abstract.Surface):
        raise NotImplementedError("Binormal vector evaluation for the surfaces is not implemented!")


# Evaluates the curve tangent at the given u parameter
def _tangent_curve(obj, u, normalize):
    """ Evaluates the curve tangent vector at the given parameter value.

    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param u: knot value
    :type u: float
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list in the order of "curve point" and "tangent"
    :rtype: list
    """
    # 1st derivative of the curve gives the tangent
    ders = obj.derivatives(u, 1)

    # For readability
    point = ders[0]
    der_u = ders[1]

    # Normalize the tangent vector
    if normalize:
        der_u = utilities.vector_normalize(der_u)

    # Return the values
    return tuple(point), tuple(der_u)


# Evaluates the curve normal at the given u parameter
def _normal_curve(obj, u, normalize):
    """ Evaluates the curve normal vector at the given parameter value.

    Curve normal is basically the second derivative of the curve.
    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param u: knot value
    :type u: float
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list in the order of "curve point" and "normal"
    :rtype: list
    """
    # 2nd derivative of the curve gives the normal
    ders = obj.derivatives(u, 2)

    # For readability
    point = ders[0]
    der_u = ders[2]

    # Normalize the normal vector
    if normalize:
        der_u = utilities.vector_normalize(der_u)

    # Return the values
    return tuple(point), tuple(der_u)


# Evaluates the curve binormal at the given u parameter
def _binormal_curve(obj, u, normalize):
    """ Evaluates the curve binormal vector at the given u parameter.

    Curve binormal is the cross product of the normal and the tangent vectors.
    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param u: knot value
    :type u: float
    :param normalize: if True, the returned vector is converted to a unit vector
    :type normalize: bool
    :return: a list in the order of "curve point" and "binormal"
    :rtype: list
    """
    tan_vector = _tangent_curve(obj, u, normalize)
    norm_vector = _normal_curve(obj, u, normalize)

    point = tan_vector[0]
    binorm_vector = utilities.vector_cross(tan_vector[1], norm_vector[1])

    # Normalize the binormal vector
    if normalize:
        binorm_vector = utilities.vector_normalize(binorm_vector)

    # Return the values
    return tuple(point), tuple(binorm_vector)


# Evaluates the surface tangent vectors at the given (u,v) parameter
def _tangent_surface(obj, u, v, normalize):
    """ Evaluates the surface tangent vector at the given (u,v) parameter pair.

    The output returns a list containing the starting point (i.e., origin) of the vector and the vectors themselves.

    :param u: parameter on the u-direction
    :type u: float
    :param v: parameter on the v-direction
    :type v: float
    :param normalize: if True, the returned tangent vector is converted to a unit vector
    :type normalize: bool
    :return: A list in the order of "surface point", "derivative w.r.t. u" and "derivative w.r.t. v"
    :rtype: list
    """
    # Tangent is the 1st derivative of the surface
    skl = obj.derivatives(u, v, 1)

    # Doing this just for readability
    point = skl[0][0]
    der_u = skl[1][0]
    der_v = skl[0][1]

    # Normalize the tangent vectors
    if normalize:
        der_u = utilities.vector_normalize(der_u)
        der_v = utilities.vector_normalize(der_v)

    # Return the list of tangents w.r.t. u and v
    return tuple(point), tuple(der_u), tuple(der_v)


# Evaluates the surface normal vector at the given (u, v) parameter
def _normal_surface(obj, u, v, normalize):
    """ Evaluates the surface normal vector at the given (u, v) parameter pair.

    The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

    :param u: parameter on the u-direction
    :type u: float
    :param v: parameter on the v-direction
    :type v: float
    :param normalize: if True, the returned normal vector is converted to a unit vector
    :type normalize: bool
    :return: a list in the order of "surface point" and "normal vector"
    :rtype: list
    """
    # Check u and v parameters are correct for the normal evaluation
    utilities.check_uv(u, v)

    # Take the 1st derivative of the surface
    skl = obj.derivatives(u, v, 1)

    # For readability
    point = skl[0][0]
    der_u = skl[1][0]
    der_v = skl[0][1]

    # Compute normal
    normal = utilities.vector_cross(der_u, der_v)

    if normalize:
        # Convert normal vector to a unit vector
        normal = utilities.vector_normalize(tuple(normal))

    # Return the surface normal at the input (u,v) parametric location
    return tuple(point), tuple(normal)
