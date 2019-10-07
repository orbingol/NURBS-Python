"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests visualization modules. Requires "pytest" to run.
"""

import os
import pytest
from geomdl import BSpline
from geomdl import multi
from geomdl import operations

import matplotlib
matplotlib.use('agg')
from geomdl.visualization import VisMPL

SAMPLE_SIZE = 5


@pytest.fixture
def bspline_curve2d():
    """ Creates a 2-dimensional B-Spline curve instance """
    # Create a curve instance
    curve = BSpline.Curve()

    # Set curve degree
    curve.degree = 3

    # Set control points
    curve.ctrlpts = [[5.0, 5.0], [10.0, 10.0], [20.0, 15.0], [35.0, 15.0], [45.0, 10.0], [50.0, 5.0]]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.33, 0.66, 1.0, 1.0, 1.0, 1.0]

    # Set sample size
    curve.sample_size = SAMPLE_SIZE

    # Return the instance
    return curve


@pytest.fixture
def bspline_curve3d():
    """ Creates a 3-dimensional B-Spline curve instance """
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


# Test if plotting a 2-dimensional curve without a window is possible
def test_curve2d_fig_nowindow(bspline_curve2d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve3D(config=conf)

    fname = conf.figure_image_filename

    bspline_curve2d.vis = vis
    bspline_curve2d.render(plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_curve2d_fig_save(bspline_curve2d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve2D(config=conf)

    fname = "test-curve.png"

    bspline_curve2d.vis = vis
    bspline_curve2d.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test if plotting a 2-dimensional multi-curve without a window is possible
def test_curve2d_multi_fig_nowindow(bspline_curve2d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve2D(config=conf)

    fname = conf.figure_image_filename

    data = operations.decompose_curve(bspline_curve2d)
    multi_shape = multi.CurveContainer(data)
    multi_shape.vis = vis
    multi_shape.render(plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_curve2d_multi_fig_save(bspline_curve2d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve2D(config=conf)

    fname = "test-multi_curve.png"

    data = operations.decompose_curve(bspline_curve2d)
    multi_shape = multi.CurveContainer(data)
    multi_shape.vis = vis
    multi_shape.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test if plotting a 3-dimensional curve without a window is possible
def test_curve3d_fig_nowindow(bspline_curve3d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve2D(config=conf)

    fname = conf.figure_image_filename

    bspline_curve3d.vis = vis
    bspline_curve3d.render(plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_curve3d_fig_save(bspline_curve3d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve3D(config=conf)

    fname = "test-curve.png"

    bspline_curve3d.vis = vis
    bspline_curve3d.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test if plotting a 3-dimensional multi-curve without a window is possible
def test_curve3d_multi_fig_nowindow(bspline_curve3d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve3D(config=conf)

    data = operations.decompose_curve(bspline_curve3d)
    multi_shape = multi.CurveContainer(data)
    multi_shape.vis = vis
    multi_shape.render(plot=False)

    assert os.path.isfile(conf.figure_image_filename)
    assert os.path.getsize(conf.figure_image_filename) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_curve3d_multi_fig_save(bspline_curve3d):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisCurve3D(config=conf)

    fname = "test-multi_curve.png"

    data = operations.decompose_curve(bspline_curve3d)
    multi_shape = multi.CurveContainer(data)
    multi_shape.vis = vis
    multi_shape.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test if plotting a surface without a window is possible
def test_surf_fig_nowindow(bspline_surface):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurface(config=conf)

    fname = conf.figure_image_filename

    bspline_surface.vis = vis
    bspline_surface.render(plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_surf_fig_save(bspline_surface):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurface(config=conf)

    fname = "test-surface.png"

    bspline_surface.vis = vis
    bspline_surface.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test offsetting control points grid
def test_surf_ctrlpts_offset(bspline_surface):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurface(config=conf)

    # Set control points grid offset
    vis.ctrlpts_offset = 3.5

    fname = "test-surface.png"

    bspline_surface.vis = vis
    bspline_surface.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


# Test if plotting a multi-surface without a window is possible
def test_surf_multi_fig_nowindow(bspline_surface):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurfScatter(config=conf)

    fname = conf.figure_image_filename

    data = operations.decompose_surface(bspline_surface)
    multi_shape = multi.SurfaceContainer(data)
    multi_shape.vis = vis
    multi_shape.render(plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


# Test if using a different file name is possible
def test_surf_multi_fig_save(bspline_surface):
    conf = VisMPL.VisConfig()
    vis = VisMPL.VisSurfWireframe(config=conf)

    fname = "test-multi_surface.png"

    data = operations.decompose_surface(bspline_surface)
    multi_shape = multi.SurfaceContainer(data)
    multi_shape.vis = vis
    multi_shape.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_deriv_curve_fig(bspline_curve2d):
    fname = "test-derivative_curve.png"

    data = operations.derivative_curve(bspline_curve2d)
    multi_shape = multi.CurveContainer(data)
    multi_shape.vis = VisMPL.VisCurve2D()
    multi_shape.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_deriv_surf_fig(bspline_surface):
    fname = "test-derivative_surface.png"

    data = operations.derivative_surface(bspline_surface)
    multi_shape = multi.SurfaceContainer(data)
    multi_shape.vis = VisMPL.VisSurface()
    multi_shape.render(filename=fname, plot=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)
