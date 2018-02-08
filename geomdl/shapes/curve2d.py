"""
.. module:: curve2d
    :platform: Unix, Windows
    :synopsis: Provides commonly used 2D curve shapes generated via NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from geomdl import NURBS


# Generates a NURBS circle from 9 control points
def full_circle(radius=1):
    """ Generates a NURBS full circle from 9 control points.

    :param radius: radius of the circle
    :type radius: int, float
    :return: a NURBS curve
    :rtype: NURBS.Curve2D
    """
    if radius <= 0:
        raise ValueError("Curve radius cannot be less than and equal to zero")

    # Control points for a unit circle
    control_points = [[0.0, -1.0, 1.0], [-0.707, -0.707, 0.707], [-1.0, 0.0, 1.0],
                      [-0.707, 0.707, 0.707], [0.0, 1.0, 1.0], [0.707, 0.707, 0.707],
                      [1.0, 0.0, 1.0], [0.707, -0.707, 0.707], [0.0, -1.0, 1.0]]

    # Set radius
    ctrlpts = []
    if radius != 1:
        for point in control_points:
            npt = [i * radius for i in point[0:2]]
            npt.append(point[-1])
            ctrlpts.append(npt)
    else:
        ctrlpts = control_points

    # Generate the curve
    curve = NURBS.Curve2D()
    curve.degree = 2
    curve.ctrlpts = ctrlpts
    curve.knotvector = [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]

    # Return the generated curve
    return curve


# Generates a NURBS circle from 7 control points
def full_circle2(radius=1):
    """ Generates a NURBS full circle from 7 control points.

    :param radius: radius of the circle
    :type radius: int, float
    :return: a NURBS curve
    :rtype: NURBS.Curve2D
    """
    if radius <= 0:
        raise ValueError("Curve radius cannot be less than and equal to zero")

    # Control points for a unit circle
    control_points = [[1.0, 0.5, 1.0], [0.0, 1.0, 0.5], [-1.0, 0.5, 1.0],
                      [-1.0, -0.5, 0.5], [0.0, -1.0, 1.0], [1.0, -0.5, 0.5],
                      [1.0, 0.5, 1.0]]

    # Set radius
    ctrlpts = []
    if radius != 1:
        for point in control_points:
            npt = [i * radius for i in point[0:2]]
            npt.append(point[-1])
            ctrlpts.append(npt)
    else:
        ctrlpts = control_points

    # Generate the curve
    curve = NURBS.Curve2D()
    curve.degree = 2
    curve.ctrlpts = ctrlpts
    curve.knotvector = [0, 0, 0, 0.33, 0.33, 0.66, 0.66, 1, 1, 1]

    # Return the generated curve
    return curve
