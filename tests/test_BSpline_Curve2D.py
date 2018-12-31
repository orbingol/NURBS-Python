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
    """ Creates a 3rd order 2D B-spline Curve instance """
    # Create a curve instance
    curve = BSpline.Curve()

    # Set curve degree
    curve.degree = 3

    # Set control points
    curve.ctrlpts = [[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    return curve


def test_bspline_curve_name(bs_curve):
    bs_curve.name = "Testing"
    assert bs_curve.name == "Testing"


def test_bspline_curve_degree(bs_curve):
    assert bs_curve.degree == 3


def test_bspline_curve_ctrlpts(bs_curve):
    assert bs_curve.ctrlpts == [[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]]
    assert bs_curve.dimension == 2


def test_bspline_curve_knot_vector(bs_curve):
    assert bs_curve.knotvector == [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]


def test_bspline_curve2d_eval1(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(0.0)

    # Evaluation result
    res = [5.0, 5.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_eval2(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(0.3)

    # Evaluation result
    res = [18.617, 13.377]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_eval3(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(0.5)

    # Evaluation result
    res = [27.645, 14.691]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_eval4(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(0.6)

    # Evaluation result
    res = [32.143, 14.328]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_eval5(bs_curve):
    # Evaluate curve
    evalpt = bs_curve.evaluate_single(1.0)

    # Evaluation result
    res = [50.0, 5.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_deriv1(bs_curve):
    # Take the derivative
    der1 = bs_curve.derivatives(u=0.35, order=2)
    bs_curve.evaluator = evaluators.CurveEvaluator2()
    der2 = bs_curve.derivatives(u=0.35, order=2)

    assert abs(der1[0][0] - der2[0][0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - der2[0][1]) < GEOMDL_DELTA
    assert abs(der1[1][0] - der2[1][0]) < GEOMDL_DELTA
    assert abs(der1[1][1] - der2[1][1]) < GEOMDL_DELTA
    assert abs(der1[2][0] - der2[2][0]) < GEOMDL_DELTA
    assert abs(der1[2][1] - der2[2][1]) < GEOMDL_DELTA


def test_bspline_curve2d_deriv2(bs_curve):
    # Take the derivative
    evalpt = bs_curve.evaluate_single(0.35)
    der1 = bs_curve.derivatives(u=0.35)
    bs_curve.evaluator = evaluators.CurveEvaluator2()
    der2 = bs_curve.derivatives(u=0.35)

    assert abs(der1[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - evalpt[1]) < GEOMDL_DELTA
    assert abs(der2[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der2[0][1] - evalpt[1]) < GEOMDL_DELTA


def test_bspline_curve2d_insert_knot1(bs_curve):
    # Set evaluation parameter
    u = 0.3

    # Insert knot
    bs_curve.insert_knot(u)

    # Evaluate curve at the given parameter
    evalpt = bs_curve.evaluate_single(u)

    # Evaluation result
    res = [18.617, 13.377]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_insert_knot2(bs_curve):
    # Set evaluation parameter
    u = 0.6

    # Insert knot
    bs_curve.insert_knot(u)

    # Evaluate curve at the given parameter
    evalpt = bs_curve.evaluate_single(u)

    # Evaluation result
    res = [32.143, 14.328]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_insert_knot3(bs_curve):
    # Set evaluation parameter
    u = 0.6

    # Insert knot
    bs_curve.insert_knot(u, r=2)

    # Evaluate curve at the given parameter
    evalpt = bs_curve.evaluate_single(u)

    # Evaluation result
    res = [32.143, 14.328]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_insert_knot4(bs_curve):
    # Set evaluation parameter
    u = 0.6

    # Insert knot
    bs_curve.insert_knot(u, r=2)

    assert bs_curve.knotvector[5] == u
