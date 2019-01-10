Visualization
^^^^^^^^^^^^^

NURBS-Python comes with the following visualization modules for direct plotting evaluated curves and surfaces:

* :doc:`VisMPL <module_vis_mpl>` module for `Matplotlib <https://matplotlib.org>`_
* :doc:`VisPlotly <module_vis_plotly>` module for `Plotly <https://plot.ly/python/>`_
* :doc:`VisVTK <module_vis_vtk>` module for `VTK <https://vtk.org>`_

Examples_ repository contains over 40 examples on how to use the visualization components in various ways. Please see
:doc:`Visualization Modules Documentation <modules_visualization>` for more details.

Examples
========

The following figures illustrate some example 2D/3D curves and surfaces that can be generated and directly visualized
using NURBS-Python.

Curves
------

.. plot::

    from geomdl import BSpline
    from geomdl import utilities
    from geomdl.visualization import VisMPL

    # Create a B-Spline curve
    curve = BSpline.Curve()

    # Set up the curve
    curve.degree = 4
    curve.ctrlpts = [[5.0, 10.0], [15.0, 25.0], [30.0, 30.0], [45.0, 5.0], [55.0, 5.0], [70.0, 40.0], [60.0, 60.0], [35.0, 60.0], [20.0, 40.0]]

    # Auto-generate knot vector
    curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))

    # Set evaluation delta
    curve.delta = 0.01

    # Plot the control point polygon and the evaluated curve
    curve.vis = VisMPL.VisCurve2D()
    curve.render()

-----

.. plot::

    from geomdl import BSpline
    from geomdl import utilities
    from geomdl.visualization import VisMPL

    ctrlpts = [[5.0, 5.0, 0.0], [5.0, 10.0, 0.0], [10.0, 10.0, 5.0], [10.0, 5.0, 5.0], [5.0, 5.0, 5.0], [5.0, 10.0, 10.0], [10.0, 10.0, 10.0], [10.0, 5.0, 10.0], [5.0, 5.0, 15.0], [5.0, 10.0, 15.0], [10.0, 10.0, 15.0], [10.0, 5.0, 20.0], [5.0, 5.0, 20.0]]

    # Create a B-Spline curve instance
    curve = BSpline.Curve()

    # Set up curve
    curve.degree = 3
    curve.ctrlpts = ctrlpts

    # Auto-generate knot vector
    curve.knotvector = utilities.generate_knot_vector(curve.degree, curve.ctrlpts_size)

    # Set evaluation delta
    curve.delta = 0.01

    # Plot the control point polygon and the evaluated curve
    curve.vis = VisMPL.VisCurve3D()
    curve.render()


Surfaces
--------

.. plot::

    from geomdl import BSpline
    from geomdl.visualization import VisMPL

    # Control points
    ctrlpts = [
        [[-25.0, -25.0, -10.0], [-25.0, -15.0, -5.0], [-25.0, -5.0, 0.0], [-25.0, 5.0, 0.0], [-25.0, 15.0, -5.0], [-25.0, 25.0, -10.0]],
        [[-15.0, -25.0, -8.0], [-15.0, -15.0, -4.0], [-15.0, -5.0, -4.0], [-15.0, 5.0, -4.0], [-15.0, 15.0, -4.0], [-15.0, 25.0, -8.0]],
        [[-5.0, -25.0, -5.0], [-5.0, -15.0, -3.0], [-5.0, -5.0, -8.0], [-5.0, 5.0, -8.0], [-5.0, 15.0, -3.0], [-5.0, 25.0, -5.0]],
        [[5.0, -25.0, -3.0], [5.0, -15.0, -2.0], [5.0, -5.0, -8.0], [5.0, 5.0, -8.0], [5.0, 15.0, -2.0], [5.0, 25.0, -3.0]],
        [[15.0, -25.0, -8.0], [15.0, -15.0, -4.0], [15.0, -5.0, -4.0], [15.0, 5.0, -4.0], [15.0, 15.0, -4.0], [15.0, 25.0, -8.0]],
        [[25.0, -25.0, -10.0], [25.0, -15.0, -5.0], [25.0, -5.0, 2.0], [25.0, 5.0, 2.0], [25.0, 15.0, -5.0], [25.0, 25.0, -10.0]]
    ]

    # Create a BSpline surface
    surf = BSpline.Surface()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Set control points
    surf.ctrlpts2d = ctrlpts

    # Set knot vectors
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]

    # Set evaluation delta
    surf.delta = 0.025

    # Evaluate surface points
    surf.evaluate()

    # Import and use Matplotlib's colormaps
    from matplotlib import cm

    # Plot the control points grid and the evaluated surface
    surf.vis = VisMPL.VisSurface()
    surf.render(colormap=cm.cool)

-----

