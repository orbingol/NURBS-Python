"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from random import randint
from geomdl.geomutils import rotate


@pytest.mark.usefixtures("surface7")
def test_geomutils_rotate_x(surface7):
    res = rotate.rotate(surface7, 45, axis=0)
    pt1 = surface7.evaluate_single((1.0, 0.0))
    pt2 = res.evaluate_single((1.0, 0.0))

    for a, b in zip(pt1, pt2):
        assert a == b


@pytest.mark.usefixtures("surface7")
def test_geomutils_rotate_y(surface7):
    res = rotate.rotate(surface7, 45, axis=1)
    pt1 = surface7.evaluate_single((0.0, 1.0))
    pt2 = res.evaluate_single((0.0, 1.0))

    for a, b in zip(pt1, pt2):
        assert a == b


@pytest.mark.usefixtures("surface7")
def test_geomutils_rotate_z(surface7):
    res = rotate.rotate(surface7, 45, axis=2)
    pt1 = surface7.evaluate_single((0.0, 0.0))
    pt2 = res.evaluate_single((0.0, 0.0))

    for a, b in zip(pt1, pt2):
        assert a == b
