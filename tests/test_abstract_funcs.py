"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2020 Onur Rauf Bingol

    Tests functions in the "abstract" module. Requires "pytest" to run.
"""

from geomdl import abstract


def test_check_uv1():
    u = -0.1
    v = 0.1
    assert not abstract.validate_params([u, v])


def test_check_uv2():
    u = 2
    v = 0.1
    assert not abstract.validate_params([u, v])


def test_check_uv3():
    v = -0.1
    u = 0.1
    assert not abstract.validate_params([u, v])


def test_check_uv4():
    v = 2
    u = 0.1
    assert not abstract.validate_params([u, v])
