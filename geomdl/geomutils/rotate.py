"""
.. module:: geomutils.rotate
    :platform: Unix, Windows
    :synopsis: Provides rotation functionality

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
import math
from .. import linalg
from ..ptmanager import CPManager
from ..base import export, GeomdlError
from . import translate


def rotate_x(ncs, opt, alpha):
    # Generate translation vector
    translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

    # Translate to the origin
    translate.translate(ncs, translate_vector, inplace=True)

    # Then, rotate about the axis
    rot = math.radians(alpha)
    new_ctrlpts = [[0.0 for _ in range(ncs.dimension)] for _ in range(ncs.ctrlpts.count)]
    for idx, pt in enumerate(ncs.ctrlpts):
        new_ctrlpts[idx][0] = pt[0]
        new_ctrlpts[idx][1] = (pt[1] * math.cos(rot)) - (pt[2] * math.sin(rot))
        new_ctrlpts[idx][2] = (pt[2] * math.cos(rot)) + (pt[1] * math.sin(rot))
    ncs.ctrlpts.points = new_ctrlpts

    # Finally, translate back to the starting location
    translate.translate(ncs, [-tv for tv in translate_vector], inplace=True)

def rotate_y(ncs, opt, alpha):
    # Generate translation vector
    translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

    # Translate to the origin
    translate.translate(ncs, translate_vector, inplace=True)

    # Then, rotate about the axis
    rot = math.radians(alpha)
    new_ctrlpts = [[0.0 for _ in range(ncs.dimension)] for _ in range(ncs.ctrlpts.count)]
    for idx, pt in enumerate(ncs.ctrlpts):
        new_ctrlpts[idx][0] = (pt[0] * math.cos(rot)) - (pt[2] * math.sin(rot))
        new_ctrlpts[idx][1] = pt[1]
        new_ctrlpts[idx][2] = (pt[2] * math.cos(rot)) + (pt[0] * math.sin(rot))
    ncs.ctrlpts.points = new_ctrlpts

    # Finally, translate back to the starting location
    translate.translate(ncs, [-tv for tv in translate_vector], inplace=True)

def rotate_z(ncs, opt, alpha):
    # Generate translation vector
    translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

    # Translate to the origin
    translate.translate(ncs, translate_vector, inplace=True)

    # Then, rotate about the axis
    rot = math.radians(alpha)
    new_ctrlpts = [list(ncs.ctrlpts.points[i]) for i in range(ncs.ctrlpts.count)]
    for idx, pt in enumerate(ncs.ctrlpts):
        new_ctrlpts[idx][0] = (pt[0] * math.cos(rot)) - (pt[1] * math.sin(rot))
        new_ctrlpts[idx][1] = (pt[1] * math.cos(rot)) + (pt[0] * math.sin(rot))
    ncs.ctrlpts.points = new_ctrlpts

    # Finally, translate back to the starting location
    translate.translate(ncs, [-tv for tv in translate_vector], inplace=True)


@export
def rotate(obj, angle, **kwargs):
    """ Rotates curves, surfaces or volumes about the chosen axis.

    Keyword Arguments:
        * ``axis``: rotation axis; x, y, z correspond to 0, 1, 2 respectively. *Default: 2*
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param obj: input geometry
    :type obj: abstract.SplineGeometry, multi.AbstractGeometry
    :param angle: angle of rotation (in degrees)
    :type angle: float
    :return: rotated geometry object
    """
    # Set rotation axis
    axis = 2 if obj.dimension == 2 else int(kwargs.get('axis', 2))
    if not 0 <= axis <= 2:
        raise GeomdlError("Value of the 'axis' argument should be 0, 1 or 2")
    rotfunc = (rotate_x, rotate_y, rotate_z)

    # Operate on a copy or the actual object
    inplace = kwargs.get('inplace', False)
    if not inplace:
        geom = copy.deepcopy(obj)
    else:
        geom = obj

    # Set a single origin
    if geom[0].pdimension == 1:
        params = geom[0].domain[0]
    else:
        params = [geom[0].domain[i][0] for i in range(geom[0].pdimension)]
    origin = geom[0].evaluate_single(params)

    # Start rotation
    for g in geom:
        rotfunc[axis](g, origin, angle)

    return geom
