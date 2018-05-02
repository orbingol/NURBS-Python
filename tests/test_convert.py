"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests B-Spline to NURBS conversions. Requires "pytest" to run.
"""

from geomdl import BSpline
from geomdl import convert


SAMPLE_SIZE = 5
C_DEGREE = 2
C_CTRLPTS = [[1, 1, 0], [2, 1, -1], [2, 2, 0]]
C_KV = [0, 0, 0, 1, 1, 1]

S_DEGREE_U = 2
S_DEGREE_V = 2
S_CTRLPTS = [[0, 0, 0], [0, 1, 0], [0, 2, -3],
             [1, 0, 6], [1, 1, 0], [1, 2, 0],
             [2, 0, 0], [2, 1, 0], [2, 2, 3]]
S_KV_U = [0, 0, 0, 1, 1, 1]
S_KV_V = [0, 0, 0, 1, 1, 1]


def test_convert_curve():
    curve_bs = BSpline.Curve()
    curve_bs.degree = C_DEGREE
    curve_bs.ctrlpts = C_CTRLPTS
    curve_bs.knotvector = C_KV
    curve_bs.sample_size = SAMPLE_SIZE

    curve_nurbs = convert.bspline_to_nurbs(curve_bs)
    curve_nurbs.sample_size = SAMPLE_SIZE

    # Expected weights vector
    res_weights = [1.0 for _ in range(len(C_CTRLPTS))]

    # Expected evaluation result
    res = [[1.0, 1.0, 0.0], [1.4375, 1.0625, -0.375], [1.75, 1.25, -0.5], [1.9375, 1.5625, -0.375], [2.0, 2.0, 0.0]]

    assert not curve_bs.rational
    assert curve_nurbs.rational
    assert curve_nurbs.evalpts == res
    assert curve_nurbs.weights == tuple(res_weights)


def test_convert_surface():
    surf_bs = BSpline.Surface()
    surf_bs.degree_u = S_DEGREE_U
    surf_bs.degree_v = S_DEGREE_V
    surf_bs.ctrlpts_size_u = 3
    surf_bs.ctrlpts_size_v = 3
    surf_bs.ctrlpts = S_CTRLPTS
    surf_bs.knotvector_u = S_KV_U
    surf_bs.knotvector_v = S_KV_V

    surf_nurbs = convert.bspline_to_nurbs(surf_bs)
    surf_nurbs.sample_size = SAMPLE_SIZE

    # Expected weights vector
    res_weights = [1.0 for _ in range(3*3)]

    # Expected output
    res = [[0.0, 0.0, 0.0], [0.0, 0.5, -0.1875], [0.0, 1.0, -0.75], [0.0, 1.5, -1.6875],
           [0.0, 2.0, -3.0], [0.5, 0.0, 2.25], [0.5, 0.5, 1.171875], [0.5, 1.0, 0.1875],
           [0.5, 1.5, -0.703125], [0.5, 2.0, -1.5], [1.0, 0.0, 3.0], [1.0, 0.5, 1.6875],
           [1.0, 1.0, 0.75], [1.0, 1.5, 0.1875], [1.0, 2.0, 0.0], [1.5, 0.0, 2.25],
           [1.5, 0.5, 1.359375], [1.5, 1.0, 0.9375], [1.5, 1.5, 0.984375], [1.5, 2.0, 1.5],
           [2.0, 0.0, 0.0], [2.0, 0.5, 0.1875], [2.0, 1.0, 0.75], [2.0, 1.5, 1.6875], [2.0, 2.0, 3.0]]

    assert not surf_bs.rational
    assert surf_nurbs.rational
    assert surf_nurbs.evalpts == res
    assert surf_nurbs.weights == tuple(res_weights)
