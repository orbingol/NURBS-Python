"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.NURBS.Curve module. Requires "pytest" to run.
"""

import pytest
from geomdl import NURBS

GEOMDL_DELTA = 0.001


@pytest.fixture
def ns_curve():
    # Create a curve instance
    curve = NURBS.Curve()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlptsw = [[5.0, 15.0, 0.0, 1.0], [10.0, 25.0, 5.0, 1.0], [20.0, 20.0, 10.0, 1.0], [15.0, -5.0, 15.0, 1.0],
                      [7.5, 10.0, 20.0, 1.0], [12.5, 15.0, 25.0, 1.0], [15.0, 0.0, 30.0, 1.0], [5.0, -10.0, 35.0, 1.0],
                      [10.0, 15.0, 40.0, 1.0], [5.0, 15.0, 30.0, 1.0]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    return curve


@pytest.fixture
def ns_curve2():
    # Create a curve instance
    curve = NURBS.Curve()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = [[5.0, 15.0, 0.0, 0.1], [10.0, 25.0, 5.0, 0.2], [20.0, 20.0, 10.0, 1.0], [15.0, -5.0, 15.0, 1.0],
                      [7.5, 10.0, 20.0, 1.0], [12.5, 15.0, 25.0, 1.0], [15.0, 0.0, 30.0, 0.5], [5.0, -10.0, 35.0, 1.0],
                      [10.0, 15.0, 40.0, 0.7], [5.0, 15.0, 30.0, 1.0], [15.0, 20.0, 40.0, 1.0]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    return curve


def test_nurbs_curve3d_eval1(ns_curve):
    # Evaluate curve
    evalpt = ns_curve.evaluate_single(0.0)

    # Evaluation result
    res = [5.0, 15.0, 0.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval2(ns_curve):
    # Evaluate curve
    evalpt = ns_curve.evaluate_single(0.2)

    # Evaluation result
    res = [15.727, 6.509, 13.692]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval3(ns_curve):
    # Evaluate curve
    evalpt = ns_curve.evaluate_single(0.5)

    # Evaluation result
    res = [10.476, 11.071, 22.5]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval4(ns_curve):
    # Evaluate curve
    evalpt = ns_curve.evaluate_single(0.8)

    # Evaluation result
    res = [10.978, -1.349, 31.307]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval5(ns_curve):
    # Evaluate curve
    evalpt = ns_curve.evaluate_single(1.0)

    # Evaluation result
    res = [5.0, 15.0, 30.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval6(ns_curve2):
    # Evaluate curve
    evalpt = ns_curve2.evaluate_single(0.0)

    # Evaluation result
    res = [50.0, 150.0, 0.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval7(ns_curve2):
    # Evaluate curve
    evalpt = ns_curve2.evaluate_single(0.2)

    # Evaluation result
    res = [14.297, 5.130, 15.395]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval8(ns_curve2):
    # Evaluate curve
    evalpt = ns_curve2.evaluate_single(0.7)

    # Evaluation result
    res = [14.735, -0.255, 41.088]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval9(ns_curve2):
    # Evaluate curve
    evalpt = ns_curve2.evaluate_single(0.1)

    # Evaluation result
    res = [19.514, 17.411, 12.515]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval10(ns_curve2):
    # Evaluate curve
    evalpt = ns_curve2.evaluate_single(0.5)

    # Evaluation result
    res = [13.421, 10.976, 28.329]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_deriv1(ns_curve2):
    # Evaluate curve
    ept = ns_curve2.evaluate_single(0.35)

    # Take the derivative
    der = ns_curve2.derivatives(u=0.35, order=7)

    assert abs(ept[0] - der[0][0]) < GEOMDL_DELTA
    assert abs(ept[1] - der[0][1]) < GEOMDL_DELTA
    assert abs(ept[2] - der[0][2]) < GEOMDL_DELTA


def test_nurbs_curve3d_insert_knot1(ns_curve2):
    # Set evaluation parameter
    u = 0.5

    # Insert knot
    ns_curve2.insert_knot(u)

    # Evaluate curve at the given parameter
    evalpt = ns_curve2.evaluate_single(u)

    # Evaluation result
    res = [13.421, 10.976, 28.329]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_insert_knot2(ns_curve2):
    # Set evaluation parameter
    u = 0.5

    # Insert knot
    ns_curve2.insert_knot(u, 3)

    # Evaluate curve at the given parameter
    evalpt = ns_curve2.evaluate_single(u)

    # Evaluation result
    res = [13.421, 10.976, 28.329]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA
