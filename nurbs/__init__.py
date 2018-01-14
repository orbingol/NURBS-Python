""" This package contains native Python implementations of several `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_ algorithms for generating B-spline / NURBS curves and surfaces. It also provides a data structure for storing elements required for evaluation these curves and surfaces.
Please follow the `README.md <https://github.com/orbingol/NURBS-Python/blob/master/README.md>`_ file included in the `repository <https://github.com/orbingol/NURBS-Python>`_ for details on the algorithms.

Some other advantages of this package are;

* Python 2.x and 3.x compatibility
* No external dependencies (such as NumPy)
* Uses Python properties for the data storage access
* A :code:`utilities` module for auto-generating and normalizing knot vectors
* A :code:`Grid` class for generating various types of control points grids

The NURBS-Python package follows an object-oriented design as much as possible. However, in order to understand the algorithms, you might need to take a look at `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_ itself.

.. moduleauthor:: Onur Rauf Bingol

"""

__version__ = "2.3.9"
