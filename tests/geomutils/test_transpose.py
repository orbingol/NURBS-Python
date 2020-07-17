"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from random import randint
from geomdl.geomutils import transpose


@pytest.mark.usefixtures("surface2")
def test_geomutils_transpose(surface2):
    res = transpose.transpose(surface2)

    assert res.degree.v == surface2.degree.u
    assert res.degree.u == surface2.degree.v


@pytest.mark.usefixtures("surface2")
def test_geomutils_ctrlpts_surface(surface2):
    res = transpose.flip(surface2)

    for a, b in zip(res.ctrlpts[0], surface2.ctrlpts[-1]):
        assert a == b
