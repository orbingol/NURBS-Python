"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.utilities module. Requires "pytest" to run.
"""

import pytest
from geomdl import control_points
from geomdl import utilities
from geomdl.base import GeomdlError

GEOMDL_DELTA = 10e-6




def test_check_uv1():
    u = -0.1
    v = 0.1
    assert not utilities.check_params([u, v])


def test_check_uv2():
    u = 2
    v = 0.1
    assert not utilities.check_params([u, v])


def test_check_uv3():
    v = -0.1
    u = 0.1
    assert not utilities.check_params([u, v])


def test_check_uv4():
    v = 2
    u = 0.1
    assert not utilities.check_params([u, v])


def test_color_generator():
    seed = 17  # some number to be used as the random seed
    result = utilities.color_generator(seed)
    to_check = utilities.color_generator(seed)
    assert to_check == result


def test_cpman_curve1():
    """ Control Points Manager: get-set point (curve) """
    pt = [0.0, 0.2, 0.3]
    p = 3
    sz = 10
    cpman = control_points.CurveManager(sz)
    cpman.set_ctrlpt(pt, p)
    assert cpman.get_ctrlpt(3) == pt


def test_cpman_curve2():
    """ Control Points Manager: get empty point (curve) """
    p = 5
    sz = 12
    cpman = control_points.CurveManager(sz)
    assert cpman.get_ctrlpt(p) == list()


def test_cpman_curve3():
    """ Control Points Manager: check for invalid index """
    p = 12
    sz = 5
    cpman = control_points.CurveManager(sz)
    assert cpman.get_ctrlpt(p) == None


def test_cpman_curve4():
    """ Control Points Manager: get-set attachment (valid, list) """
    d = [0.0, 1.0, 2.0, 3.0]
    p = 5
    sz = 12
    cpman = control_points.CurveManager(sz, testdata=4)
    cpman.set_ptdata(dict(testdata=d), p)
    retv1 = cpman.get_ptdata('testdata', p)
    retv2 = cpman.get_ptdata('testdata', p + 1)
    assert retv1[2] == 2.0
    assert retv2[2] == 0.0


def test_cpman_curve5():
    """ Control Points Manager: get-set attachment (invalid, list) """
    d = [0.0, 1.0, 2.0, 3.0]
    p = 5
    sz = 12
    cpman = control_points.CurveManager(sz, testdata=4)
    cpman.set_ptdata(dict(testdata=d), p)
    retv = cpman.get_ptdata('testdata2', p)
    assert retv == None


def test_cpman_curve6():
    """ Control Points Manager: get-set attachment (exception) """
    with pytest.raises(GeomdlError):
        d = [0.0, 1.0, 2.0, 3.0]
        p = 5
        sz = 12
        cpman = control_points.CurveManager(sz, testdata=3)
        cpman.set_ptdata(dict(testdata=d), p)


def test_cpman_curve7():
    """ Control Points Manager: get-set attachment (valid, float) """
    d = 13
    p = 5
    sz = 12
    cpman = control_points.CurveManager(sz, testdata=1)
    cpman.set_ptdata(dict(testdata=d), p)
    assert cpman.get_ptdata('testdata', 5) == 13


def test_cpman_curve8():
    """ Control Points Manager: try to set invalid key """
    with pytest.raises(GeomdlError):
        d = [0.0, 1.0, 2.0, 3.0]
        p = 5
        sz = 12
        cpman = control_points.CurveManager(sz, testdata=4)
        cpman.set_ptdata({'testdata1': d}, p)


def test_cpman_surface1():
    """ Control Points Manager: get-set point (surface) """
    pt = [1.0, 2.0, 3.0]
    p = [2 ,3]
    sz = [4, 3]
    cpman = control_points.SurfaceManager(*sz)
    cpman.set_ctrlpt(pt, *p)
    assert cpman.get_ctrlpt(2, 3) == pt


def test_cpman_volume1():
    """ Control Points Manager: get-set point (volume) """
    pt = [1.0, 2.0, 3.0]
    p = [2, 3, 1]
    sz = [4, 3, 2]
    cpman = control_points.VolumeManager(*sz)
    cpman.set_ctrlpt(pt, *p)
    assert cpman.get_ctrlpt(2, 3, 1) == pt
