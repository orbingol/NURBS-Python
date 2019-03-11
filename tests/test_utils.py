"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.utilities module. Requires "pytest" to run.
"""

import pytest
from geomdl import utilities
from geomdl import knotvector
from geomdl import utilities

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

