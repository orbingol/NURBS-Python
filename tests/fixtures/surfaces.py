"""
    pytest fixtures for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol
"""

import pytest
from geomdl import BSpline, NURBS
from geomdl.geomutils import construct


@pytest.fixture
def surface1(curve1, curve2, curve3):
    s = construct.construct_surface("u", curve1, curve2, curve3)
    return s


@pytest.fixture
def surface2(curve4, curve5, curve6):
    s = construct.construct_surface("u", curve4, curve5, curve6)
    return s


@pytest.fixture
def surface3(curve1, curve3):
    s = construct.construct_surface("v", curve1, curve3)
    return s


@pytest.fixture
def surface4(curve4, curve6):
    s = construct.construct_surface("v", curve4, curve6)
    return s


@pytest.fixture
def surface5():
    """ Creates a B-spline surface instance """
    # Create a surface instance
    surf = BSpline.Surface()

    # Set degrees
    surf.degree.u = 3
    surf.degree.v = 3

    ctrlpts = [
        [-25.0, -25.0, -10.0], [-15.0, -25.0, -8.0], [-5.0, -25.0, -5.0], [5.0, -25.0, -3.0], [15.0, -25.0, -8.0], [25.0, -25.0, -10.0],
        [-25.0, -15.0, -5.0], [-15.0, -15.0, -4.0], [-5.0, -15.0, -3.0], [5.0, -15.0, -2.0], [15.0, -15.0, -4.0], [25.0, -15.0, -5.0],
        [-25.0, -5.0, 0.0], [-15.0, -5.0, -4.0], [-5.0, -5.0, -8.0], [5.0, -5.0, -8.0], [15.0, -5.0, -4.0], [25.0, -5.0, 2.0],
        [-25.0, 5.0, 0.0], [-15.0, 5.0, -4.0], [-5.0, 5.0, -8.0], [5.0, 5.0, -8.0], [15.0, 5.0, -4.0], [25.0, 5.0, 2.0],
        [-25.0, 15.0, -5.0], [-15.0, 15.0, -4.0], [-5.0, 15.0, -3.0], [5.0, 15.0, -2.0], [15.0, 15.0, -4.0], [25.0, 15.0, -5.0],
        [-25.0, 25.0, -10.0], [-15.0, 25.0, -8.0], [-5.0, 25.0, -5.0], [5.0, 25.0, -3.0], [15.0, 25.0, -8.0],[25.0, 25.0, -10.0]
    ]

    # Set control points
    surf.set_ctrlpts(ctrlpts, 6, 6)

    # Set knot vectors
    surf.knotvector.u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector.v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    return surf


@pytest.fixture
def surface6(surface5):
    """ Creates a NURBS surface from a B-spline surface """
    surf = NURBS.Surface.from_bspline(surface5)
    return surf


@pytest.fixture
def surface7(surface5):
    """ Creates a NURBS surface from a B-spline surface """
    surf = NURBS.Surface.from_bspline(surface5)
    surf.weights = [
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4
    ]
    return surf
