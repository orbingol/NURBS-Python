"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.BSpline.Curve module. Requires "pytest" to run.
"""

import pytest
from geomdl import BSpline
from geomdl import evaluators

GEOMDL_DELTA = 0.001


@pytest.fixture
def bs_curve():
    """ Creates a 4th order 3D B-spline Curve instance """
    # Create a curve instance
    curve = BSpline.Curve()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
                  [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    return curve


def test_bspline_curve3d_eval1(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(0.0)

    # Evaluation result
    res = [5.0, 15.0, 0.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_eval2(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(0.2)

    # Evaluation result
    res = [15.727, 6.509, 13.692]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_eval3(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(0.5)

    # Evaluation result
    res = [10.476, 11.071, 22.499]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_eval4(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(0.8)

    # Evaluation result
    res = [10.978, -1.349, 31.307]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_eval5(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(1.0)

    # Evaluation result
    res = [5.0, 15.0, 30.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_bbox(bs_curve):
    # Evaluate bounding box
    to_check = bs_curve.bbox

    # Evaluation result
    result = ((5.0, -10.0, 0.0), (20.0, 25.0, 40.0))

    assert abs(to_check[0][0] - result[0][0]) < GEOMDL_DELTA
    assert abs(to_check[0][1] - result[0][1]) < GEOMDL_DELTA
    assert abs(to_check[0][2] - result[0][2]) < GEOMDL_DELTA
    assert abs(to_check[1][0] - result[1][0]) < GEOMDL_DELTA
    assert abs(to_check[1][1] - result[1][1]) < GEOMDL_DELTA
    assert abs(to_check[1][2] - result[1][2]) < GEOMDL_DELTA


def test_bspline_curve3d_deriv1(bs_curve):
    # Take the derivative
    der1 = bs_curve.derivatives(u=0.35, order=5)
    bs_curve.evaluator = evaluators.CurveEvaluator2()
    der2 = bs_curve.derivatives(u=0.35, order=5)

    assert abs(der1[0][0] - der2[0][0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - der2[0][1]) < GEOMDL_DELTA
    assert abs(der1[0][2] - der2[0][2]) < GEOMDL_DELTA
    assert abs(der1[1][0] - der2[1][0]) < GEOMDL_DELTA
    assert abs(der1[1][1] - der2[1][1]) < GEOMDL_DELTA
    assert abs(der1[1][2] - der2[1][2]) < GEOMDL_DELTA
    assert abs(der1[2][0] - der2[2][0]) < GEOMDL_DELTA
    assert abs(der1[2][1] - der2[2][1]) < GEOMDL_DELTA
    assert abs(der1[2][2] - der2[2][2]) < GEOMDL_DELTA


def test_bspline_curve3d_deriv2(bs_curve):
    # Take the derivative
    evalpt = bs_curve.evaluate_single(0.35)
    der1 = bs_curve.derivatives(u=0.35)
    bs_curve.evaluator = evaluators.CurveEvaluator2()
    der2 = bs_curve.derivatives(u=0.35)

    assert abs(der1[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - evalpt[1]) < GEOMDL_DELTA
    assert abs(der1[0][2] - evalpt[2]) < GEOMDL_DELTA
    assert abs(der2[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der2[0][1] - evalpt[1]) < GEOMDL_DELTA
    assert abs(der2[0][2] - evalpt[2]) < GEOMDL_DELTA


def test_bspline_curve3d_insert_knot1(bs_curve):
    # Set evaluation parameter
    u = 0.5

    # Insert knot
    bs_curve.insert_knot(u)

    # Evaluate curve at the given parameter
    evalpt = bs_curve.evaluate_single(u)

    # Evaluation result
    res = [10.476, 11.071, 22.499]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_insert_knot2(bs_curve):
    # Insert knot at u = 0.5
    bs_curve.insert_knot(0.5)

    # Evaluate curve at u = 0.8
    evalpt = bs_curve.evaluate_single(0.8)

    # Evaluation result
    res = [10.978, -1.349, 31.307]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_insert_knot3(bs_curve):
    bs_curve.insert_knot(0.5, r=2)

    # Evaluate curve at u = 0.8
    evalpt = bs_curve.evaluate_single(0.8)

    # Evaluation result
    res = [10.978, -1.349, 31.307]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_insert_knot4(bs_curve):
    # Insert knot at u = 0.5
    bs_curve.insert_knot(0.5, r=2)

    assert bs_curve.knotvector[6] == 0.3
    assert bs_curve.knotvector[7] == 0.5
    assert bs_curve.knotvector[8] == 0.5
    assert bs_curve.knotvector[10] == 0.7
