"""
    pytest fixtures for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol
"""

import pytest
from geomdl import NURBS
from geomdl import construct


@pytest.fixture
def surface1(curve1, curve2, curve3):
    s = construct.construct_surface("u", curve1, curve2, curve3)
    return s


@pytest.fixture
def surface2(curve4, curve5, curve6):
    s = construct.construct_surface("u", curve4, curve5, curve6)
    return s


@pytest.fixture
def surface3(curve1, curve3):
    s = construct.construct_surface("v", curve1, curve3)
    return s


@pytest.fixture
def surface4(curve4, curve6):
    s = construct.construct_surface("v", curve4, curve6)
    return s
