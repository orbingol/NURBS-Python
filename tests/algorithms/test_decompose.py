"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from geomdl.algorithms import decompose


@pytest.mark.usefixtures("curve7")
def test_algorithm_decompose_curve(curve7):
    dg = decompose.decompose_curve(curve7)

    # number of curves generated after the decomposition
    # should be equal to the number of knot spans of the
    # input curve
    kv = curve7.knotvector.u[curve7.degree.u:-curve7.degree.u]
    # num knot spans = num midknots + 1
    # num knot spans = num non-superfluous knots - 1
    assert len(dg) == len(kv) - 1


@pytest.mark.usefixtures("surface5")
def test_algorithm_hodograph_surface_u(surface5):
    dg = decompose.decompose_surface(surface5, decompose_dir='u')

    # refer to the curve test for more details
    kv = surface5.knotvector.u[surface5.degree.u:-surface5.degree.u]
    assert len(dg) == len(kv) - 1


@pytest.mark.usefixtures("surface5")
def test_algorithm_hodograph_surface_v(surface5):
    dg = decompose.decompose_surface(surface5, decompose_dir='v')

    # refer to the curve test for more details
    kv = surface5.knotvector.v[surface5.degree.v:-surface5.degree.v]
    assert len(dg) == len(kv) - 1


@pytest.mark.usefixtures("surface5")
def test_algorithm_hodograph_surface_uv(surface5):
    dg = decompose.decompose_surface(surface5)

    # refer to the curve test for more details
    kv_u = surface5.knotvector.u[surface5.degree.u:-surface5.degree.u]
    kv_v = surface5.knotvector.v[surface5.degree.v:-surface5.degree.v]
    assert len(dg) == (len(kv_u) - 1) * (len(kv_v) - 1)
