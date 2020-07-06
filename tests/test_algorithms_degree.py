"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from geomdl import helpers
from geomdl.algorithms import degree


@pytest.mark.usefixtures("curve7")
def test_bspline_curve_degree_elevate_degree(curve7):
    dops = 1
    degree_new = curve7.degree.u + dops
    de = degree.elevate_degree(curve7, [dops])
    assert de.degree.u == degree_new


@pytest.mark.usefixtures("curve7")
def test_bspline_curve_degree_elevate_ctrlpts_size(curve7):
    dops = 1
    ctrlpts_size = curve7.ctrlpts_size.u + dops
    de = degree.elevate_degree(curve7, [dops])
    assert de.ctrlpts_size.u == ctrlpts_size


@pytest.mark.usefixtures("curve7")
def test_bspline_curve_degree_reduce_degree(curve7):
    dops = 1
    degree_new = curve7.degree.u - dops
    dr = degree.reduce_degree(curve7, [dops])
    assert dr.degree.u == degree_new


@pytest.mark.usefixtures("curve7")
def test_bspline_curve_degree_reduce_ctrlpts_size(curve7):
    dops = 1
    ctrlpts_size_new = curve7.ctrlpts_size.u - dops
    dr = degree.reduce_degree(curve7, [dops])
    assert dr.ctrlpts_size.u == ctrlpts_size_new
