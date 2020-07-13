"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from geomdl.algorithms import derivative
from geomdl.base import GeomdlError, GeomdlWarning


@pytest.mark.usefixtures("curve7")
def test_bspline_hodograph_curve(curve7):
    hdg = derivative.derivative_curve(curve7)

    assert hdg.degree.u == curve7.degree.u - 1


@pytest.mark.usefixtures("surface5")
def test_bspline_hodograph_surface_len(surface5):
    hdg = derivative.derivative_surface(surface5)

    assert len(hdg) == 3


@pytest.mark.usefixtures("surface5")
def test_bspline_hodograph_surface_u(surface5):
    hdg = derivative.derivative_surface(surface5)

    # 1st derivative w.r.t. u-direction
    assert hdg[0].degree.u == surface5.degree.u - 1
    assert hdg[0].degree.v == surface5.degree.v


@pytest.mark.usefixtures("surface5")
def test_bspline_hodograph_surface_v(surface5):
    hdg = derivative.derivative_surface(surface5)

    # 1st derivative w.r.t. v-direction
    assert hdg[1].degree.u == surface5.degree.u
    assert hdg[1].degree.v == surface5.degree.v - 1


@pytest.mark.usefixtures("surface5")
def test_bspline_hodograph_surface_uv(surface5):
    hdg = derivative.derivative_surface(surface5)

    # 1st derivative w.r.t. uv-direction
    assert hdg[2].degree.u == surface5.degree.u - 1
    assert hdg[2].degree.v == surface5.degree.v - 1

# Exceptions
@pytest.mark.usefixtures("surface5")
def test_bspline_hodograph_curve_wrong_pdim(surface5):
    with pytest.raises(GeomdlError):
        hdg = derivative.derivative_curve(surface5)


@pytest.mark.usefixtures("curve6")
def test_bspline_hodograph_curve_nurbs(curve6):
    with pytest.raises(GeomdlError):
        hdg = derivative.derivative_curve(curve6)


@pytest.mark.usefixtures("curve7")
def test_bspline_hodograph_surface_wrong_pdim(curve7):
    with pytest.raises(GeomdlError):
        hdg = derivative.derivative_surface(curve7)


@pytest.mark.usefixtures("surface6")
def test_bspline_hodograph_surface_nurbs(surface6):
    with pytest.raises(GeomdlError):
        hdg = derivative.derivative_surface(surface6)
