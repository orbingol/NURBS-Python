"""
.. module:: examples.surface
    :platform: Unix, Windows
    :synopsis: Surface examples

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import base
from .. import BSpline, NURBS
from ..ptmanager import CPManager


def cylinder(radius=1.0, height=1.0):
    """ Generates a cylindrical NURBS surface.

    :param radius: radius of the cylinder
    :type radius: int, float
    :param height: height of the cylinder
    :type height: int, float
    :return: a NURBS surface
    :rtype: NURBS.Surface
    """
    if radius <= 0 or height <= 0:
        raise base.GeomdlError("Radius and/or height cannot be less than and equal to zero")

    # Control points for a unit cylinder
    ctrlpts = [
        [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [-1.0, 0.0, 0.0],
        [-1.0, -1.0, 0.0], [0.0, -1.0, 0.0], [1.0, -1.0, 0.0], [1.0, 0.0, 0.0],
        [1.0, 0.0, height], [1.0, 1.0, height], [0.0, 1.0, height], [-1.0, 1.0, height], [-1.0, 0.0, height],
        [-1.0, -1.0, height], [0.0, -1.0, height], [1.0, -1.0, height], [1.0, 0.0, height]
    ]
    weights = [1.0, 0.7071, 1.0, 0.7071, 1.0, 0.7071, 1.0, 0.7071, 1.0, 1.0, 0.7071, 1.0, 0.7071, 1.0, 0.7071, 1.0, 0.7071, 1.0]

    # Set radius
    cpman = CPManager(9, 2)
    for i, cpt in enumerate(ctrlpts):
        cpman[i] = [p * radius for p in cpt]

    # Generate the surface
    surface = NURBS.Surface()
    surface.name = "cylindrical surface"
    surface.degree = (2, 1)
    surface.ctrlpts = cpman
    surface.weights = weights
    surface.knotvector.u = [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 1.0]
    surface.knotvector.v = [0.0, 0.0, 1.0, 1.0]

    # Return the generated surface
    return surface

def surface_ex1():
    """ Creates an example B-Spline surface

    degree_u=3, degree_v=3, size_u=6, size_v=6

    :return: surface
    :rtype: NURBS.Surface
    """
    cpts = [
        [-25,-25,-10], [-25,-15,-5] , [25,-5,0], [-25,5,0], [-25,15,-5], [-25,25,-10],
        [-15,-25,-8], [-15,-15,-4], [-15,-5,-4], [-15,5,-4], [-15,15,-4], [-15,25,-8],
        [-5,-25,-5], [-5,-15,-3], [-5,-5,-8], [-5,5,-8], [-5,15,-3], [-5,25,-5],
        [5,-25,-3], [5,-15,-2], [5,-5,-8], [5,5,-8], [5,15,-2], [5,25,-3],
        [15,-25,-8], [15,-15,-4], [15,-5,-4], [15,5,-4], [15,15,-4], [15,25,-8],
        [25,-25,-10], [25,-15,-5], [25,-5,2], [25,5,2], [25,15,-5], [25,25,-10]
    ]

    # Create a BSpline surface instance
    surf = BSpline.Surface()
    surf.degree.u = 3
    surf.degree.v = 3
    surf.knotvector.u = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    surf.knotvector.v = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    surf.set_ctrlpts(cpts, 6, 6)

    return surf


def surface_ex2():
    """ Creates an example NURBS surface

    degree_u=3, degree_v=3, size_u=6, size_v=6

    This example is contributed by Dr. Adarsh Krishnamurthy <adarsh@iastate.edu>

    :return: surface
    :rtype: NURBS.Surface
    """
    # Create control points manager
    cpman = CPManager(6, 6)
    cpman.points = [
        [25.0, -25.0, 0.0, 1.0], [15.0, -25.0, 0.0, 1.0], [5.0, -25.0, 0.0, 1.0],
        [-5.0, -25.0, 0.0, 1.0], [-15.0, -25.0, 0.0, 1.0], [-25.0, -25.0, 0.0, 1.0],
        [25.0, -15.0, 0.0, 1.0], [15.0, -15.0, 0.0, 1.0], [5.0, -15.0, 0.0, 1.0],
        [-5.0, -15.0, 0.0, 1.0], [-15.0, -15.0, 0.0, 1.0], [-25.0, -15.0, 0.0, 1.0],
        [25.0, -5.0, 5.0, 1.0], [15.0, -5.0, 5.0, 1.0], [5.0, -5.0, 5.0, 1.0],
        [-5.0, -5.0, 5.0, 1.0], [-15.0, -5.0, 5.0, 1.0], [-25.0, -5.0, 5.0, 1.0],
        [25.0, 5.0, 5.0, 1.0], [15.0, 5.0, 5.0, 1.0], [5.0, 5.0, 5.0, 1.0],
        [-5.0, 5.0, 5.0, 1.0], [-15.0, 5.0, 5.0, 1.0], [-25.0, 5.0, 5.0, 1.0],
        [25.0, 15.0, 0.0, 1.0], [15.0, 15.0, 0.0, 1.0], [5.0, 15.0, 5.0, 1.0],
        [-5.0, 15.0, 5.0, 1.0], [-15.0, 15.0, 0.0, 1.0], [-25.0, 15.0, 0.0, 1.0],
        [25.0, 25.0, 0.0, 1.0], [15.0, 25.0, 0.0, 1.0], [5.0, 25.0, 5.0, 1.0],
        [-5.0, 25.0, 5.0, 1.0], [-15.0, 25.0, 0.0, 1.0], [-25.0, 25.0, 0.0, 1.0]
    ]

    # Create NURBS surface
    surf = NURBS.Surface()
    surf.degree = [3, 3]
    surf.knotvector = [
        [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    ]
    surf.ctrlptsw = cpman

    # Return the surface
    return surf
