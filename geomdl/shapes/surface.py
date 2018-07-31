"""
.. module:: surface
    :platform: Unix, Windows
    :synopsis: Provides common surface shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from geomdl import NURBS


def cylinder(radius=1, height=1):
    """ Generates a NURBS cylindrical surface.

    The cylindrical surface example is kindly contributed by John-Eric Dufour.

    :param radius: radius of the cylinder
    :type radius: int, float
    :param height: height of the cylinder
    :type height: int, float
    :return: a NURBS surface
    :rtype: NURBS.Surface
    """
    if radius <= 0 or height <= 0:
        raise ValueError("Radius and/or height cannot be less than and equal to zero")

    # Control points for a base cylinder
    control_points = [[[1.0, 0.0, 0.0, 1.0], [0.7071, 0.7071, 0.0, 0.7071], [0.0, 1.0, 0.0, 1.0],
                       [-0.7071, 0.7071, 0.0, 0.7071], [-1.0, 0.0, 0.0, 1.0], [-0.7071, -0.7071, 0.0, 0.7071],
                       [0.0, -1.0, 0.0, 1.0], [0.7071, -0.7071, 0.0, 0.7071], [1.0, 0.0, 0.0, 1.0]],
                      [[1.0, 0.0, 1.0, 1.0], [0.7071, 0.7071, 0.7071, 0.7071], [0.0, 1.0, 1.0, 1.0],
                       [-0.7071, 0.7071, 0.7071, 0.7071], [-1.0, 0.0, 1.0, 1.0], [-0.7071, -0.7071, 0.7071, 0.7071],
                       [0.0, -1.0, 1.0, 1.0], [0.7071, -0.7071, 0.7071, 0.7071], [1.0, 0.0, 1.0, 1.0]]]

    # Set height
    if height != 1:
        ctrlpts_top = []
        for point in control_points[1]:
            npt = point
            npt[2] = npt[2] * height
            ctrlpts_top.append(npt)
        control_points[1] = ctrlpts_top

    # Set radius
    ctrlpts = []
    if radius != 1:
        for row in control_points:
            temp = []
            for point in row:
                npt = [i * radius for i in point[0:2]]
                npt.append(point[2])
                npt.append(point[3])
                temp.append(npt)
            ctrlpts.append(temp)
    else:
        ctrlpts = control_points

    # Generate the surface
    surface = NURBS.Surface()
    surface.degree_u = 1
    surface.degree_v = 2
    surface.ctrlpts2d = ctrlpts
    surface.knotvector_u = [0.0, 0.0, 1.0, 1.0]
    surface.knotvector_v = [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 1.0]

    # Return the generated surface
    return surface
