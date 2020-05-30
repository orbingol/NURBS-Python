"""
.. module:: algorithms.derivative
    :platform: Unix, Windows
    :synopsis: Degree modification algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import helpers
from ..base import GeomdlError, GeomdlTypeSequence
from .decompose import decompose_curve
from .link import link_curves

__all__ = []


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
            kv, cpts, ws, knots = link_curves(*crv_list, validate=False)

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
