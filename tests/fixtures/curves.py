"""
    pytest fixtures for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol
"""

import pytest
from geomdl import NURBS


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
