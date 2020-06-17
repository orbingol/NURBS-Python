"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2020 Onur Rauf Bingol

    Tests file I/O operations. Requires "pytest" to run.
"""

import os
import pytest
from geomdl import exchange

FILE_NAME = 'testing'


@pytest.mark.usefixtures("curve1")
def test_export_json_curve_single(curve1):
    fname = FILE_NAME + ".curve.json"
    exchange.export_json(curve1, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("surface1")
def test_export_json_surface_single(surface1):
    fname = FILE_NAME + ".surface.json"
    exchange.export_json(surface1, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("volume1")
def test_export_json_volume_single(volume1):
    fname = FILE_NAME + ".volume.json"
    exchange.export_json(volume1, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .obj file exists
@pytest.mark.usefixtures("surface1")
def test_export_obj_single(surface1):
    fname = FILE_NAME + ".obj"
    exchange.export_obj(surface1, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .off file exists
@pytest.mark.usefixtures("surface1")
def test_export_off_single(surface1):
    fname = FILE_NAME + ".off"
    exchange.export_off(surface1, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .stl file exists
@pytest.mark.usefixtures("surface1")
def test_export_stl_single(surface1):
    fname = FILE_NAME + ".stl"
    exchange.export_stl(surface1, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .stl file exists (ascii)
@pytest.mark.usefixtures("surface1")
def test_export_stl_ascii_single(surface1):
    fname = FILE_NAME + ".stl"
    exchange.export_stl(surface1, fname, binary=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("curve1")
def test_export_txt_curve(curve1):
    fname = FILE_NAME + ".txt"
    exchange.export_txt(curve1, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("curve2")
def test_export_import_txt_curve(curve2):
    fname = FILE_NAME + ".txt"
    exchange.export_txt(curve2, fname)

    # Import text file
    result = exchange.import_txt(fname)

    res_array = []
    for res in result:
        res_array.append(res)

    assert res_array == list(curve2.ctrlptsw.points)

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("surface1")
def test_export_import_txt_surface(surface1):
    fname = FILE_NAME + ".txt"
    exchange.export_txt(surface1, fname)

    # Import text file
    result = exchange.import_txt(fname)

    res_array = []
    for res in result:
        res_array.append(res)

    assert res_array == list(surface1.ctrlptsw.points)

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("curve2")
def test_export_vtk_curve_ctrlpts(curve2):
    fname = FILE_NAME + ".vtk"
    exchange.export_polydata(curve2, fname, point_type="ctrlpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("surface2")
def test_export_vtk_surface_ctrlpts(surface2):
    fname = FILE_NAME + ".vtk"
    exchange.export_polydata(surface2, fname, point_type="ctrlpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("curve2")
def test_export_vtk_curve_evalpts(curve2):
    fname = FILE_NAME + ".vtk"
    exchange.export_polydata(curve2, fname, point_type="evalpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("surface2")
def test_export_vtk_surface_evalpts(surface2):
    fname = FILE_NAME + ".vtk"
    exchange.export_polydata(surface2, fname, point_type="evalpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("curve2")
def test_export_csv_curve_ctrlpts(curve2):
    fname = FILE_NAME + ".csv"
    exchange.export_csv(curve2, fname, point_type="ctrlpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("surface2")
def test_export_csv_surface_ctrlpts(surface2):
    fname = FILE_NAME + ".csv"
    exchange.export_csv(surface2, fname, point_type="ctrlpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("curve2")
def test_export_csv_curve_evalpts(curve2):
    fname = FILE_NAME + ".csv"
    exchange.export_csv(curve2, fname, point_type="evalpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("surface2")
def test_export_csv_surface_evalpts(surface2):
    fname = FILE_NAME + ".csv"
    exchange.export_csv(surface2, fname, point_type="evalpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)
