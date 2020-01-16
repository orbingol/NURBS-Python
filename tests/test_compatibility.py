"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2020 Onur Rauf Bingol

    Tests geomdl.control_points module. Requires "pytest" to run.
"""

from geomdl import control_points

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
