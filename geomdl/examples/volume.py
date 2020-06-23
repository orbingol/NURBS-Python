"""
.. module:: examples.volume
    :platform: Unix, Windows
    :synopsis: Volume examples

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import math
from .. import NURBS
from .. import fitting
from .. import geomutils
from ..ptmanager import CPManager


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
    surf_bottom = fitting.approximate_surface(points_bottom, size_u, size_v, degree_u, degree_v, ctrlpts_size_u=degree_u + 2, ctrlpts_size_v=degree_v + 2)

    # Approximate top surface
    surf_top = fitting.approximate_surface(points_top, size_u, size_v, degree_u, degree_v, ctrlpts_size_u=degree_u + 2, ctrlpts_size_v=degree_v + 2)

    # Generate Scordelis-Lo Roof as a spline volume
    slroof = geomutils.construct_volume("w", surf_bottom, surf_top)

    # Return the generated volume
    return slroof


def volume_ex1():
    """ Creates an example NURBS surface

    degree_u=3, degree_v=2, degree_w=1, size_u=6, size_v=5, size_w=2

    return: surface
    rtype: NURBS.Surface
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
