Basics
^^^^^^
In order to generate a spline shape with NURBS-Python, you need 3 components:

* degree
* knot vector
* control points

The number of components depend on the parametric dimensionality of the shape regardless of the spatial dimensionality.

* **curve** is parametrically 1-dimensional (or 1-manifold)
* **surface** is parametrically 2-dimensional (or 2-manifold)
* **volume** is parametrically 3-dimensional (or 3-manifold)

Parametric dimensions are defined by ``u``, ``v``, ``w`` and spatial dimensions are defined by ``x``, ``y``, ``z``.

How to create a curve
=====================

In this section, we will cover the basics of spline curve generation using NURBS-Python. The following code snippet is
an example to a 3-dimensional curve.

.. code-block:: python
    :linenos:

    from geomdl import BSpline

    # Create the curve instance
    crv = BSpline.Curve()

    # Set degree
    crv.degree = 2

    # Set control points
    crv.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Set knot vector
    crv.knotvector = [0, 0, 0, 1, 1, 1]

As described in the introduction text, we set the 3 required components to generate a 3-dimensional spline curve.

Evaluating the curve points
---------------------------

The code snippet is updated to retrieve evaluated curve points.

.. code-block:: python
    :linenos:

    from geomdl import BSpline

    # Create the curve instance
    crv = BSpline.Curve()

    # Set degree
    crv.degree = 2

    # Set control points
    crv.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Set knot vector
    crv.knotvector = [0, 0, 0, 1, 1, 1]

    # Get curve points
    points = crv.evalpts

    # Do something with the evaluated points
    for pt in points:
        print(pt)

``evalpts`` property will automatically call ``evaluate()`` function.

Getting the curve point at a specific parameter
-----------------------------------------------

``evaluate_single`` method will return the point evaluated as the specified parameter.

.. code-block:: python
    :linenos:

    from geomdl import BSpline

    # Create the curve instance
    crv = BSpline.Curve()

    # Set degree
    crv.degree = 2

    # Set control points
    crv.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Set knot vector
    crv.knotvector = [0, 0, 0, 1, 1, 1]

    # Get curve point at u = 0.5
    point = crv.evaluate_single(0.5)


Setting the evaluation delta
----------------------------

``delta`` property will set the evaluation delta. It is also possible to use ``sample_size`` property to set the number
of evaluated points.

.. code-block:: python
    :linenos:

    from geomdl import BSpline

    # Create the curve instance
    crv = BSpline.Curve()

    # Set degree
    crv.degree = 2

    # Set control points
    crv.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Set knot vector
    crv.knotvector = [0, 0, 0, 1, 1, 1]

    # Set evaluation delta
    crv.delta = 0.005

    # Get evaluated points
    points_a = crv.evalpts

    # Update delta
    crv.delta = 0.1

    # The curve will be automatically re-evaluated
    points_b = crv.evalpts

Inserting a knot
----------------

``insert_knot`` method is recommended for this purpose.


.. code-block:: python
    :linenos:

    from geomdl import BSpline

    # Create the curve instance
    crv = BSpline.Curve()

    # Set degree
    crv.degree = 2

    # Set control points
    crv.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Set knot vector
    crv.knotvector = [0, 0, 0, 1, 1, 1]

    # Insert knot
    crv.insert_knot(0.5)

Plotting
--------

To plot the curve, a visualization module should be imported and curve should be updated to use the visualization
module.

.. code-block:: python
    :linenos:

    from geomdl import BSpline

    # Create the curve instance
    crv = BSpline.Curve()

    # Set degree
    crv.degree = 2

    # Set control points
    crv.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Set knot vector
    crv.knotvector = [0, 0, 0, 1, 1, 1]

    # Import Matplotlib visualization module
    from geomdl.visualization import VisMPL

    # Set the visualization component of the curve
    crv.vis = VisMPL.VisCurve3D()

    # Plot the curve
    crv.render()

Convert non-rational to rational curve
--------------------------------------

The following code snippet generates a B-Spline (non-rational) curve and converts it into a NURBS (rational) curve.

.. code-block:: python
    :linenos:

    from geomdl import BSpline

    # Create the curve instance
    crv = BSpline.Curve()

    # Set degree
    crv.degree = 2

    # Set control points
    crv.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Set knot vector
    crv.knotvector = [0, 0, 0, 1, 1, 1]

    # Import convert module
    from geomdl import convert

    # BSpline to NURBS
    crv_rat = convert.bspline_to_nurbs(crv)

Using knot vector generator
---------------------------

Knot vector generator is located in the :doc:`knotvector <module_knotvector>` module.

.. code-block:: python
    :linenos:

    from geomdl import BSpline
    from geomdl import knotvector

    # Create the curve instance
    crv = BSpline.Curve()

    # Set degree
    crv.degree = 2

    # Set control points
    crv.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Generate a uniform knot vector
    crv.knotvector = knotvector.generate(crv.degree, crv.ctrlpts_size)

Please refer to the :doc:`Examples Repository <examples_repo>` for more curve examples.

How to create a surface & a volume
==================================

Please refer to the :doc:`Examples Repository <examples_repo>` for surface and volume examples.
