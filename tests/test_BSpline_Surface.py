"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.BSpline.Surface module. Requires "pytest" to run.
"""
from geomdl import BSpline
from geomdl import evaluators

GEOMDL_DELTA = 0.001
OBJECT_INSTANCE = BSpline.Surface
RESULT_LIST = [[-25.0, -25.0, -10.0], [-25.0, -11.403, -3.385], [-25.0, 25.0, -10.0], [-7.006, -25.0, -5.725],
               [-7.006, -3.308, -6.265], [-7.006, 25.0, -5.725], [3.533, -25.0, -4.224], [3.533, 3.533, -6.801],
               [3.533, 25.0, -4.224], [25.0, -25.0, -10.0], [25.0, 11.636, -2.751], [25.0, 25.0, -10.0]]
CONTROL_POINTS = [[-25.0, -25.0, -10.0], [-25.0, -15.0, -5.0], [-25.0, -5.0, 0.0], [-25.0, 5.0, 0.0],
                  [-25.0, 15.0, -5.0], [-25.0, 25.0, -10.0], [-15.0, -25.0, -8.0], [-15.0, -15.0, -4.0],
                  [-15.0, -5.0, -4.0], [-15.0, 5.0, -4.0], [-15.0, 15.0, -4.0], [-15.0, 25.0, -8.0],
                  [-5.0, -25.0, -5.0], [-5.0, -15.0, -3.0], [-5.0, -5.0, -8.0], [-5.0, 5.0, -8.0],
                  [-5.0, 15.0, -3.0], [-5.0, 25.0, -5.0], [5.0, -25.0, -3.0], [5.0, -15.0, -2.0],
                  [5.0, -5.0, -8.0], [5.0, 5.0, -8.0], [5.0, 15.0, -2.0], [5.0, 25.0, -3.0],
                  [15.0, -25.0, -8.0], [15.0, -15.0, -4.0], [15.0, -5.0, -4.0], [15.0, 5.0, -4.0],
                  [15.0, 15.0, -4.0], [15.0, 25.0, -8.0], [25.0, -25.0, -10.0], [25.0, -15.0, -5.0],
                  [25.0, -5.0, 2.0], [25.0, 5.0, 2.0], [25.0, 15.0, -5.0], [25.0, 25.0, -10.0]]


def test_bspline_curve_name():
    surf = OBJECT_INSTANCE()
    surf.name = "Testing"

    assert surf.name == "Testing"


def test_bspline_surface_degree_u():
    surf = OBJECT_INSTANCE()
    surf.degree_u = 5

    # Check assignment
    assert surf.degree_u == 5


def test_bspline_surface_degree_v():
    surf = OBJECT_INSTANCE()
    surf.degree_v = 2

    # Check assignment
    assert surf.degree_v == 2


def test_bspline_surface_ctrlpts1():
    surf = OBJECT_INSTANCE()
    ctrlpts = [[1.0, 1.0, 10.0],
               [1.0, 2.0, 11.0],
               [1.0, 3.0, 12.0],
               [2.0, 1.0, 13.0],
               [2.0, 2.0, 14.0],
               [2.0, 3.0, 15.0],
               [3.0, 1.0, 16.0],
               [3.0, 2.0, 17.0],
               [3.0, 3.0, 18.0],
               [4.0, 1.0, 19.0],
               [4.0, 2.0, 20.0],
               [4.0, 3.0, 21.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlpts = ctrlpts

    # Check assignment
    assert surf.ctrlpts2d[1][1] == (2.0, 2.0, 14.0)
    assert surf.dimension == 3


def test_bspline_surface_ctrlpts2():
    surf = OBJECT_INSTANCE()
    ctrlpts = [[1.0, 1.0, 10.0],
               [1.0, 2.0, 11.0],
               [1.0, 3.0, 12.0],
               [2.0, 1.0, 13.0],
               [2.0, 2.0, 14.0],
               [2.0, 3.0, 15.0],
               [3.0, 1.0, 16.0],
               [3.0, 2.0, 17.0],
               [3.0, 3.0, 18.0],
               [4.0, 1.0, 19.0],
               [4.0, 2.0, 20.0],
               [4.0, 3.0, 21.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlpts = ctrlpts

    # Check assignment
    assert surf.ctrlpts2d[2][1] == (3.0, 2.0, 17.0)


def test_bspline_surface_knot_vector_u():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    assert surf.knotvector_u == (0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0)


def test_bspline_surface_knot_vector_v():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    assert surf.knotvector_v == (0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0)


def test_bspline_surface_eval1():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=0.0, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[0][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[0][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[0][2]) < GEOMDL_DELTA


def test_bspline_surface_eval2():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=0.0, v=0.2)

    assert abs(evalpt[0] - RESULT_LIST[1][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[1][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[1][2]) < GEOMDL_DELTA


def test_bspline_surface_eval3():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate curve
    evalpt = surf.surfpt(u=0.0, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[2][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[2][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[2][2]) < GEOMDL_DELTA


def test_bspline_surface_eval4():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=0.3, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[3][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[3][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[3][2]) < GEOMDL_DELTA


def test_bspline_surface_eval5():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_bspline_surface_eval6():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=0.3, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[5][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[5][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[5][2]) < GEOMDL_DELTA


def test_bspline_surface_eval7():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=0.6, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[6][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[6][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[6][2]) < GEOMDL_DELTA


def test_bspline_surface_eval8():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=0.6, v=0.6)

    assert abs(evalpt[0] - RESULT_LIST[7][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[7][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[7][2]) < GEOMDL_DELTA


def test_bspline_surface_eval9():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=0.6, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[8][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[8][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[8][2]) < GEOMDL_DELTA


def test_bspline_surface_eval10():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=1.0, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[9][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[9][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[9][2]) < GEOMDL_DELTA


def test_bspline_surface_eval11():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=1.0, v=0.8)

    assert abs(evalpt[0] - RESULT_LIST[10][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[10][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[10][2]) < GEOMDL_DELTA


def test_bspline_surface_eval12():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate surface
    evalpt = surf.surfpt(u=1.0, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[11][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[11][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[11][2]) < GEOMDL_DELTA


def test_bspline_surface_deriv():
    # Create a surface isntance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Take the derivative
    der1 = surf.derivatives(u=0.35, v=0.35, order=2)
    surf.evaluator = evaluators.SurfaceEvaluator2()
    der2 = surf.derivatives(u=0.35, v=0.35, order=2)

    for k in range(0, 3):
        for l in range(0, 3 - k):
            assert abs(der1[k][l][0] - der2[k][l][0]) < GEOMDL_DELTA
            assert abs(der1[k][l][1] - der2[k][l][1]) < GEOMDL_DELTA
            assert abs(der1[k][l][2] - der2[k][l][2]) < GEOMDL_DELTA


def test_bspline_surface_bbox():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Evaluate bounding box
    to_check = surf.bbox

    # Evaluation result
    result = ((-25.0, -25.0, -10.0), (25.0, 25.0, 2.0))

    assert abs(to_check[0][0] - result[0][0]) < GEOMDL_DELTA
    assert abs(to_check[0][1] - result[0][1]) < GEOMDL_DELTA
    assert abs(to_check[0][2] - result[0][2]) < GEOMDL_DELTA
    assert abs(to_check[1][0] - result[1][0]) < GEOMDL_DELTA
    assert abs(to_check[1][1] - result[1][1]) < GEOMDL_DELTA
    assert abs(to_check[1][2] - result[1][2]) < GEOMDL_DELTA


def test_bspline_surface_insert_knot1():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Insert knot
    surf.insert_knot(u=0.3, v=0.4)

    # Evaluate surface
    evalpt = surf.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_bspline_surface_insert_knot2():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Insert knot
    surf.insert_knot(u=0.3, ru=2)

    # Evaluate surface
    evalpt = surf.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_bspline_surface_insert_knot3():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Insert knot
    surf.insert_knot(v=0.3, rv=2)

    # Evaluate surface
    evalpt = surf.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_bspline_surface_insert_knot4():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Insert knot
    surf.insert_knot(v=0.3, rv=2)

    assert surf.knotvector_v[4] == 0.3
    assert surf.knotvector_v[6] == 0.33


def test_bspline_surface_insert_knot5():
    # Create a surface instance
    surf = OBJECT_INSTANCE()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Insert knot
    surf.insert_knot(u=0.33, ru=1)

    assert surf.knotvector_u[3] == 0.0
    assert surf.knotvector_u[6] == 0.66
