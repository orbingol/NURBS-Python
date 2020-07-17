"""
.. module:: geomutils.dimension
    :platform: Unix, Windows
    :synopsis: Provides dimensional change functionality

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import abstract
from ..ptmanager import CPManager
from ..base import export, GeomdlError


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
        raise GeomdlError("Can only operate on spline geometry objects")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)
    offset_value = kwargs.get('offset', 0.0)

    # Update control points
    new_ctrlpts = [[] for _ in range(obj.ctrlpts.count)]
    for idx, point in enumerate(obj.ctrlpts):
        temp = [float(p) for p in point[0:obj.dimension]]
        temp.append(offset_value)
        new_ctrlpts[idx] = temp

    if inplace:
        obj.ctrlpts.points = new_ctrlpts
        return obj
    else:
        ret = copy.deepcopy(obj)
        ret.ctrlpts.points = new_ctrlpts
        return ret
