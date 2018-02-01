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
    check_result = utilities.check_knot_vector(degree=degree, control_points_size=num_ctrlpts, knot_vector=autogen_kv)
    assert check_result


def test_normalize_knot_vector():
    input_kv = (-5, -5, -3, -2, 2, 3, 5, 5)
    output_kv = [0.0, 0.0, 0.2, 0.3, 0.7, 0.8, 1.0, 1.0]
    to_check = utilities.normalize_knot_vector(input_kv)
    assert to_check == output_kv
