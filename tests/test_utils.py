"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.utilities module. Requires "pytest" to run.
"""
import pytest
from geomdl import utilities

GEOMDL_DELTA = 10e-8


def test_generate_knot_vector1():
    with pytest.raises(ValueError):
        degree = 0
        num_ctrlpts = 12
        utilities.generate_knot_vector(degree, num_ctrlpts)


def test_generate_knot_vector2():
    with pytest.raises(ValueError):
        degree = 4
        num_ctrlpts = 0
        utilities.generate_knot_vector(degree, num_ctrlpts)


def test_generate_knot_vector3():
    with pytest.raises(ValueError):
        degree = 0
        num_ctrlpts = 0
        utilities.generate_knot_vector(degree, num_ctrlpts)


def test_generate_knot_vector4():
    degree = 4
    num_ctrlpts = 12
    autogen_kv = utilities.generate_knot_vector(degree, num_ctrlpts)
    result = [0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert autogen_kv == result


def test_check_knot_vector1():
    with pytest.raises(ValueError):
        utilities.check_knot_vector(4, tuple(), 12)


def test_check_knot_vector2():
    to_check = utilities.check_knot_vector(4, (1, 2, 3, 4), 12)
    result = False
    assert to_check == result


def test_check_knot_vector3():
    to_check = utilities.check_knot_vector(3, (5, 3, 6, 5, 4, 5, 6), 3)
    result = False
    assert to_check == result


def test_check_knot_vector4():
    degree = 4
    num_ctrlpts = 12
    autogen_kv = utilities.generate_knot_vector(degree, num_ctrlpts)
    check_result = utilities.check_knot_vector(degree=degree, num_ctrlpts=num_ctrlpts, knot_vector=autogen_kv)
    assert check_result


def test_check_knot_vector5():
    degree = 4
    num_ctrlpts = 12
    with pytest.raises(TypeError):
        utilities.check_knot_vector(degree=degree, num_ctrlpts=num_ctrlpts, knot_vector=5)


def test_normalize_knot_vector1():
    # check for empty list/tuple
    with pytest.raises(ValueError):
        utilities.normalize_knot_vector(tuple())


def test_normalize_knot_vector2():
    input_kv = (-5, -5, -3, -2, 2, 3, 5, 5)
    output_kv = [0.0, 0.0, 0.2, 0.3, 0.7, 0.8, 1.0, 1.0]
    to_check = utilities.normalize_knot_vector(input_kv)
    assert to_check == output_kv


def test_normalize_knot_vector3():
    with pytest.raises(TypeError):
        utilities.normalize_knot_vector(5)


def test_check_uv1():
    with pytest.raises(ValueError):
        u = -0.1
        v = 0.1
        utilities.check_uv(u, v)


def test_check_uv2():
    with pytest.raises(ValueError):
        u = 2
        v = 0.1
        utilities.check_uv(u, v)


def test_check_uv3():
    with pytest.raises(ValueError):
        v = -0.1
        u = 0.1
        utilities.check_uv(u, v)


def test_check_uv4():
    with pytest.raises(ValueError):
        v = 2
        u = 0.1
        utilities.check_uv(u, v)


def test_linspace():
    start = 5
    stop = 11
    num = 4
    result = [5.0, 7.0, 9.0, 11.0]
    to_check = utilities.linspace(start, stop, num)
    assert to_check == result


def test_vector_dot1():
    with pytest.raises(ValueError):
        vec1 = ()
        vec2 = ()
        utilities.vector_dot(vec1, vec2)


def test_vector_dot2():
    result = 32
    vec1 = (1, 2, 3)
    vec2 = (1, 5, 7)
    to_check = utilities.vector_dot(vec1, vec2)
    assert to_check == result


def test_vector_dot3():
    with pytest.raises(TypeError):
        utilities.vector_dot(5, 9.7)


def test_vector_cross1():
    with pytest.raises(ValueError):
        vec1 = ()
        vec2 = ()
        utilities.vector_cross(vec1, vec2)


def test_vector_cross2():
    with pytest.raises(ValueError):
        vec1 = (1, 2, 3, 4)
        vec2 = (1, 5, 7, 9)
        utilities.vector_cross(vec1, vec2)


def test_vector_cross3():
    result = [-1.0, -4.0, 3.0]
    vec1 = (1, 2, 3)
    vec2 = (1, 5, 7)
    to_check = utilities.vector_cross(vec1, vec2)
    assert to_check == result


def test_vector_cross4():
    with pytest.raises(TypeError):
        utilities.vector_cross(5, 9.7)


def test_vector_normalize1():
    with pytest.raises(ValueError):
        vec = ()
        utilities.vector_normalize(vec)


def test_vector_normalize2():
    with pytest.raises(ValueError):
        vec = (0, 0)
        utilities.vector_normalize(vec)


def test_vector_normalize3():
    with pytest.raises(TypeError):
        utilities.vector_normalize(5)


def test_vector3_normalize():
    vec = (5, 2.5, 5)
    result = [0.667, 0.333, 0.667]
    to_check = utilities.vector_normalize(vec, decimals=3)
    assert to_check == result


def test_vector4_normalize():
    vec = (5, 2.5, 5, 10)
    result = [0.4, 0.2, 0.4, 0.8]
    to_check = utilities.vector_normalize(vec)
    assert to_check == result


def test_vector_generate1():
    with pytest.raises(ValueError):
        pt1 = ()
        pt2 = (1, 2, 3)
        utilities.vector_generate(pt1, pt2)


def test_vector_generate2():
    pt1 = (0, 0, 0)
    pt2 = (5, 3, 4)
    result = [5, 3, 4]
    result_normalized = [0.707107, 0.424264, 0.565685]
    to_check = utilities.vector_generate(pt1, pt2)
    to_check_normalized = utilities.vector_generate(pt1, pt2, normalize=True)
    assert to_check == result
    assert to_check_normalized == result_normalized


def test_vector_generate3():
    with pytest.raises(TypeError):
        utilities.vector_generate(5, 9.7)


def test_point_translate1():
    with pytest.raises(ValueError):
        pt1 = ()
        pt2 = (1, 2, 3)
        utilities.point_translate(pt1, pt2)


def test_point_translate2():
    pt = (1, 0, 0)
    vec = (5, 5, 5)
    result = [6, 5, 5]
    to_check = utilities.point_translate(pt, vec)
    assert to_check == result


def test_point_translate3():
    with pytest.raises(TypeError):
        utilities.point_translate(5, 9.7)


def test_binomial_coefficient1():
    result = 0.0
    to_check = utilities.binomial_coefficient(13, 14)
    assert to_check == result


def test_binomial_coefficient2():
    result = 1.0
    to_check = utilities.binomial_coefficient(13, 13)
    assert to_check == result


def test_binomial_coefficient3():
    result = 680.0
    to_check = utilities.binomial_coefficient(17, 3)
    assert to_check == result


def test_frange1():
    start = 5
    stop = 11
    step = 2
    to_check = []
    for fr in utilities.frange(start, stop, step):
        to_check.append(fr)
    result = [5.0, 7.0, 9.0, 11.0]
    assert to_check == result


def test_frange2():
    check = list(utilities.frange(0, 1, 0.1))
    result = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    check_flag = True
    for c, r in zip(check, result):
        if abs(c - r) > GEOMDL_DELTA:
            check_flag = False
    assert check_flag


def test_color_generator():
    seed = 17  # some number to be used as the random seed
    result = utilities.color_generator(seed)
    to_check = utilities.color_generator(seed)
    assert to_check == result
