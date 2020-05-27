"""
.. module:: geomutils.translate
    :platform: Unix, Windows
    :synopsis: Provides translation functionality

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import linalg
from ..base import GeomdlError

__all__ = []


def apply_translation(obj, vec, **kwargs):
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
        raise GeomdlError("The input must be a list or a tuple")

    # Input validity checks
    if len(vec) != obj.dimension:
        raise GeomdlError("The input vector must have " + str(obj.dimension) + " components")

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
