"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.NURBS.Curve module. Requires "pytest" to run.
"""
from geomdl import NURBS

GEOMDL_DELTA = 0.001
OBJECT_INSTANCE = NURBS.Curve
CONTROL_POINTS = [[5.0, 5.0, 1.0], [10.0, 10.0, 1.0], [20.0, 15.0, 1.0], [35.0, 15.0, 1.0], [45.0, 10.0, 1.0],
                  [50.0, 5.0, 1.0]]
CONTROL_POINTS2 = [[5.0, 5.0, 0.5], [10.0, 10.0, 1.0], [20.0, 15.0, 0.1], [35.0, 15.0, 0.25], [45.0, 10.0, 1.0],
                   [50.0, 5.0, 1.0], [55.0, 15.0, 0.5]]


def test_nurbs_curve2d_eval1():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 3

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.0)

    # Evaluation result
    res = [5.0, 5.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval2():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 3

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.3)

    # Evaluation result
    res = [18.617, 13.377]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval3():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 3

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.5)

    # Evaluation result
    res = [27.645, 14.691]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval4():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 3

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.6)

    # Evaluation result
    res = [32.143, 14.328]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval5():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 3

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(1.0)

    # Evaluation result
    res = [50.0, 5.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval6():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.0)

    # Evaluation result
    res = [10.0, 10.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval7():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.2)

    # Evaluation result
    res = [33.304, 24.593]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval8():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.7)

    # Evaluation result
    res = [54.345, 13.347]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval9():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.1)

    # Evaluation result
    res = [15.675, 13.915]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_eval10():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.5)

    # Evaluation result
    res = [80.474, 32.359]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_insert_knot1():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set evaluation parameter
    u = 0.2

    # Insert knot
    curve.insert_knot(u)

    # Evaluate curve at the given parameter
    evalpt = curve.curvept(u)

    # Evaluation result
    res = [33.304, 24.593]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA


def test_nurbs_curve2d_insert_knot2():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlpts = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set evaluation parameter
    u = 0.2

    # Insert knot
    curve.insert_knot(u, 3)

    # Evaluate curve at the given parameter
    evalpt = curve.curvept(u)

    # Evaluation result
    res = [33.304, 24.593]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA