"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.NURBS.Surface module. Requires "pytest" to run.
"""
import pytest
from geomdl import NURBS

GEOMDL_DELTA = 0.001
RESULT_LIST = [[-25.0, -25.0, -10.0], [-25.0, -11.403, -3.385], [-25.0, 25.0, -10.0], [-7.006, -25.0, -5.725],
               [-7.006, -3.308, -6.265], [-7.006, 25.0, -5.725], [3.533, -25.0, -4.224], [3.533, 3.533, -6.801],
               [3.533, 25.0, -4.224], [25.0, -25.0, -10.0], [25.0, 11.636, -2.751], [25.0, 25.0, -10.0],
               [-100.0, -100.0, -40.0], [50.0, 50.0, -20.0]]
CONTROL_POINTS = [[-25.0, -25.0, -10.0, 1.0], [-25.0, -15.0, -5.0, 1.0], [-25.0, -5.0, 0.0, 1.0],
                  [-25.0, 5.0, 0.0, 1.0], [-25.0, 15.0, -5.0, 1.0], [-25.0, 25.0, -10.0, 1.0],
                  [-15.0, -25.0, -8.0, 1.0], [-15.0, -15.0, -4.0, 1.0], [-15.0, -5.0, -4.0, 1.0],
                  [-15.0, 5.0, -4.0, 1.0], [-15.0, 15.0, -4.0, 1.0], [-15.0, 25.0, -8.0, 1.0],
                  [-5.0, -25.0, -5.0, 1.0], [-5.0, -15.0, -3.0, 1.0], [-5.0, -5.0, -8.0, 1.0], [-5.0, 5.0, -8.0, 1.0],
                  [-5.0, 15.0, -3.0, 1.0], [-5.0, 25.0, -5.0, 1.0], [5.0, -25.0, -3.0, 1.0], [5.0, -15.0, -2.0, 1.0],
                  [5.0, -5.0, -8.0, 1.0], [5.0, 5.0, -8.0, 1.0], [5.0, 15.0, -2.0, 1.0], [5.0, 25.0, -3.0, 1.0],
                  [15.0, -25.0, -8.0, 1.0], [15.0, -15.0, -4.0, 1.0], [15.0, -5.0, -4.0, 1.0], [15.0, 5.0, -4.0, 1.0],
                  [15.0, 15.0, -4.0, 1.0], [15.0, 25.0, -8.0, 1.0], [25.0, -25.0, -10.0, 1.0],
                  [25.0, -15.0, -5.0, 1.0], [25.0, -5.0, 2.0, 1.0], [25.0, 5.0, 2.0, 1.0], [25.0, 15.0, -5.0, 1.0],
                  [25.0, 25.0, -10.0, 1.0]]
CONTROL_POINTS2 = [[-25.0, -25.0, -10.0, 0.25], [-25.0, -15.0, -5.0, 1.0], [-25.0, -5.0, 0.0, 1.0],
                   [-25.0, 5.0, 0.0, 1.0], [-25.0, 15.0, -5.0, 1.0], [-25.0, 25.0, -10.0, 1.0],
                   [-15.0, -25.0, -8.0, 1.0], [-15.0, -15.0, -4.0, 1.0], [-15.0, -5.0, -4.0, 1.0],
                   [-15.0, 5.0, -4.0, 1.0], [-15.0, 15.0, -4.0, 1.0], [-15.0, 25.0, -8.0, 1.0],
                   [-5.0, -25.0, -5.0, 1.0], [-5.0, -15.0, -3.0, 1.0], [-5.0, -5.0, -8.0, 1.0], [-5.0, 5.0, -8.0, 1.0],
                   [-5.0, 15.0, -3.0, 1.0], [-5.0, 25.0, -5.0, 1.0], [5.0, -25.0, -3.0, 1.0], [5.0, -15.0, -2.0, 1.0],
                   [5.0, -5.0, -8.0, 1.0], [5.0, 5.0, -8.0, 1.0], [5.0, 15.0, -2.0, 1.0], [5.0, 25.0, -3.0, 1.0],
                   [15.0, -25.0, -8.0, 1.0], [15.0, -15.0, -4.0, 1.0], [15.0, -5.0, -4.0, 1.0], [15.0, 5.0, -4.0, 1.0],
                   [15.0, 15.0, -4.0, 1.0], [15.0, 25.0, -8.0, 1.0], [25.0, -25.0, -10.0, 1.0],
                   [25.0, -15.0, -5.0, 1.0], [25.0, -5.0, 2.0, 1.0], [25.0, 5.0, 2.0, 1.0], [25.0, 15.0, -5.0, 1.0],
                   [25.0, 25.0, -10.0, 0.5]]


@pytest.fixture
def nurbs_surface():
    """ Creates a NURBS Surface instance """
    # Create a surface instance
    surf = NURBS.Surface()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set weighted control points
    surf.set_ctrlpts(CONTROL_POINTS, 6, 6)

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    return surf


@pytest.fixture
def nurbs_surface2():
    """ Creates a NURBS Surface instance (alternative control points) """
    # Create a surface instance
    surf = NURBS.Surface()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set weighted control points
    surf.ctrlpts_size_u = 6
    surf.ctrlpts_size_v = 6
    surf.ctrlptsw = CONTROL_POINTS2

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    return surf


def test_bspline_surface_degree_u():
    surf = NURBS.Surface()
    surf.degree_u = 7

    # Check assignment
    assert surf.degree_u == 7


def test_nurbs_surface_degree_v():
    surf = NURBS.Surface()
    surf.degree_v = 4

    # Check assignment
    assert surf.degree_v == 4


def test_nurbs_surface_ctrlpts1():
    surf = NURBS.Surface()
    ctrlpts = [[1.0, 1.0, 10.0, 1.0],
               [1.0, 2.0, 11.0, 1.0],
               [1.0, 3.0, 12.0, 1.0],
               [2.0, 1.0, 13.0, 1.0],
               [2.0, 2.0, 14.0, 1.0],
               [2.0, 3.0, 15.0, 1.0],
               [3.0, 1.0, 16.0, 1.0],
               [3.0, 2.0, 17.0, 1.0],
               [3.0, 3.0, 18.0, 1.0],
               [4.0, 1.0, 19.0, 1.0],
               [4.0, 2.0, 20.0, 1.0],
               [4.0, 3.0, 21.0, 1.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlptsw = ctrlpts

    # Check assignment
    assert surf.ctrlpts2d[1][1] == (2.0, 2.0, 14.0, 1.0)
    assert surf.dimension == 3


def test_nurbs_surface_ctrlpts2():
    surf = NURBS.Surface()
    ctrlpts = [[1.0, 1.0, 10.0, 1.0],
               [1.0, 2.0, 11.0, 1.0],
               [1.0, 3.0, 12.0, 1.0],
               [2.0, 1.0, 13.0, 1.0],
               [2.0, 2.0, 14.0, 1.0],
               [2.0, 3.0, 15.0, 1.0],
               [3.0, 1.0, 16.0, 1.0],
               [3.0, 2.0, 17.0, 1.0],
               [3.0, 3.0, 18.0, 1.0],
               [4.0, 1.0, 19.0, 1.0],
               [4.0, 2.0, 20.0, 1.0],
               [4.0, 3.0, 21.0, 1.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlptsw = ctrlpts

    # Check assignment
    assert surf.ctrlpts2d[2][1] == (3.0, 2.0, 17.0, 1.0)


def test_nurbs_surface_ctrlpts3():
    surf = NURBS.Surface()
    ctrlpts = [[1.0, 1.0, 10.0, 1.0],
               [1.0, 2.0, 11.0, 1.0],
               [1.0, 3.0, 12.0, 1.0],
               [2.0, 1.0, 13.0, 1.0],
               [2.0, 2.0, 14.0, 0.5],
               [2.0, 3.0, 15.0, 1.0],
               [3.0, 1.0, 16.0, 1.0],
               [3.0, 2.0, 17.0, 1.0],
               [3.0, 3.0, 18.0, 1.0],
               [4.0, 1.0, 19.0, 1.0],
               [4.0, 2.0, 20.0, 1.0],
               [4.0, 3.0, 21.0, 1.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlptsw = ctrlpts

    # Check assignment
    assert surf.ctrlpts[4] == (4.0, 4.0, 28.0)


def test_nurbs_surface_weights1():
    surf = NURBS.Surface()
    ctrlpts = [[1.0, 1.0, 10.0, 1.0],
               [1.0, 2.0, 11.0, 1.0],
               [1.0, 3.0, 12.0, 1.0],
               [2.0, 1.0, 13.0, 1.0],
               [2.0, 2.0, 14.0, 0.5],
               [2.0, 3.0, 15.0, 1.0],
               [3.0, 1.0, 16.0, 0.2],
               [3.0, 2.0, 17.0, 1.0],
               [3.0, 3.0, 18.0, 1.0],
               [4.0, 1.0, 19.0, 1.0],
               [4.0, 2.0, 20.0, 1.0],
               [4.0, 3.0, 21.0, 1.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlptsw = ctrlpts

    # Check assignment
    assert surf.weights[6] == 0.2


def test_nurbs_surface_weights2():
    surf = NURBS.Surface()
    ctrlpts = [[1.0, 1.0, 10.0, 1.0],
               [1.0, 2.0, 11.0, 1.0],
               [1.0, 3.0, 12.0, 1.0],
               [2.0, 1.0, 13.0, 1.0],
               [2.0, 2.0, 14.0, 0.5],
               [2.0, 3.0, 15.0, 1.0],
               [3.0, 1.0, 16.0, 0.2],
               [3.0, 2.0, 17.0, 1.0],
               [3.0, 3.0, 18.0, 1.0],
               [4.0, 1.0, 19.0, 1.0],
               [4.0, 2.0, 20.0, 1.0],
               [4.0, 3.0, 21.0, 1.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlptsw = ctrlpts

    # Check assignment
    assert surf.weights[7] == 1.0


def test_nurbs_surface_weights3():
    surf = NURBS.Surface()
    ctrlpts = [[1.0, 1.0, 10.0, 1.0],
               [1.0, 2.0, 11.0, 1.0],
               [1.0, 3.0, 12.0, 1.0],
               [2.0, 1.0, 13.0, 1.0],
               [2.0, 2.0, 14.0, 0.5],
               [2.0, 3.0, 15.0, 1.0],
               [3.0, 1.0, 16.0, 0.2],
               [3.0, 2.0, 17.0, 1.0],
               [3.0, 3.0, 18.0, 1.0],
               [4.0, 1.0, 19.0, 1.0],
               [4.0, 2.0, 20.0, 1.0],
               [4.0, 3.0, 21.0, 1.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlptsw = ctrlpts

    # Check assignment
    assert surf.weights[4] == 0.5


def test_nurbs_surface_knot_vector_u():
    surf = NURBS.Surface()
    ctrlpts = [[1.0, 1.0, 10.0, 1.0],
               [1.0, 2.0, 11.0, 1.0],
               [1.0, 3.0, 12.0, 1.0],
               [2.0, 1.0, 13.0, 1.0],
               [2.0, 2.0, 14.0, 1.0],
               [2.0, 3.0, 15.0, 1.0],
               [3.0, 1.0, 16.0, 1.0],
               [3.0, 2.0, 17.0, 1.0],
               [3.0, 3.0, 18.0, 1.0],
               [4.0, 1.0, 19.0, 1.0],
               [4.0, 2.0, 20.0, 1.0],
               [4.0, 3.0, 21.0, 1.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlptsw = ctrlpts
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]

    assert surf.knotvector_u == (0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0)


def test_nurbs_surface_knot_vector_v():
    surf = NURBS.Surface()
    ctrlpts = [[1.0, 1.0, 10.0, 1.0],
               [1.0, 2.0, 11.0, 1.0],
               [1.0, 3.0, 12.0, 1.0],
               [2.0, 1.0, 13.0, 1.0],
               [2.0, 2.0, 14.0, 1.0],
               [2.0, 3.0, 15.0, 1.0],
               [3.0, 1.0, 16.0, 1.0],
               [3.0, 2.0, 17.0, 1.0],
               [3.0, 3.0, 18.0, 1.0],
               [4.0, 1.0, 19.0, 1.0],
               [4.0, 2.0, 20.0, 1.0],
               [4.0, 3.0, 21.0, 1.0]]
    surf.ctrlpts_size_v = 3
    surf.ctrlpts_size_u = 4
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlptsw = ctrlpts
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]

    assert surf.knotvector_v == (0.0, 0.0, 0.0, 1.0, 1.0, 1.0)


def test_nurbs_surface_name_property(nurbs_surface):
    default_name = "Surface"
    assert nurbs_surface.name == default_name
    assert str(nurbs_surface) == default_name


def test_nurbs_surface_eval1(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.0, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[0][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[0][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[0][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval2(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.0, v=0.2)

    assert abs(evalpt[0] - RESULT_LIST[1][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[1][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[1][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval3(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.0, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[2][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[2][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[2][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval4(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.3, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[3][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[3][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[3][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval5(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval6(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.3, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[5][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[5][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[5][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval7(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.6, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[6][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[6][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[6][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval8(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.6, v=0.6)

    assert abs(evalpt[0] - RESULT_LIST[7][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[7][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[7][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval9(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=0.6, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[8][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[8][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[8][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval10(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=1.0, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[9][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[9][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[9][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval11(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=1.0, v=0.8)

    assert abs(evalpt[0] - RESULT_LIST[10][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[10][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[10][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval12(nurbs_surface):
    evalpt = nurbs_surface.surfpt(u=1.0, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[11][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[11][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[11][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval13(nurbs_surface2):
    # Evaluate curve
    evalpt = nurbs_surface2.surfpt(u=0.0, v=0.0)

    assert abs(evalpt[0] - RESULT_LIST[12][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[12][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[12][2]) < GEOMDL_DELTA


def test_nurbs_surface_eval14(nurbs_surface2):
    # Evaluate curve
    evalpt = nurbs_surface2.surfpt(u=1.0, v=1.0)

    assert abs(evalpt[0] - RESULT_LIST[13][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[13][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[13][2]) < GEOMDL_DELTA


def test_nurbs_surface_insert_knot1(nurbs_surface):
    # Insert knot
    nurbs_surface.insert_knot(0.3, 0.4)

    # Evaluate surface
    evalpt = nurbs_surface.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_nurbs_surface_insert_knot2(nurbs_surface):
    # Insert knot
    nurbs_surface.insert_knot(u=0.3, v=0.4, ru=2, rv=2)

    # Evaluate surface
    evalpt = nurbs_surface.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_nurbs_surface_insert_knot3(nurbs_surface):
    # Insert knot
    nurbs_surface.insert_knot(v=0.4, rv=2)

    # Evaluate surface
    evalpt = nurbs_surface.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA


def test_nurbs_surface_insert_knot4(nurbs_surface):
    # Insert knot
    nurbs_surface.insert_knot(u=0.3, ru=2)

    # Evaluate surface
    evalpt = nurbs_surface.surfpt(u=0.3, v=0.4)

    assert abs(evalpt[0] - RESULT_LIST[4][0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - RESULT_LIST[4][1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - RESULT_LIST[4][2]) < GEOMDL_DELTA
