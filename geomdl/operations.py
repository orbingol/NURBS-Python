"""
.. module:: operations
    :platform: Unix, Windows
    :synopsis: Provides geometric operations for spline geometry classes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import math
import copy
import warnings
from . import abstract, helpers, linalg, compatibility
from . import _operations as ops
from .exceptions import GeomdlException
from ._utilities import export


@export
def insert_knot(obj, param, num, **kwargs):
    """ Inserts knots n-times to a spline geometry.

    The following code snippet illustrates the usage of this function:

    .. code-block:: python

        # Insert knot u=0.5 to a curve 2 times
        operations.insert_knot(curve, [0.5], [2])

        # Insert knot v=0.25 to a surface 1 time
        operations.insert_knot(surface, [None, 0.25], [0, 1])

        # Insert knots u=0.75, v=0.25 to a surface 2 and 1 times, respectively
        operations.insert_knot(surface, [0.75, 0.25], [2, 1])

        # Insert knot w=0.5 to a volume 1 time
        operations.insert_knot(volume, [None, None, 0.5], [0, 0, 1])

    Please note that input spline geometry object will always be updated if the knot insertion operation is successful.

    Keyword Arguments:
        * ``check_num``: enables/disables operation validity checks. *Default: True*

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param param: knot(s) to be inserted in [u, v, w] format
    :type param: list, tuple
    :param num: number of knot insertions in [num_u, num_v, num_w] format
    :type num: list, tuple
    :return: updated spline geometry
    """
    # Get keyword arguments
    check_num = kwargs.get('check_num', True)  # can be set to False when the caller checks number of insertions

    if check_num:
        # Check the validity of number of insertions
        if not isinstance(num, (list, tuple)):
            raise GeomdlException("The number of insertions must be a list or a tuple",
                                  data=dict(num=num))

        if len(num) != obj.pdimension:
            raise GeomdlException("The length of the num array must be equal to the number of parametric dimensions",
                                  data=dict(pdim=obj.pdimension, num_len=len(num)))

        for idx, val in enumerate(num):
            if val < 0:
                raise GeomdlException('Number of insertions must be a positive integer value',
                                      data=dict(idx=idx, num=val))

    # Start curve knot insertion
    if isinstance(obj, abstract.Curve):
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s = helpers.find_multiplicity(param[0], obj.knotvector)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree - s:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s))

            # Find knot span
            span = helpers.find_span_linear(obj.degree, obj.knotvector, obj.ctrlpts_size, param[0])

            # Compute new knot vector
            kv_new = helpers.knot_insertion_kv(obj.knotvector, param[0], span, num[0])

            # Compute new control points
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            cpts_tmp = helpers.knot_insertion(obj.degree, obj.knotvector, cpts, param[0],
                                              num=num[0], s=s, span=span)

            # Update curve
            obj.set_ctrlpts(cpts_tmp)
            obj.knotvector = kv_new

    # Start surface knot insertion
    if isinstance(obj, abstract.Surface):
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector_u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree_u - s_u:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times (u-dir)",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param[0])

            # Compute new knot vector
            kv_u = helpers.knot_insertion_kv(obj.knotvector_u, param[0], span_u, num[0])

            # Get curves
            cpts_tmp = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for v in range(obj.ctrlpts_size_v):
                ccu = [cpts[v + (obj.ctrlpts_size_v * u)] for u in range(obj.ctrlpts_size_u)]
                ctrlpts_tmp = helpers.knot_insertion(obj.degree_u, obj.knotvector_u, ccu, param[0],
                                                     num=num[0], s=s_u, span=span_u)
                cpts_tmp += ctrlpts_tmp

            # Update the surface after knot insertion
            obj.set_ctrlpts(compatibility.flip_ctrlpts_u(cpts_tmp, obj.ctrlpts_size_u + num[0], obj.ctrlpts_size_v),
                            obj.ctrlpts_size_u + num[0], obj.ctrlpts_size_v)
            obj.knotvector_u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > obj.degree_v - s_v:
                raise GeomdlException("Knot " + str(param[1]) + " cannot be inserted " + str(num[1]) + " times (v-dir)",
                                      data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param[1])

            # Compute new knot vector
            kv_v = helpers.knot_insertion_kv(obj.knotvector_v, param[1], span_v, num[1])

            # Get curves
            cpts_tmp = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for u in range(obj.ctrlpts_size_u):
                ccv = [cpts[v + (obj.ctrlpts_size_v * u)] for v in range(obj.ctrlpts_size_v)]
                ctrlpts_tmp = helpers.knot_insertion(obj.degree_v, obj.knotvector_v, ccv, param[1],
                                                     num=num[1], s=s_v, span=span_v)
                cpts_tmp += ctrlpts_tmp

            # Update the surface after knot insertion
            obj.set_ctrlpts(cpts_tmp, obj.ctrlpts_size_u, obj.ctrlpts_size_v + num[1])
            obj.knotvector_v = kv_v

    # Start volume knot insertion
    if isinstance(obj, abstract.Volume):
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector_u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree_u - s_u:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times (u-dir)",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param[0])

            # Compute new knot vector
            kv_u = helpers.knot_insertion_kv(obj.knotvector_u, param[0], span_u, num[0])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(obj.ctrlpts_size_u):
                temp_surf = []
                for w in range(obj.ctrlpts_size_w):
                    for v in range(obj.ctrlpts_size_v):
                        temp_pt = cpts[v + (u * obj.ctrlpts_size_v) + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree_u, obj.knotvector_u, cpt2d, param[0],
                                                 num=num[0], s=s_u, span=span_u)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w):
                for u in range(obj.ctrlpts_size_u + num[0]):
                    for v in range(obj.ctrlpts_size_v):
                        temp_pt = ctrlpts_tmp[u][v + (w * obj.ctrlpts_size_v)]
                        ctrlpts_new.append(temp_pt)

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u + num[0], obj.ctrlpts_size_v, obj.ctrlpts_size_w)
            obj.knotvector_u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > obj.degree_v - s_v:
                raise GeomdlException("Knot " + str(param[1]) + " cannot be inserted " + str(num[1]) + " times (v-dir)",
                                      data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param[1])

            # Compute new knot vector
            kv_v = helpers.knot_insertion_kv(obj.knotvector_v, param[1], span_v, num[1])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(obj.ctrlpts_size_v):
                temp_surf = []
                for w in range(obj.ctrlpts_size_w):
                    for u in range(obj.ctrlpts_size_u):
                        temp_pt = cpts[v + (u * obj.ctrlpts_size_v) + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree_v, obj.knotvector_v, cpt2d, param[1],
                                                 num=num[1], s=s_v, span=span_v)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w):
                for u in range(obj.ctrlpts_size_u):
                    for v in range(obj.ctrlpts_size_v + num[1]):
                        temp_pt = ctrlpts_tmp[v][u + (w * obj.ctrlpts_size_u)]
                        ctrlpts_new.append(temp_pt)

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v + num[1], obj.ctrlpts_size_w)
            obj.knotvector_v = kv_v

        # w-direction
        if param[2] is not None and num[2] > 0:
            # Find knot multiplicity
            s_w = helpers.find_multiplicity(param[2], obj.knotvector_w)

            # Check if it is possible add that many number of knots
            if check_num and num[2] > obj.degree_w - s_w:
                raise GeomdlException("Knot " + str(param[2]) + " cannot be inserted " + str(num[2]) + " times (w-dir)",
                                      data=dict(knot=param[2], num=num[2], multiplicity=s_w))

            # Find knot span
            span_w = helpers.find_span_linear(obj.degree_w, obj.knotvector_w, obj.ctrlpts_size_w, param[2])

            # Compute new knot vector
            kv_w = helpers.knot_insertion_kv(obj.knotvector_w, param[2], span_w, num[2])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(obj.ctrlpts_size_w):
                temp_surf = [cpts[uv + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)] for uv in
                             range(obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree_w, obj.knotvector_w, cpt2d, param[2],
                                                 num=num[2], s=s_w, span=span_w)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w + num[2]):
                ctrlpts_new += ctrlpts_tmp[w]

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v, obj.ctrlpts_size_w + num[2])
            obj.knotvector_w = kv_w

    # Return updated spline geometry
    return obj


@export
def remove_knot(obj, param, num, **kwargs):
    """ Removes knots n-times from a spline geometry.

    The following code snippet illustrates the usage of this function:

    .. code-block:: python

        # Remove knot u=0.5 from a curve 2 times
        operations.remove_knot(curve, [0.5], [2])

        # Remove knot v=0.25 from a surface 1 time
        operations.remove_knot(surface, [None, 0.25], [0, 1])

        # Remove knots u=0.75, v=0.25 from a surface 2 and 1 times, respectively
        operations.remove_knot(surface, [0.75, 0.25], [2, 1])

        # Remove knot w=0.5 from a volume 1 time
        operations.remove_knot(volume, [None, None, 0.5], [0, 0, 1])

    Please note that input spline geometry object will always be updated if the knot removal operation is successful.

    Keyword Arguments:
        * ``check_num``: enables/disables operation validity checks. *Default: True*

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param param: knot(s) to be removed in [u, v, w] format
    :type param: list, tuple
    :param num: number of knot removals in [num_u, num_v, num_w] format
    :type num: list, tuple
    :return: updated spline geometry
    """
    # Get keyword arguments
    check_num = kwargs.get('check_num', True)  # can be set to False when the caller checks number of removals

    if check_num:
        # Check the validity of number of insertions
        if not isinstance(num, (list, tuple)):
            raise GeomdlException("The number of removals must be a list or a tuple",
                                  data=dict(num=num))

        if len(num) != obj.pdimension:
            raise GeomdlException("The length of the num array must be equal to the number of parametric dimensions",
                                  data=dict(pdim=obj.pdimension, num_len=len(num)))

        for idx, val in enumerate(num):
            if val < 0:
                raise GeomdlException('Number of removals must be a positive integer value',
                                      data=dict(idx=idx, num=val))

    # Start curve knot removal
    if isinstance(obj, abstract.Curve):
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s = helpers.find_multiplicity(param[0], obj.knotvector)

            # It is impossible to remove knots if num > s
            if check_num and num[0] > s:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s))

            # Find knot span
            span = helpers.find_span_linear(obj.degree, obj.knotvector, obj.ctrlpts_size, param[0])

            # Compute new control points
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            ctrlpts_new = helpers.knot_removal(obj.degree, obj.knotvector, cpts, param[0], num=num[0], s=s, span=span)

            # Compute new knot vector
            kv_new = helpers.knot_removal_kv(obj.knotvector, span, num[0])

            # Update curve
            obj.set_ctrlpts(ctrlpts_new)
            obj.knotvector = kv_new

    # Start surface knot removal
    if isinstance(obj, abstract.Surface):
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector_u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > s_u:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times (u-dir)",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param[0])

            # Get curves
            ctrlpts_new = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for v in range(obj.ctrlpts_size_v):
                ccu = [cpts[v + (obj.ctrlpts_size_v * u)] for u in range(obj.ctrlpts_size_u)]
                ctrlpts_tmp = helpers.knot_removal(obj.degree_u, obj.knotvector_u, ccu, param[0],
                                                   num=num[0], s=s_u, span=span_u)
                ctrlpts_new += ctrlpts_tmp

            # Compute new knot vector
            kv_u = helpers.knot_removal_kv(obj.knotvector_u, span_u, num[0])

            # Update the surface after knot removal
            obj.set_ctrlpts(compatibility.flip_ctrlpts_u(ctrlpts_new, obj.ctrlpts_size_u - num[0], obj.ctrlpts_size_v),
                            obj.ctrlpts_size_u - num[0], obj.ctrlpts_size_v)
            obj.knotvector_u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > s_v:
                raise GeomdlException("Knot " + str(param[1]) + " cannot be removed " + str(num[1]) + " times (v-dir)",
                                      data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param[1])

            # Get curves
            ctrlpts_new = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for u in range(obj.ctrlpts_size_u):
                ccv = [cpts[v + (obj.ctrlpts_size_v * u)] for v in range(obj.ctrlpts_size_v)]
                ctrlpts_tmp = helpers.knot_removal(obj.degree_v, obj.knotvector_v, ccv, param[1],
                                                   num=num[1], s=s_v, span=span_v)
                ctrlpts_new += ctrlpts_tmp

            # Compute new knot vector
            kv_v = helpers.knot_removal_kv(obj.knotvector_v, span_v, num[1])

            # Update the surface after knot removal
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v - num[1])
            obj.knotvector_v = kv_v

    # Start volume knot removal
    if isinstance(obj, abstract.Volume):
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector_u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > s_u:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times (u-dir)",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param[0])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(obj.ctrlpts_size_u):
                temp_surf = []
                for w in range(obj.ctrlpts_size_w):
                    for v in range(obj.ctrlpts_size_v):
                        temp_pt = cpts[v + (u * obj.ctrlpts_size_v) + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_removal(obj.degree_u, obj.knotvector_u, cpt2d, param[0],
                                               num=num[0], s=s_u, span=span_u)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w):
                for u in range(obj.ctrlpts_size_u - num[0]):
                    for v in range(obj.ctrlpts_size_v):
                        temp_pt = ctrlpts_tmp[u][v + (w * obj.ctrlpts_size_v)]
                        ctrlpts_new.append(temp_pt)

            # Compute new knot vector
            kv_u = helpers.knot_removal_kv(obj.knotvector_u, span_u, num[0])

            # Update the volume after knot removal
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u - num[0], obj.ctrlpts_size_v, obj.ctrlpts_size_w)
            obj.knotvector_u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > s_v:
                raise GeomdlException("Knot " + str(param[1]) + " cannot be removed " + str(num[1]) + " times (v-dir)",
                                      data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param[1])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(obj.ctrlpts_size_v):
                temp_surf = []
                for w in range(obj.ctrlpts_size_w):
                    for u in range(obj.ctrlpts_size_u):
                        temp_pt = cpts[v + (u * obj.ctrlpts_size_v) + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_removal(obj.degree_v, obj.knotvector_v, cpt2d, param[1],
                                               num=num[1], s=s_v, span=span_v)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w):
                for u in range(obj.ctrlpts_size_u):
                    for v in range(obj.ctrlpts_size_v - num[1]):
                        temp_pt = ctrlpts_tmp[v][u + (w * obj.ctrlpts_size_u)]
                        ctrlpts_new.append(temp_pt)

            # Compute new knot vector
            kv_v = helpers.knot_removal_kv(obj.knotvector_v, span_v, num[1])

            # Update the volume after knot removal
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v - num[1], obj.ctrlpts_size_w)
            obj.knotvector_v = kv_v

        # w-direction
        if param[2] is not None and num[2] > 0:
            # Find knot multiplicity
            s_w = helpers.find_multiplicity(param[2], obj.knotvector_w)

            # Check if it is possible add that many number of knots
            if check_num and num[2] > s_w:
                raise GeomdlException("Knot " + str(param[2]) + " cannot be removed " + str(num[2]) + " times (w-dir)",
                                      data=dict(knot=param[2], num=num[2], multiplicity=s_w))

            # Find knot span
            span_w = helpers.find_span_linear(obj.degree_w, obj.knotvector_w, obj.ctrlpts_size_w, param[2])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(obj.ctrlpts_size_w):
                temp_surf = [cpts[uv + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)] for uv in
                             range(obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_removal(obj.degree_w, obj.knotvector_w, cpt2d, param[2],
                                               num=num[2], s=s_w, span=span_w)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w - num[2]):
                ctrlpts_new += ctrlpts_tmp[w]

            # Compute new knot vector
            kv_w = helpers.knot_removal_kv(obj.knotvector_w, span_w, num[2])

            # Update the volume after knot removal
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v, obj.ctrlpts_size_w - num[2])
            obj.knotvector_w = kv_w

    # Return updated spline geometry
    return obj


@export
def refine_knotvector(obj, param, **kwargs):
    """ Refines the knot vector(s) of a spline geometry.

    The following code snippet illustrates the usage of this function:

    .. code-block:: python

        # Refines the knot vector of a curve
        operations.refine_knotvector(curve, [1])

        # Refines the knot vector on the v-direction of a surface
        operations.refine_knotvector(surface, [0, 1])

        # Refines the both knot vectors of a surface
        operations.refine_knotvector(surface, [1, 1])

        # Refines the knot vector on the w-direction of a volume
        operations.refine_knotvector(volume, [0, 0, 1])

    The values of ``param`` argument can be used to set the *knot refinement density*. If *density* is bigger than 1,
    then the algorithm finds the middle knots in each internal knot span to increase the number of knots to be refined.

    **Example**: Let the degree is 2 and the knot vector to be refined is ``[0, 2, 4]`` with the superfluous knots
    from the start and end are removed. Knot vectors with the changing ``density (d)`` value will be:

    * ``d = 1``, knot vector ``[0, 1, 1, 2, 2, 3, 3, 4]``
    * ``d = 2``, knot vector ``[0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2, 2, 2.5, 2.5, 3, 3, 3.5, 3.5, 4]``

    The following code snippet illustrates the usage of knot refinement densities:

    .. code-block:: python

        # Refines the knot vector of a curve with density = 3
        operations.refine_knotvector(curve, [3])

        # Refines the knot vectors of a surface with density for
        # u-dir = 2 and v-dir = 3
        operations.refine_knotvector(surface, [2, 3])

        # Refines only the knot vector on the v-direction of a surface with density = 1
        operations.refine_knotvector(surface, [0, 1])

        # Refines the knot vectors of a volume with density for
        # u-dir = 1, v-dir = 3 and w-dir = 2
        operations.refine_knotvector(volume, [1, 3, 2])

    Please refer to :func:`.helpers.knot_refinement` function for more usage options.

    Keyword Arguments:
        * ``check_num``: enables/disables operation validity checks. *Default: True*

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param param: parametric dimensions to be refined in [u, v, w] format
    :type param: list, tuple
    :return: updated spline geometry
    """
    # Get keyword arguments
    check_num = kwargs.get('check_num', True)  # enables/disables input validity checks

    if check_num:
        if not isinstance(param, (list, tuple)):
            raise GeomdlException("Parametric dimensions argument (param) must be a list or a tuple")

        if len(param) != obj.pdimension:
            raise GeomdlException("The length of the param array must be equal to the number of parametric dimensions",
                                  data=dict(pdim=obj.pdimension, param_len=len(param)))

    # Start curve knot refinement
    if isinstance(obj, abstract.Curve):
        if param[0] > 0:
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            new_cpts, new_kv = helpers.knot_refinement(obj.degree, obj.knotvector, cpts, density=param[0])
            obj.set_ctrlpts(new_cpts)
            obj.knotvector = new_kv

    # Start surface knot refinement
    if isinstance(obj, abstract.Surface):
        # u-direction
        if param[0] > 0:
            # Get curves
            new_cpts = []
            new_cpts_size = 0
            new_kv = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for v in range(obj.ctrlpts_size_v):
                ccu = [cpts[v + (obj.ctrlpts_size_v * u)] for u in range(obj.ctrlpts_size_u)]
                ptmp, new_kv = helpers.knot_refinement(obj.degree_u, obj.knotvector_u, ccu, density=param[0])
                new_cpts_size = len(ptmp)
                new_cpts += ptmp

            # Update the surface after knot refinement
            obj.set_ctrlpts(compatibility.flip_ctrlpts_u(new_cpts, new_cpts_size, obj.ctrlpts_size_v),
                            new_cpts_size, obj.ctrlpts_size_v)
            obj.knotvector_u = new_kv

        # v-direction
        if param[1] > 0:
            # Get curves
            new_cpts = []
            new_cpts_size = 0
            new_kv = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for u in range(obj.ctrlpts_size_u):
                ccv = [cpts[v + (obj.ctrlpts_size_v * u)] for v in range(obj.ctrlpts_size_v)]
                ptmp, new_kv = helpers.knot_refinement(obj.degree_v, obj.knotvector_v, ccv, density=param[1])
                new_cpts_size = len(ptmp)
                new_cpts += ptmp

            # Update the surface after knot refinement
            obj.set_ctrlpts(new_cpts, obj.ctrlpts_size_u, new_cpts_size)
            obj.knotvector_v = new_kv

    # Start volume knot refinement
    if isinstance(obj, abstract.Volume):
        # u-direction
        if param[0] > 0:
            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(obj.ctrlpts_size_u):
                temp_surf = []
                for w in range(obj.ctrlpts_size_w):
                    for v in range(obj.ctrlpts_size_v):
                        temp_pt = cpts[v + (u * obj.ctrlpts_size_v) + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(obj.degree_u, obj.knotvector_u, cpt2d, density=param[0])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w):
                for u in range(new_cpts_size):
                    for v in range(obj.ctrlpts_size_v):
                        temp_pt = ctrlpts_tmp[u][v + (w * obj.ctrlpts_size_v)]
                        ctrlpts_new.append(temp_pt)

            # Update the volume after knot removal
            obj.set_ctrlpts(ctrlpts_new, new_cpts_size, obj.ctrlpts_size_v, obj.ctrlpts_size_w)
            obj.knotvector_u = kv_new

        # v-direction
        if param[1] > 0:
            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(obj.ctrlpts_size_v):
                temp_surf = []
                for w in range(obj.ctrlpts_size_w):
                    for u in range(obj.ctrlpts_size_u):
                        temp_pt = cpts[v + (u * obj.ctrlpts_size_v) + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(obj.degree_v, obj.knotvector_v, cpt2d, density=param[1])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w):
                for u in range(obj.ctrlpts_size_u):
                    for v in range(new_cpts_size):
                        temp_pt = ctrlpts_tmp[v][u + (w * obj.ctrlpts_size_u)]
                        ctrlpts_new.append(temp_pt)

            # Update the volume after knot removal
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, new_cpts_size, obj.ctrlpts_size_w)
            obj.knotvector_v = kv_new

        # w-direction
        if param[2] > 0:
            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(obj.ctrlpts_size_w):
                temp_surf = [cpts[uv + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)] for uv in
                             range(obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(obj.degree_w, obj.knotvector_w, cpt2d, density=param[2])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(new_cpts_size):
                ctrlpts_new += ctrlpts_tmp[w]

            # Update the volume after knot removal
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v, new_cpts_size)
            obj.knotvector_w = kv_new

    # Return updated spline geometry
    return obj


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
            raise GeomdlException("Input spline geometry must have degree > 1")

    # Start curve degree manipulation operations
    if isinstance(obj, abstract.Curve):
        if param[0] is not None and param[0] != 0:
            # Find multiplicity of the internal knots
            int_knots = set(obj.knotvector[obj.degree + 1:-(obj.degree + 1)])
            mult_arr = []
            for ik in int_knots:
                s = helpers.find_multiplicity(ik, obj.knotvector)
                mult_arr.append(s)

            # Decompose the input by knot insertion
            crv_list = decompose_curve(obj, **kwargs)

            # If parameter is positive, apply degree elevation. Otherwise, apply degree reduction
            if param[0] > 0:
                # Loop through to apply degree elevation
                for crv in crv_list:
                    cpts = crv.ctrlptsw if crv.rational else crv.ctrlpts
                    new_cpts = helpers.degree_elevation(crv.degree, cpts, num=param[0])
                    crv.degree += param[0]
                    crv.set_ctrlpts(new_cpts)
                    crv.knotvector = [crv.knotvector[0] for _ in range(param[0])] + list(crv.knotvector) + [crv.knotvector[-1] for _ in range(param[0])]

                # Compute new degree
                nd = obj.degree + param[0]

                # Number of knot removals
                num = obj.degree + 1
            else:
                # Validate degree reduction operation
                validate_reduction(obj.degree)

                # Loop through to apply degree reduction
                for crv in crv_list:
                    cpts = crv.ctrlptsw if crv.rational else crv.ctrlpts
                    new_cpts = helpers.degree_reduction(crv.degree, cpts)
                    crv.degree -= 1
                    crv.set_ctrlpts(new_cpts)
                    crv.knotvector = list(crv.knotvector[1:-1])

                # Compute new degree
                nd = obj.degree - 1

                # Number of knot removals
                num = obj.degree - 1

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
    if isinstance(obj, abstract.Surface):
        # u-direction
        if param[0] is not None and param[0] != 0:

            # If parameter is positive, apply degree elevation. Else, apply degree reduction
            if param[0] > 0:
                pass
            else:
                # Apply degree reduction operation
                validate_reduction(obj.degree_u)

        # v-direction
        if param[1] is not None and param[1] != 0:

            # If parameter is positive, apply degree elevation. Otherwise, apply degree reduction
            if param[1] > 0:
                pass
            else:
                # Validate degree reduction operation
                validate_reduction(obj.degree_v)

    # Start surface degree manipulation operations
    if isinstance(obj, abstract.Volume):
        raise GeomdlException("Degree manipulation operations are not available for spline volumes")

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
        raise GeomdlException("Can only operate on spline geometry objects")

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
        raise GeomdlException("Input shape must be an instance of abstract.Curve class")

    if param == obj.domain[0] or param == obj.domain[1]:
        raise GeomdlException("Cannot split from the domain edge")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)  # FindSpan implementation
    insert_knot_func = kwargs.get('insert_knot_func', insert_knot)  # Knot insertion algorithm

    # Find multiplicity of the knot and define how many times we need to add the knot
    ks = span_func(obj.degree, obj.knotvector, len(obj.ctrlpts), param) - obj.degree + 1
    s = helpers.find_multiplicity(param, obj.knotvector)
    r = obj.degree - s

    # Create backups of the original curve
    temp_obj = copy.deepcopy(obj)

    # Insert knot
    insert_knot_func(temp_obj, [param], num=[r], check_num=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree, temp_obj.knotvector, len(temp_obj.ctrlpts), param) + 1
    curve1_kv = list(temp_obj.knotvector[0:knot_span])
    curve1_kv.append(param)
    curve2_kv = list(temp_obj.knotvector[knot_span:])
    for _ in range(0, temp_obj.degree + 1):
        curve2_kv.insert(0, param)

    # Control points (use Pw if rational)
    cpts = temp_obj.ctrlptsw if obj.rational else temp_obj.ctrlpts
    curve1_ctrlpts = cpts[0:ks + r]
    curve2_ctrlpts = cpts[ks + r - 1:]

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
        raise GeomdlException("Input shape must be an instance of abstract.Curve class")

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
        raise GeomdlException("Input shape must be an instance of abstract.Curve class")

    # Unfortunately, rational curves do NOT have this property
    # Ref: https://pages.mtu.edu/~shene/COURSES/cs3621/LAB/curve/1st-2nd.html
    if obj.rational:
        warnings.warn("Cannot compute hodograph curve for a rational curve")
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
def length_curve(obj):
    """ Computes the approximate length of the parametric curve.

    Uses the following equation to compute the approximate length:

    .. math::

        \\sum_{i=0}^{n-1} \\sqrt{P_{i + 1}^2-P_{i}^2}

    where :math:`n` is number of evaluated curve points and :math:`P` is the n-dimensional point.

    :param obj: input curve
    :type obj: abstract.Curve
    :return: length
    :rtype: float
    """
    if not isinstance(obj, abstract.Curve):
        raise GeomdlException("Input shape must be an instance of abstract.Curve class")

    length = 0.0
    evalpts = obj.evalpts
    num_evalpts = len(obj.evalpts)
    for idx in range(num_evalpts - 1):
        length += linalg.point_distance(evalpts[idx], evalpts[idx + 1])
    return length


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
        raise GeomdlException("Input shape must be an instance of abstract.Surface class")

    if param == obj.domain[0][0] or param == obj.domain[0][1]:
        raise GeomdlException("Cannot split from the u-domain edge")

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
        raise GeomdlException("Input shape must be an instance of abstract.Surface class")

    if param == obj.domain[1][0] or param == obj.domain[1][1]:
        raise GeomdlException("Cannot split from the v-domain edge")

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
        raise GeomdlException("Input shape must be an instance of abstract.Surface class")

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
        raise GeomdlException("Cannot decompose in " + str(decompose_dir) + " direction. Acceptable values: u, v, uv")


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
        raise GeomdlException("Input shape must be an instance of abstract.Surface class")

    if obj.rational:
        warnings.warn("Cannot compute hodograph surface for a rational surface")
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


@export
def find_ctrlpts(obj, u, v=None, **kwargs):
    """ Finds the control points involved in the evaluation of the curve/surface point defined by the input parameter(s).

    :param obj: curve or surface
    :type obj: abstract.Curve or abstract.Surface
    :param u: parameter (for curve), parameter on the u-direction (for surface)
    :type u: float
    :param v: parameter on the v-direction (for surface only)
    :type v: float
    :return: control points; 1-dimensional array for curve, 2-dimensional array for surface
    :rtype: list
    """
    if isinstance(obj, abstract.Curve):
        return ops.find_ctrlpts_curve(u, obj, **kwargs)
    elif isinstance(obj, abstract.Surface):
        if v is None:
            raise GeomdlException("Parameter value for the v-direction must be set for operating on surfaces")
        return ops.find_ctrlpts_surface(u, v, obj, **kwargs)
    else:
        raise GeomdlException("The input must be an instance of abstract.Curve or abstract.Surface")


@export
def tangent(obj, params, **kwargs):
    """ Evaluates the tangent vector of the curves or surfaces at the input parameter values.

    This function is designed to evaluate tangent vectors of the B-Spline and NURBS shapes at single or
    multiple parameter positions.

    :param obj: input shape
    :type obj: abstract.Curve or abstract.Surface
    :param params: parameters
    :type params: float, list or tuple
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, abstract.Curve):
        if isinstance(params, (list, tuple)):
            return ops.tangent_curve_single_list(obj, params, normalize)
        else:
            return ops.tangent_curve_single(obj, params, normalize)
    if isinstance(obj, abstract.Surface):
        if isinstance(params[0], float):
            return ops.tangent_surface_single(obj, params, normalize)
        else:
            return ops.tangent_surface_single_list(obj, params, normalize)


