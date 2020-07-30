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
from geomdl import convert
from geomdl import operations
from geomdl import linalg

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
    spline_curve.insert_knot(param, num=num_insert)
    s_post = helpers.find_multiplicity(param, spline_curve.knotvector)
    evalpt = spline_curve.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert s_pre + num_insert == s_post


def test_bspline_curve2d_insert_knot_kv(spline_curve):
    spline_curve.insert_knot(0.66, num=2)
    s = helpers.find_multiplicity(0.66, spline_curve.knotvector)

    assert spline_curve.knotvector[5] == 0.66
    assert s == 3


@mark.parametrize("param, num_remove", [
    (0.33, 1),
    (0.66, 1)
])
def test_bspline_curve2d_remove_knot(spline_curve, param, num_remove):
    s_pre = helpers.find_multiplicity(param, spline_curve.knotvector)
    c_pre = spline_curve.ctrlpts_size
    spline_curve.remove_knot(param, num=num_remove)
    s_post = helpers.find_multiplicity(param, spline_curve.knotvector)
    c_post = spline_curve.ctrlpts_size

    assert c_pre - num_remove == c_post
    assert s_pre - num_remove == s_post


def test_bspline_curve2d_remove_knot_kv(spline_curve):
    spline_curve.remove_knot(0.66, num=1)
    s = helpers.find_multiplicity(0.66, spline_curve.knotvector)

    assert 0.66 not in spline_curve.knotvector
    assert s == 0


@mark.parametrize("density, kv", [
    (0, [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]),
    (1, [0.0, 0.0, 0.0, 0.0, 0.165, 0.165, 0.165, 0.33, 0.33, 0.33, 0.495, 0.495, 0.495, 0.66, 0.66, 0.66, 0.830, 0.830, 0.830, 1.0, 1.0, 1.0, 1.0]),
])
def test_bspline_curve2d_knot_refine(spline_curve, density, kv):
    operations.refine_knotvector(spline_curve, [density])
    for a, b in zip(kv, spline_curve.knotvector):
        assert abs(a - b) < GEOMDL_DELTA


def test_bspline_curve2d_degree_elevate_degree(spline_curve):
    dops = 1
    degree_new = spline_curve.degree + dops
    operations.degree_operations(spline_curve, [dops])
    assert spline_curve.degree == degree_new


def test_bspline_curve2d_degree_elevate_ctrlpts_size(spline_curve):
    dops = 1
    ctrlpts_size = spline_curve.ctrlpts_size + dops
    operations.degree_operations(spline_curve, [dops])
    assert spline_curve.ctrlpts_size == ctrlpts_size


def test_bspline_curve2d_degree_reduce_degree(spline_curve):
    dops = -1
    degree_new = spline_curve.degree + dops
    operations.degree_operations(spline_curve, [dops])
    assert spline_curve.degree == degree_new


def test_bspline_curve2d_degree_reduce_ctrlpts_size(spline_curve):
    dops = -1
    ctrlpts_size_new = spline_curve.ctrlpts_size + dops
    operations.degree_operations(spline_curve, [dops])
    assert spline_curve.ctrlpts_size == ctrlpts_size_new


@fixture
def spline_curve3d(spline_curve):
    curve3d = operations.add_dimension(spline_curve, offset=1.0)
    return curve3d


def test_bspline_curve3d_ctrlpts(spline_curve3d):
    assert spline_curve3d.ctrlpts == [[5.0, 5.0, 1.0], [10.0, 10.0, 1.0], [20.0, 15.0, 1.0], [35.0, 15.0, 1.0], [45.0, 10.0, 1.0], [50.0, 5.0, 1.0]]
    assert spline_curve3d.dimension == 3


@fixture
def nurbs_curve(spline_curve):
    curve = convert.bspline_to_nurbs(spline_curve)
    curve.weights = [0.5, 1.0, 0.75, 1.0, 0.25, 1.0]
    return curve


def test_nurbs_curve2d_weights(nurbs_curve):
    assert nurbs_curve.weights == [0.5, 1.0, 0.75, 1.0, 0.25, 1.0]


@mark.parametrize("param, res", [
    (0.0, (5.0, 5.0)),
    (0.2, (13.8181, 11.5103)),
    (0.5, (28.1775, 14.7858)),
    (0.95, (48.7837, 6.0022))
])
def test_nurbs_curve2d_eval(nurbs_curve, param, res):
    evalpt = nurbs_curve.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


@mark.parametrize("param, order, res", [
    (0.0, 1, ((5.0, 5.0), (90.9090, 90.9090))),
    (0.2, 2, ((13.8181, 11.5103), (40.0602, 17.3878), (104.4062, -29.3672))),
    (0.5, 3, ((28.1775, 14.7858), (39.7272, 2.2562), (-116.9254, -49.7367), (125.5276, 196.8865))),
    (0.95, 1, ((48.7837, 6.0022), (39.5178, -29.9962)))
])
def test_nurbs_curve2d_deriv(nurbs_curve, param, order, res):
    deriv = nurbs_curve.derivatives(u=param, order=order)

    for computed, expected in zip(deriv, res):
        for c, e in zip(computed, expected):
            assert abs(c - e) < GEOMDL_DELTA


@fixture
def spline_curve_kv_norm1():
    """ Creates a spline Curve with knot vector normalization """
    curve = BSpline.Curve(normalize_kv=True)
    curve.degree = 3
    curve.ctrlpts = [[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]]
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    return curve


@mark.parametrize("param, res", [
    (0.0, (5.0, 5.0)),
    (0.33333, (19.9998, 13.7499)),
    (0.5, (27.5, 14.687)),
    (0.66666, (34.9997, 13.75)),
    (1.0, (50.0, 5.0))
])
def test_bspline_curve2d_eval_kv_norm1(spline_curve_kv_norm1, param, res):
    evalpt = spline_curve_kv_norm1.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


@fixture
def spline_curve_kv_norm2():
    """ Creates a spline Curve without knot vector normalization """
    curve = BSpline.Curve(normalize_kv=False)
    curve.degree = 3
    curve.ctrlpts = [[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]]
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    return curve


@mark.parametrize("param, res", [
    (0.0, (5.0, 5.0)),
    (1.0, (19.9998, 13.7499)),
    (1.5, (27.5, 14.687)),
    (2.0, (34.9997, 13.75)),
    (3.0, (50.0, 5.0))
])
def test_bspline_curve2d_eval_kv_norm2(spline_curve_kv_norm2, param, res):
    evalpt = spline_curve_kv_norm2.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
