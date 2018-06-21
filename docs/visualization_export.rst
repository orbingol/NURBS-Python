Exporting Plots as Image Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``render()`` method allows users to directly plot the curves and surfaces using predefined visualization classes.
This method takes some keyword arguments to control plot properties at runtime. Please see the class documentation on
description of these keywords. The ``render()`` method also allows users to save the plots directly as a file and
to control the plot window visibility. The keyword arguments that control these features are ``filename`` and ``plot``,
respectively.

The following example script illustrates creating a 3-dimensional Bézier curve and saving the plot as
``bezier-curve3d.pdf`` without popping up the Matplotlib plot window. ``filename`` argument is a string value defining
the name of the file to be saved and ``plot`` flag controls the visibility of the plot window.

.. code-block:: python

    import os
    from geomdl import BSpline
    from geomdl import utilities
    from geomdl.visualization import VisMPL

    # Fix file path
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Create a 3D B-Spline curve instance (Bezier Curve)
    curve = BSpline.Curve()

    # Set up the Bezier curve
    curve.degree = 3
    curve.ctrlpts = [[10, 5, 10], [10, 20, -30], [40, 10, 25], [-10, 5, 0]]

    # Auto-generate knot vector
    curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))

    # Set sample size
    curve.sample_size = 40

    # Evaluate curve
    curve.evaluate()

    # Plot the control point polygon and the evaluated curve
    vis_comp = VisMPL.VisCurve3D()
    curve.vis = vis_comp

    # Don't pop up the plot window, instead save it as a PDF file
    curve.render(filename="bezier-curve3d.pdf", plot=False)

This functionality strongly depends on the plotting library used. Please see the documentation of the plotting library
that you are using for more details on its figure exporting capabilities.
