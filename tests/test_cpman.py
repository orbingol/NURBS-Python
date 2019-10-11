"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2019 Onur Rauf Bingol

    Tests control points manager module. Requires "pytest" to run.
"""

import pytest
from geomdl.control_points import CPManager

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


@pytest.fixture
def cpman1d():
    cpman = CPManager(6)
    return cpman


@pytest.fixture
def cpman2d():
    cpman = CPManager(3, 2)
    return cpman


@pytest.fixture
def cpman3d():
    cpman = CPManager(2, 3, 2)
    return cpman


def test_point_assignment1(cpman1d):
    cpman1d.points = GEOMDL_TEST_CPTS1
    for i in range(len(GEOMDL_TEST_CPTS1[1])):
        assert cpman1d.get_pt(1)[i] == GEOMDL_TEST_CPTS1[1][i]


def test_point_assignment2(cpman2d):
    cpman2d.points = GEOMDL_TEST_CPTS2
    for i in range(len(GEOMDL_TEST_CPTS3[3])):
        assert cpman2d.get_pt(0, 1)[i] == GEOMDL_TEST_CPTS2[3][i]


def test_point_assignment3(cpman3d):
    cpman3d.points = GEOMDL_TEST_CPTS3
    for i in range(len(GEOMDL_TEST_CPTS3[11])):
        assert cpman3d.get_pt(1, 2, 1)[i] == GEOMDL_TEST_CPTS3[11][i]


def test_point_assignment4(cpman3d):
    cpman3d.points = GEOMDL_TEST_CPTS3
    for i in range(len(GEOMDL_TEST_CPTS3[0])):
        assert cpman3d.get_pt(0, 0, 0)[i] == GEOMDL_TEST_CPTS3[0][i]


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
        assert cpman1d.get_pt(2)[i] == pt[i]


def test_point_get_set2(cpman1d):
    pt = (2, 3, 4)
    cpman1d[2] = pt
    for i in range(0, 3):
        assert cpman1d.get_pt(2)[i] == pt[i]


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

