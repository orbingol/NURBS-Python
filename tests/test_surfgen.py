"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.GPGen module. Requires "pytest" to run.
"""
import os
import pytest
from geomdl import CPGen

GRID_TOL = 10e-8


@pytest.fixture
def grid():
    """ Generates a 3x4 control points grid """
    surfgrid = CPGen.Grid(7, 13)
    surfgrid.generate(3, 4)
    return surfgrid


@pytest.fixture
def grid2():
    """ Generates a 6x6 control points grid """
    surfgrid = CPGen.Grid(7, 13)
    surfgrid.generate(16, 16)
    return surfgrid


@pytest.fixture
def gridw():
    """ Generates a weighted control points grid """
    surfgrid = CPGen.GridWeighted(7, 13)
    surfgrid.generate(3, 4)
    return surfgrid


def test_grid_generate1():
    test_grid = CPGen.GridWeighted(7, 13)
    with pytest.raises(ValueError):
        test_grid.generate(-1, 5)


def test_grid_generate2():
    test_grid = CPGen.GridWeighted(7, 13)
    with pytest.raises(ValueError):
        test_grid.generate(5, -1)


def test_grid_generate3():
    test_grid = CPGen.GridWeighted(7, 13)
    with pytest.warns(UserWarning):
        test_grid.generate(3.5, 4)


def test_grid_generate4():
    test_grid = CPGen.GridWeighted(7, 13)
    with pytest.warns(UserWarning):
        test_grid.generate(3, 4.2)


def test_grid_generate5(grid):
    # testing regeneration of the grid
    grid.generate(13, 17)

    assert grid._size_u == 13
    assert grid._size_v == 17
    assert len(grid.grid) == 14
    assert len(grid.grid[0]) == 18


def test_grid(grid):
    result = [[[0.0, 0.0, 0.0], [0.0, 3.25, 0.0], [0.0, 6.5, 0.0], [0.0, 9.75, 0.0], [0.0, 13.0, 0.0]],
              [[2.3333333333333335, 0.0, 0.0], [2.3333333333333335, 3.25, 0.0],
               [2.3333333333333335, 6.5, 0.0], [2.3333333333333335, 9.75, 0.0], [2.3333333333333335, 13.0, 0.0]],
              [[4.666666666666667, 0.0, 0.0], [4.666666666666667, 3.25, 0.0], [4.666666666666667, 6.5, 0.0],
               [4.666666666666667, 9.75, 0.0], [4.666666666666667, 13.0, 0.0]],
              [[7.0, 0.0, 0.0], [7.0, 3.25, 0.0], [7.0, 6.5, 0.0], [7.0, 9.75, 0.0], [7.0, 13.0, 0.0]]]

    assert grid.grid == result


def test_grid_reset1(grid):
    grid.reset()

    assert grid._grid_points == []
    assert grid._size_u == 0
    assert grid._size_v == 0
    assert grid._origin == [0.0, 0.0, 0.0]


def test_grid_reset2(gridw):
    gridw.weight = 0.33
    gridw.reset()

    assert gridw._grid_points == []
    assert gridw._size_u == 0
    assert gridw._size_v == 0
    assert gridw._origin == [0.0, 0.0, 0.0]
    assert gridw._cache['grid_points'] == []
    assert gridw._weight == 1.0


def test_grid_weight1(gridw):
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

    # default weight is 1.0
    assert gridw.grid == result


def test_grid_weight2(gridw):
    with pytest.raises(TypeError):
        gridw.weight = "test string"


def test_grid_weight3(gridw):
    with pytest.raises(ValueError):
        gridw.weight = -0.1


def test_grid_weight4(gridw):
    # default weight should be 1.0
    assert gridw.weight == 1.0


def test_grid_weight5(gridw):
    # try to change weight
    gridw.weight = 0.35
    assert gridw.weight == 0.35


def test_grid_weight6(gridw):
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

    gen_cache_var = gridw.grid

    # this should pull up the grid from the cache
    assert gridw.grid == result


def test_grid_save1(grid):
    fname = "test_grid.txt"
    grid.save(fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_grid_save1_weighted(gridw):
    fname = "test_gridw.txt"
    gridw.save(fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_grid_save2():
    test_grid = CPGen.Grid(5, 7)
    with pytest.raises(RuntimeError):
        # trying to save before generate()
        test_grid.save()


def test_grid_save3(grid):
    with pytest.raises(TypeError):
        # file name should be a string
        grid.save(5)


def test_grid_save4(grid):
    with pytest.raises(IOError):
        # impossible file name
        grid.save("")


def test_bumps1(grid2):
    grid2.bumps(num_bumps=2, bump_height=[5.0, 7.0], base_extent=2)
    check_vals = grid2.grid

    check = False
    for rows in check_vals:
        for val in rows:
            if val[2] == 5.0 or val[2] == 7.0:
                check = True

    assert check


def test_bumps1_all_positive_heights(grid2):
    grid2.bumps(num_bumps=2, bump_height=5, base_extent=2)
    check_vals = grid2.grid

    check = False
    for rows in check_vals:
        for val in rows:
            if val[2] == 5.0:
                check = True

    assert check


def test_bumps2(grid2):
    with pytest.raises(RuntimeError):
        # impossible to add 100 bumps on this specific grid
        grid2.bumps(num_bumps=100, bump_height=5, base_extent=2)


def test_bumps4():
    test_grid = CPGen.Grid(5, 7)
    with pytest.raises(RuntimeError):
        # bumps before calling generate()
        test_grid.bumps(num_bumps=3)


def test_bumps5(grid2):
    with pytest.warns(UserWarning):
        # non-integer num_bumps
        grid2.bumps(num_bumps=1.1, bump_height=5, base_extent=2)


def test_bumps8(grid2):
    with pytest.raises(ValueError):
        # large base_extent
        grid2.bumps(num_bumps=1, bump_height=5, base_extent=20)


def test_bumps9(grid2):
    with pytest.raises(ValueError):
        # small base_extent
        grid2.bumps(num_bumps=1, bump_height=5, base_extent=0)


def test_grid_translate1(grid):
    grid.translate(pos=(2, 3, 4))

    result = [[[2.0, 3.0, 4.0], [2.0, 6.25, 4.0], [2.0, 9.5, 4.0], [2.0, 12.75, 4.0], [2.0, 16.0, 4.0]],
              [[4.333333333333334, 3.0, 4.0], [4.333333333333334, 6.25, 4.0], [4.333333333333334, 9.5, 4.0], [4.333333333333334, 12.75, 4.0], [4.333333333333334, 16.0, 4.0]],
              [[6.666666666666667, 3.0, 4.0], [6.666666666666667, 6.25, 4.0], [6.666666666666667, 9.5, 4.0], [6.666666666666667, 12.75, 4.0], [6.666666666666667, 16.0, 4.0]],
              [[9.0, 3.0, 4.0], [9.0, 6.25, 4.0], [9.0, 9.5, 4.0], [9.0, 12.75, 4.0], [9.0, 16.0, 4.0]]]

    assert grid._origin == [2, 3, 4]
    assert grid.grid == result


def test_grid_translate2():
    test_grid = CPGen.Grid(7, 13)
    with pytest.raises(RuntimeError):
        # translate before generating the grid
        test_grid.translate(pos=(1, 2, 3))


def test_grid_translate3(grid):
    with pytest.raises(TypeError):
        # input is not a list of tuple
        grid.translate("(5, 4, 5)")


def test_grid_translate4(grid):
    with pytest.raises(ValueError):
        # input is not a list of tuple
        grid.translate(pos=[5, 4])


def test_grid_translate5(grid):
    with pytest.raises(ValueError):
        # input is not a list of tuple
        grid.translate(pos=[5, 4, 6, 7])


def test_grid_rotate_x1(grid):
    grid.rotate_x(45)

    result = [[[0.0, 0.0, 0.0], [0.0, 2.29809703885628, 2.29809703885628], [0.0, 4.59619407771256, 4.59619407771256], [0.0, 6.894291116568839, 6.894291116568839], [0.0, 9.19238815542512, 9.19238815542512]],
              [[2.3333333333333335, 0.0, 0.0], [2.3333333333333335, 2.29809703885628, 2.29809703885628], [2.3333333333333335, 4.59619407771256, 4.59619407771256], [2.3333333333333335, 6.894291116568839, 6.894291116568839], [2.3333333333333335, 9.19238815542512, 9.19238815542512]],
              [[4.666666666666667, 0.0, 0.0], [4.666666666666667, 2.29809703885628, 2.29809703885628], [4.666666666666667, 4.59619407771256, 4.59619407771256], [4.666666666666667, 6.894291116568839, 6.894291116568839], [4.666666666666667, 9.19238815542512, 9.19238815542512]],
              [[7.0, 0.0, 0.0], [7.0, 2.29809703885628, 2.29809703885628], [7.0, 4.59619407771256, 4.59619407771256], [7.0, 6.894291116568839, 6.894291116568839], [7.0, 9.19238815542512, 9.19238815542512]]]

    check = True
    assert len(grid.grid) == len(result)
    size1 = len(grid.grid)
    for idx1 in range(size1):
        assert len(grid.grid[idx1]) == len(result[idx1])
        size2 = len(grid.grid[idx1])
        for idx2 in range(size2):
            for g, r in zip(grid.grid[idx1][idx2], result[idx1][idx2]):
                if abs(g - r) > GRID_TOL:
                    check = False

    assert check


def test_grid_rotate_x2():
    test_grid = CPGen.Grid(7, 13)
    with pytest.raises(RuntimeError):
        test_grid.rotate_x(15)


def test_grid_rotate_y1(grid):
    grid.rotate_y(45)

    result = [[[0.0, 0.0, 0.0], [0.0, 3.25, 0.0], [0.0, 6.5, 0.0], [0.0, 9.75, 0.0], [0.0, 13.0, 0.0]],
              [[1.649915822768611, 0.0, 1.649915822768611], [1.649915822768611, 3.25, 1.649915822768611], [1.649915822768611, 6.5, 1.649915822768611], [1.649915822768611, 9.75, 1.649915822768611], [1.649915822768611, 13.0, 1.649915822768611]],
              [[3.299831645537222, 0.0, 3.299831645537222], [3.299831645537222, 3.25, 3.299831645537222], [3.299831645537222, 6.5, 3.299831645537222], [3.299831645537222, 9.75, 3.299831645537222], [3.299831645537222, 13.0, 3.299831645537222]],
              [[4.949747468305833, 0.0, 4.949747468305833], [4.949747468305833, 3.25, 4.949747468305833], [4.949747468305833, 6.5, 4.949747468305833], [4.949747468305833, 9.75, 4.949747468305833], [4.949747468305833, 13.0, 4.949747468305833]]]

    check = True
    assert len(grid.grid) == len(result)
    size1 = len(grid.grid)
    for idx1 in range(size1):
        assert len(grid.grid[idx1]) == len(result[idx1])
        size2 = len(grid.grid[idx1])
        for idx2 in range(size2):
            for g, r in zip(grid.grid[idx1][idx2], result[idx1][idx2]):
                if abs(g - r) > GRID_TOL:
                    check = False

    assert check


def test_grid_rotate_y2():
    test_grid = CPGen.Grid(7, 13)
    with pytest.raises(RuntimeError):
        test_grid.rotate_y(15)


def test_grid_rotate_z1(grid):
    grid.rotate_z(45)

    result = [[[0.0, 0.0, 0.0], [-2.29809703885628, 2.29809703885628, 0.0], [-4.59619407771256, 4.59619407771256, 0.0], [-6.894291116568839, 6.894291116568839, 0.0], [-9.19238815542512, 9.19238815542512, 0.0]],
              [[1.649915822768611, 1.649915822768611, 0.0], [-0.6481812160876688, 3.948012861624891, 0.0], [-2.9462782549439486, 6.246109900481171, 0.0], [-5.244375293800228, 8.54420693933745, 0.0], [-7.542472332656509, 10.84230397819373, 0.0]],
              [[3.299831645537222, 3.299831645537222, 0.0], [1.0017346066809423, 5.597928684393501, 0.0], [-1.2963624321753375, 7.896025723249782, 0.0], [-3.594459471031617, 10.194122762106062, 0.0], [-5.892556509887897, 12.492219800962342, 0.0]],
              [[4.949747468305833, 4.949747468305833, 0.0], [2.651650429449553, 7.247844507162112, 0.0], [0.35355339059327306, 9.545941546018392, 0.0], [-1.9445436482630063, 11.84403858487467, 0.0], [-4.2426406871192865, 14.142135623730951, 0.0]]]

    check = True
    assert len(grid.grid) == len(result)
    size1 = len(grid.grid)
    for idx1 in range(size1):
        assert len(grid.grid[idx1]) == len(result[idx1])
        size2 = len(grid.grid[idx1])
        for idx2 in range(size2):
            for g, r in zip(grid.grid[idx1][idx2], result[idx1][idx2]):
                if abs(g - r) > GRID_TOL:
                    check = False

    assert check


def test_grid_rotate_z2():
    test_grid = CPGen.Grid(7, 13)
    with pytest.raises(RuntimeError):
        test_grid.rotate_z(15)
