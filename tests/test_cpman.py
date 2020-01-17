"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2019-2020 Onur Rauf Bingol

    Tests geomdl.control_points module. Requires "pytest" to run.
"""

import pytest
from geomdl import control_points
from geomdl.base import GeomdlError

GEOMDL_TEST_CPTS1 = [
    [1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0], [9.0, 10.0], [11.0, 12.0]
]
GEOMDL_TEST_CPTS2 = [
    [1.0, 2.0, 3.0], [3.0, 4.0, 5.0], [5.0, 6.0, 7.0], [7.0, 8.0, 9.0], [9.0, 10.0, 11.0], [11.0, 12.0, 13.0]
]

GEOMDL_TEST_CPTS3 = [
    [1.0, 2.0, 3.0], [3.0, 4.0, 5.0], [5.0, 6.0, 7.0], [7.0, 8.0, 9.0], [9.0, 10.0, 11.0],
    [11.0, 12.0, 13.0], [21.0, 22.0, 23.0], [23.0, 24.0, 25.0], [25.0, 26.0, 27.0], [27.0, 28.0, 29.0],
    [31.0, 32.0, 33.0], [33.0, 34.0, 35.0]
]

P = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
W = [0.5, 2, 1]
PW = [[0.5, 1, 1.5, 0.5], [8, 10, 12, 2], [7, 8, 9, 1]]
PW_ONES = [[1, 2, 3, 1], [4, 5, 6, 1], [7, 8, 9, 1]]


# Combine with a predefined set of weights
def test_combine_ctrlpts_weights1():
    check = control_points.combine_ctrlpts_weights(P, W)

    assert PW == check


# Combine with default weights
def test_combine_ctrlpts_weights2():
    check = control_points.combine_ctrlpts_weights(P)

    assert PW_ONES == check


def test_separate_ctrlpts_weights():
    c_ctrlpts, c_weights = control_points.separate_ctrlpts_weights(PW)

    assert P == c_ctrlpts
    assert W == c_weights


@pytest.fixture
def cpman1d():
    cpman = control_points.CPManager(6)
    return cpman


@pytest.fixture
def cpman2d():
    cpman = control_points.CPManager(3, 2)
    return cpman


@pytest.fixture
def cpman3d():
    cpman = control_points.CPManager(2, 3, 2)
    return cpman


def test_point_assignment1(cpman1d):
    cpman1d.points = GEOMDL_TEST_CPTS1
    for i in range(len(GEOMDL_TEST_CPTS1[1])):
        assert cpman1d.pt(1)[i] == GEOMDL_TEST_CPTS1[1][i]


def test_point_assignment2(cpman2d):
    cpman2d.points = GEOMDL_TEST_CPTS2
    for i in range(len(GEOMDL_TEST_CPTS3[3])):
        assert cpman2d.pt(0, 1)[i] == GEOMDL_TEST_CPTS2[3][i]


def test_point_assignment3(cpman3d):
    cpman3d.points = GEOMDL_TEST_CPTS3
    for i in range(len(GEOMDL_TEST_CPTS3[11])):
        assert cpman3d.pt(1, 2, 1)[i] == GEOMDL_TEST_CPTS3[11][i]


def test_point_assignment4(cpman3d):
    cpman3d.points = GEOMDL_TEST_CPTS3
    for i in range(len(GEOMDL_TEST_CPTS3[0])):
        assert cpman3d.pt(0, 0, 0)[i] == GEOMDL_TEST_CPTS3[0][i]


def test_point_assignment5(cpman3d):
    cpman3d.points = GEOMDL_TEST_CPTS3
    for i in range(len(GEOMDL_TEST_CPTS3[11])):
        assert cpman3d[1, 2, 1][i] == GEOMDL_TEST_CPTS3[11][i]


def test_point_assignment6(cpman3d):
    cpman3d.points = GEOMDL_TEST_CPTS3
    for i in range(len(GEOMDL_TEST_CPTS3[0])):
        assert cpman3d[0, 0, 0][i] == GEOMDL_TEST_CPTS3[0][i]


def test_point_get_set1(cpman1d):
    pt = (2, 3, 4)
    cpman1d.set_pt(pt, 2)
    for i in range(0, 3):
        assert cpman1d.pt(2)[i] == pt[i]


def test_point_get_set2(cpman1d):
    pt = (2, 3, 4)
    cpman1d[2] = pt
    for i in range(0, 3):
        assert cpman1d.pt(2)[i] == pt[i]


def test_point_dim(cpman1d):
    pt = (2, 3, 4)
    cpman1d.set_pt(pt, 2)
    assert cpman1d.dimension == len(pt)


def test_point_count1(cpman3d):
    assert cpman3d.count == len(GEOMDL_TEST_CPTS3)


def test_point_count2(cpman3d):
    assert len(cpman3d) == len(GEOMDL_TEST_CPTS3)


def test_point_iter(cpman2d):
    cpman2d.points = GEOMDL_TEST_CPTS2
    for i, pt in enumerate(cpman2d):
        for j in range(len(GEOMDL_TEST_CPTS2[i])):
            assert pt[j] == GEOMDL_TEST_CPTS2[i][j]


def test_point_data1():
    """ Control Points Manager: get-set attachment (valid, list) """
    d = [0.0, 1.0, 2.0, 3.0]
    p = 5
    sz = 12
    cpman = control_points.CPManager(sz, testdata=4)
    cpman.set_ptdata(dict(testdata=d), p)
    retv1 = cpman.ptdata('testdata', p)
    retv2 = cpman.ptdata('testdata', p + 1)
    assert retv1[2] == 2.0
    assert retv2[2] == 0.0


def test_point_data2():
    """ Control Points Manager: get-set attachment (invalid, list) """
    d = [0.0, 1.0, 2.0, 3.0]
    p = 5
    sz = 12
    cpman = control_points.CPManager(sz, testdata=4)
    cpman.set_ptdata(dict(testdata=d), p)
    retv = cpman.ptdata('testdata2', p)
    assert retv is None


def test_point_data3():
    """ Control Points Manager: get-set attachment (exception) """
    with pytest.raises(GeomdlError):
        d = [0.0, 1.0, 2.0, 3.0]
        p = 5
        sz = 12
        cpman = control_points.CPManager(sz, testdata=3)
        cpman.set_ptdata(dict(testdata=d), p)


def test_point_data4():
    """ Control Points Manager: get-set attachment (valid, float) """
    d = 13
    p = 5
    sz = 12
    cpman = control_points.CPManager(sz, testdata=1)
    cpman.set_ptdata(dict(testdata=d), p)
    assert cpman.ptdata('testdata', 5) == 13
