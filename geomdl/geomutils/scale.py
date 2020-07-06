"""
.. module:: geomutils.scale
    :platform: Unix, Windows
    :synopsis: Provides scaling functionality

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from ..base import export, GeomdlError


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
        raise GeomdlError("The multiplier must be a float or an integer")

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
