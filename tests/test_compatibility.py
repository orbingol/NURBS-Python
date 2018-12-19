"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.compatibility module. Requires "pytest" to run.
"""
from geomdl import compatibility

P = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
W = [0.5, 2, 1]
PW = [[0.5, 1, 1.5, 0.5], [8, 10, 12, 2], [7, 8, 9, 1]]
PW_ONES = [[1, 2, 3, 1], [4, 5, 6, 1], [7, 8, 9, 1]]
PW_SEP = [[1, 2, 3, 0.5], [4, 5, 6, 2], [7, 8, 9, 1]]


# Combine with a predefined set of weights
def test_combine_ctrlpts_weights1():
    check = compatibility.combine_ctrlpts_weights(P, W)

    assert PW == check


# Combine with default weights
def test_combine_ctrlpts_weights2():
    check = compatibility.combine_ctrlpts_weights(P)

    assert PW_ONES == check


def test_generate_ctrlpts_weights():
    check = compatibility.generate_ctrlpts_weights(PW)

    assert PW_SEP == check


def test_generate_ctrlptsw():
    check = compatibility.generate_ctrlptsw(PW_SEP)

    assert PW == check


def test_separate_ctrlpts_weights():
    c_ctrlpts, c_weights = compatibility.separate_ctrlpts_weights(PW)

    assert P == c_ctrlpts
    assert W == c_weights


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

    check = compatibility.flip_ctrlpts_u(ctrlpts, size_u, size_v)

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


def test_generate_ctrlptsw2d_ops():
    ctrlpts_weights_2d = [[[0, 0, 0, 1], [0, 1, 0, 0.5], [0, 2, -3, 0.25], [0, 3, 7, 0.75]],
                          [[1, 0, 6, 1], [1, 1, 0, 0.5], [1, 2, 0, 0.25], [1, 3, 8, 0.75]],
                          [[2, 0, 0, 1], [2, 1, 0, 0.5], [2, 2, 3, 0.25], [1, 3, 7, 0.75]]]

    ctrlptsw_2d = compatibility.generate_ctrlptsw2d(ctrlpts_weights_2d)
    check = compatibility.generate_ctrlpts2d_weights(ctrlptsw_2d)

    assert check == ctrlpts_weights_2d
