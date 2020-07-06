"""
.. module:: geomutils.dimension
    :platform: Unix, Windows
    :synopsis: Provides dimensional change functionality

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import abstract
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
    array_init = kwargs.get('array_init', [[] for _ in range(len(obj.ctrlpts))])
    offset_value = kwargs.get('offset', 0.0)

    # Update control points
    new_ctrlpts = array_init
    for idx, point in enumerate(obj.ctrlpts):
        temp = [float(p) for p in point[0:obj.dimension]]
        temp.append(offset_value)
        new_ctrlpts[idx] = temp

    if inplace:
        obj.ctrlpts = new_ctrlpts
        return obj
    else:
        ret = copy.deepcopy(obj)
        ret.ctrlpts = new_ctrlpts
        return ret
