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
def nurbs_curve():
    """ Creates a 4th order 2D NURBS Curve instance """
    # Create a curve instance
    curve = NURBS.Curve()

    # Set curve degree
    curve.degree = 3

    # Set weighted control points
    curve.ctrlptsw = [[5.0, 5.0, 1.0], [10.0, 10.0, 1.0], [20.0, 15.0, 1.0],
                      [35.0, 15.0, 1.0], [45.0, 10.0, 1.0], [50.0, 5.0, 1.0]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    return curve


@pytest.fixture
def nurbs_curve2():
    """ Creates a 5th order 2D NURBS Curve instance """
    # Create a curve instance
    curve = NURBS.Curve()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlptsw = [[5.0, 5.0, 0.5], [10.0, 10.0, 1.0], [20.0, 15.0, 0.1],
                      [35.0, 15.0, 0.25], [45.0, 10.0, 1.0], [50.0, 5.0, 1.0], [55.0, 15.0, 0.5]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0, 1.0]

    return curve


def test_nurbs_curve2d_name_property(nurbs_curve):
    default_name = "Curve"
    assert nurbs_curve.name == default_name
    assert str(nurbs_curve) == default_name


def test_nurbs_curve2d_eval1(nurbs_curve):
    # Evaluate curve
    evalpt = nurbs_curve.curvept(0.0)

    # Evaluation result
    res = [5.0, 5.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval2(nurbs_curve):
    # Evaluate curve
    evalpt = nurbs_curve.curvept(0.3)

    # Evaluation result
    res = [18.617, 13.377]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval3(nurbs_curve):
    # Evaluate curve
    evalpt = nurbs_curve.curvept(0.5)

    # Evaluation result
    res = [27.645, 14.691]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval4(nurbs_curve):
    # Evaluate curve
    evalpt = nurbs_curve.curvept(0.6)

    # Evaluation result
    res = [32.143, 14.328]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval5(nurbs_curve):
    # Evaluate curve
    evalpt = nurbs_curve.curvept(1.0)

    # Evaluation result
    res = [50.0, 5.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval6(nurbs_curve2):
    # Evaluate curve
    evalpt = nurbs_curve2.curvept(0.0)

    # Evaluation result
    res = [10.0, 10.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval7(nurbs_curve2):
    # Evaluate curve
    evalpt = nurbs_curve2.curvept(0.2)

    # Evaluation result
    res = [33.304, 24.593]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval8(nurbs_curve2):
    # Evaluate curve
    evalpt = nurbs_curve2.curvept(0.7)

    # Evaluation result
    res = [54.345, 13.347]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval9(nurbs_curve2):
    # Evaluate curve
    evalpt = nurbs_curve2.curvept(0.1)

    # Evaluation result
    res = [15.675, 13.915]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval10(nurbs_curve2):
    # Evaluate curve
    evalpt = nurbs_curve2.curvept(0.5)

    # Evaluation result
    res = [80.474, 32.359]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_insert_knot1(nurbs_curve2):
    # Set evaluation parameter
    u = 0.2

    # Insert knot
    nurbs_curve2.insert_knot(u)

    # Evaluate curve at the given parameter
    evalpt = nurbs_curve2.curvept(u)

    # Evaluation result
    res = [33.304, 24.593]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_insert_knot2(nurbs_curve2):
    # Set evaluation parameter
    u = 0.2

    # Insert knot
    nurbs_curve2.insert_knot(u, 3)

    # Evaluate curve at the given parameter
    evalpt = nurbs_curve2.curvept(u)

    # Evaluation result
    res = [33.304, 24.593]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
