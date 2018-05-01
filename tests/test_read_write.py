"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests pickled load and save operations. Requires "pytest" to run.
"""

import os
from geomdl import BSpline

FILE_NAME = 'testing.pickle'
SAMPLE_SIZE = 5
C_DEGREE = 2
C_CTRLPTS3D = [[1, 1, 0], [2, 1, -1], [2, 2, 0]]
C_KV = [0, 0, 0, 1, 1, 1]


def test_bspline_curve_loadsave():
    curve_save = BSpline.Curve()
    curve_save.degree = C_DEGREE
    curve_save.ctrlpts = C_CTRLPTS3D
    curve_save.knotvector = C_KV
    curve_save.save(FILE_NAME)

    curve_load = BSpline.Curve()
    curve_load.load(FILE_NAME)

    # Remove save file
    os.remove(FILE_NAME)

    assert curve_save.degree == curve_load.degree
    assert curve_save.knotvector == curve_load.knotvector
    assert curve_save.ctrlpts == curve_load.ctrlpts
    assert curve_save.dimension == curve_load.dimension
