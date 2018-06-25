"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.utilities module. Requires "pytest" to run.
"""
from geomdl import utilities


def test_autogen_knot_vector():
    degree = 4
    num_ctrlpts = 12
    autogen_kv = utilities.generate_knot_vector(degree, num_ctrlpts)
    result = [0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert autogen_kv == result


def test_check_knot_vector():
    degree = 4
    num_ctrlpts = 12
    autogen_kv = utilities.generate_knot_vector(degree, num_ctrlpts)
    check_result = utilities.check_knot_vector(degree=degree, num_ctrlpts=num_ctrlpts, knot_vector=autogen_kv)
    assert check_result


def test_normalize_knot_vector():
    input_kv = (-5, -5, -3, -2, 2, 3, 5, 5)
    output_kv = [0.0, 0.0, 0.2, 0.3, 0.7, 0.8, 1.0, 1.0]
    to_check = utilities.normalize_knot_vector(input_kv)
    assert to_check == output_kv


def test_linspace():
    start = 5
    stop = 11
    num = 4
    result = [5.0, 7.0, 9.0, 11.0]
    to_check = utilities.linspace(start, stop, num)
    assert to_check == result


def test_vector_dot():
    result = 32
    vec1 = (1, 2, 3)
    vec2 = (1, 5, 7)
    to_check = utilities.vector_dot(vec1, vec2)
    assert to_check == result


def test_vector_cross():
    result = [-1.0, -4.0, 3.0]
    vec1 = (1, 2, 3)
    vec2 = (1, 5, 7)
    to_check = utilities.vector_cross(vec1, vec2)
    assert to_check == result


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


def test_vector_generate():
    pt1 = (0, 0, 0)
    pt2 = (5, 3, 4)
    result = [5, 3, 4]
    result_normalized = [0.707107, 0.424264, 0.565685]
    to_check = utilities.vector_generate(pt1, pt2)
    to_check_normalized = utilities.vector_generate(pt1, pt2, normalize=True)
    assert to_check == result
    assert to_check_normalized == result_normalized


def test_point_translate():
    pt = (1, 0, 0)
    vec = (5, 5, 5)
    result = [6, 5, 5]
    to_check = utilities.point_translate(pt, vec)
    assert to_check == result


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
