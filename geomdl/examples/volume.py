"""
.. module:: examples.volume
    :platform: Unix, Windows
    :synopsis: Volume examples

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import math
from .. import BSpline, NURBS, knotvector
from ..fitting import approximate_global
from ..geomutils import construct
from ..ptmanager import CPManager
from .surfgen import Grid


def scordelis_lo(radius=25, thickness=0.25, length=50, angle=40, **kwargs):
    """ Generates a Scordelis-Lo Roof.

    The Scordelis-Lo roof is a classical test case for linear static analysis. Please refer to the
    following articles for details:

    * https://doi.org/10.14359/7796
    * https://doi.org/10.1016/0045-7825(85)90035-0
    * https://doi.org/10.1016/j.cma.2010.03.029

    Keyword Arguments:
        * ``jump_angle``: iteration step for `angle` value. *Default: 2*
        * ``jump_length``: iteration step for `length` value. *Default: 2*
        * ``degree_u``: degree of the volume (u-dir). *Default: 2*
        * ``degree_v``: degree of the volume (v-dir). *Default: 2*
        * ``size_u``: number of control points (u-dir). *Default: degree_u + 2*
        * ``size_v``: number of control points (v-dir). *Default: degree_v + 2*

    :param radius: radius (R)
    :type radius: int, float
    :param thickness: thickness (t)
    :type thickness: int, float
    :param length: length (L)
    :type length: int, float
    :param angle: angle in degrees (Theta)
    :type angle: int, float
    :return: Scordelis-Lo Roof as a shell/volume
    :rtype: BSpline.Volume
    """
    # Iteration parameters
    jump_angle = kwargs.get('jump_angle', 2)
    jump_length = kwargs.get('jump_length', 2)

    # Spline parameters
    degree_u = kwargs.get('degree_u', 2)
    degree_v = kwargs.get('degree_v', 2)
    size_u = kwargs.get('size_u', degree_u + 2)
    size_v = kwargs.get('size_v', degree_v + 2)

    # Generate data points
    points_bottom = []  # data points for the bottom surface
    points_top = []  # data points for the top surface
    size_u = 0
    size_v = 0
    for l in range(0, length, jump_length):  # y-direction
        size_u = 0
        for a in range(0, angle, jump_angle):  # x-z plane
            arad = math.radians(a)
            pt_bottom = [radius * math.sin(arad), l, radius * math.cos(arad)]
            points_bottom.append(pt_bottom)
            pt_top = [(radius + thickness) * math.sin(arad), l, (radius + thickness) * math.cos(arad)]
            points_top.append(pt_top)
            size_u += 1
        size_v += 1

    # Approximate bottom surface
    surf_bottom = approximate_global.approximate_surface(points_bottom, size_u, size_v, degree_u, degree_v, ctrlpts_size_u=degree_u + 2, ctrlpts_size_v=degree_v + 2)

    # Approximate top surface
    surf_top = approximate_global.approximate_surface(points_top, size_u, size_v, degree_u, degree_v, ctrlpts_size_u=degree_u + 2, ctrlpts_size_v=degree_v + 2)

    # Generate Scordelis-Lo Roof as a spline volume
    slroof = construct.construct_volume("w", surf_bottom, surf_top)

    # Return the generated volume
    return slroof


def volume_ex1():
    """ Creates an example NURBS volume

    degree_u=3, degree_v=2, degree_w=1, size_u=6, size_v=5, size_w=2

    return: volume
    rtype: NURBS.Volume
    """
    # Create control points manager
    cpman = CPManager(6, 5, 2)
    cpman.points = [
        [25.0, -25.0, 0.0, 1.0], [15.0, -25.0, 0.0, 1.0], [5.0, -25.0, 0.0, 1.0], [-5.0, -25.0, 0.0, 1.0], [-15.0, -25.0, 0.0, 1.0], [-25.0, -25.0, 0.0, 1.0],
        [25.0, -15.0, 0.0, 1.0], [15.0, -15.0, 0.0, 1.0], [5.0, -15.0, 0.0, 1.0], [-5.0, -15.0, 0.0, 1.0], [-15.0, -15.0, 0.0, 1.0], [-25.0, -15.0, 0.0, 1.0],
        [25.0, -5.0, 0.0, 1.0], [15.0, -5.0, 0.0, 1.0], [5.0, -5.0, 0.0, 1.0], [-5.0, -5.0, 0.0, 1.0], [-15.0, -5.0, 0.0, 1.0], [-25.0, -5.0, 0.0, 1.0],
        [25.0, 5.0, 0.0, 1.0], [15.0, 5.0, 0.0, 1.0], [5.0, 5.0, 0.0, 1.0], [-5.0, 5.0, 0.0, 1.0], [-15.0, 5.0, 0.0, 1.0], [-25.0, 5.0, 0.0, 1.0],
        [25.0, 15.0, 0.0, 1.0], [15.0, 15.0, 0.0, 1.0], [5.0, 15.0, 0.0, 1.0], [-5.0, 15.0, 0.0, 1.0], [-15.0, 15.0, 0.0, 1.0], [-25.0, 15.0, 0.0, 1.0],
        [25.0, -25.0, 10.0, 1.0], [15.0, -25.0, 10.0, 1.0], [5.0, -25.0, 10.0, 1.0], [-5.0, -25.0, 10.0, 1.0], [-15.0, -25.0, 10.0, 1.0], [-25.0,-25.0, 10.0, 1.0],
        [25.0, -15.0, 10.0, 1.0], [15.0, -15.0, 10.0, 1.0], [5.0, -15.0, 10.0, 1.0], [-5.0, -15.0, 10.0, 1.0], [-15.0, -15.0, 10.0, 1.0], [-25.0, -15.0, 10.0, 1.0],
        [25.0, -5.0, 10.0, 1.0], [15.0, -5.0, 10.0, 1.0], [5.0, -5.0, 10.0, 1.0], [-5.0, -5.0, 10.0, 1.0], [-15.0, -5.0, 10.0, 1.0], [-25.0, -5.0, 10.0, 1.0],
        [25.0, 5.0, 10.0, 1.0], [15.0, 5.0, 10.0, 1.0], [5.0, 5.0, 10.0, 1.0], [-5.0, 5.0, 10.0, 1.0], [-15.0, 5.0, 10.0, 1.0], [-25.0, 5.0, 10.0, 1.0],
        [25.0, 15.0, 10.0, 1.0], [15.0, 15.0, 10.0, 1.0], [5.0, 15.0, 10.0, 1.0], [-5.0, 15.0, 10.0, 1.0], [-15.0, 15.0, 10.0, 1.0], [-25.0, 15.0, 10.0, 1.0]
    ]

    # Create NURBS volume
    vol = NURBS.Volume()
    vol.degree = [3, 2, 1]
    vol.knotvector = [
        [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0],
        [0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0],
        [0.0, 0.0, 1.0, 1.0]
    ]
    vol.ctrlptsw = cpman

    # Return the volume
    return vol

def volume_ex2():
    """ Creates an example NURBS volume using surface generator

    degree_u=1, degree_v=1, degree_w=1, size_u=8, size_v=8, size_w=3

    return: volume
    rtype: NURBS.Volume
    """
    # Generate control points grid for Surface #1
    sg01 = Grid(15, 10, z_value=0.0)
    sg01.generate(8, 8)

    # Create a BSpline surface instance
    surf01 = BSpline.Surface()

    # Set degrees
    surf01.degree.u = 1
    surf01.degree.v = 1

    # Get the control points from the generated grid
    surf01.set_ctrlpts(sg01.grid, 8, 8)

    # Set knot vectors
    surf01.knotvector.u = knotvector.generate(surf01.degree.u, surf01.ctrlpts_size.u)
    surf01.knotvector.v = knotvector.generate(surf01.degree.v, surf01.ctrlpts_size.v)

    # Generate control points grid for Surface #2
    sg02 = Grid(15, 10, z_value=1.0)
    sg02.generate(8, 8)

    # Create a BSpline surface instance
    surf02 = BSpline.Surface()

    # Set degrees
    surf02.degree.u = 1
    surf02.degree.v = 1

    # Get the control points from the generated grid
    surf02.set_ctrlpts(sg02.grid, 8, 8)

    # Set knot vectors
    surf02.knotvector.u = knotvector.generate(surf02.degree.u, surf02.ctrlpts_size.u)
    surf02.knotvector.v = knotvector.generate(surf02.degree.v, surf02.ctrlpts_size.v)

    # Generate control points grid for Surface #3
    sg03 = Grid(15, 10, z_value=2.0)
    sg03.generate(8, 8)

    # Create a BSpline surface instance
    surf03 = BSpline.Surface()

    # Set degrees
    surf03.degree.u = 1
    surf03.degree.v = 1

    # Get the control points from the generated grid
    surf03.set_ctrlpts(sg03.grid, 8, 8)

    # Set knot vectors
    surf03.knotvector.u = knotvector.generate(surf03.degree.u, surf03.ctrlpts_size.u)
    surf03.knotvector.v = knotvector.generate(surf03.degree.v, surf03.ctrlpts_size.v)

    # Construct the volume
    pvolume = construct.construct_volume('w', surf01, surf02, surf03, degree=1)

    return pvolume
