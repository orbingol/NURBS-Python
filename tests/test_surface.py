"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

from pytest import fixture, mark
from geomdl import BSpline
from geomdl import evaluators

GEOMDL_DELTA = 0.001


@fixture
def bsplsurf():
    """ Creates a B-spline surface instance """
    # Create a surface instance
    surf = BSpline.Surface()

    # Set degrees
    surf.degree.u = 3
    surf.degree.v = 3

    ctrlpts = [
        [-25.0, -25.0, -10.0], [-15.0, -25.0, -8.0], [-5.0, -25.0, -5.0], [5.0, -25.0, -3.0], [15.0, -25.0, -8.0], [25.0, -25.0, -10.0],
        [-25.0, -15.0, -5.0], [-15.0, -15.0, -4.0], [-5.0, -15.0, -3.0], [5.0, -15.0, -2.0], [15.0, -15.0, -4.0], [25.0, -15.0, -5.0],
        [-25.0, -5.0, 0.0], [-15.0, -5.0, -4.0], [-5.0, -5.0, -8.0], [5.0, -5.0, -8.0], [15.0, -5.0, -4.0], [25.0, -5.0, 2.0],
        [-25.0, 5.0, 0.0], [-15.0, 5.0, -4.0], [-5.0, 5.0, -8.0], [5.0, 5.0, -8.0], [15.0, 5.0, -4.0], [25.0, 5.0, 2.0],
        [-25.0, 15.0, -5.0], [-15.0, 15.0, -4.0], [-5.0, 15.0, -3.0], [5.0, 15.0, -2.0], [15.0, 15.0, -4.0], [25.0, 15.0, -5.0],
        [-25.0, 25.0, -10.0], [-15.0, 25.0, -8.0], [-5.0, 25.0, -5.0], [5.0, 25.0, -3.0], [15.0, 25.0, -8.0],[25.0, 25.0, -10.0]
    ]

    # Set control points
    surf.set_ctrlpts(ctrlpts, 6, 6)

    # Set knot vectors
    surf.knotvector.u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector.v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    return surf


def test_bspline_surface_name(bsplsurf):
    bsplsurf.name = "Surface Testing"
    assert bsplsurf.name == "Surface Testing"


def test_bspline_surface_degree(bsplsurf):
    assert all([x == y for x, y in zip(bsplsurf.degree, [3, 3])])


def test_bspline_surface_degree_u(bsplsurf):
    assert bsplsurf.degree.u == 3


def test_bspline_surface_degree_v(bsplsurf):
    assert bsplsurf.degree.v == 3


def test_bspline_surface_ctrlpts(bsplsurf):
    assert all([x == y for x, y in zip(bsplsurf.ctrlpts[1, 1], [-15.0, -15.0, -4.0])])
    assert bsplsurf.dimension == 3


def test_bspline_surface_knot_vector_u(bsplsurf):
    assert all([x == y for x, y in zip(bsplsurf.knotvector.u, [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0])])


def test_bspline_surface_knot_vector_v(bsplsurf):
    assert all([x == y for x, y in zip(bsplsurf.knotvector.v, [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0])])


@mark.parametrize("param, res", [
    ((0.0, 0.0), (-25.0, -25.0, -10.0)),
    ((0.0, 0.2), (-25.0, -11.403, -3.385)),
    ((0.0, 1.0), (-25.0, 25.0, -10.0)),
    ((0.3, 0.0), (-7.006, -25.0, -5.725)),
    ((0.3, 0.4), [-7.006, -3.308, -6.265]),
    ((0.3, 1.0), [-7.006, 25.0, -5.725]),
    ((0.6, 0.0), (3.533, -25.0, -4.224)),
    ((0.6, 0.6), (3.533, 3.533, -6.801)),
    ((0.6, 1.0), (3.533, 25.0, -4.224)),
    ((1.0, 0.0), (25.0, -25.0, -10.0)),
    ((1.0, 0.8), (25.0, 11.636, -2.751)),
    ((1.0, 1.0), (25.0, 25.0, -10.0))
])
def test_bspline_surface_eval(bsplsurf, param, res):
    evalpt = bsplsurf.evaluate_single(param)
    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


def test_bspline_surface_deriv(bsplsurf):
    der1 = bsplsurf.derivatives(param=(0.35, 0.35), order=2)
    bsplsurf.evaluator = evaluators.SurfaceEvaluator2()
    der2 = bsplsurf.derivatives(param=(0.35, 0.35), order=2)
    for k in range(0, 3):
        for l in range(0, 3 - k):
            assert abs(der1[k][l][0] - der2[k][l][0]) < GEOMDL_DELTA
            assert abs(der1[k][l][1] - der2[k][l][1]) < GEOMDL_DELTA
            assert abs(der1[k][l][2] - der2[k][l][2]) < GEOMDL_DELTA
