"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

from pytest import fixture, mark
from geomdl import BSpline, NURBS
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


@fixture
def nbsurf(bsplsurf):
    """ Creates a NURBS surface from a B-spline surface """
    surf = NURBS.Surface.from_bspline(bsplsurf)
    return surf


@fixture
def nbsurf2(bsplsurf):
    """ Creates a NURBS surface from a B-spline surface """
    surf = NURBS.Surface.from_bspline(bsplsurf)
    surf.weights = [
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4
    ]
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


def test_bspline_surface_bounding_box(bsplsurf):
    # Evaluate bounding box
    to_check = bsplsurf.bbox

    # Evaluation result
    result = ((-25.0, -25.0, -10.0), (25.0, 25.0, 2.0))

    assert abs(to_check[0][0] - result[0][0]) < GEOMDL_DELTA
    assert abs(to_check[0][1] - result[0][1]) < GEOMDL_DELTA
    assert abs(to_check[0][2] - result[0][2]) < GEOMDL_DELTA
    assert abs(to_check[1][0] - result[1][0]) < GEOMDL_DELTA
    assert abs(to_check[1][1] - result[1][1]) < GEOMDL_DELTA
    assert abs(to_check[1][2] - result[1][2]) < GEOMDL_DELTA


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


def test_bspline_surface_to_nurbs(bsplsurf):
    nbsurf2 = NURBS.Surface.from_bspline(bsplsurf)
    assert all([x == 1.0 for x in nbsurf2.weights])


@mark.parametrize("param, res", [
    ((0.0, 0.0), (-25.0, -25.0, -10.0)),
    # ((0.0, 0.2), (-25.0, -11.403, -3.385)),
    # ((0.0, 1.0), (-25.0, 25.0, -10.0)),
    # ((0.3, 0.0), (-7.006, -25.0, -5.725)),
    # ((0.3, 0.4), [-7.006, -3.308, -6.265]),
    # ((0.3, 1.0), [-7.006, 25.0, -5.725]),
    # ((0.6, 0.0), (3.533, -25.0, -4.224)),
    # ((0.6, 0.6), (3.533, 3.533, -6.801)),
    # ((0.6, 1.0), (3.533, 25.0, -4.224)),
    # ((1.0, 0.0), (25.0, -25.0, -10.0)),
    # ((1.0, 0.8), (25.0, 11.636, -2.751)),
    # ((1.0, 1.0), (25.0, 25.0, -10.0))
])
def test_nurbs_surface_eval(nbsurf, param, res):
    evalpt = nbsurf.evaluate_single(param)
    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


# @mark.parametrize("param, order, res", [
#     ((0.0, 0.25), 1, [[[-25.0, -9.0771, -2.3972], [5.5511e-15, 43.6910, 17.5411]], [[90.9090, 0.0, -15.0882],[-5.9750e-15, 0.0, -140.0367]]]),
#     ((0.95, 0.75), 2, [[[20.8948, 9.3097, -2.4845], [-1.1347e-14, 43.7672, -15.0153], [-5.0393e-30, 100.1022, -74.1165]], [[76.2308, -1.6965e-15, 18.0372], [9.8212e-15, -5.9448e-15, -158.5462], [4.3615e-30, -2.4356e-13, -284.3037]], [[224.5342, -5.6794e-14, 93.3843], [4.9856e-14, -4.0400e-13, -542.6274], [2.2140e-29, -1.88662e-12, -318.8808]]])
# ])
# def test_nurbs_surface_deriv(nbsurf, param, order, res):
#     deriv = nbsurf.derivatives(param, order=order)

#     for computed, expected in zip(deriv, res):
#         for idx in range(order + 1):
#             for c, e in zip(computed[idx], expected[idx]):
#                 assert abs(c - e) < GEOMDL_DELTA


def test_nurbs_surface_weights(nbsurf2):
    weights = [
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4,
        1.0, 1.0, 0.75, 1.0, 0.25, 0.4
    ]
    assert all([x == y for x, y in zip(nbsurf2.weights, weights)])


def test_nurbs_surface_dimension(nbsurf2):
    assert nbsurf2.dimension == 3


def test_nurbs_surface_point(nbsurf2):
    assert all([x == y for x, y in zip(nbsurf2.ctrlpts[1, 1], [-15.0, -15.0, -4.0])])


def test_nurbs_surface_pointw(nbsurf2):
    assert all([x == y for x, y in zip(nbsurf2.ctrlptsw[1, 1], [-15.0, -15.0, -4.0, 1.0])])
