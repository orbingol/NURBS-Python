"""
    Tests for the NURBS-Python (geomdl) package
    Released under the MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Tests geomdl.base.GeomdlFloat class. Requires "pytest" to run.
"""

from pytest import fixture, mark
from geomdl.base import GeomdlFloat


@fixture
def fnum():
    """ Pytest fixture for an arbitrary floating point number """
    return GeomdlFloat(3.2)


@mark.parametrize("inp, res", [
    (1, 4.2),
    (2.8, 6.0),
])
def test_add(fnum, inp, res):
    c = fnum + inp
    assert isinstance(c, GeomdlFloat)
    assert round(c, 2) == res

@mark.parametrize("inp, res", [
    (1, 2.2),
    (2.8, 0.4),
])
def test_sub(fnum, inp, res):
    c = fnum - inp
    assert isinstance(c, GeomdlFloat)
    assert round(c, 2) == res


@mark.parametrize("inp, res", [
    (1, 3.2),
    (2.8, 8.96),
])
def test_mul(fnum, inp, res):
    c = fnum * inp
    assert isinstance(c, GeomdlFloat)
    assert round(c, 2) == res


@mark.parametrize("inp, res", [
    (1, 3.2),
    (2.8, 1.14),
])
def test_div(fnum, inp, res):
    c = fnum / inp
    assert isinstance(c, GeomdlFloat)
    assert round(c, 2) == res


@mark.parametrize("inp, res", [
    (1, 4.2),
    (2.8, 6.0),
])
def test_iadd(fnum, inp, res):
    fnum += inp
    assert isinstance(fnum, GeomdlFloat)
    assert round(fnum, 2) == res


@mark.parametrize("inp, res", [
    (1, 2.2),
    (2.8, 0.4),
])
def test_isub(fnum, inp, res):
    fnum -= inp
    assert isinstance(fnum, GeomdlFloat)
    assert round(fnum, 2) == res


@mark.parametrize("inp, res", [
    (1, 3.2),
    (2.8, 8.96),
])
def test_imul(fnum, inp, res):
    fnum *= inp
    assert isinstance(fnum, GeomdlFloat)
    assert round(fnum, 2) == res


@mark.parametrize("inp, res", [
    (1, 3.2),
    (2.8, 1.14),
])
def test_idiv(fnum, inp, res):
    fnum /= inp
    assert isinstance(fnum, GeomdlFloat)
    assert round(fnum, 2) == res


@mark.parametrize("inp, res", [
    (1, 4.2),
    (2.8, 6.0),
])
def test_radd(fnum, inp, res):
    c = inp + fnum
    assert isinstance(c, GeomdlFloat)
    assert round(c, 2) == res

@mark.parametrize("inp, res", [
    (4.2, 1.0),
    (6.4, 3.2),
])
def test_rsub(fnum, inp, res):
    c = inp - fnum
    assert isinstance(c, GeomdlFloat)
    assert round(c, 2) == res


@mark.parametrize("inp, res", [
    (1, 3.2),
    (2.8, 8.96),
])
def test_rmul(fnum, inp, res):
    c = inp * fnum
    assert isinstance(c, GeomdlFloat)
    assert round(c, 2) == res


@mark.parametrize("inp, res", [
    (6.4, 2.0),
    (3.2, 1.0),
])
def test_rdiv(fnum, inp, res):
    c = inp / fnum
    assert isinstance(c, GeomdlFloat)
    assert round(c, 2) == res


@mark.parametrize("inp, res", [
    (GeomdlFloat(3.2), True),
    (3.2, True),
    (3.19, False),
    (7, False),
    (GeomdlFloat(11), False),
])
def test_eq(fnum, inp, res):
    c = (fnum == inp)
    assert c == res


@mark.parametrize("inp, res", [
    (GeomdlFloat(3.2), False),
    (3.2, False),
    (3.19, True),
    (7, True),
    (GeomdlFloat(11), True),
])
def test_nq(fnum, inp, res):
    c = (fnum != inp)
    assert c == res


@mark.parametrize("inp, res", [
    (GeomdlFloat(3.2), False),
    (2, False),
    (3.21, True),
    (GeomdlFloat(5.12), True),
])
def test_lt(fnum, inp, res):
    c = (fnum < inp)
    assert c == res


@mark.parametrize("inp, res", [
    (GeomdlFloat(3.2), True),
    (2, False),
    (3.21, True),
    (GeomdlFloat(5.12), True),
])
def test_le(fnum, inp, res):
    c = (fnum <= inp)
    assert c == res


@mark.parametrize("inp, res", [
    (GeomdlFloat(3.2), False),
    (2, True),
    (3.21, False),
    (GeomdlFloat(5.12), False),
])
def test_gt(fnum, inp, res):
    c = (fnum > inp)
    assert c == res


@mark.parametrize("inp, res", [
    (GeomdlFloat(3.2), True),
    (2, True),
    (3.21, False),
    (GeomdlFloat(5.12), False),
])
def test_ge(fnum, inp, res):
    c = (fnum >= inp)
    assert c == res
