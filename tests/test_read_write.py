"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests file I/O operations. Requires "pytest" to run.
"""

import os
import pytest
from geomdl import BSpline, NURBS
from geomdl import exchange
from geomdl import compatibility
from geomdl import operations

FILE_NAME = 'testing'
SAMPLE_SIZE = 25


@pytest.fixture
def bspline_curve3d():
    """ Creates a B-Spline 3-dimensional curve instance """
    curve = BSpline.Curve()
    curve.degree = 2
    curve.ctrlpts = [[1, 1, 0], [2, 1, -1], [2, 2, 0]]
    curve.knotvector = [0, 0, 0, 1, 1, 1]
    return curve


@pytest.fixture
def bspline_surface():
    """ Creates a B-Spline surface instance """
    surf = BSpline.Surface()
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlpts_size_u = 3
    surf.ctrlpts_size_v = 3
    surf.ctrlpts = [[0, 0, 0], [0, 1, 0], [0, 2, -3],
                    [1, 0, 6], [1, 1, 0], [1, 2, 0],
                    [2, 0, 0], [2, 1, 0], [2, 2, 3]]
    surf.knotvector_u = [0, 0, 0, 1, 1, 1]
    surf.knotvector_v = [0, 0, 0, 1, 1, 1]
    return surf


@pytest.fixture
def nurbs_surface():
    """ Creates a NURBS surface instance """
    surf = NURBS.Surface()
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlpts_size_u = 3
    surf.ctrlpts_size_v = 3
    surf.ctrlpts = [[0, 0, 0], [0, 1, 0], [0, 2, -3],
                    [1, 0, 6], [1, 1, 0], [1, 2, 0],
                    [2, 0, 0], [2, 1, 0], [2, 2, 3]]
    # use the auto-generated weights vector
    surf.knotvector_u = [0, 0, 0, 1, 1, 1]
    surf.knotvector_v = [0, 0, 0, 1, 1, 1]
    return surf


@pytest.fixture
def nurbs_surface_decompose():
    """ Creates a NURBS surface instance (decomposable) """
    surf = NURBS.Surface()
    surf.degree_u = 2
    surf.degree_v = 2
    surf.ctrlpts_size_u = 3
    surf.ctrlpts_size_v = 4
    surf.ctrlpts = [[0, 0, 0], [0, 1, 0], [0, 2, -3], [0, 3, 7],
                    [1, 0, 6], [1, 1, 0], [1, 2, 0], [1, 3, 8],
                    [2, 0, 0], [2, 1, 0], [2, 2, 3], [1, 3, 7]]
    # use the auto-generated weights vector
    surf.knotvector_u = [0, 0, 0, 1, 1, 1]
    surf.knotvector_v = [0, 0, 0, 0.5, 1, 1, 1]
    return surf


# Tests pickled load-save operations on curves
def test_bspline_curve_loadsave(bspline_curve3d):
    fname = FILE_NAME + ".pickle"

    bspline_curve3d.save(fname)

    curve_load = BSpline.Curve()
    curve_load.load(fname)

    # Remove save file
    os.remove(fname)

    assert bspline_curve3d.degree == curve_load.degree
    assert bspline_curve3d.knotvector == curve_load.knotvector
    assert bspline_curve3d.ctrlpts == curve_load.ctrlpts
    assert bspline_curve3d.dimension == curve_load.dimension


def test_bspline_curve_save_error(bspline_curve3d):
    fname = ""

    with pytest.raises(IOError):
        bspline_curve3d.save(fname)


def test_bspline_curve_load_error(bspline_curve3d):
    fname = ""

    with pytest.raises(IOError):
        bspline_curve3d.load(fname)


# Tests pickled load-save operations on surfaces
def test_bspline_surface_loadsave(bspline_surface):
    fname = FILE_NAME + ".pickle"

    bspline_surface.save(fname)

    surf_load = BSpline.Surface()
    surf_load.load(fname)

    # Remove save file
    os.remove(fname)

    assert bspline_surface.degree_u == surf_load.degree_u
    assert bspline_surface.degree_v == surf_load.degree_v
    assert bspline_surface.knotvector_u == surf_load.knotvector_u
    assert bspline_surface.knotvector_v == surf_load.knotvector_v
    assert bspline_surface.ctrlpts == surf_load.ctrlpts
    assert bspline_surface.ctrlpts_size_u == surf_load.ctrlpts_size_u
    assert bspline_surface.ctrlpts_size_v == surf_load.ctrlpts_size_v
    assert bspline_surface.dimension == surf_load.dimension


# Tests if the .obj file exists
def test_export_obj_single(nurbs_surface):
    fname = FILE_NAME + ".obj"

    nurbs_surface.sample_size = SAMPLE_SIZE
    exchange.export_obj(nurbs_surface, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .off file exists
def test_export_off_single(nurbs_surface):
    fname = FILE_NAME + ".off"

    nurbs_surface.sample_size = SAMPLE_SIZE
    exchange.export_off(nurbs_surface, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .stl file exists
def test_export_stl_single(nurbs_surface):
    fname = FILE_NAME + ".stl"

    nurbs_surface.sample_size = SAMPLE_SIZE
    exchange.export_stl(nurbs_surface, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .stl file exists (ascii)
def test_export_stl_ascii_single(nurbs_surface):
    fname = FILE_NAME + ".stl"

    nurbs_surface.sample_size = SAMPLE_SIZE
    exchange.export_stl(nurbs_surface, fname, binary=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .obj file exists
def test_export_obj_multi(nurbs_surface_decompose):
    fname = FILE_NAME + ".obj"

    nurbs_multi = operations.decompose_surface(nurbs_surface_decompose)

    nurbs_multi.sample_size = SAMPLE_SIZE
    exchange.export_obj(nurbs_multi, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .off file exists
def test_export_off_multi(nurbs_surface_decompose):
    fname = FILE_NAME + ".off"

    nurbs_multi = operations.decompose_surface(nurbs_surface_decompose)

    nurbs_multi.sample_size = SAMPLE_SIZE
    exchange.export_off(nurbs_multi, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .stl file exists
def test_export_stl_multi(nurbs_surface_decompose):
    fname = FILE_NAME + ".stl"

    nurbs_multi = operations.decompose_surface(nurbs_surface_decompose)

    nurbs_multi.sample_size = SAMPLE_SIZE
    exchange.export_stl(nurbs_multi, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Tests if the .stl file exists (ascii)
def test_export_stl_ascii_multi(nurbs_surface_decompose):
    fname = FILE_NAME + ".stl"

    nurbs_multi = operations.decompose_surface(nurbs_surface_decompose)

    nurbs_multi.sample_size = SAMPLE_SIZE
    exchange.export_stl(nurbs_multi, fname, binary=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_txt_curve(bspline_curve3d):
    fname = FILE_NAME + ".txt"

    bspline_curve3d.sample_size = SAMPLE_SIZE
    exchange.export_txt(bspline_curve3d, fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_import_txt_curve(bspline_curve3d):
    fname = FILE_NAME + ".txt"

    bspline_curve3d.sample_size = SAMPLE_SIZE
    exchange.export_txt(bspline_curve3d, fname)

    # Import text file
    result = exchange.import_txt(fname)

    res_array = []
    for res in result:
        res_array.append(tuple(res))

    assert tuple(res_array) == bspline_curve3d.ctrlpts

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_import_txt_surface1(bspline_surface):
    fname = FILE_NAME + ".txt"

    bspline_surface.sample_size = SAMPLE_SIZE
    exchange.export_txt(bspline_surface, fname, two_dimensional=False)

    # Import text file
    result = exchange.import_txt(fname, two_dimensional=False)

    res_array = []
    for res in result:
        res_array.append(tuple(res))

    assert tuple(res_array) == bspline_surface.ctrlpts

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_import_txt_surface2(bspline_surface):
    fname = FILE_NAME + ".txt"

    bspline_surface.sample_size = SAMPLE_SIZE
    exchange.export_txt(bspline_surface, fname, two_dimensional=True)

    # Import text file
    result, size_u, size_v = exchange.import_txt(fname, two_dimensional=True)

    res_array = []
    for res in result:
        res_array.append(tuple(res))

    assert tuple(res_array) == bspline_surface.ctrlpts
    assert size_u == bspline_surface.ctrlpts_size_u
    assert size_v == bspline_surface.ctrlpts_size_v

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_vtk_curve_ctrlpts(bspline_curve3d):
    fname = FILE_NAME + ".vtk"

    bspline_curve3d.sample_size = SAMPLE_SIZE
    exchange.export_vtk(bspline_curve3d, fname, point_type="ctrlpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_vtk_surface_ctrlpts(bspline_surface):
    fname = FILE_NAME + ".vtk"

    bspline_surface.sample_size = SAMPLE_SIZE
    exchange.export_vtk(bspline_surface, fname, point_type="ctrlpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_vtk_curve_evalpts(bspline_curve3d):
    fname = FILE_NAME + ".vtk"

    bspline_curve3d.sample_size = SAMPLE_SIZE
    exchange.export_vtk(bspline_curve3d, fname, point_type="evalpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_vtk_surface_evalpts(bspline_surface):
    fname = FILE_NAME + ".vtk"

    bspline_surface.sample_size = SAMPLE_SIZE
    exchange.export_vtk(bspline_surface, fname, point_type="evalpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_csv_curve_ctrlpts(bspline_curve3d):
    fname = FILE_NAME + ".csv"

    bspline_curve3d.sample_size = SAMPLE_SIZE
    exchange.export_csv(bspline_curve3d, fname, point_type="ctrlpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_csv_surface_ctrlpts(bspline_surface):
    fname = FILE_NAME + ".csv"

    bspline_surface.sample_size = SAMPLE_SIZE
    exchange.export_csv(bspline_surface, fname, point_type="ctrlpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_csv_curve_evalpts(bspline_curve3d):
    fname = FILE_NAME + ".csv"

    bspline_curve3d.sample_size = SAMPLE_SIZE
    exchange.export_csv(bspline_curve3d, fname, point_type="evalpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_export_csv_surface_evalpts(bspline_surface):
    fname = FILE_NAME + ".csv"

    bspline_surface.sample_size = SAMPLE_SIZE
    exchange.export_csv(bspline_surface, fname, point_type="evalpts")

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Testing read-write operations in compatibility module
def test_compatibility_flip_ctrlpts2d_file1(bspline_surface):
    fname_in = FILE_NAME + "_in.txt"
    fname_out = FILE_NAME + "_out.txt"

    bspline_surface.sample_size = SAMPLE_SIZE
    exchange.export_txt(bspline_surface, fname_in, two_dimensional=True)

    compatibility.flip_ctrlpts2d_file(fname_in, fname_out)

    assert os.path.isfile(fname_out)
    assert os.path.getsize(fname_out) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname_in):
        os.remove(fname_in)
        os.remove(fname_out)


def test_compatibility_flip_ctrlpts2d_file2(bspline_surface):
    fname_in = FILE_NAME + "_in.txt"
    fname_out = FILE_NAME + "_out.txt"

    with pytest.raises(IOError):
        compatibility.flip_ctrlpts2d_file(fname_in, fname_out)


def test_compatibility_flip_ctrlpts2d_file3(bspline_surface):
    fname_in = FILE_NAME + "_in.txt"
    fname_out = ""

    bspline_surface.sample_size = SAMPLE_SIZE
    exchange.export_txt(bspline_surface, fname_in, two_dimensional=True)

    with pytest.raises(IOError):
        compatibility.flip_ctrlpts2d_file(fname_in, fname_out)

    # Clean up temporary file if exists
    if os.path.isfile(fname_in):
        os.remove(fname_in)


def test_compatibility_generate_ctrlpts2d_weights_file(nurbs_surface):
    fname_in = FILE_NAME + "_in.txt"
    fname_out = FILE_NAME + "_out.txt"

    nurbs_surface.sample_size = SAMPLE_SIZE
    exchange.export_txt(nurbs_surface, fname_in, two_dimensional=True)

    compatibility.generate_ctrlpts2d_weights_file(fname_in, fname_out)

    assert os.path.isfile(fname_out)
    assert os.path.getsize(fname_out) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname_in):
        os.remove(fname_in)
        os.remove(fname_out)


def test_compatibility_generate_ctrlptsw2d_file1(nurbs_surface):
    fname_in = FILE_NAME + "_in.txt"
    fname_out = FILE_NAME + "_out.txt"
    fname_final = FILE_NAME + "_final.txt"

    exchange.export_txt(nurbs_surface, fname_in, two_dimensional=True)

    compatibility.generate_ctrlpts2d_weights_file(fname_in, fname_out)
    compatibility.generate_ctrlptsw2d_file(fname_out, fname_final)

    assert os.path.isfile(fname_final)
    assert os.path.getsize(fname_final) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname_in):
        os.remove(fname_in)
        os.remove(fname_out)
        os.remove(fname_final)


def test_compatibility_generate_ctrlptsw2d_file2(nurbs_surface):
    fname_in = FILE_NAME + "_in.txt"
    fname_out = FILE_NAME + "_out.txt"
    fname_final = FILE_NAME + "_final.txt"

    exchange.export_txt(nurbs_surface, fname_in, two_dimensional=True)

    compatibility.generate_ctrlpts2d_weights_file(fname_in, fname_out)
    compatibility.generate_ctrlptsw2d_file(fname_out, fname_final)
    ctrlpts, size_u, size_v = exchange.import_txt(fname_final, two_dimensional=True)
    ctrlptsw = compatibility.generate_ctrlptsw(ctrlpts)

    res_array = []
    for res in ctrlptsw:
        res_array.append(tuple(res))

    assert nurbs_surface.ctrlptsw == tuple(res_array)
    assert nurbs_surface.ctrlpts_size_u == size_u
    assert nurbs_surface.ctrlpts_size_v == size_v

    # Clean up temporary file if exists
    if os.path.isfile(fname_in):
        os.remove(fname_in)
        os.remove(fname_out)
        os.remove(fname_final)