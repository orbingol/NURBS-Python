"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.GPGen module. Requires "pytest" to run.
"""
import os
import pytest
from geomdl import CPGen


@pytest.fixture
def grid():
    """ Generates a control points grid """
    surfgrid = CPGen.Grid(7, 13)
    surfgrid.generate(3, 4)
    return surfgrid


@pytest.fixture
def gridw():
    """ Generates a weighted control points grid """
    surfgrid = CPGen.GridWeighted(7, 13)
    surfgrid.generate(3, 4)
    return surfgrid


def test_grid(grid):
    result = [[[0.0, 0.0, 0.0], [0.0, 3.25, 0.0], [0.0, 6.5, 0.0], [0.0, 9.75, 0.0], [0.0, 13.0, 0.0]],
              [[2.3333333333333335, 0.0, 0.0], [2.3333333333333335, 3.25, 0.0],
               [2.3333333333333335, 6.5, 0.0], [2.3333333333333335, 9.75, 0.0], [2.3333333333333335, 13.0, 0.0]],
              [[4.666666666666667, 0.0, 0.0], [4.666666666666667, 3.25, 0.0], [4.666666666666667, 6.5, 0.0],
               [4.666666666666667, 9.75, 0.0], [4.666666666666667, 13.0, 0.0]],
              [[7.0, 0.0, 0.0], [7.0, 3.25, 0.0], [7.0, 6.5, 0.0], [7.0, 9.75, 0.0], [7.0, 13.0, 0.0]]]

    assert grid.grid() == result


def test_bumps1(grid):
    grid.bumps(num_bumps=1, all_positive=False, bump_height=5, smoothness=2)
    check_vals = grid.grid()

    check = False
    for rows in check_vals:
        for val in rows:
            # should consider negative values too
            if abs(val[2]) == 5.0:
                check = True

    assert check


def test_bumps2(grid):
    with pytest.raises(ValueError):
        # impossible to add 10 bumps with a smoothness of 5 on this specific grid
        grid.bumps(num_bumps=10, all_positive=False, bump_height=5, smoothness=5)


def test_add_weight1(gridw):
    result = [[[0.0, 0.0, 0.0, 1.0], [0.0, 3.25, 0.0, 1.0], [0.0, 6.5, 0.0, 1.0],
               [0.0, 9.75, 0.0, 1.0], [0.0, 13.0, 0.0, 1.0]],
              [[2.3333333333333335, 0.0, 0.0, 1.0], [2.3333333333333335, 3.25, 0.0, 1.0],
               [2.3333333333333335, 6.5, 0.0, 1.0], [2.3333333333333335, 9.75, 0.0, 1.0],
               [2.3333333333333335, 13.0, 0.0, 1.0]],
              [[4.666666666666667, 0.0, 0.0, 1.0],
               [4.666666666666667, 3.25, 0.0, 1.0], [4.666666666666667, 6.5, 0.0, 1.0],
               [4.666666666666667, 9.75, 0.0, 1.0], [4.666666666666667, 13.0, 0.0, 1.0]],
              [[7.0, 0.0, 0.0, 1.0], [7.0, 3.25, 0.0, 1.0], [7.0, 6.5, 0.0, 1.0],
               [7.0, 9.75, 0.0, 1.0], [7.0, 13.0, 0.0, 1.0]]]

    gridw.add_weight()

    assert gridw.grid() == result


def test_add_weight2(gridw):
    with pytest.warns(UserWarning):
        # add weights
        gridw.add_weight()
        # second call should issue a UserWarning
        gridw.add_weight()


def test_add_weight3(gridw):
    with pytest.raises(ValueError):
        gridw.add_weight(-0.1)


def test_modify_weight1(gridw):
    result = [[[0.0, 0.0, 0.0, 0.25], [0.0, 13.0, 0.0, 0.25], [0.0, 26.0, 0.0, 0.25],
               [0.0, 39.0, 0.0, 0.25], [0.0, 52.0, 0.0, 0.25]],
              [[9.333333333333334, 0.0, 0.0, 0.25], [9.333333333333334, 13.0, 0.0, 0.25],
               [9.333333333333334, 26.0, 0.0, 0.25], [9.333333333333334, 39.0, 0.0, 0.25],
               [9.333333333333334, 52.0, 0.0, 0.25]],
              [[18.666666666666668, 0.0, 0.0, 0.25], [18.666666666666668, 13.0, 0.0, 0.25],
               [18.666666666666668, 26.0, 0.0, 0.25], [18.666666666666668, 39.0, 0.0, 0.25],
               [18.666666666666668, 52.0, 0.0, 0.25]],
              [[28.0, 0.0, 0.0, 0.25], [28.0, 13.0, 0.0, 0.25], [28.0, 26.0, 0.0, 0.25],
               [28.0, 39.0, 0.0, 0.25], [28.0, 52.0, 0.0, 0.25]]]

    gridw.add_weight()
    gridw.modify_weight(0.25)

    assert gridw.grid() == result


def test_modify_weight2(gridw):
    with pytest.warns(UserWarning):
        # calling modify weights should issue a UserWarning
        gridw.modify_weight(0.5)


def test_modify_weight3(gridw):
    with pytest.raises(ValueError):
        gridw.add_weight()
        gridw.modify_weight(-0.5)


def test_grid_save(grid):
    fname = "test_grid.txt"
    grid.save(fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)
