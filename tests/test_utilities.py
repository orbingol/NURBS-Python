"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.utilities module. Requires "pytest" to run.
"""

from geomdl import utilities


def test_color_generator():
    seed = 17  # some number to be used as the random seed
    result = utilities.color_generator(seed)
    to_check = utilities.color_generator(seed)
    assert to_check == result
