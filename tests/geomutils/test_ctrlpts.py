"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from random import randint
from geomdl.geomutils import ctrlpts


@pytest.mark.usefixtures("curve5")
def test_geomutils_ctrlpts_curve(curve5):
    res = ctrlpts.find_ctrlpts(curve5, u=0.5)

    assert len(res) == curve5.degree.u + 1


@pytest.mark.usefixtures("surface5")
def test_geomutils_ctrlpts_surface(surface5):
    res = ctrlpts.find_ctrlpts(surface5, u=0.5, v=0.9)

    assert len(res) == (surface5.degree.u + 1) * (surface5.degree.v + 1)
