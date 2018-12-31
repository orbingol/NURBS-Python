"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.BSpline.Surface module. Requires "pytest" to run.
"""

import pytest
from geomdl import BSpline
from geomdl import evaluators

GEOMDL_DELTA = 0.001
RESULT_LIST = [[-25.0, -25.0, -10.0], [-25.0, -11.403, -3.385], [-25.0, 25.0, -10.0], [-7.006, -25.0, -5.725],
               [-7.006, -3.308, -6.265], [-7.006, 25.0, -5.725], [3.533, -25.0, -4.224], [3.533, 3.533, -6.801],
               [3.533, 25.0, -4.224], [25.0, -25.0, -10.0], [25.0, 11.636, -2.751], [25.0, 25.0, -10.0]]


@pytest.fixture
def bs_surface():
    """ Creates a surface instance """
    # Create a surface instance
    surf = BSpline.Surface()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    ctrlpts = [[-25.0, -25.0, -10.0], [-25.0, -15.0, -5.0], [-25.0, -5.0, 0.0], [-25.0, 5.0, 0.0],
               [-25.0, 15.0, -5.0], [-25.0, 25.0, -10.0], [-15.0, -25.0, -8.0], [-15.0, -15.0, -4.0],
               [-15.0, -5.0, -4.0], [-15.0, 5.0, -4.0], [-15.0, 15.0, -4.0], [-15.0, 25.0, -8.0],
               [-5.0, -25.0, -5.0], [-5.0, -15.0, -3.0], [-5.0, -5.0, -8.0], [-5.0, 5.0, -8.0],
               [-5.0, 15.0, -3.0], [-5.0, 25.0, -5.0], [5.0, -25.0, -3.0], [5.0, -15.0, -2.0],
               [5.0, -5.0, -8.0], [5.0, 5.0, -8.0], [5.0, 15.0, -2.0], [5.0, 25.0, -3.0],
               [15.0, -25.0, -8.0], [15.0, -15.0, -4.0], [15.0, -5.0, -4.0], [15.0, 5.0, -4.0],
               [15.0, 15.0, -4.0], [15.0, 25.0, -8.0], [25.0, -25.0, -10.0], [25.0, -15.0, -5.0],
               [25.0, -5.0, 2.0], [25.0, 5.0, 2.0], [25.0, 15.0, -5.0], [25.0, 25.0, -10.0]]

    # Set control points
    surf.set_ctrlpts(ctrlpts, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    return surf


@pytest.fixture
def bs_surface2():
    surf = BSpline.Surface()
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
    return surf


def test_bspline_curve_name(bs_surface):
    bs_surface.name = "Testing"
    assert bs_surface.name == "Testing"


def test_bspline_surface_degree_u(bs_surface):
    assert bs_surface.degree_u == 3


def test_bspline_surface_degree_v(bs_surface2):
    assert bs_surface2.degree_v == 2


def test_bspline_surface_ctrlpts1(bs_surface2):
    assert bs_surface2.ctrlpts2d[1][1] == [2.0, 2.0, 14.0]
    assert bs_surface2.dimension == 3


def test_bspline_surface_ctrlpts2(bs_surface2):
    assert bs_surface2.ctrlpts2d[2][1] == [3.0, 2.0, 17.0]


def test_bspline_surface_knot_vector_u(bs_surface):
    assert bs_surface.knotvector_u == [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]


def test_bspline_surface_knot_vector_v(bs_surface):
    assert bs_surface.knotvector_v == [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]


def test_bspline_surface_eval1(bs_surface):
    evalpt = bs_surface.evaluate_single((0.0, 0.0))
    assert abs(evalpt[0] - RESULT_LIST[0][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[0][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[0][2]) < GEOMDL_DELTA


def test_bspline_surface_eval2(bs_surface):
    evalpt = bs_surface.evaluate_single((0.0, 0.2))
    assert abs(evalpt[0] - RESULT_LIST[1][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[1][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[1][2]) < GEOMDL_DELTA


def test_bspline_surface_eval3(bs_surface):
    evalpt = bs_surface.evaluate_single((0.0, 1.0))
    assert abs(evalpt[0] - RESULT_LIST[2][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[2][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[2][2]) < GEOMDL_DELTA


def test_bspline_surface_eval4(bs_surface):
    evalpt = bs_surface.evaluate_single((0.3, 0.0))
    assert abs(evalpt[0] - RESULT_LIST[3][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[3][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[3][2]) < GEOMDL_DELTA


def test_bspline_surface_eval5(bs_surface):
    evalpt = bs_surface.evaluate_single((0.3, 0.4))
    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_bspline_surface_eval6(bs_surface):
    evalpt = bs_surface.evaluate_single((0.3, 1.0))
    assert abs(evalpt[0] - RESULT_LIST[5][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[5][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[5][2]) < GEOMDL_DELTA


def test_bspline_surface_eval7(bs_surface):
    evalpt = bs_surface.evaluate_single((0.6, 0.0))
    assert abs(evalpt[0] - RESULT_LIST[6][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[6][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[6][2]) < GEOMDL_DELTA


def test_bspline_surface_eval8(bs_surface):
    evalpt = bs_surface.evaluate_single((0.6, 0.6))
    assert abs(evalpt[0] - RESULT_LIST[7][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[7][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[7][2]) < GEOMDL_DELTA


def test_bspline_surface_eval9(bs_surface):
    evalpt = bs_surface.evaluate_single((0.6, 1.0))
    assert abs(evalpt[0] - RESULT_LIST[8][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[8][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[8][2]) < GEOMDL_DELTA


def test_bspline_surface_eval10(bs_surface):
    evalpt = bs_surface.evaluate_single((1.0, 0.0))
    assert abs(evalpt[0] - RESULT_LIST[9][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[9][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[9][2]) < GEOMDL_DELTA


def test_bspline_surface_eval11(bs_surface):
    evalpt = bs_surface.evaluate_single((1.0, 0.8))
    assert abs(evalpt[0] - RESULT_LIST[10][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[10][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[10][2]) < GEOMDL_DELTA


def test_bspline_surface_eval12(bs_surface):
    evalpt = bs_surface.evaluate_single((1.0, 1.0))
    assert abs(evalpt[0] - RESULT_LIST[11][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[11][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[11][2]) < GEOMDL_DELTA


def test_bspline_surface_deriv(bs_surface):
    der1 = bs_surface.derivatives(u=0.35, v=0.35, order=2)
    bs_surface.evaluator = evaluators.SurfaceEvaluator2()
    der2 = bs_surface.derivatives(u=0.35, v=0.35, order=2)
    for k in range(0, 3):
        for l in range(0, 3 - k):
            assert abs(der1[k][l][0] - der2[k][l][0]) < GEOMDL_DELTA
            assert abs(der1[k][l][1] - der2[k][l][1]) < GEOMDL_DELTA
            assert abs(der1[k][l][2] - der2[k][l][2]) < GEOMDL_DELTA


def test_bspline_surface_bbox(bs_surface):
    # Evaluate bounding box
    to_check = bs_surface.bbox

    # Evaluation result
    result = ((-25.0, -25.0, -10.0), (25.0, 25.0, 2.0))

    assert abs(to_check[0][0] - result[0][0]) < GEOMDL_DELTA
    assert abs(to_check[0][1] - result[0][1]) < GEOMDL_DELTA
    assert abs(to_check[0][2] - result[0][2]) < GEOMDL_DELTA
    assert abs(to_check[1][0] - result[1][0]) < GEOMDL_DELTA
    assert abs(to_check[1][1] - result[1][1]) < GEOMDL_DELTA
    assert abs(to_check[1][2] - result[1][2]) < GEOMDL_DELTA


def test_bspline_surface_insert_knot1(bs_surface):
    # Insert knot
    bs_surface.insert_knot(u=0.3, v=0.4)

    # Evaluate surface
    evalpt = bs_surface.evaluate_single((0.3, 0.4))

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_bspline_surface_insert_knot2(bs_surface):
    # Insert knot
    bs_surface.insert_knot(u=0.3, ru=2)

    # Evaluate surface
    evalpt = bs_surface.evaluate_single((0.3, 0.4))

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_bspline_surface_insert_knot3(bs_surface):
    # Insert knot
    bs_surface.insert_knot(v=0.3, rv=2)

    # Evaluate surface
    evalpt = bs_surface.evaluate_single((0.3, 0.4))

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_bspline_surface_insert_knot4(bs_surface):
    # Insert knot
    bs_surface.insert_knot(v=0.3, rv=2)

    assert bs_surface.knotvector_v[4] == 0.3
    assert bs_surface.knotvector_v[6] == 0.33


def test_bspline_surface_insert_knot5(bs_surface):
    # Insert knot
    bs_surface.insert_knot(u=0.33, ru=1)

    assert bs_surface.knotvector_u[3] == 0.0
    assert bs_surface.knotvector_u[6] == 0.66
