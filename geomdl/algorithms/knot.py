"""
.. module:: algorithms.knot
    :platform: Unix, Windows
    :synopsis: Knot manipulation algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import helpers
from ..base import GeomdlError, GeomdlTypeSequence

__all__ = []


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
        if not isinstance(num, GeomdlTypeSequence):
            raise GeomdlError("The number of insertions must be a list or a tuple",
                              data=dict(num=num))

        if len(num) != obj.pdimension:
            raise GeomdlError("The length of the num array must be equal to the number of parametric dimensions",
                              data=dict(pdim=obj.pdimension, num_len=len(num)))

        for idx, val in enumerate(num):
            if val < 0:
                raise GeomdlError('Number of insertions must be a positive integer value',
                                  data=dict(idx=idx, num=val))

    # Create a copy of the geometry object
    objc = copy.deepcopy(obj)

    # Start curve knot insertion
    if objc.pdimension == 1:
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s = helpers.find_multiplicity(param[0], objc.knotvector.u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > objc.degree.u - s:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s))

            # Find knot span
            span = helpers.find_span_linear(objc.degree.u, objc.knotvector.u, objc.ctrlpts_size.u, param[0])

            # Compute new knot vector
            kv_new = helpers.knot_insertion_kv(objc.knotvector.u, param[0], span, num[0])

            # Compute new control points
            cpts = list(objc.ctrlptsw.points)
            cpts_tmp = helpers.knot_insertion(objc.degree.u, objc.knotvector.u, cpts, param[0],
                                              num=num[0], s=s, span=span)

            # Update curve
            objc.set_ctrlpts(cpts_tmp)
            objc.knotvector.u = kv_new

    # Start surface knot insertion
    if objc.pdimension == 2:
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], objc.knotvector.u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > objc.degree.u - s_u:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times (u-dir)",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(objc.degree.u, objc.knotvector.u, objc.ctrlpts_size.u, param[0])

            # Compute new knot vector
            kv_u = helpers.knot_insertion_kv(objc.knotvector.u, param[0], span_u, num[0])

            # Get curves
            cpts_tmp = []
            cpts = objc.ctrlptsw
            for v in range(objc.ctrlpts_size.v):
                ccu = [cpts[u, v] for u in range(objc.ctrlpts_size.u)]
                ctrlpts_tmp = helpers.knot_insertion(objc.degree.u, objc.knotvector.u, ccu, param[0],
                                                     num=num[0], s=s_u, span=span_u)
                cpts_tmp += ctrlpts_tmp

            # Update the surface
            objc.set_ctrlpts(cpts_tmp, objc.ctrlpts_size.u + num[0], objc.ctrlpts_size.v)
            objc.knotvector.u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], objc.knotvector.v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > objc.degree.v - s_v:
                raise GeomdlError("Knot " + str(param[1]) + " cannot be inserted " + str(num[1]) + " times (v-dir)",
                                  data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(objc.degree.v, objc.knotvector.v, objc.ctrlpts_size.v, param[1])

            # Compute new knot vector
            kv_v = helpers.knot_insertion_kv(objc.knotvector.v, param[1], span_v, num[1])

            # Get curves
            cpts_tmp = []
            cpts = objc.ctrlptsw
            for u in range(objc.ctrlpts_size.u):
                ccv = [cpts[u, v] for v in range(objc.ctrlpts_size.v)]
                ctrlpts_tmp = helpers.knot_insertion(objc.degree.v, objc.knotvector.v, ccv, param[1],
                                                     num=num[1], s=s_v, span=span_v)
                cpts_tmp += ctrlpts_tmp

            # Update the surface
            ctrlpts_new = []
            for v in range(objc.ctrlpts_size.v + num[1]):
                for u in range(objc.ctrlpts_size.u):
                    ctrlpts_new.append(cpts_tmp[v + (u * (objc.ctrlpts_size.v + num[1]))])

            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, objc.ctrlpts_size.v + num[1])
            objc.knotvector.v = kv_v

    # Start volume knot insertion
    if objc.pdimension == 3:
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], objc.knotvector.u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > objc.degree.u - s_u:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times (u-dir)",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(objc.degree.u, objc.knotvector.u, objc.ctrlpts_size.u, param[0])

            # Compute new knot vector
            kv_u = helpers.knot_insertion_kv(objc.knotvector.u, param[0], span_u, num[0])

            # Use Pw
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(objc.ctrlpts_size.u):
                temp_surf = []
                for v in range(objc.ctrlpts_size.v):
                    for w in range(objc.ctrlpts_size.w):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(objc.degree.u, objc.knotvector.u, cpt2d, param[0],
                                                 num=num[0], s=s_u, span=span_u)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(objc.ctrlpts_size.w):
                for v in range(objc.ctrlpts_size.v):
                    for u in range(objc.ctrlpts_size.u + num[0]):
                        ctrlpts_new.append(ctrlpts_tmp[u][w + (v * objc.ctrlpts_size.w)])

            # Update the volume after knot insertion
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u + num[0], objc.ctrlpts_size.v, objc.ctrlpts_size.w)
            objc.knotvector.u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], objc.knotvector.v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > objc.degree.v - s_v:
                raise GeomdlError("Knot " + str(param[1]) + " cannot be inserted " + str(num[1]) + " times (v-dir)",
                                  data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(objc.degree.v, objc.knotvector.v, objc.ctrlpts_size.v, param[1])

            # Compute new knot vector
            kv_v = helpers.knot_insertion_kv(objc.knotvector.v, param[1], span_v, num[1])

            # Use Pw
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(objc.ctrlpts_size.v):
                temp_surf = []
                for u in range(objc.ctrlpts_size.u):
                    for w in range(objc.ctrlpts_size.w):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(objc.degree.v, objc.knotvector.v, cpt2d, param[1],
                                                 num=num[1], s=s_v, span=span_v)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(objc.ctrlpts_size.w):
                for v in range(objc.ctrlpts_size.v + num[1]):
                    for u in range(objc.ctrlpts_size.u):
                        ctrlpts_new.append(ctrlpts_tmp[v][w + (u * objc.ctrlpts_size.w)])

            # Update the volume after knot insertion
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, objc.ctrlpts_size.v + num[1], objc.ctrlpts_size.w)
            objc.knotvector.v = kv_v

        # w-direction
        if param[2] is not None and num[2] > 0:
            # Find knot multiplicity
            s_w = helpers.find_multiplicity(param[2], objc.knotvector.w)

            # Check if it is possible add that many number of knots
            if check_num and num[2] > objc.degree.w - s_w:
                raise GeomdlError("Knot " + str(param[2]) + " cannot be inserted " + str(num[2]) + " times (w-dir)",
                                  data=dict(knot=param[2], num=num[2], multiplicity=s_w))

            # Find knot span
            span_w = helpers.find_span_linear(objc.degree.w, objc.knotvector.w, objc.ctrlpts_size.w, param[2])

            # Compute new knot vector
            kv_w = helpers.knot_insertion_kv(objc.knotvector.w, param[2], span_w, num[2])

            # Use Pw
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(objc.ctrlpts_size.w):
                temp_surf = []
                for v in range(objc.ctrlpts_size.v):
                    for u in range(objc.ctrlpts_size.u):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(objc.degree.w, objc.knotvector.w, cpt2d, param[2],
                                                 num=num[2], s=s_w, span=span_w)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(objc.ctrlpts_size.w + num[2]):
                for v in range(objc.ctrlpts_size.v):
                    for u in range(objc.ctrlpts_size.u):
                        ctrlpts_new.append(ctrlpts_tmp[w][u + (v * objc.ctrlpts_size.u)])

            # Update the volume after knot insertion
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, objc.ctrlpts_size.v, objc.ctrlpts_size.w + num[2])
            objc.knotvector.w = kv_w

    # Return updated geometry
    return objc


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
        if not isinstance(num, GeomdlTypeSequence):
            raise GeomdlError("The number of removals must be a list or a tuple",
                              data=dict(num=num))

        if len(num) != obj.pdimension:
            raise GeomdlError("The length of the num array must be equal to the number of parametric dimensions",
                              data=dict(pdim=obj.pdimension, num_len=len(num)))

        for idx, val in enumerate(num):
            if val < 0:
                raise GeomdlError('Number of removals must be a positive integer value',
                                  data=dict(idx=idx, num=val))

    # Create a copy of the geometry object
    objc = copy.deepcopy(obj)

    # Start curve knot removal
    if objc.pdimension == 1:
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s = helpers.find_multiplicity(param[0], objc.knotvector.u)

            # It is impossible to remove knots if num > s
            if check_num and num[0] > s:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s))

            # Find knot span
            span = helpers.find_span_linear(objc.degree.u, objc.knotvector.u, objc.ctrlpts_size.u, param[0])

            # Compute new control points
            cpts = list(objc.ctrlptsw.points)
            ctrlpts_new = helpers.knot_removal(objc.degree.u, objc.knotvector.u, cpts, param[0], num=num[0], s=s, span=span)

            # Compute new knot vector
            kv_new = helpers.knot_removal_kv(objc.knotvector.u, span, num[0])

            # Update curve
            objc.set_ctrlpts(ctrlpts_new)
            objc.knotvector.u = kv_new

    # Start surface knot removal
    if objc.pdimension == 2:
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], objc.knotvector.u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > s_u:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times (u-dir)",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(objc.degree.u, objc.knotvector.u, objc.ctrlpts_size.u, param[0])

            # Get curves
            cpts_tmp = []
            cpts = objc.ctrlptsw
            for v in range(objc.ctrlpts_size.v):
                ccu = [cpts[u, v] for u in range(objc.ctrlpts_size.u)]
                ctrlpts_tmp = helpers.knot_removal(objc.degree.u, objc.knotvector.u, ccu, param[0],
                                                     num=num[0], s=s_u, span=span_u)
                cpts_tmp += ctrlpts_tmp

            # Compute new knot vector
            kv_u = helpers.knot_removal_kv(objc.knotvector.u, span_u, num[0])

            # Update the surface
            objc.set_ctrlpts(cpts_tmp, objc.ctrlpts_size.u - num[0], objc.ctrlpts_size.v)
            objc.knotvector.u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], objc.knotvector.v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > s_v:
                raise GeomdlError("Knot " + str(param[1]) + " cannot be removed " + str(num[1]) + " times (v-dir)",
                                  data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(objc.degree.v, objc.knotvector.v, objc.ctrlpts_size.v, param[1])

            # Get curves
            cpts_tmp = []
            cpts = objc.ctrlptsw
            for u in range(objc.ctrlpts_size.u):
                ccv = [cpts[u, v] for v in range(objc.ctrlpts_size.v)]
                ctrlpts_tmp = helpers.knot_removal(objc.degree.v, objc.knotvector.v, ccv, param[1],
                                                     num=num[1], s=s_v, span=span_v)
                cpts_tmp += ctrlpts_tmp

            # Compute new knot vector
            kv_v = helpers.knot_removal_kv(objc.knotvector.v, span_v, num[1])

            # Rearrange control points
            ctrlpts_new = []
            for v in range(objc.ctrlpts_size.v - num[1]):
                for u in range(objc.ctrlpts_size.u):
                    ctrlpts_new.append(cpts_tmp[v + (u * (objc.ctrlpts_size.v - num[1]))])

            # Update the surface
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, objc.ctrlpts_size.v - num[1])
            objc.knotvector.v = kv_v

    # Start volume knot removal
    if objc.pdimension == 3:
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], objc.knotvector.u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > s_u:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times (u-dir)",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(objc.degree.u, objc.knotvector.u, objc.ctrlpts_size.u, param[0])

            # Use Pw
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(objc.ctrlpts_size.u):
                temp_surf = []
                for v in range(objc.ctrlpts_size.v):
                    for w in range(objc.ctrlpts_size.w):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_removal(objc.degree.u, objc.knotvector.u, cpt2d, param[0],
                                                 num=num[0], s=s_u, span=span_u)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(objc.ctrlpts_size.w):
                for v in range(objc.ctrlpts_size.v):
                    for u in range(objc.ctrlpts_size.u - num[0]):
                        ctrlpts_new.append(ctrlpts_tmp[u][w + (v * objc.ctrlpts_size.w)])

            # Compute new knot vector
            kv_u = helpers.knot_removal_kv(objc.knotvector.u, span_u, num[0])

            # Update the volume after knot removal
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u - num[0], objc.ctrlpts_size.v, objc.ctrlpts_size.w)
            objc.knotvector.u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], objc.knotvector.v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > s_v:
                raise GeomdlError("Knot " + str(param[1]) + " cannot be removed " + str(num[1]) + " times (v-dir)",
                                  data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(objc.degree.v, objc.knotvector.v, objc.ctrlpts_size.v, param[1])

            # Use Pw
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(objc.ctrlpts_size.v):
                temp_surf = []
                for u in range(objc.ctrlpts_size.u):
                    for w in range(objc.ctrlpts_size.w):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_removal(objc.degree.v, objc.knotvector.v, cpt2d, param[1],
                                                 num=num[1], s=s_v, span=span_v)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(objc.ctrlpts_size.w):
                for v in range(objc.ctrlpts_size.v -num[1]):
                    for u in range(objc.ctrlpts_size.u):
                        ctrlpts_new.append(ctrlpts_tmp[v][w + (u * objc.ctrlpts_size.w)])

            # Compute new knot vector
            kv_v = helpers.knot_removal_kv(objc.knotvector.v, span_v, num[1])

            # Update the volume after knot removal
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, objc.ctrlpts_size.v - num[1], objc.ctrlpts_size.w)
            objc.knotvector.v = kv_v

        # w-direction
        if param[2] is not None and num[2] > 0:
            # Find knot multiplicity
            s_w = helpers.find_multiplicity(param[2], objc.knotvector.w)

            # Check if it is possible add that many number of knots
            if check_num and num[2] > s_w:
                raise GeomdlError("Knot " + str(param[2]) + " cannot be removed " + str(num[2]) + " times (w-dir)",
                                  data=dict(knot=param[2], num=num[2], multiplicity=s_w))

            # Find knot span
            span_w = helpers.find_span_linear(objc.degree.w, objc.knotvector.w, objc.ctrlpts_size.w, param[2])

            # Use Pw
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(objc.ctrlpts_size.w):
                temp_surf = []
                for v in range(objc.ctrlpts_size.v):
                    for u in range(objc.ctrlpts_size.u):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_removal(objc.degree.w, objc.knotvector.w, cpt2d, param[2],
                                                 num=num[2], s=s_w, span=span_w)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(objc.ctrlpts_size.w - num[2]):
                for v in range(objc.ctrlpts_size.v):
                    for u in range(objc.ctrlpts_size.u):
                        ctrlpts_new.append(ctrlpts_tmp[w][u + (v * objc.ctrlpts_size.u)])

            # Compute new knot vector
            kv_w = helpers.knot_removal_kv(objc.knotvector.w, span_w, num[2])

            # Update the volume after knot removal
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, objc.ctrlpts_size.v, objc.ctrlpts_size.w - num[2])
            objc.knotvector.w = kv_w

    # Return updated geometry
    return objc


def refine_knot(obj, param, **kwargs):
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
        if not isinstance(param, GeomdlTypeSequence):
            raise GeomdlError("Parametric dimensions argument (param) must be a list or a tuple")

        if len(param) != obj.pdimension:
            raise GeomdlError("The length of the param array must be equal to the number of parametric dimensions",
                              data=dict(pdim=obj.pdimension, param_len=len(param)))

    # Create a copy of the geometry object
    objc = copy.deepcopy(obj)

    # Start curve knot refinement
    if objc.pdimension == 1:
        if param[0] > 0:
            cpts = objc.ctrlptsw
            new_cpts, new_kv = helpers.knot_refinement(objc.degree.u, objc.knotvector.u, cpts, density=param[0])

            # Update the curve
            objc.set_ctrlpts(new_cpts)
            objc.knotvector.u = new_kv

    # Start surface knot refinement
    if objc.pdimension == 2:
        # u-direction
        if param[0] > 0:
            # Get curves
            new_cpts = []
            new_cpts_size = 0
            new_kv = []
            cpts = objc.ctrlptsw
            for v in range(objc.ctrlpts_size.v):
                ccu = [cpts[u, v] for u in range(objc.ctrlpts_size.u)]
                ptmp, new_kv = helpers.knot_refinement(objc.degree.u, objc.knotvector.u, ccu, density=param[0])
                new_cpts_size = len(ptmp)
                new_cpts += ptmp

            # Update the surface
            objc.set_ctrlpts(new_cpts, new_cpts_size, objc.ctrlpts_size.v)
            objc.knotvector.u = new_kv

        # v-direction
        if param[1] > 0:
            # Get curves
            new_cpts = []
            new_cpts_size = 0
            new_kv = []
            cpts = objc.ctrlptsw
            for u in range(objc.ctrlpts_size.u):
                ccv = [cpts[u, v] for v in range(objc.ctrlpts_size.v)]
                ptmp, new_kv = helpers.knot_refinement(objc.degree.v, objc.knotvector.v, ccv, density=param[1])
                new_cpts_size = len(ptmp)
                new_cpts += ptmp

            # Update control points
            ctrlpts_new = []
            for v in range(new_cpts_size):
                for u in range(objc.ctrlpts_size.u):
                    ctrlpts_new.append(new_cpts[v + (u * new_cpts_size)])

            # Update the surface
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, new_cpts_size)
            objc.knotvector.v = new_kv

    # Start volume knot refinement
    if objc.pdimension == 3:
        # u-direction
        if param[0] > 0:
            # Use Pw
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(objc.ctrlpts_size.u):
                temp_surf = []
                for v in range(objc.ctrlpts_size.v):
                    for w in range(objc.ctrlpts_size.w):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(objc.degree.u, objc.knotvector.u, cpt2d, density=param[0])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(objc.ctrlpts_size.w):
                for v in range(objc.ctrlpts_size.v):
                    for u in range(new_cpts_size):
                        ctrlpts_new.append(ctrlpts_tmp[u][w + (v * objc.ctrlpts_size.w)])

            # Update the volume
            objc.set_ctrlpts(ctrlpts_new, new_cpts_size, objc.ctrlpts_size.v, objc.ctrlpts_size.w)
            objc.knotvector.u = kv_new

        # v-direction
        if param[1] > 0:
            # Use Pw if rational
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(objc.ctrlpts_size.v):
                temp_surf = []
                for u in range(objc.ctrlpts_size.u):
                    for w in range(objc.ctrlpts_size.w):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(objc.degree.v, objc.knotvector.v, cpt2d, density=param[1])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(objc.ctrlpts_size.w):
                for v in range(new_cpts_size):
                    for u in range(objc.ctrlpts_size.u):
                        ctrlpts_new.append(ctrlpts_tmp[v][w + (u * objc.ctrlpts_size.w)])

            # Update the volume
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, new_cpts_size, objc.ctrlpts_size.w)
            objc.knotvector.v = kv_new

        # w-direction
        if param[2] > 0:
            # Use Pw if rational
            cpts = objc.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(objc.ctrlpts_size.w):
                temp_surf = []
                for v in range(objc.ctrlpts_size.v):
                    for u in range(objc.ctrlpts_size.u):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(objc.degree.w, objc.knotvector.w, cpt2d, density=param[2])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(new_cpts_size):
                for v in range(objc.ctrlpts_size.v):
                    for u in range(objc.ctrlpts_size.u):
                        ctrlpts_new.append(ctrlpts_tmp[w][u + (v * objc.ctrlpts_size.u)])

            # Update the volume
            objc.set_ctrlpts(ctrlpts_new, objc.ctrlpts_size.u, objc.ctrlpts_size.v, new_cpts_size)
            objc.knotvector.w = kv_new

    # Return updated geometry
    return objc
