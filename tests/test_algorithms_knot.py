"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from geomdl import helpers
from geomdl import algorithms

GEOMDL_DELTA = 0.001


@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("param, num_insert, res", [
    (0.3, 1, (18.617, 13.377)),
    (0.6, 1, (32.143, 14.328)),
    (0.6, 2, (32.143, 14.328))
])
def test_bspline_curve2d_insert_knot(curve7, param, num_insert, res):
    s_pre = helpers.find_multiplicity(param, curve7.knotvector.u)
    algorithms.insert_knot(curve7, [param,], [num_insert,])
    s_post = helpers.find_multiplicity(param, curve7.knotvector.u)
    evalpt = curve7.evaluate_single(param)

    assert abs(evalpt[0] - res[0]) < GEOMDL_DELTA
    assert abs(evalpt[1] - res[1]) < GEOMDL_DELTA
    assert s_pre + num_insert == s_post


@pytest.mark.usefixtures("curve7")
def test_bspline_curve2d_insert_knot_kv(curve7):
    algorithms.insert_knot(curve7, (0.66,), (2,))
    s = helpers.find_multiplicity(0.66, curve7.knotvector.u)

    assert curve7.knotvector.u[5] == 0.66
    assert s == 3


@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("param, num_remove", [
    (0.33, 1),
    (0.66, 1)
])
def test_bspline_curve2d_remove_knot(curve7, param, num_remove):
    s_pre = helpers.find_multiplicity(param, curve7.knotvector.u)
    c_pre = curve7.ctrlpts_size.u
    algorithms.remove_knot(curve7, [param,], [num_remove,])
    s_post = helpers.find_multiplicity(param, curve7.knotvector.u)
    c_post = curve7.ctrlpts_size.u

    assert c_pre - num_remove == c_post
    assert s_pre - num_remove == s_post


@pytest.mark.usefixtures("curve7")
def test_bspline_curve2d_remove_knot_kv(curve7):
    algorithms.remove_knot(curve7, (0.66,), (1,))
    s = helpers.find_multiplicity(0.66, curve7.knotvector.u)

    assert 0.66 not in curve7.knotvector.u
    assert s == 0


@pytest.mark.usefixtures("curve7")
@pytest.mark.parametrize("density, kv", [
    (0, [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]),
    (1, [0.0, 0.0, 0.0, 0.0, 0.165, 0.165, 0.165, 0.33, 0.33, 0.33, 0.495, 0.495, 0.495, 0.66, 0.66, 0.66, 0.830, 0.830, 0.830, 1.0, 1.0, 1.0, 1.0]),
])
def test_bspline_curve2d_knot_refine(curve7, density, kv):
    algorithms.refine_knotvector(curve7, [density])
    for a, b in zip(kv, curve7.knotvector.u):
        assert abs(a - b) < GEOMDL_DELTA


# @pytest.mark.usefixtures("curve7")
# def test_bspline_curve2d_degree_elevate_degree(curve7):
#     dops = 1
#     degree_new = curve7.degree.u + dops
#     operations.degree_operations(curve7, [dops])
#     assert curve7.degree.u == degree_new


# @pytest.mark.usefixtures("curve7")
# def test_bspline_curve2d_degree_elevate_ctrlpts_size(curve7):
#     dops = 1
#     ctrlpts_size = curve7.ctrlpts_size.u + dops
#     operations.degree_operations(curve7, [dops])
#     assert curve7.ctrlpts_size.u == ctrlpts_size


# @pytest.mark.usefixtures("curve7")
# def test_bspline_curve2d_degree_reduce_degree(curve7):
#     dops = -1
#     degree_new = curve7.degree.u + dops
#     operations.degree_operations(curve7, [dops])
#     assert curve7.degree.u == degree_new


# @pytest.mark.usefixtures("curve7")
# def test_bspline_curve2d_degree_reduce_ctrlpts_size(curve7):
#     dops = -1
#     ctrlpts_size_new = curve7.ctrlpts_size.u + dops
#     operations.degree_operations(curve7, [dops])
#     assert curve7.ctrlpts_size.u == ctrlpts_size_new
