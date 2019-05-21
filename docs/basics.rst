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

Working with the curves
=======================

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

Evaluation delta is used to change the number of evaluated points. Increasing the number of points will result in a
bigger evaluated points array, as described with ``evalpts`` property and decreasing will reduce the size of the
``evalpts`` array. Therefore, evaluation delta can also be used to change smoothness of the plots generated using
the visualization modules.

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

Plotting multiple curves
------------------------

:doc:`multi <module_container>` module can be used to plot multiple curves on the same figure.

.. code-block:: python
    :linenos:

    from geomdl import BSpline
    from geomdl import multi
    from geomdl import knotvector

    # Create the curve instance #1
    crv1 = BSpline.Curve()

    # Set degree
    crv1.degree = 2

    # Set control points
    crv1.ctrlpts = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    # Generate a uniform knot vector
    crv1.knotvector = knotvector.generate(crv1.degree, crv1.ctrlpts_size)

    # Create the curve instance #2
    crv2 = BSpline.Curve()

    # Set degree
    crv2.degree = 3

    # Set control points
    crv2.ctrlpts = [[1, 0, 0], [1, 1, 0], [2, 1, 0], [1, 1, 0]]

    # Generate a uniform knot vector
    crv2.knotvector = knotvector.generate(crv2.degree, crv2.ctrlpts_size)

    # Create a curve container
    mcrv = multi.CurveContainer(crv1, crv2)

    # Import Matplotlib visualization module
    from geomdl.visualization import VisMPL

    # Set the visualization component of the curve container
    mcrv.vis = VisMPL.VisCurve3D()

    # Plot the curves in the curve container
    mcrv.render()

Please refer to the :doc:`Examples Repository <examples_repo>` for more curve examples.

Working with the surfaces
=========================

The majority of the surface API is very similar to the curve API. Since a surface is defined on a 2-dimensional
parametric space, the getters/setters have a suffix of ``_u`` and ``_v``; such as ``knotvector_u`` and
``knotvector_v``.

Please refer to the :doc:`Examples Repository <examples_repo>` for surface examples.

Working with the volumes
========================

Volumes are defined on a 3-dimensional parametric space. Working with the volumes are very similar to Working
with the surfaces. The only difference is the 3rd parametric dimension, ``w``. For instance, to access the
knot vectors, the properties you will use are ``knotvector_u``, ``knotvector_v`` and ``knotvector_w``. 

Please refer to the :doc:`Examples Repository <examples_repo>` for volume examples.