@export
def normal(obj, params, **kwargs):
    """ Evaluates the normal vector of the curves or surfaces at the input parameter values.

    This function is designed to evaluate normal vectors of the B-Spline and NURBS shapes at single or
    multiple parameter positions.

    :param obj: input geometry
    :type obj: abstract.Curve or abstract.Surface
    :param params: parameters
    :type params: float, list or tuple
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, abstract.Curve):
        raise GeomdlException("Not implemented for curves")
    if isinstance(obj, abstract.Surface):
        if isinstance(params[0], float):
            return ops.normal_surface_single(obj, params, normalize)
        else:
            return ops.normal_surface_single_list(obj, params, normalize)


@export
def translate(obj, vec, **kwargs):
    """ Translates curves, surface or volumes by the input vector.

    Keyword Arguments:
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param obj: input geometry
    :type obj: abstract.SplineGeometry or multi.AbstractContainer
    :param vec: translation vector
    :type vec: list, tuple
    :return: translated geometry object
    """
    # Input validity checks
    if not vec or not isinstance(vec, (tuple, list)):
        raise GeomdlException("The input must be a list or a tuple")

    # Input validity checks
    if len(vec) != obj.dimension:
        raise GeomdlException("The input vector must have " + str(obj.dimension) + " components")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    if not inplace:
        geom = copy.deepcopy(obj)
    else:
        geom = obj

    # Translate control points
    for g in geom:
        new_ctrlpts = []
        for pt in g.ctrlpts:
            temp = [v + vec[i] for i, v in enumerate(pt)]
            new_ctrlpts.append(temp)
        g.ctrlpts = new_ctrlpts

    return geom


@export
def rotate(obj, angle, **kwargs):
    """ Rotates curves, surfaces or volumes about the chosen axis.

    Keyword Arguments:
        * ``axis``: rotation axis; x, y, z correspond to 0, 1, 2 respectively. *Default: 2*
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param obj: input geometry
    :type obj: abstract.SplineGeometry, multi.AbstractGeometry
    :param angle: angle of rotation (in degrees)
    :type angle: float
    :return: rotated geometry object
    """
    def rotate_x(ncs, opt, alpha):
        # Generate translation vector
        translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

        # Translate to the origin
        translate(ncs, translate_vector, inplace=True)

        # Then, rotate about the axis
        rot = math.radians(alpha)
        new_ctrlpts = [[0.0 for _ in range(ncs.dimension)] for _ in range(len(ncs.ctrlpts))]
        for idx, pt in enumerate(ncs.ctrlpts):
            new_ctrlpts[idx][0] = pt[0]
            new_ctrlpts[idx][1] = (pt[1] * math.cos(rot)) - (pt[2] * math.sin(rot))
            new_ctrlpts[idx][2] = (pt[2] * math.cos(rot)) + (pt[1] * math.sin(rot))
        ncs.ctrlpts = new_ctrlpts

        # Finally, translate back to the starting location
        translate(ncs, [-tv for tv in translate_vector], inplace=True)

    def rotate_y(ncs, opt, alpha):
        # Generate translation vector
        translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

        # Translate to the origin
        translate(ncs, translate_vector, inplace=True)

        # Then, rotate about the axis
        rot = math.radians(alpha)
        new_ctrlpts = [[0.0 for _ in range(ncs.dimension)] for _ in range(len(ncs.ctrlpts))]
        for idx, pt in enumerate(ncs.ctrlpts):
            new_ctrlpts[idx][0] = (pt[0] * math.cos(rot)) - (pt[2] * math.sin(rot))
            new_ctrlpts[idx][1] = pt[1]
            new_ctrlpts[idx][2] = (pt[2] * math.cos(rot)) + (pt[0] * math.sin(rot))
        ncs.ctrlpts = new_ctrlpts

        # Finally, translate back to the starting location
        translate(ncs, [-tv for tv in translate_vector], inplace=True)

    def rotate_z(ncs, opt, alpha):
        # Generate translation vector
        translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

        # Translate to the origin
        translate(ncs, translate_vector, inplace=True)

        # Then, rotate about the axis
        rot = math.radians(alpha)
        new_ctrlpts = [list(ncs.ctrlpts[i]) for i in range(len(ncs.ctrlpts))]
        for idx, pt in enumerate(ncs.ctrlpts):
            new_ctrlpts[idx][0] = (pt[0] * math.cos(rot)) - (pt[1] * math.sin(rot))
            new_ctrlpts[idx][1] = (pt[1] * math.cos(rot)) + (pt[0] * math.sin(rot))
        ncs.ctrlpts = new_ctrlpts

        # Finally, translate back to the starting location
        translate(ncs, [-tv for tv in translate_vector], inplace=True)

    # Set rotation axis
    axis = 2 if obj.dimension == 2 else int(kwargs.get('axis', 2))
    if not 0 <= axis <= 2:
        raise GeomdlException("Value of the 'axis' argument should be 0, 1 or 2")
    rotfunc = (rotate_x, rotate_y, rotate_z)

    # Operate on a copy or the actual object
    inplace = kwargs.get('inplace', False)
    if not inplace:
        geom = copy.deepcopy(obj)
    else:
        geom = obj

    # Set a single origin
    if geom[0].pdimension == 1:
        params = geom[0].domain[0]
    else:
        params = [geom[0].domain[i][0] for i in range(geom[0].pdimension)]
    origin = geom[0].evaluate_single(params)

    # Start rotation
    for g in geom:
        rotfunc[axis](g, origin, angle)

    return geom


@export
def scale(obj, multiplier, **kwargs):
    """ Scales curves, surfaces or volumes by the input multiplier.

    Keyword Arguments:
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param obj: input geometry
    :type obj: abstract.SplineGeometry, multi.AbstractGeometry
    :param multiplier: scaling multiplier
    :type multiplier: float
    :return: scaled geometry object
    """
    # Input validity checks
    if not isinstance(multiplier, (int, float)):
        raise GeomdlException("The multiplier must be a float or an integer")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    if not inplace:
        geom = copy.deepcopy(obj)
    else:
        geom = obj

    # Scale control points
    for g in geom:
        new_ctrlpts = [[] for _ in range(g.ctrlpts_size)]
        for idx, pts in enumerate(g.ctrlpts):
            new_ctrlpts[idx] = [p * float(multiplier) for p in pts]
        g.ctrlpts = new_ctrlpts

    return geom


@export
def transpose(surf, **kwargs):
    """ Transposes the input surface(s) by swapping u and v parametric directions.

    Keyword Arguments:
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param surf: input surface(s)
    :type surf: abstract.Surface, multi.SurfaceContainer
    :return: transposed surface(s)
    """
    if surf.pdimension != 2:
        raise GeomdlException("Can only transpose surfaces")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    if not inplace:
        geom = copy.deepcopy(surf)
    else:
        geom = surf

    for g in geom:
        # Get existing data
        degree_u_new = g.degree_v
        degree_v_new = g.degree_u
        kv_u_new = g.knotvector_v
        kv_v_new = g.knotvector_u
        ctrlpts2d_old = g.ctrlpts2d

        # Find new control points
        ctrlpts2d_new = []
        for v in range(0, g.ctrlpts_size_v):
            ctrlpts_u = []
            for u in range(0, g.ctrlpts_size_u):
                temp = ctrlpts2d_old[u][v]
                ctrlpts_u.append(temp)
            ctrlpts2d_new.append(ctrlpts_u)

        g.degree_u = degree_u_new
        g.degree_v = degree_v_new
        g.ctrlpts2d = ctrlpts2d_new
        g.knotvector_u = kv_u_new
        g.knotvector_v = kv_v_new

    return geom


@export
def flip(surf, **kwargs):
    """ Flips the control points grid of the input surface(s).

    Keyword Arguments:
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param surf: input surface(s)
    :type surf: abstract.Surface, multi.SurfaceContainer
    :return: flipped surface(s)
    """
    if surf.pdimension != 2:
        raise GeomdlException("Can only flip surfaces")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    if not inplace:
        geom = copy.deepcopy(surf)
    else:
        geom = surf

    for g in geom:
        size_u = g.ctrlpts_size_u
        size_v = g.ctrlpts_size_v
        cpts = g.ctrlptsw if g.rational else g.ctrlpts
        new_cpts = [[] for _ in range(g.ctrlpts_size)]
        idx = g.ctrlpts_size - 1
        for pt in cpts:
            new_cpts[idx] = pt
            idx -= 1
        g.set_ctrlpts(new_cpts, size_u, size_v)

    return geom
