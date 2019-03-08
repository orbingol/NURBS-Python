"""
.. module:: _operations
    :platform: Unix, Windows
    :synopsis: Helper functions for operations module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import math
import copy
from . import linalg, helpers, ray


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


def get_par_box(domain, last=False):
    """ Returns the bounding box of the surface parametric domain in ccw direction. """
    u_range = domain[0]
    v_range = domain[1]
    verts = [(u_range[0], v_range[0]), (u_range[1], v_range[0]), (u_range[1], v_range[1]), (u_range[0], v_range[1])]
    if last:
        verts.append(verts[0])
    return tuple(verts)


def detect_sense(curve, tol):
    """ Detects the sense, i.e. clockwise or counter-clockwise, of the curve

    :param curve: 2-dimensional trim curve
    :type curve: abstract.Curve
    :param tol: tolerance value
    :type tol: float
    :return: True if detection is successful, False otherwise
    :rtype: bool
    """
    if curve.opt_get('sense') is None:
        # Detect sense since it is unset
        pts = curve.evalpts
        num_pts = len(pts)
        for idx in range(1, num_pts - 1):
            sense = detect_ccw(pts[idx - 1], pts[idx], pts[idx + 1], tol)
            if sense < 0:  # cw
                curve.opt = ['sense', 0]
                return True
            elif sense > 0:  # ccw
                curve.opt = ['sense', 1]
                return True
            else:
                continue
        # One final test with random points to determine the orientation
        sense = detect_ccw(pts[int(num_pts/3)], pts[int(2*num_pts/3)], pts[-int(num_pts/3)], tol)
        if sense < 0:  # cw
            curve.opt = ['sense', 0]
            return True
        elif sense > 0:  # ccw
            curve.opt = ['sense', 1]
            return True
        else:
            # Cannot determine the sense
            return False
    else:
        # Don't touch the sense value as it has been already set
        return True


def detect_ccw(pt1, pt2, pt3, tol):
    vec1 = linalg.vector_generate(pt1, pt2)
    vec2 = linalg.vector_generate(pt2, pt3)
    cross = linalg.vector_cross(vec1, vec2)
    if cross[2] > tol:  # cw
        return -1
    elif cross[2] < -tol:  # ccw
        return 1
    return 0


def detect_intersection(start_pt, end_pt, test_pt, tol):
    dist_num = abs(((end_pt[1] - start_pt[1]) * test_pt[0]) - ((end_pt[0] - start_pt[0]) * test_pt[1]) + (end_pt[0] * start_pt[1]) - (end_pt[1] * start_pt[0]))
    dist_denom = math.sqrt(math.pow(end_pt[1] - start_pt[1], 2) + math.pow(end_pt[0] - start_pt[0], 2))
    dist = dist_num / dist_denom
    if abs(dist) < tol:
        return True
    return False


def check_trim_curve(curve, parbox, **kwargs):
    """

    :param curve: trim curve
    :param parbox: parameter space bounding box of the underlying surface
    :return:
    """
    def next_idx(edge_idx, direction):
        tmp = edge_idx + direction
        if tmp < 0:
            return 3
        if tmp > 3:
            return 0
        return tmp

    # Keyword arguments
    tol = kwargs.get('tol', 10e-8)

    # First, check if the curve is closed
    dist = linalg.point_distance(curve.evalpts[0], curve.evalpts[-1])
    if dist <= tol:
        # Curve is closed
        return detect_sense(curve, tol), []
    else:
        # Curve is not closed but it could be on the edge on the parametric domain
        # Apply ray intersection to find which edge the end points of the curve is on
        # Connect end points with a line and create a curve container

        # Define start and end points of the trim curve
        pt_start = curve.evalpts[0]
        pt_end = curve.evalpts[-1]

        # Search for intersections
        idx_spt = -1
        idx_ept = -1
        for idx in range(len(parbox) - 1):
            if detect_intersection(parbox[idx], parbox[idx + 1], pt_start, tol):
                idx_spt = idx
            if detect_intersection(parbox[idx], parbox[idx + 1], pt_end, tol):
                idx_ept = idx

        # Check result of the intersection
        if idx_spt < 0 or idx_ept < 0:
            # Curve does not intersect any edges of the parametric space
            # TODO: Extrapolate the curve using the tangent vector and find intersections
            return False, []
        else:
            # Get sense of the original curve
            c_sense = curve.opt_get('sense')

            # If sense is None, then detect sense
            if c_sense is None:
                # Get evaluated points
                pts = curve.evalpts
                num_pts = len(pts)

                # Find sense
                tmp_sense = 0
                for pti in range(1, num_pts - 1):
                    tmp_sense = detect_ccw(pts[pti - 1], pts[pti], pts[pti + 1], tol)
                    if tmp_sense != 0:
                        break
                if tmp_sense == 0:
                    tmp_sense2 = detect_ccw(pts[int(num_pts/3)], pts[int(2*num_pts/3)], pts[-int(num_pts/3)], tol)
                    if tmp_sense2 != 0:
                        tmp_sense = -tmp_sense2
                    else:
                        # We cannot decide which region to trim. Therefore, ignore this curve.
                        return False, []

                c_sense = 0 if tmp_sense > 0 else 1

                # Update sense of the original curve
                curve.opt = ['sense', c_sense]

            # Generate a curve container and add the original curve
            cont = [curve]

            move_dir = -1 if c_sense == 0 else 1

            # Curve intersects with the edges of the parametric space
            counter = 0
            while counter < 4:
                if idx_ept == idx_spt:
                    counter = 5
                    pt_start = curve.evalpts[0]
                else:
                    # Find next index
                    idx_ept = next_idx(idx_ept, move_dir)
                    # Update tracked last point
                    pt_start = parbox[idx_ept + 1 - c_sense]
                    # Increment counter
                    counter += 1

                # Generate the curve segment
                crv = curve.__class__()
                crv.degree = 1
                crv.ctrlpts = [pt_end, pt_start]
                crv.knotvector = [0, 0, 1, 1]
                crv.opt = ['sense', c_sense]

                pt_end = pt_start

                # Add it to the container
                cont.append(crv)

            # Update curve
            return True, cont
