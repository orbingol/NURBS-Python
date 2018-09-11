Surface Generator
^^^^^^^^^^^^^^^^^

NURBS-Python comes with a simple surface generator which is designed to generate a control points grid to be used as
a randomized input to :py:class:`.BSpline.Surface` and :py:class:`.NURBS.Surface`. It is capable of generating
custom-sized surfaces with arbitrary divisions and generating hills (or bumps) on the surface. It is also possible to
export the surface as a text file in the format described under :doc:`File Formats <file_formats>` documentation.

The classes :py:class:`.CPGen.Grid` and :py:class:`.CPGen.GridWeighted` are responsible for generating surfaces and
they are documented under :doc:`Core Libraries <modules>`.

The following example illustrates a sample usage of the B-Spline surface generator:

.. code-block:: python

    from geomdl import CPGen
    from geomdl import BSpline
    from geomdl import utilities
    from geomdl.visualization import VisPlotly

    # Generate a plane with the dimensions 50x100
    surfgrid = CPGen.Grid(50, 100)

    # Generate a grid of 25x30
    surfgrid.generate(25, 30)

    # Generate bumps on the grid
    surfgrid.bumps(num_bumps=5, bump_height=20, base_extent=4)

    # Create a BSpline surface instance
    surf = BSpline.Surface()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    # Get the control points from the generated grid
    surf.ctrlpts2d = surfgrid.grid

    # Set knot vectors
    surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, surf.ctrlpts_size_u)
    surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, surf.ctrlpts_size_v)

    # Set sample size
    surf.sample_size = 30

    # Generate the visualization component and its configuration
    vis_config = VisPlotly.VisConfig(ctrlpts=False, legend=False)
    vis_comp = VisPlotly.VisSurface(vis_config)

    # Set visualization component
    surf.vis = vis_comp

    # Plot the surface
    surf.render()

:py:meth:`.CPGen.Grid.bumps()` method takes the following keyword arguments:

* ``num_bumps``: Number of hills to be generated
* ``bump_height``: Defines the peak height of the generated hills
* ``base_extent``: Due to the structure of the grid, the hill base can be defined as a square with the edge length of *a*. ``base_extent`` is defined by the value of *a/2*.
* ``padding``: Defines the padding of the area where the hills are generated. It accepts positive and negative values. A negative value means a padding to the inside of the grid and a positive value means padding to the outside of the grid.
