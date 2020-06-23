"""
    pytest fixtures for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol
"""

import pytest
from geomdl import BSpline, NURBS, knotvector
from geomdl.geomutils import construct
from geomdl.examples.volume import volume_ex2


@pytest.fixture
def volume1(surface1, surface2):
    v = construct.construct_volume("w", surface1, surface2)
    return v


@pytest.fixture
def volume2():
    return volume_ex2()
