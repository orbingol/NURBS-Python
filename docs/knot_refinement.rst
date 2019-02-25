Knot Refinement
^^^^^^^^^^^^^^^

Knot refinement is simply the operation of *inserting multiple different knots at the same time*. NURBS-Python (geomdl)
supports knot refinement operation for curves, surfaces and volumes via :func:`.operations.refine_knotvector` function.

One of the interesting features of the :func:`.operations.refine_knotvector` function is the controlling of
**knot refinement density**. It can increase the number of knots to be inserted in a knot vector. Therefore, it
increases the number of control points.

The following code snippet and the figure illustrate a 2-dimensional spline curve with knot refinement:

.. code-block:: python
    :linenos:

    from geomdl import BSpline
    from geomdl import utilities
    from geomdl import exchange
    from geomdl.visualization import VisMPL

    # Create a curve instance
    curve = BSpline.Curve()

    # Set degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [
        [5.0, 10.0], [15.0, 25.0], [30.0, 30.0], [45.0, 5.0], [55.0, 5.0],
        [70.0, 40.0], [60.0, 60.0], [35.0, 60.0], [20.0, 40.0]
    ]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set visualization component
    curve.vis = VisMPL.VisCurve2D()

    # Refine knot vector
    operations.refine_knotvector(curve, [1])

    # Visualize
    curve.render()

.. plot::

    from geomdl import BSpline
    from geomdl import operations
    from geomdl.visualization import VisMPL

    # Create a curve instance
    curve = BSpline.Curve()

    # Set degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [
        [5.0, 10.0], [15.0, 25.0], [30.0, 30.0], [45.0, 5.0], [55.0, 5.0],
        [70.0, 40.0], [60.0, 60.0], [35.0, 60.0], [20.0, 40.0]
    ]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set visualization component
    curve.vis = VisMPL.VisCurve2D()

    # Refine knot vector
    operations.refine_knotvector(curve, [1])

    # Visualize
    curve.render()

The default ``density`` value is **1** for the knot refinement operation. The following code snippet and the figure
illustrate the result of the knot refinement operation if ``density`` is set to **2**.

.. code-block:: python
    :linenos:

    from geomdl import BSpline
    from geomdl import utilities
    from geomdl import exchange
    from geomdl.visualization import VisMPL

    # Create a curve instance
    curve = BSpline.Curve()

    # Set degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [
        [5.0, 10.0], [15.0, 25.0], [30.0, 30.0], [45.0, 5.0], [55.0, 5.0],
        [70.0, 40.0], [60.0, 60.0], [35.0, 60.0], [20.0, 40.0]
    ]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set visualization component
    curve.vis = VisMPL.VisCurve2D()

    # Refine knot vector
    operations.refine_knotvector(curve, [2])

    # Visualize
    curve.render()

.. plot::

    from geomdl import BSpline
    from geomdl import operations
    from geomdl.visualization import VisMPL

    # Create a curve instance
    curve = BSpline.Curve()

    # Set degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [
        [5.0, 10.0], [15.0, 25.0], [30.0, 30.0], [45.0, 5.0], [55.0, 5.0],
        [70.0, 40.0], [60.0, 60.0], [35.0, 60.0], [20.0, 40.0]
    ]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set visualization component
    curve.vis = VisMPL.VisCurve2D()

    # Refine knot vector
    operations.refine_knotvector(curve, [2])

    # Visualize
    curve.render()

The following code snippet and the figure illustrate the result of the knot refinement operation if ``density`` is set
to **3**.

.. code-block:: python
    :linenos:

    from geomdl import BSpline
    from geomdl import utilities
    from geomdl import exchange
    from geomdl.visualization import VisMPL

    # Create a curve instance
    curve = BSpline.Curve()

    # Set degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [
        [5.0, 10.0], [15.0, 25.0], [30.0, 30.0], [45.0, 5.0], [55.0, 5.0],
        [70.0, 40.0], [60.0, 60.0], [35.0, 60.0], [20.0, 40.0]
    ]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set visualization component
    curve.vis = VisMPL.VisCurve2D()

    # Refine knot vector
    operations.refine_knotvector(curve, [3])

    # Visualize
    curve.render()

.. plot::

    from geomdl import BSpline
    from geomdl import operations
    from geomdl.visualization import VisMPL

    # Create a curve instance
    curve = BSpline.Curve()

    # Set degree
    curve.degree = 4

    # Set control points
    curve.ctrlpts = [
        [5.0, 10.0], [15.0, 25.0], [30.0, 30.0], [45.0, 5.0], [55.0, 5.0],
        [70.0, 40.0], [60.0, 60.0], [35.0, 60.0], [20.0, 40.0]
    ]

    # Set knot vector
    curve.knotvector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Set visualization component
    curve.vis = VisMPL.VisCurve2D()

    # Refine knot vector
    operations.refine_knotvector(curve, [3])

    # Visualize
    curve.render()

The following code snippet and the figure illustrate the knot refinement operation applied to a surface with ``density``
value of **3** for the u-direction. No refinement was applied for the v-direction.

