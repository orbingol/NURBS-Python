"""
.. module:: examples.curve
    :platform: Unix, Windows
    :synopsis: Curve examples

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import NURBS
from ..base import GeomdlError
from ..ptmanager import CPManager


# Generates a NURBS circle from 9 control points
def full_circle(radius=1):
    """ Generates a full NURBS circle from 9 control points.

    :param radius: radius of the circle
    :type radius: int, float
    :return: a NURBS curve
    :rtype: NURBS.Curve
    """
    if radius <= 0:
        raise GeomdlError("Curve radius cannot be less than and equal to zero")

    # Control points for a unit circle
    ctrlpts = [[0.0, -1.0], [-1.0, -1.0], [-1.0, 0.0], [-1.0, 1.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [1.0, -1.0], [0.0, -1.0]]
    weights = [1.0, 0.707, 1.0, 0.707, 1.0, 0.707, 1.0, 0.707, 1.0]

    # Set radius
    cpman = CPManager(len(ctrlpts))
    for i, cpt in enumerate(ctrlpts):
        cpman[i] = [p * radius for p in cpt]

    # Generate the curve
    curve = NURBS.Curve()
    curve.name = "circle from 9 control points"
    curve.degree = 2
    curve.ctrlpts = cpman
    curve.weights = weights
    curve.knotvector = [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]

    # Return the generated curve
    return curve
