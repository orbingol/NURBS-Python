Loading and Saving Data
^^^^^^^^^^^^^^^^^^^^^^^

NURBS-Python provides the following methods for loading curve and surface data from a file:

* :py:meth:`.BSpline.Curve.load()` and :py:meth:`.NURBS.Curve.load()`
* :py:meth:`.BSpline.Surface.load()` and :py:meth:`.NURBS.Surface.load()`

Additionally, save functionality is provided via the following methods:

* :py:meth:`.BSpline.Curve.save()` and :py:meth:`.NURBS.Curve.save()`
* :py:meth:`.BSpline.Surface.save()` and :py:meth:`.NURBS.Surface.save()`

These functions implement Python's ``pickle`` module to serialize the degree, knot vector and the control points data.
The idea behind this system is only to provide users a basic data persistence capability, not to introduce a new
file type. Since the data is *pickled*, it can be loaded with any compatible Python version even without using
any special library.

The following example demonstrates the save functionality on a curve:

.. code-block:: python

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

    # Save the curve
    curve.save("mycurve.pickle")

The saved curve can be loaded from the file with the following simple code segment:

.. code-block:: python

    from geomdl import BSpline

    # Create a B-Spline curve instance
    curve2 = BSpline.Curve()

    # Load the saved curve from a file
    curve2.load("mycurve.pickle")

Since the load-save functionality implements Python's ``pickle`` module, the saved file can also be loaded directly
without using the NURBS-Python library.

.. code-block:: python

    import pickle

    # "data" variable will be a dictionary containing the curve information
    data = pickle.load(open("mycurve.pickle"), "rb")

The ``pickle`` module has its own limitations by its design. Please see the Python documentation for more details.
