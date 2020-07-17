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
    # mid points should be the same
    mid_pt1 = surface7.evaluate_single((0.5, 0.5))
    mid_pt2 = res.evaluate_single((0.5, 0.5))

    for a, b in zip(mid_pt1, mid_pt2):
        assert a == b


@pytest.mark.usefixtures("surface7")
def test_geomutils_rotate_y(surface7):
    res = rotate.rotate(surface7, 45, axis=1)
    # mid points should be the same
    mid_pt1 = surface7.evaluate_single((0.5, 0.5))
    mid_pt2 = res.evaluate_single((0.5, 0.5))

    for a, b in zip(mid_pt1, mid_pt2):
        assert a == b


@pytest.mark.usefixtures("surface7")
def test_geomutils_rotate_z(surface7):
    res = rotate.rotate(surface7, 45, axis=2)
    # mid points should be the same
    mid_pt1 = surface7.evaluate_single((0.5, 0.5))
    mid_pt2 = res.evaluate_single((0.5, 0.5))

    for a, b in zip(mid_pt1, mid_pt2):
        assert a == b


@pytest.mark.usefixtures("surface7")
def test_geomutils_rotate_x2(surface7):
    res = rotate.rotate(surface7, 45, axis=0)
    mid_pt1 = surface7.evaluate_single((0.0, 0.0))
    mid_pt2 = res.evaluate_single((0.0, 0.0))

    for a, b in zip(mid_pt1, mid_pt2):
        assert a != b


@pytest.mark.usefixtures("surface7")
def test_geomutils_rotate_y2(surface7):
    res = rotate.rotate(surface7, 45, axis=1)
    mid_pt1 = surface7.evaluate_single((0.0, 0.0))
    mid_pt2 = res.evaluate_single((0.0, 0.0))

    for a, b in zip(mid_pt1, mid_pt2):
        assert a != b


@pytest.mark.usefixtures("surface7")
def test_geomutils_rotate_z2(surface7):
    res = rotate.rotate(surface7, 45, axis=2)
    mid_pt1 = surface7.evaluate_single((0.2, 0.2))
    mid_pt2 = res.evaluate_single((0.2, 0.2))

    for a, b in zip(mid_pt1, mid_pt2):
        assert a != b
