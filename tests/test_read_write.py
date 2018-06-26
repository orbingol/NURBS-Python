"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests file I/O operations. Requires "pytest" to run.
"""

import os
from geomdl import BSpline

FILE_NAME = 'testing'
SAMPLE_SIZE = 25
C_DEGREE = 2
C_CTRLPTS3D = [[1, 1, 0], [2, 1, -1], [2, 2, 0]]
C_KV = [0, 0, 0, 1, 1, 1]

S_DEGREE_U = 2
S_DEGREE_V = 2
S_CTRLPTS = [[0, 0, 0], [0, 1, 0], [0, 2, -3],
             [1, 0, 6], [1, 1, 0], [1, 2, 0],
             [2, 0, 0], [2, 1, 0], [2, 2, 3]]
S_KV_U = [0, 0, 0, 1, 1, 1]
S_KV_V = [0, 0, 0, 1, 1, 1]


# Tests pickled load-save operations on curves
def test_bspline_curve_loadsave():
    fname = FILE_NAME + ".pickle"

    curve_save = BSpline.Curve()
    curve_save.degree = C_DEGREE
    curve_save.ctrlpts = C_CTRLPTS3D
    curve_save.knotvector = C_KV
    curve_save.save(fname)

    curve_load = BSpline.Curve()
    curve_load.load(fname)

    # Remove save file
    os.remove(fname)

    assert curve_save.degree == curve_load.degree
    assert curve_save.knotvector == curve_load.knotvector
    assert curve_save.ctrlpts == curve_load.ctrlpts
    assert curve_save.dimension == curve_load.dimension


# Tests pickled load-save operations on surfaces
def test_bspline_surface_loadsave():
    fname = FILE_NAME + ".pickle"

    surf_save = BSpline.Surface()
    surf_save.degree_u = S_DEGREE_U
    surf_save.degree_v = S_DEGREE_V
    surf_save.ctrlpts_size_u = 3
    surf_save.ctrlpts_size_v = 3
    surf_save.ctrlpts = S_CTRLPTS
    surf_save.knotvector_u = S_KV_U
    surf_save.knotvector_v = S_KV_V
    surf_save.save(fname)

    surf_load = BSpline.Surface()
    surf_load.load(fname)

    # Remove save file
    os.remove(fname)

    assert surf_save.degree_u == surf_load.degree_u
    assert surf_save.degree_v == surf_load.degree_v
    assert surf_save.knotvector_u == surf_load.knotvector_u
    assert surf_save.knotvector_v == surf_load.knotvector_v
    assert surf_save.ctrlpts == surf_load.ctrlpts
    assert surf_save.ctrlpts_size_u == surf_load.ctrlpts_size_u
    assert surf_save.ctrlpts_size_v == surf_load.ctrlpts_size_v
    assert surf_save.dimension == surf_load.dimension
