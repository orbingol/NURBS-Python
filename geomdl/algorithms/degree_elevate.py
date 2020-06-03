"""
.. module:: algorithms.derivative
    :platform: Unix, Windows
    :synopsis: Degree elevation algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import helpers
from .. import control_points
from ..base import GeomdlError, GeomdlTypeSequence
from .decompose import decompose_curve
from .link import link_curves

__all__ = []


def elevate_degree(obj, param, **kwargs):
    """ Applies degree elevation algorithms to B-spline geometries.

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param param: operation definition
    :type param: list, tuple
    :return: updated spline geometry
    """
    # Start curve degree manipulation operations
    if obj.pdimension == 1:
        if param[0] is not None and param[0] > 0:
            # Find multiplicity of the internal knots
            int_knots = set(obj.knotvector[obj.degree.u + 1:-(obj.degree.u + 1)])
            mult_arr = []
            for ik in int_knots:
                s = helpers.find_multiplicity(ik, obj.knotvector.u)
                mult_arr.append(s)

            # Decompose the input by knot insertion
            crv_list = decompose_curve(obj, **kwargs)

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

            # Link curves together (reverse of decomposition)
            kv, cpts, ws, knots = link_curves(*crv_list, validate=False)

            # Organize control points (if necessary)
            ctrlpts = control_points.combine_ctrlpts_weights(cpts, ws) if obj.rational else cpts

            # Apply knot removal
            for k, s in zip(knots, mult_arr):
                span = helpers.find_span_linear(nd, kv, len(ctrlpts), k)
                ctrlpts = helpers.knot_removal(nd, kv, ctrlpts, k, num=num-s)
                kv = helpers.knot_removal_kv(kv, span, num-s)

            # Update input curve
            obj.degree.u = nd
            obj.set_ctrlpts(ctrlpts)
            obj.knotvector.u = kv

    # Start surface degree manipulation operations
    if obj.pdimension == 2:
        # u-direction
        if param[0] is not None and param[0] > 0:
            pass

        # v-direction
        if param[1] is not None and param[1] > 0:
            pass

    # Start surface degree manipulation operations
    if obj.pdimension == 3:
        raise GeomdlError("Degree elevation has not been implemented for B-spline volumes")

    # Return updated geometry
    return obj
