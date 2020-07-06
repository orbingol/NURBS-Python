"""
.. module:: algorithms.derivative
    :platform: Unix, Windows
    :synopsis: Degree elevation algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import helpers
from .. import ptmanager
from ..base import GeomdlError
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
    # Create a copy of the geometry object
    objc = copy.deepcopy(obj)

    # Start curve degree manipulation operations
    if objc.pdimension == 1:
        if param[0] is not None and param[0] > 0:
            # Find multiplicity of the internal knots
            int_knots = set(objc.knotvector.u[objc.degree.u + 1:-(objc.degree.u + 1)])
            mult_arr = []
            for ik in int_knots:
                s = helpers.find_multiplicity(ik, objc.knotvector.u)
                mult_arr.append(s)

            # Decompose the input by knot insertion
            crv_list = decompose_curve(obj, **kwargs)

            # Loop through to apply degree elevation
            for crv in crv_list:
                cpts = crv.ctrlptsw.points
                new_cpts = helpers.degree_elevation(crv.degree.u, cpts, num=param[0])
                crv.degree.u += param[0]
                crv.set_ctrlpts(new_cpts)
                crv.knotvector.u = [crv.knotvector.u[0] for _ in range(param[0])] + list(crv.knotvector.u) + [crv.knotvector.u[-1] for _ in range(param[0])]

            # Compute new degree
            nd = objc.degree.u + param[0]

            # Number of knot removals
            num = objc.degree.u + 1

            # Link curves together (reverse of decomposition)
            kv, cpts, knots = link_curves(*crv_list, validate=False)

            # Apply knot removal
            for k, s in zip(knots, mult_arr):
                span = helpers.find_span_linear(nd, kv, len(cpts), k)
                cpts = helpers.knot_removal(nd, kv, cpts, k, num=num-s)
                kv = helpers.knot_removal_kv(kv, span, num-s)

            # Update input curve
            objc.degree.u = nd
            objc.set_ctrlpts(cpts)
            objc.knotvector.u = kv

    # Start surface degree manipulation operations
    if objc.pdimension == 2:
        # u-direction
        if param[0] is not None and param[0] > 0:
            pass

        # v-direction
        if param[1] is not None and param[1] > 0:
            pass

    # Start surface degree manipulation operations
    if objc.pdimension == 3:
        raise GeomdlError("Degree elevation has not been implemented for B-spline volumes")

    # Return updated geometry
    return objc


def reduce_degree(obj, param, **kwargs):
    """ Applies degree reduction algorithms to B-spline geometries.

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param param: operation definition
    :type param: list, tuple
    :return: updated spline geometry
    """
    def validate_reduction(degree):
        if degree < 2:
            raise GeomdlError("Input geometry must have degree > 1")

    # Create a copy of the geometry object
    objc = copy.deepcopy(obj)

    # Start curve degree manipulation operations
    if objc.pdimension == 1:
        if param[0] is not None and param[0] > 0:
            # Find multiplicity of the internal knots
            int_knots = set(objc.knotvector.u[objc.degree.u + 1:-(objc.degree.u + 1)])
            mult_arr = []
            for ik in int_knots:
                s = helpers.find_multiplicity(ik, objc.knotvector.u)
                mult_arr.append(s)

            # Decompose the input by knot insertion
            crv_list = decompose_curve(obj, **kwargs)

            # Validate degree reduction operation
            validate_reduction(objc.degree.u)

            # Loop through to apply degree reduction
            for crv in crv_list:
                cpts = crv.ctrlptsw.points
                new_cpts = helpers.degree_reduction(crv.degree.u, cpts)
                crv.degree.u -= 1
                crv.set_ctrlpts(new_cpts)
                crv.knotvector.u = list(crv.knotvector.u[1:-1])

            # Compute new degree
            nd = objc.degree.u - 1

            # Number of knot removals
            num = objc.degree.u - 1

            # Link curves together (inverse of decomposition)
            kv, cpts, knots = link_curves(*crv_list, validate=False)

            # Apply knot removal
            for k, s in zip(knots, mult_arr):
                span = helpers.find_span_linear(nd, kv, len(cpts), k)
                cpts = helpers.knot_removal(nd, kv, cpts, k, num=num-s)
                kv = helpers.knot_removal_kv(kv, span, num-s)

            # Update input curve
            objc.degree.u = nd
            objc.set_ctrlpts(cpts)
            objc.knotvector.u = kv

    # Start surface degree manipulation operations
    if objc.pdimension == 2:
        # u-direction
        if param[0] is not None and param[0] > 0:
            # Apply degree reduction operation
            validate_reduction(objc.degree.u)

        # v-direction
        if param[1] is not None and param[1] > 0:
            # Validate degree reduction operation
            validate_reduction(objc.degree.v)

    # Start surface degree manipulation operations
    if objc.pdimension == 3:
        raise GeomdlError("Degree elevation has not been implemented for B-spline volumes")

    # Return updated geometry
    return objc
