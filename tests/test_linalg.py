"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.linalg module. Requires "pytest" to run.
"""

import pytest
from geomdl import linalg

GEOMDL_DELTA = 10e-6


def test_linspace():
    start = 5
    stop = 11
    num = 4
    result = [5.0, 7.0, 9.0, 11.0]
    to_check = linalg.linspace(start, stop, num)
    assert to_check == result


def test_vector_dot1():
    with pytest.raises(ValueError):
        vec1 = ()
        vec2 = ()
        linalg.vector_dot(vec1, vec2)


def test_vector_dot2():
    result = 32
    vec1 = (1, 2, 3)
    vec2 = (1, 5, 7)
    to_check = linalg.vector_dot(vec1, vec2)
    assert to_check == result


def test_vector_dot3():
    with pytest.raises(TypeError):
        linalg.vector_dot(5, 9.7)


def test_vector_cross1():
    with pytest.raises(ValueError):
        vec1 = ()
        vec2 = ()
        linalg.vector_cross(vec1, vec2)


def test_vector_cross2():
    with pytest.raises(ValueError):
        vec1 = (1, 2, 3, 4)
        vec2 = (1, 5, 7, 9)
        linalg.vector_cross(vec1, vec2)


def test_vector_cross3():
    result = [-1.0, -4.0, 3.0]
    vec1 = (1, 2, 3)
    vec2 = (1, 5, 7)
    to_check = linalg.vector_cross(vec1, vec2)
    assert to_check == result


def test_vector_cross4():
    with pytest.raises(TypeError):
        linalg.vector_cross(5, 9.7)


def test_vector_cross5():
    result = [0.0, 0.0, 3.0]
    vec1 = (1, 2)
    vec2 = (1, 5)
    to_check = linalg.vector_cross(vec1, vec2)
    assert to_check == result


def test_vector_normalize1():
    with pytest.raises(ValueError):
        vec = ()
        linalg.vector_normalize(vec)


def test_vector_normalize2():
    with pytest.raises(ValueError):
        vec = (0, 0)
        linalg.vector_normalize(vec)


def test_vector_normalize3():
    with pytest.raises(TypeError):
        linalg.vector_normalize(5)


def test_vector3_normalize():
    vec = (5, 2.5, 5)
    result = [0.667, 0.333, 0.667]
    to_check = linalg.vector_normalize(vec, decimals=3)
    assert to_check == result


def test_vector4_normalize():
    vec = (5, 2.5, 5, 10)
    result = [0.4, 0.2, 0.4, 0.8]
    to_check = linalg.vector_normalize(vec)
    assert to_check == result


def test_vector_generate1():
    with pytest.raises(ValueError):
        pt1 = ()
        pt2 = (1, 2, 3)
        linalg.vector_generate(pt1, pt2)


def test_vector_generate2():
    pt1 = (0, 0, 0)
    pt2 = (5, 3, 4)
    result = (5, 3, 4)
    result_normalized = (0.707107, 0.424264, 0.565685)
    to_check = linalg.vector_generate(pt1, pt2)
    to_check_normalized = linalg.vector_generate(pt1, pt2, normalize=True)
    assert abs(to_check[0] - result[0]) <= GEOMDL_DELTA
    assert abs(to_check[1] - result[1]) <= GEOMDL_DELTA
    assert abs(to_check[2] - result[2]) <= GEOMDL_DELTA
    assert abs(to_check_normalized[0] - result_normalized[0]) <= GEOMDL_DELTA
    assert abs(to_check_normalized[1] - result_normalized[1]) <= GEOMDL_DELTA
    assert abs(to_check_normalized[2] - result_normalized[2]) <= GEOMDL_DELTA


def test_vector_generate3():
    with pytest.raises(TypeError):
        linalg.vector_generate(5, 9.7)


def test_point_translate1():
    with pytest.raises(ValueError):
        pt1 = ()
        pt2 = (1, 2, 3)
        linalg.point_translate(pt1, pt2)


def test_point_translate2():
    pt = (1, 0, 0)
    vec = (5, 5, 5)
    result = [6, 5, 5]
    to_check = linalg.point_translate(pt, vec)
    assert to_check == result


def test_point_translate3():
    with pytest.raises(TypeError):
        linalg.point_translate(5, 9.7)


def test_binomial_coefficient1():
    result = 0.0
    to_check = linalg.binomial_coefficient(13, 14)
    assert to_check == result


def test_binomial_coefficient2():
    result = 1.0
    to_check = linalg.binomial_coefficient(13, 13)
    assert to_check == result


def test_binomial_coefficient3():
    result = 680.0
    to_check = linalg.binomial_coefficient(17, 3)
    assert to_check == result


def test_frange1():
    start = 5
    stop = 11
    step = 2
    to_check = []
    for fr in linalg.frange(start, stop, step):
        to_check.append(fr)
    result = [5.0, 7.0, 9.0, 11.0]
    assert to_check == result


def test_frange2():
    check = list(linalg.frange(0, 1, 0.1))
    result = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    check_flag = True
    for c, r in zip(check, result):
        if abs(c - r) > GEOMDL_DELTA:
            check_flag = False
    assert check_flag


def test_vector_multiply():
    result = [2, 4, 6]
    computed = linalg.vector_multiply((1, 2, 3), 2)
    assert result == computed


def test_vector_mean():
    vector_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    result = [4, 5, 6]
    computed = linalg.vector_mean(*vector_list)
    assert result == computed


def test_vector_angle_between():
    computed_deg = linalg.vector_angle_between((1, 2, 3), (3, 2, 1), degrees=True)
    computed_rad = linalg.vector_angle_between((1, 2, 3), (3, 2, 1), degrees=False)
    result_deg = 44.415308597193
    result_rad = 0.775193373310361
    assert abs(computed_deg - result_deg) < GEOMDL_DELTA
    assert abs(computed_rad - result_rad) < GEOMDL_DELTA


def test_point_distance():
    result = 17.691806
    computed = linalg.point_distance((5, 7, 9), (-7, -5, 4))
    assert abs(result - computed) < GEOMDL_DELTA


def test_point_mid():
    result = [2.5, 3.5, 4.5]
    computed = linalg.point_mid((1, 2, 3), (4, 5, 6))
    assert result == computed


def test_vector_sum():
    vec1 = (1.0, 2.0, 3.0)
    vec2 = (4.0, 5.0, 6.0)
    result = [5.0, 7.0, 9.0]
    computed = linalg.vector_sum(vec1, vec2)
    assert  result == computed


def test_is_vector_zero():
    vec = [10e-4 for _ in range(3)]
    assert linalg.vector_is_zero(vec, 10e-3)
