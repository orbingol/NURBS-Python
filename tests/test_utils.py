"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.utilities module. Requires "pytest" to run.
"""

import pytest
from geomdl import utilities
from geomdl import knotvector
from geomdl import control_points
from geomdl import utilities
from geomdl.exceptions import GeomdlException

GEOMDL_DELTA = 10e-6


def test_generate_knot_vector1():
    with pytest.raises(ValueError):
        degree = 0
        num_ctrlpts = 12
        knotvector.generate(degree, num_ctrlpts)


def test_generate_knot_vector2():
    with pytest.raises(ValueError):
        degree = 4
        num_ctrlpts = 0
        knotvector.generate(degree, num_ctrlpts)


def test_generate_knot_vector3():
    with pytest.raises(ValueError):
        degree = 0
        num_ctrlpts = 0
        knotvector.generate(degree, num_ctrlpts)


def test_generate_knot_vector4():
    degree = 4
    num_ctrlpts = 12
    autogen_kv = knotvector.generate(degree, num_ctrlpts)
    result = [0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert autogen_kv == result


def test_generate_knot_vector5():
    # testing auto-generated unclamped knot vector
    degree = 3
    num_ctrlpts = 5
    result = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]
    autogen_kv = knotvector.generate(degree, num_ctrlpts, clamped=False)
    assert autogen_kv == result


def test_check_knot_vector1():
    with pytest.raises(ValueError):
        knotvector.check(4, tuple(), 12)


def test_check_knot_vector2():
    to_check = knotvector.check(4, (1, 2, 3, 4), 12)
    result = False
    assert to_check == result


def test_check_knot_vector3():
    to_check = knotvector.check(3, (5, 3, 6, 5, 4, 5, 6), 3)
    result = False
    assert to_check == result


def test_check_knot_vector4():
    degree = 4
    num_ctrlpts = 12
    autogen_kv = knotvector.generate(degree, num_ctrlpts)
    check_result = knotvector.check(degree=degree, num_ctrlpts=num_ctrlpts, knot_vector=autogen_kv)
    assert check_result


def test_check_knot_vector5():
    degree = 4
    num_ctrlpts = 12
    with pytest.raises(TypeError):
        knotvector.check(degree=degree, num_ctrlpts=num_ctrlpts, knot_vector=5)


def test_normalize_knot_vector1():
    # check for empty list/tuple
    with pytest.raises(ValueError):
        knotvector.normalize(tuple())


def test_normalize_knot_vector2():
    input_kv = (-5, -5, -3, -2, 2, 3, 5, 5)
    output_kv = [0.0, 0.0, 0.2, 0.3, 0.7, 0.8, 1.0, 1.0]
    to_check = knotvector.normalize(input_kv)
    assert to_check == output_kv


def test_normalize_knot_vector3():
    with pytest.raises(TypeError):
        knotvector.normalize(5)


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
    with pytest.raises(GeomdlException):
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
    with pytest.raises(GeomdlException):
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
