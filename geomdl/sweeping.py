"""
.. module:: sweeping
    :platform: Unix, Windows
    :synopsis: Provides functions for generating swept geometries

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from copy import deepcopy
from . import linalg
from . import construct
from .exceptions import GeomdlException
from ._utilities import export


@export
def sweep_vector(obj, vec, **kwargs):
    """ Sweeps spline geometries along a vector.

    This API call generates

    * swept surfaces from curves
    * swept volumes from surfaces

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param vec: vector to sweep along
    :type vec: list, tuple
    :return: swept geometry
    """
    if not 0 < obj.pdimension < 3:
        raise GeomdlException("Can only sweep curves and surfaces with curves and surface")

    # Translate control points
    swept_cps = [[] for _ in range(obj.ctrlpts_size)]
    for i, p in enumerate(obj.ctrlpts):
        swept_cps[i] = linalg.point_translate(p, vec)

    # Generate copy of the input geometry
    obj_swept = deepcopy(obj)

    # Update control points of the copy
    obj_swept.ctrlpts = swept_cps

    # Generate the resulting surface or volume
    if obj.pdimension == 1:
        return construct.construct_surface("u", obj, obj_swept)
    return construct.construct_volume("w", obj, obj_swept)
