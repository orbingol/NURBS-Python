"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests B-Spline to NURBS conversions. Requires "pytest" to run.
"""

import pytest
from geomdl import NURBS


@pytest.mark.usefixtures("curve7")
def test_convert_curve(curve7):
    nbs = NURBS.Curve.from_bspline(curve7)

    assert nbs.rational == True
    assert len(nbs.weights) == nbs.ctrlpts.count


@pytest.mark.usefixtures("surface5")
def test_convert_surface(surface5):
    nbs = NURBS.Surface.from_bspline(surface5)

    assert nbs.rational == True
    assert len(nbs.weights) == nbs.ctrlpts.count


@pytest.mark.usefixtures("volume2")
def test_convert_volume(volume2):
    nbs = NURBS.Volume.from_bspline(volume2)

    assert nbs.rational == True
    assert len(nbs.weights) == nbs.ctrlpts.count
