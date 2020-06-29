"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from geomdl import BSpline, NURBS
from geomdl.evaluators import default2

GEOMDL_DELTA = 0.001


@pytest.mark.usefixtures("curve7")
def test_bsplcurve_name(curve7):
    curve7.name = "Curve Testing"
    assert curve7.name == "Curve Testing"


@pytest.mark.usefixtures("curve7")
def test_bsplcurve_degree(curve7):
    assert curve7.degree[0] == 3


@pytest.mark.usefixtures("curve7")
def test_bsplcurve_ctrlpts(curve7):
    assert all([x == y for x, y in zip(curve7.ctrlpts[4], [45.0, 10.0])])
    assert all([x == y for x, y in zip(curve7.ctrlpts[2], [20.0, 15.0])])
    assert curve7.dimension == 2


@pytest.mark.usefixtures("curve7")
def test_bsplcurve_knot_vector(curve7):
    assert all([x == y for x, y in zip(curve7.knotvector[0], [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0])])


@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("param, res", [
    (0.0, (5.0, 5.0)),
    (0.3, (18.617, 13.377)),
    (0.5, (27.645, 14.691)),
    (0.6, (32.143, 14.328)),
    (1.0, (50.0, 5.0))
])
def test_bsplcurve2d_eval(curve7, param, res):
    evalpt = curve7.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("param", [0.11, 0.35, 0.67, 0.99])
def test_bsplcurve2d_deriv(curve7, param):
    der1 = curve7.derivatives(param=(param,), order=2)
    curve7.evaluator = default2.CurveEvaluator2()
    der2 = curve7.derivatives(param=(param,), order=2)

    assert abs(der1[0][0] - der2[0][0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - der2[0][1]) < GEOMDL_DELTA
    assert abs(der1[1][0] - der2[1][0]) < GEOMDL_DELTA
    assert abs(der1[1][1] - der2[1][1]) < GEOMDL_DELTA
    assert abs(der1[2][0] - der2[2][0]) < GEOMDL_DELTA
    assert abs(der1[2][1] - der2[2][1]) < GEOMDL_DELTA


@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("param", [0.11, 0.35, 0.67, 0.99])
def test_bsplcurve2d_deriv_eval(curve7, param):
    evalpt = curve7.evaluate_single(param)
    der1 = curve7.derivatives(param=param)
    curve7.evaluator = default2.CurveEvaluator2()
    der2 = curve7.derivatives(param=param)

    assert abs(der1[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - evalpt[1]) < GEOMDL_DELTA
    assert abs(der2[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der2[0][1] - evalpt[1]) < GEOMDL_DELTA


@pytest.mark.usefixtures("curve7")
def test_bsplcurve2d_to_nurbs(curve7):
    nbcurve = NURBS.Curve.from_bspline(curve7)
    assert all([x == 1.0 for x in nbcurve.weights])


@pytest.mark.usefixtures("curve8")
def test_nbcurve2d_weights(curve8):
    assert all([x == y for x, y in zip(curve8.weights, [1.0, 1.0, 0.75, 1.0, 0.25, 0.4])])


@pytest.mark.usefixtures("curve8")
def test_nbcurve2d_ctrlpts(curve8):
    for pta, ptb in zip(curve8.ctrlpts, [[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]]):
        assert all([x == y for x, y in zip(pta, ptb)])


@pytest.mark.usefixtures("curve8")
def test_nbcurve2d_ctrlptsw(curve8):
    ctrlptsw = [[c * w for c in pt] + [w] for pt, w in zip([[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]], [1.0, 1.0, 0.75, 1.0, 0.25, 0.4])]
    for pta, ptb in zip(curve8.ctrlptsw, ctrlptsw):
        assert all([x == y for x, y in zip(pta, ptb)])