.. plot::

    from geomdl import NURBS
    from geomdl.visualization import VisMPL

    ctrlpts = [
        [[1.0, 0.0, 0.0, 1.0], [0.7071, 0.7071, 0.0, 0.7071], [0.0, 1.0, 0.0, 1.0], [-0.7071, 0.7071, 0.0, 0.7071], [-1.0, 0.0, 0.0, 1.0], [-0.7071, -0.7071, 0.0, 0.7071], [0.0, -1.0, 0.0, 1.0], [0.7071, -0.7071, 0.0, 0.7071], [1.0, 0.0, 0.0, 1.0]],
        [[1.0, 0.0, 1.0, 1.0], [0.7071, 0.7071, 0.7071, 0.7071], [0.0, 1.0, 1.0, 1.0], [-0.7071, 0.7071, 0.7071, 0.7071], [-1.0, 0.0, 1.0, 1.0], [-0.7071, -0.7071, 0.7071, 0.7071], [0.0, -1.0, 1.0, 1.0], [0.7071, -0.7071, 0.7071, 0.7071], [1.0, 0.0, 1.0, 1.0]]
    ]

    # Create a NURBS surface
    surf = NURBS.Surface()

    # Set degrees
    surf.degree_u = 1
    surf.degree_v = 2

    # Set control points
    surf.ctrlpts2d = ctrlpts

    # Set knot vectors
    surf.knotvector_u = [0, 0, 1, 1]
    surf.knotvector_v = [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]

    # Set evaluation delta
    surf.delta = 0.05

    # Plot the control point grid and the evaluated surface
    surf.vis = VisMPL.VisSurface()
    surf.render()

Volumes
-------

.. plot::

    from geomdl import BSpline
    from geomdl import CPGen
    from geomdl import multi
    from geomdl import utilities
    from geomdl import construct
    from geomdl.visualization import VisMPL

    # Generate control points grid for Surface #1
    sg01 = CPGen.Grid(15, 10, z_value=0.0)
    sg01.generate(8, 8)

    # Create a BSpline surface instance
    surf01 = BSpline.Surface()

    # Set degrees
    surf01.degree_u = 1
    surf01.degree_v = 1

    # Get the control points from the generated grid
    surf01.ctrlpts2d = sg01.grid

    # Set knot vectors
    surf01.knotvector_u = utilities.generate_knot_vector(surf01.degree_u, surf01.ctrlpts_size_u)
    surf01.knotvector_v = utilities.generate_knot_vector(surf01.degree_v, surf01.ctrlpts_size_v)

    # Generate control points grid for Surface #2
    sg02 = CPGen.Grid(15, 10, z_value=1.0)
    sg02.generate(8, 8)

    # Create a BSpline surface instance
    surf02 = BSpline.Surface()

    # Set degrees
    surf02.degree_u = 1
    surf02.degree_v = 1

    # Get the control points from the generated grid
    surf02.ctrlpts2d = sg02.grid

    # Set knot vectors
    surf02.knotvector_u = utilities.generate_knot_vector(surf02.degree_u, surf02.ctrlpts_size_u)
    surf02.knotvector_v = utilities.generate_knot_vector(surf02.degree_v, surf02.ctrlpts_size_v)

    # Generate control points grid for Surface #3
    sg03 = CPGen.Grid(15, 10, z_value=2.0)
    sg03.generate(8, 8)

    # Create a BSpline surface instance
    surf03 = BSpline.Surface()

    # Set degrees
    surf03.degree_u = 1
    surf03.degree_v = 1

    # Get the control points from the generated grid
    surf03.ctrlpts2d = sg03.grid

    # Set knot vectors
    surf03.knotvector_u = utilities.generate_knot_vector(surf03.degree_u, surf03.ctrlpts_size_u)
    surf03.knotvector_v = utilities.generate_knot_vector(surf03.degree_v, surf03.ctrlpts_size_v)

    # Construct the parametric volume
    pvolume = construct.construct_volume(surf01, surf02, surf03, degree=1)

    # Construct the isosurface
    surfiso = construct.extract_isosurface(pvolume)
    msurf = multi.SurfaceContainer(surfiso)

    # Render the isourface
    msurf.vis = VisMPL.VisSurface(VisMPL.VisConfig(ctrlpts=False, legend=False))
    msurf.delta = 0.05
    msurf.render(evalcolor=["skyblue", "cadetblue", "crimson", "crimson", "crimson", "crimson"])

Advanced Visualization Examples
-------------------------------

The following example scripts can be found in Examples_ repository under the ``visualization`` directory.

mpl_curve2d_tangents.py
~~~~~~~~~~~~~~~~~~~~~~~

This example illustrates a more advanced visualization option for plotting the 2D curve tangents alongside with the
control points grid and the evaluated curve.

.. image:: images/ex_curve03_mpl.png
    :alt: 2D curve example 2 with tangent vector quiver plots

mpl_curve3d_tangents.py
~~~~~~~~~~~~~~~~~~~~~~~

This example illustrates a more advanced visualization option for plotting the 3D curve tangents alongside with the
control points grid and the evaluated curve.

.. image:: images/ex_curve3d01_mpl.png
    :alt: 3D curve example 1 with tangent vector quiver plots

mpl_curve3d_vectors.py
~~~~~~~~~~~~~~~~~~~~~~

This example illustrates a visualization option for plotting the 3D curve tangent, normal and binormal vectors
alongside with the control points grid and the evaluated curve.

.. image:: images/ex_curve3d02_mpl.png
    :alt: 3D curve example 2 with tangent, normal and binormal vector quiver plots

mpl_trisurf_vectors.py
~~~~~~~~~~~~~~~~~~~~~~

The following figure illustrates tangent and normal vectors on ``ex_surface02.py`` example.

.. image:: images/ex_surface02_mpl_vectors.png
    :alt: Surface example 2 with tangent and normal vectors


.. _Examples: https://github.com/orbingol/NURBS-Python_Examples
