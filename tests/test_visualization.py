"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests visualization modules. Requires "pytest" to run.
"""
import os
import pytest
from geomdl import BSpline, NURBS
from geomdl.visualization import VisMPL

SAMPLE_SIZE = 25


@pytest.fixture
def bspline_curve3d():
    """ Creates a B-Spline 3-dimensional curve instance """
    # Create a curve instance
    curve = BSpline.Curve()

    # Set curve degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
                     [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set sample size
    curve.sample_size = SAMPLE_SIZE

    # Return the instance
    return curve


@pytest.fixture
def bspline_surface():
    """ Creates a B-Spline surface instance """
    # Create a surface instance
    surf = BSpline.Surface()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.ctrlpts_size_u = 6
    surf.ctrlpts_size_v = 6
    surf.ctrlpts = [[-25.0, -25.0, -10.0], [-25.0, -15.0, -5.0], [-25.0, -5.0, 0.0], [-25.0, 5.0, 0.0],
                    [-25.0, 15.0, -5.0], [-25.0, 25.0, -10.0], [-15.0, -25.0, -8.0], [-15.0, -15.0, -4.0],
                    [-15.0, -5.0, -4.0], [-15.0, 5.0, -4.0], [-15.0, 15.0, -4.0], [-15.0, 25.0, -8.0],
                    [-5.0, -25.0, -5.0], [-5.0, -15.0, -3.0], [-5.0, -5.0, -8.0], [-5.0, 5.0, -8.0],
                    [-5.0, 15.0, -3.0], [-5.0, 25.0, -5.0], [5.0, -25.0, -3.0], [5.0, -15.0, -2.0],
                    [5.0, -5.0, -8.0], [5.0, 5.0, -8.0], [5.0, 15.0, -2.0], [5.0, 25.0, -3.0],
                    [15.0, -25.0, -8.0], [15.0, -15.0, -4.0], [15.0, -5.0, -4.0], [15.0, 5.0, -4.0],
                    [15.0, 15.0, -4.0], [15.0, 25.0, -8.0], [25.0, -25.0, -10.0], [25.0, -15.0, -5.0],
                    [25.0, -5.0, 2.0], [25.0, 5.0, 2.0], [25.0, 15.0, -5.0], [25.0, 25.0, -10.0]]

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Set sample size
    surf.sample_size = SAMPLE_SIZE

    # Return the instance
    return surf


# Test if plotting a 3-dimensional curve without a window is possible
def test_curve3d_fig_nowindow(bspline_curve3d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve3D(config=conf)
    bspline_curve3d.vis = vis
    bspline_curve3d.render(plot=False)

    assert os.path.isfile(conf.figure_image_filename)
    assert os.path.getsize(conf.figure_image_filename) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_curve3d_fig_save(bspline_curve3d):
    fname = "test-curve.png"
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve3D(config=conf)
    bspline_curve3d.vis = vis
    bspline_curve3d.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test if plotting a 3-dimensional multi-curve without a window is possible
def test_curve3d_multi_fig_nowindow(bspline_curve3d):
    multi = bspline_curve3d.decompose()
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve3D(config=conf)
    multi.vis = vis
    multi.render(plot=False)

    assert os.path.isfile(conf.figure_image_filename)
    assert os.path.getsize(conf.figure_image_filename) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_curve3d_multi_fig_save(bspline_curve3d):
    fname = "test-multi_curve.png"
    multi = bspline_curve3d.decompose()
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve3D(config=conf)
    multi.vis = vis
    multi.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test if plotting a surface without a window is possible
def test_surf_fig_nowindow(bspline_surface):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurface(config=conf)
    bspline_surface.vis = vis
    bspline_surface.render(plot=False)

    assert os.path.isfile(conf.figure_image_filename)
    assert os.path.getsize(conf.figure_image_filename) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_surf_fig_save(bspline_surface):
    fname = "test-surface.png"
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurface(config=conf)
    bspline_surface.vis = vis
    bspline_surface.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test if plotting a multi-surface without a window is possible
def test_surf_multi_fig_nowindow(bspline_surface):
    multi = bspline_surface.decompose()
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurface(config=conf)
    multi.vis = vis
    multi.render(plot=False)

    assert os.path.isfile(conf.figure_image_filename)
    assert os.path.getsize(conf.figure_image_filename) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_surf_multi_fig_save(bspline_surface):
    fname = "test-multi_surface.png"
    multi = bspline_surface.decompose()
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurface(config=conf)
    multi.vis = vis
    multi.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)
