"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2019 Onur Rauf Bingol

    Requires "pytest" to run.
"""

from pytest import fixture, mark
from geomdl import BSpline
from geomdl import evaluators
from geomdl import helpers

GEOMDL_DELTA = 0.001


@fixture
def spline_curve():
    """ Creates a spline Curve """
    curve = BSpline.Curve()
    curve.degree = 3
    curve.ctrlpts = [[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]]
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    return curve


def test_bspline_curve_name(spline_curve):
    spline_curve.name = "Curve Testing"
    assert spline_curve.name == "Curve Testing"


def test_bspline_curve_degree(spline_curve):
    assert spline_curve.degree == 3


def test_bspline_curve_ctrlpts(spline_curve):
    assert spline_curve.ctrlpts == [[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]]
    assert spline_curve.dimension == 2


def test_bspline_curve_knot_vector(spline_curve):
    assert spline_curve.knotvector == [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]


@mark.parametrize("param, res", [
    (0.0, (5.0, 5.0)),
    (0.3, (18.617, 13.377)),
    (0.5, (27.645, 14.691)),
    (0.6, (32.143, 14.328)),
    (1.0, (50.0, 5.0))
])
def test_bspline_curve2d_eval(spline_curve, param, res):
    evalpt = spline_curve.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_bspline_curve2d_deriv(spline_curve):
    der1 = spline_curve.derivatives(u=0.35, order=2)
    spline_curve.evaluator = evaluators.CurveEvaluator2()
    der2 = spline_curve.derivatives(u=0.35, order=2)

    assert abs(der1[0][0] - der2[0][0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - der2[0][1]) < GEOMDL_DELTA
    assert abs(der1[1][0] - der2[1][0]) < GEOMDL_DELTA
    assert abs(der1[1][1] - der2[1][1]) < GEOMDL_DELTA
    assert abs(der1[2][0] - der2[2][0]) < GEOMDL_DELTA
    assert abs(der1[2][1] - der2[2][1]) < GEOMDL_DELTA


def test_bspline_curve2d_deriv_eval(spline_curve):
    evalpt = spline_curve.evaluate_single(0.35)
    der1 = spline_curve.derivatives(u=0.35)
    spline_curve.evaluator = evaluators.CurveEvaluator2()
    der2 = spline_curve.derivatives(u=0.35)

    assert abs(der1[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - evalpt[1]) < GEOMDL_DELTA
    assert abs(der2[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der2[0][1] - evalpt[1]) < GEOMDL_DELTA


@mark.parametrize("param, num_insert, res", [
    (0.3, 1, (18.617, 13.377)),
    (0.6, 1, (32.143, 14.328)),
    (0.6, 2, (32.143, 14.328))
])
def test_bspline_curve2d_insert_knot(spline_curve, param, num_insert, res):
    s_pre = helpers.find_multiplicity(param, spline_curve.knotvector)
    spline_curve.insert_knot(param, r=num_insert)
    s_post = helpers.find_multiplicity(param, spline_curve.knotvector)
    evalpt = spline_curve.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert s_pre + num_insert == s_post


def test_bspline_curve2d_insert_knot_kv(spline_curve):
    spline_curve.insert_knot(0.66, r=2)
    s = helpers.find_multiplicity(0.66, spline_curve.knotvector)

    assert spline_curve.knotvector[5] == 0.66
    assert s == 3
