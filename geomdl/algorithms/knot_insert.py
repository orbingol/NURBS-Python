"""
.. module:: algorithms.knot_insert
    :platform: Unix, Windows
    :synopsis: Knot insertion algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

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

    # Start curve knot insertion
    if obj.pdimension == 1:
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s = helpers.find_multiplicity(param[0], obj.knotvector.u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree.u - s:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s))

            # Find knot span
            span = helpers.find_span_linear(obj.degree.u, obj.knotvector.u, obj.ctrlpts_size.u, param[0])

            # Compute new knot vector
            kv_new = helpers.knot_insertion_kv(obj.knotvector.u, param[0], span, num[0])

            # Compute new control points
            cpts = list(obj.ctrlptsw.points)
            cpts_tmp = helpers.knot_insertion(obj.degree.u, obj.knotvector.u, cpts, param[0],
                                              num=num[0], s=s, span=span)

            # Update curve
            obj.set_ctrlpts(cpts_tmp)
            obj.knotvector.u = kv_new

    # Start surface knot insertion
    if obj.pdimension == 2:
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector.u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree_u - s_u:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times (u-dir)",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree.u, obj.knotvector.u, obj.ctrlpts_size.u, param[0])

            # Compute new knot vector
            kv_u = helpers.knot_insertion_kv(obj.knotvector_u, param[0], span_u, num[0])

            # Get curves
            cpts_tmp = []
            cpts = obj.ctrlptsw.points
            for v in range(obj.ctrlpts_size.v):
                ccu = [cpts[u + (obj.ctrlpts_size.u * v)] for u in range(obj.ctrlpts_size.u)]
                ctrlpts_tmp = helpers.knot_insertion(obj.degree.u, obj.knotvector.u, ccu, param[0],
                                                     num=num[0], s=s_u, span=span_u)
                cpts_tmp += ctrlpts_tmp

            # Update the surface after knot insertion
            obj.set_ctrlpts(cpts_tmp, obj.ctrlpts_size.u + num[0], obj.ctrlpts_size.v)
            obj.knotvector.u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > obj.degree.v - s_v:
                raise GeomdlError("Knot " + str(param[1]) + " cannot be inserted " + str(num[1]) + " times (v-dir)",
                                  data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree.v, obj.knotvector.v, obj.ctrlpts_size.v, param[1])

            # Compute new knot vector
            kv_v = helpers.knot_insertion_kv(obj.knotvector.v, param[1], span_v, num[1])

            # Get curves
            cpts_tmp = []
            cpts = obj.ctrlptsw.points
            for u in range(obj.ctrlpts_size.u):
                ccv = [cpts[u + (obj.ctrlpts_size_u * v)] for v in range(obj.ctrlpts_size_v)]
                ctrlpts_tmp = helpers.knot_insertion(obj.degree.v, obj.knotvector.v, ccv, param[1],
                                                     num=num[1], s=s_v, span=span_v)
                cpts_tmp += ctrlpts_tmp

            # Update the surface after knot insertion
            ctrlpts_new = []
            for v in range(obj.ctrlpts_size.v + num[1]):
                for u in range(obj.ctrlpts_size.u):
                    ctrlpts_new.append(cpts_tmp[v + (u * obj.ctrlpts_size.v + num[1])])

            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size.u, obj.ctrlpts_size.v + num[1])
            obj.knotvector.v = kv_v

    # Start volume knot insertion
    if obj.pdimension == 3:
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector.u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree.u - s_u:
                raise GeomdlError("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times (u-dir)",
                                  data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree.u, obj.knotvector.u, obj.ctrlpts_size.u, param[0])

            # Compute new knot vector
            kv_u = helpers.knot_insertion_kv(obj.knotvector.u, param[0], span_u, num[0])

            # Use Pw if rational
            cpts = obj.ctrlptsw.points

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(obj.ctrlpts_size.u):
                temp_surf = []
                for w in range(obj.ctrlpts_size.w):
                    for v in range(obj.ctrlpts_size.v):
                        temp_pt = cpts[u + (v * obj.ctrlpts_size.u) + (w * obj.ctrlpts_size.u * obj.ctrlpts_size.v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree.u, obj.knotvector.u, cpt2d, param[0],
                                                 num=num[0], s=s_u, span=span_u)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size.w):
                for u in range(obj.ctrlpts_size.u + num[0]):
                    for v in range(obj.ctrlpts_size.v):
                        temp_pt = ctrlpts_tmp[u][v + (w * obj.ctrlpts_size.v)]
                        ctrlpts_new.append(temp_pt)

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size.u + num[0], obj.ctrlpts_size.v, obj.ctrlpts_size.w)
            obj.knotvector.u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector.v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > obj.degree.v - s_v:
                raise GeomdlError("Knot " + str(param[1]) + " cannot be inserted " + str(num[1]) + " times (v-dir)",
                                  data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree.v, obj.knotvector.v, obj.ctrlpts_size.v, param[1])

            # Compute new knot vector
            kv_v = helpers.knot_insertion_kv(obj.knotvector.v, param[1], span_v, num[1])

            # Use Pw if rational
            cpts = list(obj.ctrlptsw.points)

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(obj.ctrlpts_size.v):
                temp_surf = []
                for w in range(obj.ctrlpts_size.w):
                    for u in range(obj.ctrlpts_size.u):
                        temp_pt = cpts[u + (v * obj.ctrlpts_size.u) + (w * obj.ctrlpts_size.u * obj.ctrlpts_size.v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree.v, obj.knotvector.v, cpt2d, param[1],
                                                 num=num[1], s=s_v, span=span_v)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size.w):
                for u in range(obj.ctrlpts_size.u):
                    for v in range(obj.ctrlpts_size.v + num[1]):
                        temp_pt = ctrlpts_tmp[v][u + (w * obj.ctrlpts_size_u)]  # FIX
                        ctrlpts_new.append(temp_pt)

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size.u, obj.ctrlpts_size.v + num[1], obj.ctrlpts_size.w)
            obj.knotvector.v = kv_v

        # w-direction
        if param[2] is not None and num[2] > 0:
            # Find knot multiplicity
            s_w = helpers.find_multiplicity(param[2], obj.knotvector.w)

            # Check if it is possible add that many number of knots
            if check_num and num[2] > obj.degree.w - s_w:
                raise GeomdlError("Knot " + str(param[2]) + " cannot be inserted " + str(num[2]) + " times (w-dir)",
                                  data=dict(knot=param[2], num=num[2], multiplicity=s_w))

            # Find knot span
            span_w = helpers.find_span_linear(obj.degree.w, obj.knotvector.w, obj.ctrlpts_size.w, param[2])

            # Compute new knot vector
            kv_w = helpers.knot_insertion_kv(obj.knotvector.w, param[2], span_w, num[2])

            # Use Pw if rational
            cpts = obj.ctrlptsw.points

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(obj.ctrlpts_size.w):
                temp_surf = [cpts[uv + (w * obj.ctrlpts_size.u * obj.ctrlpts_size.v)] for uv in
                             range(obj.ctrlpts_size.u * obj.ctrlpts_size.v)]
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree.w, obj.knotvector.w, cpt2d, param[2],
                                                 num=num[2], s=s_w, span=span_w)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size.w + num[2]):
                ctrlpts_new += ctrlpts_tmp[w]

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size.u, obj.ctrlpts_size.v, obj.ctrlpts_size.w + num[2])
            obj.knotvector_w = kv_w

    # Return updated spline geometry
    return obj