.. code-block:: python
    :linenos:

    from geomdl import NURBS
    from geomdl import operations
    from geomdl.visualization import VisMPL


    # Control points
    ctrlpts = [[[25.0, -25.0, 0.0, 1.0], [15.0, -25.0, 0.0, 1.0], [5.0, -25.0, 0.0, 1.0],
                [-5.0, -25.0, 0.0, 1.0], [-15.0, -25.0, 0.0, 1.0], [-25.0, -25.0, 0.0, 1.0]],
               [[25.0, -15.0, 0.0, 1.0], [15.0, -15.0, 0.0, 1.0], [5.0, -15.0, 0.0, 1.0],
                [-5.0, -15.0, 0.0, 1.0], [-15.0, -15.0, 0.0, 1.0], [-25.0, -15.0, 0.0, 1.0]],
               [[25.0, -5.0, 5.0, 1.0], [15.0, -5.0, 5.0, 1.0], [5.0, -5.0, 5.0, 1.0],
                [-5.0, -5.0, 5.0, 1.0], [-15.0, -5.0, 5.0, 1.0], [-25.0, -5.0, 5.0, 1.0]],
               [[25.0, 5.0, 5.0, 1.0], [15.0, 5.0, 5.0, 1.0], [5.0, 5.0, 5.0, 1.0],
                [-5.0, 5.0, 5.0, 1.0], [-15.0, 5.0, 5.0, 1.0], [-25.0, 5.0, 5.0, 1.0]],
               [[25.0, 15.0, 0.0, 1.0], [15.0, 15.0, 0.0, 1.0], [5.0, 15.0, 5.0, 1.0],
                [-5.0, 15.0, 5.0, 1.0], [-15.0, 15.0, 0.0, 1.0], [-25.0, 15.0, 0.0, 1.0]],
               [[25.0, 25.0, 0.0, 1.0], [15.0, 25.0, 0.0, 1.0], [5.0, 25.0, 5.0, 1.0],
                [-5.0, 25.0, 5.0, 1.0], [-15.0, 25.0, 0.0, 1.0], [-25.0, 25.0, 0.0, 1.0]]]

    # Generate surface
    surf = NURBS.Surface()
    surf.degree_u = 3
    surf.degree_v = 3
    surf.ctrlpts2d = ctrlpts
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    surf.sample_size = 30

    # Set visualization component
    surf.vis = VisMPL.VisSurface(VisMPL.VisConfig(alpha=0.75))

    # Refine knot vectors
    operations.refine_knotvector(surf, [3, 0])

    # Visualize
    surf.render()

.. plot::

    from geomdl import NURBS
    from geomdl import operations
    from geomdl.visualization import VisMPL


    # Control points
    ctrlpts = [[[25.0, -25.0, 0.0, 1.0], [15.0, -25.0, 0.0, 1.0], [5.0, -25.0, 0.0, 1.0],
                [-5.0, -25.0, 0.0, 1.0], [-15.0, -25.0, 0.0, 1.0], [-25.0, -25.0, 0.0, 1.0]],
               [[25.0, -15.0, 0.0, 1.0], [15.0, -15.0, 0.0, 1.0], [5.0, -15.0, 0.0, 1.0],
                [-5.0, -15.0, 0.0, 1.0], [-15.0, -15.0, 0.0, 1.0], [-25.0, -15.0, 0.0, 1.0]],
               [[25.0, -5.0, 5.0, 1.0], [15.0, -5.0, 5.0, 1.0], [5.0, -5.0, 5.0, 1.0],
                [-5.0, -5.0, 5.0, 1.0], [-15.0, -5.0, 5.0, 1.0], [-25.0, -5.0, 5.0, 1.0]],
               [[25.0, 5.0, 5.0, 1.0], [15.0, 5.0, 5.0, 1.0], [5.0, 5.0, 5.0, 1.0],
                [-5.0, 5.0, 5.0, 1.0], [-15.0, 5.0, 5.0, 1.0], [-25.0, 5.0, 5.0, 1.0]],
               [[25.0, 15.0, 0.0, 1.0], [15.0, 15.0, 0.0, 1.0], [5.0, 15.0, 5.0, 1.0],
                [-5.0, 15.0, 5.0, 1.0], [-15.0, 15.0, 0.0, 1.0], [-25.0, 15.0, 0.0, 1.0]],
               [[25.0, 25.0, 0.0, 1.0], [15.0, 25.0, 0.0, 1.0], [5.0, 25.0, 5.0, 1.0],
                [-5.0, 25.0, 5.0, 1.0], [-15.0, 25.0, 0.0, 1.0], [-25.0, 25.0, 0.0, 1.0]]]

    # Generate surface
    surf = NURBS.Surface()
    surf.degree_u = 3
    surf.degree_v = 3
    surf.ctrlpts2d = ctrlpts
    surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    surf.sample_size = 30

    # Set visualization component
    surf.vis = VisMPL.VisSurface(VisMPL.VisConfig(alpha=0.75))

    # Refine knot vectors
    operations.refine_knotvector(surf, [3, 0])

    # Visualize
    surf.render()
