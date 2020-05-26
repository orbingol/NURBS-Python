"""
    pytest fixtures for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol
"""

import pytest
from geomdl import BSpline, NURBS

# star-import (from xxx import *) fix
__all__ = ["curve1", "curve2", "curve3", "curve4", "curve5", "curve6", "curve7", "curve8"]


@pytest.fixture
def curve1():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[1.0, 1.0, 0.0, 1.0], [2.0, 3.0, 0.0, 1.0], [5.0, 3.0, 1.0, 1.0], [5.0, 4.0, 0.5, 1.0], [6.0, 6.0, 0.0, 1.0]])
    return c

@pytest.fixture
def curve2():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[1.0, 1.0, 1.0, 1.0], [2.0, 3.0, 1.0, 1.0], [5.0, 3.0, 2.0, 1.0], [5.0, 4.0, 1.5, 1.0], [6.0, 6.0, 1.0, 1.0]])
    return c

@pytest.fixture
def curve3():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[1.0, 1.0, 4.0, 1.0], [2.0, 3.0, 4.0, 1.0], [5.0, 3.0, 4.0, 1.0], [5.0, 4.0, 4.0, 1.0], [6.0, 6.0, 4.0, 1.0]])
    return c

@pytest.fixture
def curve4():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[2.0, 1.0, 0.0, 1.0], [3.0, 3.0, 0.0, 1.0], [6.0, 3.0, 1.0, 1.0], [6.0, 4.0, 0.5, 1.0], [7.0, 6.0, 0.0, 1.0]])
    return c

@pytest.fixture
def curve5():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[2.0, 1.0, 1.0, 1.0], [3.0, 3.0, 1.0, 1.0], [6.0, 3.0, 2.0, 1.0], [6.0, 4.0, 1.5, 1.0], [7.0, 6.0, 1.0, 1.0]])
    return c


@pytest.fixture
def curve6():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[2.0, 1.0, 4.0, 1.0], [3.0, 3.0, 4.0, 1.0], [6.0, 3.0, 4.0, 1.0], [6.0, 4.0, 4.0, 1.0], [7.0, 6.0, 4.0, 1.0]])
    return c


@pytest.fixture
def curve7():
    """ Creates a B-spline Curve """
    curve = BSpline.Curve()
    curve.degree = 3
    curve.set_ctrlpts([[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]])
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    return curve


@pytest.fixture
def curve8(curve7):
    """ Creates a NURBS curve from a B-spline curve """
    curve = NURBS.Curve.from_bspline(curve7)
    curve.weights = [1.0, 1.0, 0.75, 1.0, 0.25, 0.4]
    return curve
