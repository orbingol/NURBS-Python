"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

from pytest import fixture
from geomdl import NURBS
from geomdl import construct


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
