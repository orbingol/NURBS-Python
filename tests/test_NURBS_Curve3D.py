"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.NURBS.Curve module. Requires "pytest" to run.
"""
from geomdl import NURBS

GEOMDL_DELTA = 0.001
OBJECT_INSTANCE = NURBS.Curve
CONTROL_POINTS = [[5.0, 15.0, 0.0, 1.0], [10.0, 25.0, 5.0, 1.0], [20.0, 20.0, 10.0, 1.0], [15.0, -5.0, 15.0, 1.0],
                  [7.5, 10.0, 20.0, 1.0], [12.5, 15.0, 25.0, 1.0], [15.0, 0.0, 30.0, 1.0], [5.0, -10.0, 35.0, 1.0],
                  [10.0, 15.0, 40.0, 1.0], [5.0, 15.0, 30.0, 1.0]]
CONTROL_POINTS2 = [[5.0, 15.0, 0.0, 0.1], [10.0, 25.0, 5.0, 0.2], [20.0, 20.0, 10.0, 1.0], [15.0, -5.0, 15.0, 1.0],
                   [7.5, 10.0, 20.0, 1.0], [12.5, 15.0, 25.0, 1.0], [15.0, 0.0, 30.0, 0.5], [5.0, -10.0, 35.0, 1.0],
                   [10.0, 15.0, 40.0, 0.7], [5.0, 15.0, 30.0, 1.0], [15.0, 20.0, 40.0, 1.0]]


def test_nurbs_curve3d_eval1():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.0)

    # Evaluation result
    res = [5.0, 15.0, 0.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval2():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.2)

    # Evaluation result
    res = [15.727, 6.509, 13.692]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval3():
    # Create an object instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.5)

    # Evaluation result
    res = [10.476, 11.071, 22.5]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval4():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.8)

    # Evaluation result
    res = [10.978, -1.349, 31.307]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval5():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 4

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(1.0)

    # Evaluation result
    res = [5.0, 15.0, 30.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval6():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.0)

    # Evaluation result
    res = [50.0, 150.0, 0.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval7():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.2)

    # Evaluation result
    res = [14.297, 5.130, 15.395]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval8():
    # Create an object instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.7)

    # Evaluation result
    res = [14.735, -0.255, 41.088]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval9():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.1)

    # Evaluation result
    res = [19.514, 17.411, 12.515]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_eval10():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(0.5)

    # Evaluation result
    res = [13.421, 10.976, 28.329]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_deriv1():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    ept = curve.curvept(0.35)

    # Take the derivative
    der = curve.derivatives(u=0.35, order=7)

    assert abs(ept[0] - der[0][0]) < GEOMDL_DELTA
    assert abs(ept[1] - der[0][1]) < GEOMDL_DELTA
    assert abs(ept[2] - der[0][2]) < GEOMDL_DELTA


def test_nurbs_curve3d_insert_knot1():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set evaluation parameter
    u = 0.5

    # Insert knot
    curve.insert_knot(u)

    # Evaluate curve at the given parameter
    evalpt = curve.curvept(u)

    # Evaluation result
    res = [13.421, 10.976, 28.329]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_nurbs_curve3d_insert_knot2():
    # Create a curve instance
    curve = OBJECT_INSTANCE()

    # Set curve degree
    curve.degree = 5

    # Set weighted control points
    curve.ctrlptsw = CONTROL_POINTS2

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set evaluation parameter
    u = 0.5

    # Insert knot
    curve.insert_knot(u, 3)

    # Evaluate curve at the given parameter
    evalpt = curve.curvept(u)

    # Evaluation result
    res = [13.421, 10.976, 28.329]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA
