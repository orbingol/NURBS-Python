"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from geomdl import helpers
from geomdl.algorithms import knot

GEOMDL_DELTA = 0.001

# Curve knot algorithms
@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("param, num_insert, res", [
    (0.3, 1, (18.617, 13.377)),
    (0.6, 1, (32.143, 14.328)),
    (0.6, 2, (32.143, 14.328))
])
def test_bspline_curve2d_insert_knot(curve7, param, num_insert, res):
    s_pre = helpers.find_multiplicity(param, curve7.knotvector.u)
    ki = knot.insert_knot(curve7, [param,], [num_insert,])
    s_post = helpers.find_multiplicity(param, ki.knotvector.u)
    evalpt = ki.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert s_pre + num_insert == s_post


@pytest.mark.usefixtures("curve7")
def test_bspline_curve2d_insert_knot_kv(curve7):
    ki = knot.insert_knot(curve7, (0.66,), (2,))
    s = helpers.find_multiplicity(0.66, ki.knotvector.u)

    assert ki.knotvector.u[5] == 0.66
    assert s == 3


@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("param, num_remove", [
    (0.33, 1),
    (0.66, 1)
])
def test_bspline_curve2d_remove_knot(curve7, param, num_remove):
    s_pre = helpers.find_multiplicity(param, curve7.knotvector.u)
    c_pre = curve7.ctrlpts_size.u
    kr = knot.remove_knot(curve7, [param,], [num_remove,])
    s_post = helpers.find_multiplicity(param, kr.knotvector.u)
    c_post = kr.ctrlpts_size.u

    assert c_pre - num_remove == c_post
    assert s_pre - num_remove == s_post


@pytest.mark.usefixtures("curve7")
def test_bspline_curve2d_remove_knot_kv(curve7):
    kr = knot.remove_knot(curve7, (0.66,), (1,))
    s = helpers.find_multiplicity(0.66, kr.knotvector.u)

    assert 0.66 not in kr.knotvector.u
    assert s == 0


@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("density, kv", [
    (0, [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]),
    (1, [0.0, 0.0, 0.0, 0.0, 0.165, 0.165, 0.165, 0.33, 0.33, 0.33, 0.495, 0.495, 0.495, 0.66, 0.66, 0.66, 0.830, 0.830, 0.830, 1.0, 1.0, 1.0, 1.0]),
])
def test_bspline_curve2d_knot_refine(curve7, density, kv):
    kk = knot.refine_knot(curve7, [density])
    for a, b in zip(kv, kk.knotvector.u):
        assert abs(a - b) < GEOMDL_DELTA


# Surface knot algorithms
@pytest.mark.usefixtures("surface5")
@pytest.mark.parametrize("params, num, uv, res", [
    ((0.3, 0.4), (1, 1), (0.3, 0.4), (-7.006, -3.308, -6.265)),
    ((0.3, None), (2, 0), (0.3, 0.4), (-7.006, -3.308, -6.265)),
    ((None, 0.3), (0, 2), (0.3, 0.4), (-7.006, -3.308, -6.265)),
])
def test_bspline_surface_insert_knot_eval(surface5, params, num, uv, res):
    # Insert knot
    ki = knot.insert_knot(surface5, params, num)

    # Evaluate surface
    evalpt = ki.evaluate_single(uv)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert abs(evalpt[2] - res[2]) < GEOMDL_DELTA


@pytest.mark.usefixtures("surface5")
@pytest.mark.parametrize("params, num, idx, val", [
    ((0.33, None), (2, 0), 3, 0.0),
    ((0.33, None), (1, 0), 6, 0.66)
])
def test_bspline_surface_insert_knot_kv_u(surface5, params, num, idx, val):
    # Insert knot
    ki = knot.insert_knot(surface5, params, num)

    assert ki.knotvector.u[idx] == val


@pytest.mark.usefixtures("surface5")
@pytest.mark.parametrize("params, num, idx, val", [
    ((None, 0.3), (0, 2), 4, 0.3),
    ((None, 0.3), (0, 2), 6, 0.33)
])
def test_bspline_surface_insert_knot_kv_v(surface5, params, num, idx, val):
    # Insert knot
    ki = knot.insert_knot(surface5, params, num)

    assert ki.knotvector.v[idx] == val


@pytest.mark.usefixtures("surface5")
@pytest.mark.parametrize("param, num_remove", [
    ((0.33, None), (1, 0)),
    ((0.66, None), (1, 0))
])
def test_bspline_surface_remove_knot_u(surface5, param, num_remove):
    s_pre = helpers.find_multiplicity(param[0], surface5.knotvector.u)
    c_pre = surface5.ctrlpts_size.u
    kr = knot.remove_knot(surface5, param, num_remove)
    s_post = helpers.find_multiplicity(param[0], kr.knotvector.u)
    c_post = kr.ctrlpts_size.u

    assert c_pre - num_remove[0] == c_post
    assert s_pre - num_remove[0] == s_post


@pytest.mark.usefixtures("surface5")
@pytest.mark.parametrize("param, num_remove", [
    ((None, 0.33), (0, 1)),
    ((None, 0.66), (0, 1))
])
def test_bspline_surface_remove_knot_v(surface5, param, num_remove):
    s_pre = helpers.find_multiplicity(param[1], surface5.knotvector.v)
    c_pre = surface5.ctrlpts_size.v
    kr = knot.remove_knot(surface5, param, num_remove)
    s_post = helpers.find_multiplicity(param[1], kr.knotvector.v)
    c_post = kr.ctrlpts_size.v

    assert c_pre - num_remove[1] == c_post
    assert s_pre - num_remove[1] == s_post


@pytest.mark.usefixtures("surface5")
def test_bspline_surface_remove_knot_kv_u(surface5):
    kr = knot.remove_knot(surface5, (0.66, None), (1, 0))
    s = helpers.find_multiplicity(0.66, kr.knotvector.u)

    assert 0.66 not in kr.knotvector.u
    assert s == 0


@pytest.mark.usefixtures("surface5")
def test_bspline_surface_remove_knot_kv_v(surface5):
    kr = knot.remove_knot(surface5, (None, 0.33), (0, 1))
    s = helpers.find_multiplicity(0.33, kr.knotvector.v)

    assert 0.33 not in kr.knotvector.v
    assert s == 0

    # Insert knot
    ki = knot.insert_knot(surface5, params, num)

    assert ki.knotvector.u[idx] == val


# @pytest.mark.parametrize("param, num_remove", [
#     (0.33, 1),
#     (0.66, 1)
# ])
# def test_bspline_surface_remove_knot_u(spline_surf, param, num_remove):
#     s_pre = helpers.find_multiplicity(param, spline_surf.knotvector_u)
#     c_pre = spline_surf.ctrlpts_size_u
#     spline_surf.remove_knot(u=param, num_u=num_remove)
#     s_post = helpers.find_multiplicity(param, spline_surf.knotvector_u)
#     c_post = spline_surf.ctrlpts_size_u

#     assert c_pre - num_remove == c_post
#     assert s_pre - num_remove == s_post


# @pytest.mark.parametrize("param, num_remove", [
#     (0.33, 1),
#     (0.66, 1)
# ])
# def test_bspline_surface_remove_knot_v(spline_surf, param, num_remove):
#     s_pre = helpers.find_multiplicity(param, spline_surf.knotvector_v)
#     c_pre = spline_surf.ctrlpts_size_v
#     spline_surf.remove_knot(v=param, num_v=num_remove)
#     s_post = helpers.find_multiplicity(param, spline_surf.knotvector_v)
#     c_post = spline_surf.ctrlpts_size_v

#     assert c_pre - num_remove == c_post
#     assert s_pre - num_remove == s_post


# def test_bspline_surface_remove_knot_kv_u(spline_surf):
#     spline_surf.remove_knot(u=0.66, num_u=1)
#     s = helpers.find_multiplicity(0.66, spline_surf.knotvector_u)

#     assert 0.66 not in spline_surf.knotvector_u
#     assert s == 0


# def test_bspline_surface_remove_knot_kv_v(spline_surf):
#     spline_surf.remove_knot(v=0.33, num_v=1)
#     s = helpers.find_multiplicity(0.33, spline_surf.knotvector_v)

#     assert 0.33 not in spline_surf.knotvector_v
#     assert s == 0
