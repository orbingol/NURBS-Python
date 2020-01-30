"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

from pytest import fixture, mark
from geomdl import BSpline
from geomdl import evaluators

GEOMDL_DELTA = 0.001


@fixture
def bsplcurve():
    """ Creates a spline Curve """
    curve = BSpline.Curve()
    curve.degree = 3
    curve.set_ctrlpts([[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]])
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    return curve


def test_bsplcurve_name(bsplcurve):
    bsplcurve.name = "Curve Testing"
    assert bsplcurve.name == "Curve Testing"


def test_bsplcurve_degree(bsplcurve):
    assert bsplcurve.degree[0] == 3


def test_bsplcurve_ctrlpts(bsplcurve):
    assert all([x == y for x, y in zip(bsplcurve.ctrlpts[4], [45.0, 10.0])])
    assert all([x == y for x, y in zip(bsplcurve.ctrlpts[2], [20.0, 15.0])])
    assert bsplcurve.dimension == 2


def test_bsplcurve_knot_vector(bsplcurve):
    assert all([x == y for x, y in zip(bsplcurve.knotvector[0], [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0])])


@mark.parametrize("param, res", [
    (0.0, (5.0, 5.0)),
    (0.3, (18.617, 13.377)),
    (0.5, (27.645, 14.691)),
    (0.6, (32.143, 14.328)),
    (1.0, (50.0, 5.0))
])
def test_bsplcurve2d_eval(bsplcurve, param, res):
    evalpt = bsplcurve.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


@mark.parametrize("param", [0.11, 0.35, 0.67, 0.99])
def test_bsplcurve2d_deriv(bsplcurve, param):
    der1 = bsplcurve.derivatives(param=(param,), order=2)
    bsplcurve.evaluator = evaluators.CurveEvaluator2()
    der2 = bsplcurve.derivatives(param=(param,), order=2)

    assert abs(der1[0][0] - der2[0][0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - der2[0][1]) < GEOMDL_DELTA
    assert abs(der1[1][0] - der2[1][0]) < GEOMDL_DELTA
    assert abs(der1[1][1] - der2[1][1]) < GEOMDL_DELTA
    assert abs(der1[2][0] - der2[2][0]) < GEOMDL_DELTA
    assert abs(der1[2][1] - der2[2][1]) < GEOMDL_DELTA


@mark.parametrize("param", [0.11, 0.35, 0.67, 0.99])
def test_bsplcurve2d_deriv_eval(bsplcurve, param):
    evalpt = bsplcurve.evaluate_single(param)
    der1 = bsplcurve.derivatives(param=param)
    bsplcurve.evaluator = evaluators.CurveEvaluator2()
    der2 = bsplcurve.derivatives(param=param)

    assert abs(der1[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - evalpt[1]) < GEOMDL_DELTA
    assert abs(der2[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der2[0][1] - evalpt[1]) < GEOMDL_DELTA
