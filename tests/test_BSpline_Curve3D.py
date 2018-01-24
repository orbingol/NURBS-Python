"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.BSpline.Curve module. Requires "pytest" to run.
"""
from geomdl import BSpline

GEOMDL_DELTA = 0.001
objinstance = BSpline.Curve


def test_bspline_curve3d_eval1():
    # Create a curve instance
    curve = objinstance()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
                     [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]

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
    curve = objinstance()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
                     [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]

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
    curve = objinstance()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
                     [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]

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
    curve = objinstance()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
                     [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]

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
    curve = objinstance()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
                     [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = curve.curvept(1.0)

    # Evaluation result
    res = [5.0, 15.0, 30.0]

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA
