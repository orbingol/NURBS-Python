"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Requires "pytest" to run.
"""

import pytest
from random import randint
from geomdl.geomutils import dimension


@pytest.mark.usefixtures("curve7")
def test_geomutils_add_dimension(curve7):
    # curve7 is a 2-dimensional curve
    res = dimension.add_dimension(curve7)

    assert res.dimension == curve7.dimension + 1

@pytest.mark.usefixtures("curve7")
def test_geomutils_add_dimension_ctrlpts(curve7):
    # curve7 is a 2-dimensional curve
    res = dimension.add_dimension(curve7)

    idx = randint(0, res.ctrlpts.count)
    assert len(res.ctrlpts[idx]) == curve7.dimension + 1


@pytest.mark.usefixtures("curve7")
def test_geomutils_add_dimension_inplace(curve7):
    # curve7 is a 2-dimensional curve
    res = dimension.add_dimension(curve7, inplace=True)

    assert res.dimension == curve7.dimension
