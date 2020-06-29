"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Tests visualization utility functions. Requires "pytest" to run.
"""

from geomdl.visualization import visutils


def test_color_generator():
    seed = 17  # some number to be used as the random seed
    result = visutils.color_generator(seed)
    to_check = visutils.color_generator(seed)
    assert to_check == result
