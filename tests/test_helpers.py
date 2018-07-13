"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.helpers module.
"""

from geomdl import helpers

GEOMDL_DELTA = 10e-8

def test_basis_function_one():
	degree = 2
	knot_vector = [0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 5]
	knot = 5. / 2.
	span = 3

	to_check = helpers.basis_function_one(degree, knot_vector, span, knot)
	result = 0.75

	assert to_check == result

def test_basis_function_ders_one():
	degree = 2
	knot_vector = [0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 5]
	knot = 5. / 2.
	span = 4

	to_check = helpers.basis_function_ders_one(degree, knot_vector, 4, knot, 2)
	result = [0.125, 0.5, 1.0]

	assert to_check == result
