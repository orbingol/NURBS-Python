"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.compatibility module. Requires "pytest" to run.
"""
from geomdl import compatibility


def test_change_ctrlpts_row_order():
    size_u = 3
    size_v = 4
    # the following is in u-order
    ctrlpts = [[0, 0, 0], [1, 0, 6], [2, 0, 0],
              [0, 1, 0], [1, 1, 0], [2, 1, 0],
              [0, 2, -3], [1, 2, 0], [2, 2, 3],
              [0, 3, 7], [1, 3, 8], [1, 3, 7]]
    # the following is in v-order
    result = [[0, 0, 0], [0, 1, 0], [0, 2, -3], [0, 3, 7],
              [1, 0, 6], [1, 1, 0], [1, 2, 0], [1, 3, 8],
              [2, 0, 0], [2, 1, 0], [2, 2, 3], [1, 3, 7]]

    check = compatibility.change_ctrlpts_row_order(ctrlpts, size_u, size_v)

    assert check == result


def test_flip_ctrlpts():
    size_u = 3
    size_v = 4

    # the following is in v-order
    ctrlpts = [[0, 0, 0], [0, 1, 0], [0, 2, -3], [0, 3, 7],
               [1, 0, 6], [1, 1, 0], [1, 2, 0], [1, 3, 8],
               [2, 0, 0], [2, 1, 0], [2, 2, 3], [1, 3, 7]]

    # the following is in u-order
    result = [[0, 0, 0], [1, 0, 6], [2, 0, 0],
              [0, 1, 0], [1, 1, 0], [2, 1, 0],
              [0, 2, -3], [1, 2, 0], [2, 2, 3],
              [0, 3, 7], [1, 3, 8], [1, 3, 7]]

    check = compatibility.flip_ctrlpts(ctrlpts, size_u, size_v)

    assert check == result


def test_flip_ctrlpts2d():
    # the following is in v-order
    ctrlpts = [[[0, 0, 0], [0, 1, 0], [0, 2, -3], [0, 3, 7]],
               [[1, 0, 6], [1, 1, 0], [1, 2, 0], [1, 3, 8]],
               [[2, 0, 0], [2, 1, 0], [2, 2, 3], [1, 3, 7]]]

    # the following is in u-order
    result = [[[0, 0, 0], [1, 0, 6], [2, 0, 0]],
              [[0, 1, 0], [1, 1, 0], [2, 1, 0]],
              [[0, 2, -3], [1, 2, 0], [2, 2, 3]],
              [[0, 3, 7], [1, 3, 8], [1, 3, 7]]]

    check = compatibility.flip_ctrlpts2d(ctrlpts)

    assert check == result
