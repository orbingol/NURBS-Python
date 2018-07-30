"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.BSpline.Curve module. Requires "pytest" to run.
"""
from geomdl import BSpline
from geomdl import evaluators

GEOMDL_DELTA = 0.001
OBJECT_INSTANCE = BSpline.Curve
CONTROL_POINTS = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
                  [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]


def test_bspline_curve3d_eval1():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.0)

    # Evaluation result
    res = [5.0, 15.0, 0.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_eval2():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.2)

    # Evaluation result
    res = [15.727, 6.509, 13.692]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_eval3():
    # Create an object instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.5)

    # Evaluation result
    res = [10.476, 11.071, 22.499]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_eval4():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.8)

    # Evaluation result
    res = [10.978, -1.349, 31.307]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_eval5():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(1.0)

    # Evaluation result
    res = [5.0, 15.0, 30.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_bbox():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate bounding box
    to_check = curve.bbox

    # Evaluation result
    result = ((5.0, -10.0, 0.0), (20.0, 25.0, 40.0))

    assert abs(to_check[0][0] - result[0][0]) < GEOMDL_DELTA
    assert abs(to_check[0][1] - result[0][1]) < GEOMDL_DELTA
    assert abs(to_check[0][2] - result[0][2]) < GEOMDL_DELTA
    assert abs(to_check[1][0] - result[1][0]) < GEOMDL_DELTA
    assert abs(to_check[1][1] - result[1][1]) < GEOMDL_DELTA
    assert abs(to_check[1][2] - result[1][2]) < GEOMDL_DELTA


def test_bspline_curve3d_deriv1():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Take the derivative
    der1 = curve.derivatives(u=0.35, order=5)
    curve.evaluator = evaluators.CurveEvaluator2()
    der2 = curve.derivatives(u=0.35, order=5)

    assert abs(der1[0][0] - der2[0][0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - der2[0][1]) < GEOMDL_DELTA
    assert abs(der1[0][2] - der2[0][2]) < GEOMDL_DELTA
    assert abs(der1[1][0] - der2[1][0]) < GEOMDL_DELTA
    assert abs(der1[1][1] - der2[1][1]) < GEOMDL_DELTA
    assert abs(der1[1][2] - der2[1][2]) < GEOMDL_DELTA
    assert abs(der1[2][0] - der2[2][0]) < GEOMDL_DELTA
    assert abs(der1[2][1] - der2[2][1]) < GEOMDL_DELTA
    assert abs(der1[2][2] - der2[2][2]) < GEOMDL_DELTA


def test_bspline_curve3d_deriv2():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Take the derivative
    evalpt = curve.curvept(u=0.35)
    der1 = curve.derivatives(u=0.35)
    curve.evaluator = evaluators.CurveEvaluator2()
    der2 = curve.derivatives(u=0.35)

    assert abs(der1[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der1[0][1] - evalpt[1]) < GEOMDL_DELTA
    assert abs(der1[0][2] - evalpt[2]) < GEOMDL_DELTA
    assert abs(der2[0][0] - evalpt[0]) < GEOMDL_DELTA
    assert abs(der2[0][1] - evalpt[1]) < GEOMDL_DELTA
    assert abs(der2[0][2] - evalpt[2]) < GEOMDL_DELTA


def test_bspline_curve3d_insert_knot1():
    # Create an object instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set evaluation parameter
    u = 0.5

    # Insert knot
    curve.insert_knot(u)

    # Evaluate curve at the given parameter
    evalpt = curve.curvept(u)

    # Evaluation result
    res = [10.476, 11.071, 22.499]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_insert_knot2():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Insert knot at u = 0.5
    curve.insert_knot(0.5)

    # Evaluate curve at u = 0.8
    evalpt = curve.curvept(0.8)

    # Evaluation result
    res = [10.978, -1.349, 31.307]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_insert_knot3():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Insert knot at u = 0.5
    curve.insert_knot(0.5, 2)

    # Evaluate curve at u = 0.8
    evalpt = curve.curvept(0.8)

    # Evaluation result
    res = [10.978, -1.349, 31.307]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_curve3d_insert_knot4():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Insert knot at u = 0.5
    curve.insert_knot(0.5, 2)

    assert curve.knotvector[6] == 0.3
    assert curve.knotvector[7] == 0.5
    assert curve.knotvector[8] == 0.5
    assert curve.knotvector[10] == 0.7
