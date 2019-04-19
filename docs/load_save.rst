Loading and Saving Data
^^^^^^^^^^^^^^^^^^^^^^^

NURBS-Python provides the following API calls for exporting and importing spline geometry data:

* :py:func:`.exchange.import_json()`
* :py:func:`.exchange.export_json()`

JSON import/export works with all spline geometry and container objects. Please refer to
:doc:`File Formats <file_formats>` for more details.

The following code snippet illustrates a B-spline curve generation and its JSON export:

.. code-block:: python
    :linenos:

    from geomdl import BSpline
    from geomdl import utilities
    from geomdl import exchange

    # Create a B-Spline curve instance
    curve = BSpline.Curve()

    # Set the degree
    curve.degree = 3

    # Load control points from a text file
    curve.ctrlpts = exchange.import_txt("control_points.txt")

    # Auto-generate the knot vector
    curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))

    # Export the curve as a JSON file
    exchange.export_json(curve, "curve.json")

The following code snippet illustrates importing from a JSON file and adding the result to
a container object:

.. code-block:: python
    :linenos:

    from geomdl import multi
    from geomdl import exchange

    # Import curve from a JSON file
    curve_list = exchange.import_json("curve.json")

    # Add curve list to the container
    curve_container = multi.CurveContainer(curve_list)
