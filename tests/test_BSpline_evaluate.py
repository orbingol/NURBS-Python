"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests B-Spline curve and surface evaluations. Requires "pytest" to run.
"""

from geomdl import BSpline


SAMPLE_SIZE = 5
C_DEGREE = 2
C_CTRLPTS2D = [[1, 1], [2, 1], [2, 2]]
C_CTRLPTS3D = [[1, 1, 0], [2, 1, -1], [2, 2, 0]]
C_KV = [0, 0, 0, 1, 1, 1]


def test_bspline_curve2d_evaluate():
    curve = BSpline.Curve()
    curve.degree = C_DEGREE
    curve.ctrlpts = C_CTRLPTS2D
    curve.knotvector = C_KV
    curve.sample_size = SAMPLE_SIZE

    # Expected output
    res = [[1.0, 1.0], [1.4375, 1.0625], [1.75, 1.25], [1.9375, 1.5625], [2.0, 2.0]]

    assert curve.evalpts == res


def test_bspline_curve3d_evaluate():
    curve = BSpline.Curve()
    curve.degree = C_DEGREE
    curve.ctrlpts = C_CTRLPTS3D
    curve.knotvector = C_KV
    curve.sample_size = SAMPLE_SIZE

    # Expected output
    res = [[1.0, 1.0, 0.0], [1.4375, 1.0625, -0.375], [1.75, 1.25, -0.5], [1.9375, 1.5625, -0.375], [2.0, 2.0, 0.0]]

    assert curve.evalpts == res
