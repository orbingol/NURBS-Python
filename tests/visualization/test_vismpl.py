"""
    Tests for the NURBS-Python (geomdl) package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2020 Onur Rauf Bingol

    Tests VisMPL visualization module. Requires "pytest" to run.
"""

import os
import pytest
import matplotlib
matplotlib.use('agg')
from geomdl import BSpline
from geomdl.visualization import VisMPL as vis
from geomdl.visualization import render


@pytest.mark.usefixtures("curve7")
def test_curve2d_fig_nowindow(curve7):
    conf = vis.VisConfig()
    vism = vis.VisCurve2D(config=conf)

    fname = conf.figure_image_filename

    render.render(curve7, vism, display=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


@pytest.mark.usefixtures("curve8")
def test_curve2d_fig_save(curve8):
    conf = vis.VisConfig()
    vism = vis.VisCurve2D(config=conf)

    fname = "test-curve.png"

    render.render(curve8, vism, filename=fname, display=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("curve6")
def test_curve3d_fig_nowindow(curve6):
    conf = vis.VisConfig()
    vism = vis.VisCurve3D(config=conf)

    fname = conf.figure_image_filename

    render.render(curve6, vism, display=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


@pytest.mark.usefixtures("curve6")
def test_curve3d_fig_save(curve6):
    conf = vis.VisConfig()
    vism = vis.VisCurve3D(config=conf)

    fname = "test-curve.png"

    render.render(curve6, vism, filename=fname, display=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("surface1")
def test_surf_fig_nowindow(surface1):
    conf = vis.VisConfig()
    vism = vis.VisSurface(config=conf)

    fname = conf.figure_image_filename

    render.render(surface1, vism, display=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(conf.figure_image_filename):
        os.remove(conf.figure_image_filename)


@pytest.mark.usefixtures("surface1")
def test_surf_fig_save(surface1):
    conf = vis.VisConfig()
    vism = vis.VisSurface(config=conf)

    fname = "test-surface.png"

    render.render(surface1, vism, filename=fname, display=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


@pytest.mark.usefixtures("surface1")
def test_surf_ctrlpts_offset(surface1):
    conf = vis.VisConfig()
    vism = vis.VisSurface(config=conf)

    # Set control points grid offset
    vis.ctrlpts_offset = 3.5

    fname = "test-surface.png"

    render.render(surface1, vism, filename=fname, display=False)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)
