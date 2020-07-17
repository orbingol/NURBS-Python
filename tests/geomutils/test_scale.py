"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from random import randint
from geomdl.geomutils import scale


@pytest.mark.usefixtures("surface7")
@pytest.mark.parametrize("scale_factor", [1, 2, 10, 0.5, 0.25, 0.1])
def test_geomutils_scale(surface7, scale_factor):
    res = scale.scale(surface7, scale_factor)
    pt1 = surface7.evaluate_single((1.0, 1.0))
    pt2 = res.evaluate_single((1.0, 1.0))

    for a, b in zip(pt1, pt2):
        assert b == scale_factor * a
