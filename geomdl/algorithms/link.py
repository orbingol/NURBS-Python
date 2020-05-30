"""
.. module:: algorithms.link
    :platform: Unix, Windows
    :synopsis: Linking algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import linalg, helpers
from ..base import GeomdlError

__all__ = []


def link_curves(*args, **kwargs):
    """ Links the input curves together.

    The end control point of the curve k has to be the same with the start control point of the curve k + 1.

    Keyword Arguments:
        * ``tol``: tolerance value for checking equality. *Default: 10e-8*
        * ``validate``: flag to enable input validation. *Default: False*

    :return: a tuple containing knot vector, control points, weights vector and knots
    """
    # Get keyword arguments
    tol = kwargs.get('tol', 10e-8)
    validate = kwargs.get('validate', False)

    # Validate input
    if validate:
        for idx in range(len(args) - 1):
            if linalg.point_distance(args[idx].ctrlpts[-1], args[idx + 1].ctrlpts[0]) > tol:
                raise GeomdlError("Curve #" + str(idx) + " and Curve #" + str(idx + 1) + " don't touch each other")

    kv = []  # new knot vector
    cpts = []  # new control points array
    wgts = []  # new weights array
    kv_connected = []  # superfluous knots to be removed
    pdomain_end = 0

    # Loop though the curves
    for arg in args:
        # Process knot vectors
        if not kv:
            kv += list(arg.knotvector[:-(arg.degree + 1)])  # get rid of the last superfluous knot to maintain split curve notation
            cpts += list(arg.ctrlpts)
            # Process control points
            if arg.rational:
                wgts += list(arg.weights)
            else:
                tmp_w = [1.0 for _ in range(arg.ctrlpts_size)]
                wgts += tmp_w
        else:
            tmp_kv = [pdomain_end + k for k in arg.knotvector[1:-(arg.degree + 1)]]
            kv += tmp_kv
            cpts += list(arg.ctrlpts[1:])
            # Process control points
            if arg.rational:
                wgts += list(arg.weights[1:])
            else:
                tmp_w = [1.0 for _ in range(arg.ctrlpts_size - 1)]
                wgts += tmp_w

        pdomain_end += arg.knotvector[-1]
        kv_connected.append(pdomain_end)

    # Fix curve by appending the last knot to the end
    kv += [pdomain_end for _ in range(arg.degree + 1)]
    # Remove the last knot from knot insertion list
    kv_connected.pop()

    return kv, cpts, wgts, kv_connected
