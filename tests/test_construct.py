"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from pytest import fixture
from geomdl import NURBS
from geomdl import construct
from geomdl.base import GeomdlError


@fixture
def curve1():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[1.0, 1.0, 0.0, 1.0], [2.0, 3.0, 0.0, 1.0], [5.0, 3.0, 1.0, 1.0], [5.0, 4.0, 0.5, 1.0], [6.0, 6.0, 0.0, 1.0]])
    return c


@fixture
def curve2():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[1.0, 1.0, 1.0, 1.0], [2.0, 3.0, 1.0, 1.0], [5.0, 3.0, 2.0, 1.0], [5.0, 4.0, 1.5, 1.0], [6.0, 6.0, 1.0, 1.0]])
    return c


@fixture
def curve3():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[1.0, 1.0, 4.0, 1.0], [2.0, 3.0, 4.0, 1.0], [5.0, 3.0, 4.0, 1.0], [5.0, 4.0, 4.0, 1.0], [6.0, 6.0, 4.0, 1.0]])
    return c


@fixture
def curve4():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[2.0, 1.0, 0.0, 1.0], [3.0, 3.0, 0.0, 1.0], [6.0, 3.0, 1.0, 1.0], [6.0, 4.0, 0.5, 1.0], [7.0, 6.0, 0.0, 1.0]])
    return c


@fixture
def curve5():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[2.0, 1.0, 1.0, 1.0], [3.0, 3.0, 1.0, 1.0], [6.0, 3.0, 2.0, 1.0], [6.0, 4.0, 1.5, 1.0], [7.0, 6.0, 1.0, 1.0]])
    return c


@fixture
def curve6():
    c = NURBS.Curve()
    c.degree = 3
    c.knotvector = [0, 0, 0, 0, 1, 2, 2, 2, 2]
    c.set_ctrlpts([[2.0, 1.0, 4.0, 1.0], [3.0, 3.0, 4.0, 1.0], [6.0, 3.0, 4.0, 1.0], [6.0, 4.0, 4.0, 1.0], [7.0, 6.0, 4.0, 1.0]])
    return c


@fixture
def surface1(curve1, curve2, curve3):
    s = construct.construct_surface("u", curve1, curve2, curve3)
    return s


@fixture
def surface2(curve4, curve5, curve6):
    s = construct.construct_surface("u", curve4, curve5, curve6)
    return s


@fixture
def surface3(curve1, curve3):
    s = construct.construct_surface("v", curve1, curve3)
    return s


@fixture
def surface4(curve4, curve6):
    s = construct.construct_surface("v", curve4, curve6)
    return s


@fixture
def volume1(surface1, surface2):
    v = construct.construct_volume("w", surface1, surface2)
    return v


def test_construct_surface_v_degree(curve1, curve2):
    surf = construct.construct_surface('v', curve1, curve2)
    assert surf.degree.u == curve1.degree.u
    assert surf.degree.u == curve2.degree.u
    assert surf.degree.v == 2


def test_construct_surface_v_knotvector(curve1, curve2):
    surf = construct.construct_surface('v', curve1, curve2)
    assert all([x == y for x, y in zip(surf.knotvector.v, [0.0, 0.0, 0.0, 1.0, 1.0, 1.0])])


def test_construct_surface_v_ctrlpts(curve1, curve2):
    surf = construct.construct_surface('v', curve1, curve2)
    for ptx, pty in zip(surf.ctrlpts, list(curve1.ctrlpts) + list(curve2.ctrlpts)):
        assert all([x == y for x, y in zip(ptx, pty)])


def test_construct_surface_u_degree(curve1, curve2):
    surf = construct.construct_surface('u', curve1, curve2)
    assert surf.degree.v == curve1.degree.u
    assert surf.degree.v == curve2.degree.u
    assert surf.degree.u == 2


def test_construct_surface_u_knotvector(curve1, curve2):
    surf = construct.construct_surface('u', curve1, curve2)
    assert all([x == y for x, y in zip(surf.knotvector.u, [0.0, 0.0, 0.0, 1.0, 1.0, 1.0])])


def test_construct_surface_u_ctrlpts(curve1, curve2):
    surf = construct.construct_surface('u', curve1, curve2)
    assert all([x == y for x, y in zip(surf.ctrlpts[1], curve2.ctrlpts[0])])
    assert all([x == y for x, y in zip(surf.ctrlpts[2], curve1.ctrlpts[1])])


def test_construct_volume_u_degree(surface1, surface2):
    vol = construct.construct_volume('u', surface1, surface2)
    assert vol.degree.u == 1
    assert vol.degree.v == surface1.degree.u
    assert vol.degree.v == surface2.degree.u
    assert vol.degree.w == surface1.degree.v
    assert vol.degree.w == surface2.degree.v


def test_construct_volume_v_degree(surface1, surface2):
    vol = construct.construct_volume('v', surface1, surface2)
    assert vol.degree.u == surface1.degree.u
    assert vol.degree.u == surface2.degree.u
    assert vol.degree.v == 1
    assert vol.degree.w == surface1.degree.v
    assert vol.degree.w == surface2.degree.v


def test_construct_volume_w_degree(surface1, surface2):
    vol = construct.construct_volume('w', surface1, surface2)
    assert vol.degree.u == surface1.degree.u
    assert vol.degree.u == surface2.degree.u
    assert vol.degree.v == surface1.degree.v
    assert vol.degree.v == surface2.degree.v
    assert vol.degree.w == 1


def test_extract_curves_error1(volume1):
    with pytest.raises(GeomdlError):
        construct.extract_curves(volume1)

def test_extract_curves1(surface1):
    cs = construct.extract_curves(surface1)
    assert isinstance(cs, dict)
    assert "u" in cs.keys()
    assert "v" in cs.keys()


def test_extract_curves2(surface1):
    cs = construct.extract_curves(surface1)
    assert len(cs['u']) == surface1.ctrlpts_size.v
    assert len(cs['v']) == surface1.ctrlpts_size.u


def test_extract_surfaces_error1(surface1):
    with pytest.raises(GeomdlError):
        construct.extract_surfaces(surface1)


def test_extract_surfaces1(volume1):
    ss = construct.extract_surfaces(volume1)
    assert isinstance(ss, dict)
    assert "uv" in ss.keys()
    assert "uw" in ss.keys()
    assert "vw" in ss.keys()


def test_extract_surfaces2(volume1):
    ss = construct.extract_surfaces(volume1)
    assert len(ss['uv']) == volume1.ctrlpts_size.w
    assert len(ss['uw']) == volume1.ctrlpts_size.v
    assert len(ss['vw']) == volume1.ctrlpts_size.u
