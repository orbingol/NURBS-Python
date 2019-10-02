Curve & Surface Fitting
^^^^^^^^^^^^^^^^^^^^^^^

``geomdl`` includes 2 fitting methods for curves and surfaces: approximation and interpolation. Please refer to the
:doc:`module_fitting` page for more details on the curve and surface fitting API.

The following sections explain 2-dimensional curve fitting using the included fitting methods. ``geomdl`` also supports
3-dimensional curve and surface fitting (not shown here). Please refer to the :doc:`examples_repo` for more examples on
curve and surface fitting.

Interpolation
=============

The following code snippet and the figure illustrate interpolation for a 2-dimensional curve:

.. code-block:: python
    :linenos:

    from geomdl import fitting
    from geomdl.visualization import VisMPL as vis

    # The NURBS Book Ex9.1
    points = ((0, 0), (3, 4), (-1, 4), (-4, 0), (-4, -3))
    degree = 3  # cubic curve

    # Do global curve interpolation
    curve = fitting.interpolate_curve(points, degree)

    # Plot the interpolated curve
    curve.delta = 0.01
    curve.vis = vis.VisCurve2D()
    curve.render()


.. plot::

    from geomdl import fitting
    from geomdl.visualization import VisMPL as vis

    # The NURBS Book Ex9.1
    points = ((0, 0), (3, 4), (-1, 4), (-4, 0), (-4, -3))
    degree = 3  # cubic curve

    # Do global curve interpolation
    curve = fitting.interpolate_curve(points, degree)

    # Plot the interpolated curve
    curve.delta = 0.01
    curve.vis = vis.VisCurve2D()
    curve.render()

The following figure displays the input data (sample) points in red and the evaluated curve after interpolation in blue:

.. plot::

    from geomdl import fitting
    from geomdl.visualization import VisMPL as vis
    import numpy as np
    import matplotlib.pyplot as plt

    # The NURBS Book Ex9.1
    points = ((0, 0), (3, 4), (-1, 4), (-4, 0), (-4, -3))
    degree = 3  # cubic curve

    # Do global curve interpolation
    curve = fitting.interpolate_curve(points, degree)

    # Prepare points
    evalpts = np.array(curve.evalpts)
    pts = np.array(points)

    # Plot points together on the same graph
    fig = plt.figure(figsize=(10, 8), dpi=96)
    plt.plot(evalpts[:, 0], evalpts[:, 1])
    plt.scatter(pts[:, 0], pts[:, 1], color="red")
    plt.show()

Approximation
=============

The following code snippet and the figure illustrate approximation method for a 2-dimensional curve:

.. code-block:: python
    :linenos:

    from geomdl import fitting
    from geomdl.visualization import VisMPL as vis

    # The NURBS Book Ex9.1
    points = ((0, 0), (3, 4), (-1, 4), (-4, 0), (-4, -3))
    degree = 3  # cubic curve

    # Do global curve approximation
    curve = fitting.approximate_curve(points, degree)

    # Plot the interpolated curve
    curve.delta = 0.01
    curve.vis = vis.VisCurve2D()
    curve.render()


.. plot::

    from geomdl import fitting
    from geomdl.visualization import VisMPL as vis

    # The NURBS Book Ex9.1
    points = ((0, 0), (3, 4), (-1, 4), (-4, 0), (-4, -3))
    degree = 3  # cubic curve

    # Do global curve approximation
    curve = fitting.approximate_curve(points, degree)

    # Plot the interpolated curve
    curve.delta = 0.01
    curve.vis = vis.VisCurve2D()
    curve.render()

The following figure displays the input data (sample) points in red and the evaluated curve after approximation in blue:

.. plot::

    from geomdl import fitting
    from geomdl.visualization import VisMPL as vis
    import numpy as np
    import matplotlib.pyplot as plt

    # The NURBS Book Ex9.1
    points = ((0, 0), (3, 4), (-1, 4), (-4, 0), (-4, -3))
    degree = 3  # cubic curve

    # Do global curve approximation
    curve = fitting.approximate_curve(points, degree)

    # Prepare points
    evalpts = np.array(curve.evalpts)
    pts = np.array(points)

    # Plot points together on the same graph
    fig = plt.figure(figsize=(10, 8), dpi=96)
    plt.plot(evalpts[:, 0], evalpts[:, 1])
    plt.scatter(pts[:, 0], pts[:, 1], color="red")
    plt.show()

Please note that a spline geometry with a constant set of evaluated points may be represented with an infinite set of
control points. The number and positions of the control points depend on the application and the method used to
generate the control points.
