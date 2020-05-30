"""
.. module:: operations
    :platform: Unix, Windows
    :synopsis: Provides geometric operations for spline geometry classes

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import math
import copy
from . import abstract, helpers, linalg
from . import _operations as ops
from .base import export, GeomdlTypeSequence, GeomdlError, GeomdlWarning


def degree_operations(obj, param, **kwargs):
    """ Applies degree elevation and degree reduction algorithms to spline geometries.

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param param: operation definition
    :type param: list, tuple
    :return: updated spline geometry
    """
    def validate_reduction(degree):
        if degree < 2:
            raise GeomdlError("Input spline geometry must have degree > 1")

    # Start curve degree manipulation operations
    if obj.pdimension == 1:
        if param[0] is not None and param[0] != 0:
            # Find multiplicity of the internal knots
            int_knots = set(obj.knotvector[obj.degree.u + 1:-(obj.degree.u + 1)])
            mult_arr = []
            for ik in int_knots:
                s = helpers.find_multiplicity(ik, obj.knotvector.u)
                mult_arr.append(s)

            # Decompose the input by knot insertion
            crv_list = decompose_curve(obj, **kwargs)

            # If parameter is positive, apply degree elevation. Otherwise, apply degree reduction
            if param[0] > 0:
                # Loop through to apply degree elevation
                for crv in crv_list:
                    cpts = crv.ctrlptsw
                    new_cpts = helpers.degree_elevation(crv.degree.u, cpts, num=param[0])
                    crv.degree += param[0]
                    crv.set_ctrlpts(new_cpts)
                    crv.knotvector.u = [crv.knotvector.u[0] for _ in range(param[0])] + list(crv.knotvector.u) + [crv.knotvector.u[-1] for _ in range(param[0])]

                # Compute new degree
                nd = obj.degree.u + param[0]

                # Number of knot removals
                num = obj.degree.u + 1
            else:
                # Validate degree reduction operation
                validate_reduction(obj.degree.u)

                # Loop through to apply degree reduction
                for crv in crv_list:
                    cpts = crv.ctrlptsw
                    new_cpts = helpers.degree_reduction(crv.degree.u, cpts)
                    crv.degree -= 1
                    crv.set_ctrlpts(new_cpts)
                    crv.knotvector = list(crv.knotvector.u[1:-1])

                # Compute new degree
                nd = obj.degree.u - 1

                # Number of knot removals
                num = obj.degree.u - 1

            # Link curves together (reverse of decomposition)
            kv, cpts, ws, knots = ops.link_curves(*crv_list, validate=False)

            # Organize control points (if necessary)
            ctrlpts = compatibility.combine_ctrlpts_weights(cpts, ws) if obj.rational else cpts

            # Apply knot removal
            for k, s in zip(knots, mult_arr):
                span = helpers.find_span_linear(nd, kv, len(ctrlpts), k)
                ctrlpts = helpers.knot_removal(nd, kv, ctrlpts, k, num=num-s)
                kv = helpers.knot_removal_kv(kv, span, num-s)

            # Update input curve
            obj.degree = nd
            obj.set_ctrlpts(ctrlpts)
            obj.knotvector = kv

    # Start surface degree manipulation operations
    if obj.pdimension == 2:
        # u-direction
        if param[0] is not None and param[0] != 0:

            # If parameter is positive, apply degree elevation. Else, apply degree reduction
            if param[0] > 0:
                pass
            else:
                # Apply degree reduction operation
                validate_reduction(obj.degree.u)

        # v-direction
        if param[1] is not None and param[1] != 0:

            # If parameter is positive, apply degree elevation. Otherwise, apply degree reduction
            if param[1] > 0:
                pass
            else:
                # Validate degree reduction operation
                validate_reduction(obj.degree.v)

    # Start surface degree manipulation operations
    if obj.pdimension == 3:
        raise GeomdlError("Degree manipulation operations are not available for spline volumes")

    # Return updated spline geometry
    return obj


@export
def add_dimension(obj, **kwargs):
    """ Elevates the spatial dimension of the spline geometry.

    If you pass ``inplace=True`` keyword argument, the input will be updated. Otherwise, this function does not
    change the input but returns a new instance with the updated data.

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :return: updated spline geometry
    :rtype: abstract.SplineGeometry
    """
    if not isinstance(obj, abstract.SplineGeometry):
        raise GeomdlError("Can only operate on spline geometry objects")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)
    array_init = kwargs.get('array_init', [[] for _ in range(len(obj.ctrlpts))])
    offset_value = kwargs.get('offset', 0.0)

    # Update control points
    new_ctrlpts = array_init
    for idx, point in enumerate(obj.ctrlpts):
        temp = [float(p) for p in point[0:obj.dimension]]
        temp.append(offset_value)
        new_ctrlpts[idx] = temp

    if inplace:
        obj.ctrlpts = new_ctrlpts
        return obj
    else:
        ret = copy.deepcopy(obj)
        ret.ctrlpts = new_ctrlpts
        return ret


@export
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
    if not isinstance(obj, abstract.Curve):
        raise GeomdlError("Input shape must be an instance of abstract.Curve class")

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


@export
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
    if not isinstance(obj, abstract.Curve):
        raise GeomdlError("Input shape must be an instance of abstract.Curve class")

    multi_curve = []
    curve = copy.deepcopy(obj)
    knots = curve.knotvector[curve.degree + 1:-(curve.degree + 1)]
    while knots:
        knot = knots[0]
        curves = split_curve(curve, param=knot, **kwargs)
        multi_curve.append(curves[0])
        curve = curves[1]
        knots = curve.knotvector[curve.degree + 1:-(curve.degree + 1)]
    multi_curve.append(curve)

    return multi_curve


@export
def derivative_curve(obj):
    """ Computes the hodograph (first derivative) curve of the input curve.

    This function constructs the hodograph (first derivative) curve from the input curve by computing the degrees,
    knot vectors and the control points of the derivative curve.

    :param obj: input curve
    :type obj: abstract.Curve
    :return: derivative curve
    """
    if not isinstance(obj, abstract.Curve):
        raise GeomdlError("Input shape must be an instance of abstract.Curve class")

    # Unfortunately, rational curves do NOT have this property
    # Ref: https://pages.mtu.edu/~shene/COURSES/cs3621/LAB/curve/1st-2nd.html
    if obj.rational:
        GeomdlWarning("Cannot compute hodograph curve for a rational curve")
        return obj

    # Find the control points of the derivative curve
    pkl = helpers.curve_deriv_cpts(obj.dimension, obj.degree, obj.knotvector, obj.ctrlpts,
                                          rs=(0, obj.ctrlpts_size - 1), deriv_order=1)

    # Generate the derivative curve
    curve = obj.__class__()
    curve.degree = obj.degree - 1
    curve.ctrlpts = pkl[1][0:-1]
    curve.knotvector = obj.knotvector[1:-1]
    curve.delta = obj.delta

    return curve


@export
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
    if not isinstance(obj, abstract.Surface):
        raise GeomdlError("Input shape must be an instance of abstract.Surface class")

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


@export
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
    if not isinstance(obj, abstract.Surface):
        raise GeomdlError("Input shape must be an instance of abstract.Surface class")

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


@export
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
    def decompose(srf, idx, split_func_list, **kws):
        srf_list = []
        knots = srf.knotvector[idx][srf.degree[idx] + 1:-(srf.degree[idx] + 1)]
        while knots:
            knot = knots[0]
            srfs = split_func_list[idx](srf, param=knot, **kws)
            srf_list.append(srfs[0])
            srf = srfs[1]
            knots = srf.knotvector[idx][srf.degree[idx] + 1:-(srf.degree[idx] + 1)]
        srf_list.append(srf)
        return srf_list

    # Validate input
    if not isinstance(obj, abstract.Surface):
        raise GeomdlError("Input shape must be an instance of abstract.Surface class")

    # Get keyword arguments
    decompose_dir = kwargs.get('decompose_dir', 'uv')  # possible directions: u, v, uv
    if "decompose_dir" in kwargs:
        kwargs.pop("decompose_dir")

    # List of split functions
    split_funcs = [split_surface_u, split_surface_v]

    # Work with an identical copy
    surf = copy.deepcopy(obj)

    # Only u-direction
    if decompose_dir == 'u':
        return decompose(surf, 0, split_funcs, **kwargs)

    # Only v-direction
    if decompose_dir == 'v':
        return decompose(surf, 1, split_funcs, **kwargs)

    # Both u- and v-directions
    if decompose_dir == 'uv':
        multi_surf = []
        # Process u-direction
        surfs_u = decompose(surf, 0, split_funcs, **kwargs)
        # Process v-direction
        for sfu in surfs_u:
            multi_surf += decompose(sfu, 1, split_funcs, **kwargs)
        return multi_surf
    else:
        raise GeomdlError("Cannot decompose in " + str(decompose_dir) + " direction. Acceptable values: u, v, uv")


@export
def derivative_surface(obj):
    """ Computes the hodograph (first derivative) surface of the input surface.

    This function constructs the hodograph (first derivative) surface from the input surface by computing the degrees,
    knot vectors and the control points of the derivative surface.

    The return value of this function is a tuple containing the following derivative surfaces in the given order:

    * U-derivative surface (derivative taken only on the u-direction)
    * V-derivative surface (derivative taken only on the v-direction)
    * UV-derivative surface (derivative taken on both the u- and the v-direction)

    :param obj: input surface
    :type obj: abstract.Surface
    :return: derivative surfaces w.r.t. u, v and both u-v
    :rtype: tuple
    """
    if not isinstance(obj, abstract.Surface):
        raise GeomdlError("Input shape must be an instance of abstract.Surface class")

    if obj.rational:
        GeomdlWarning("Cannot compute hodograph surface for a rational surface")
        return obj

    # Find the control points of the derivative surface
    d = 2  # 0 <= k + l <= d, see pg. 114 of The NURBS Book, 2nd Ed.
    pkl = helpers.surface_deriv_cpts(obj.dimension, obj.degree, obj.knotvector, obj.ctrlpts, obj.cpsize,
                                            rs=(0, obj.ctrlpts_size_u - 1), ss=(0, obj.ctrlpts_size_v - 1), deriv_order=d)

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
