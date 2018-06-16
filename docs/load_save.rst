Loading and Saving Data
^^^^^^^^^^^^^^^^^^^^^^^

NURBS-Python provides the following methods for loading curve and surface data from a file:

* :py:meth:`.BSpline.Curve.load()` and :py:meth:`.NURBS.Curve.load()`
* :py:meth:`.BSpline.Surface.load()` and :py:meth:`.NURBS.Surface.load()`

Additionally, save functionality is provided via the following methods:

* :py:meth:`.BSpline.Curve.save()` and :py:meth:`.NURBS.Curve.save()`
* :py:meth:`.BSpline.Surface.save()` and :py:meth:`.NURBS.Surface.save()`

These functions implement Python's `pickle` module to serialize the degree, knot vector and the control points data.
The idea behind this system is only to provide users a basic data persistence capability, not to introduce a new
file type. Since the data is *pickled*, it can be loaded with any compatible Python version even without using
any special library.
