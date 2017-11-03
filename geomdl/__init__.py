""" This package contains native Python implementations of several `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_ algorithms for generating B-spline / NURBS curves and surfaces. It also provides a data structure for storing elements required for evaluation these curves and surfaces.
Please follow the `README.md <https://github.com/orbingol/NURBS-Python/blob/master/README.md>`_ file included in the `repository <https://github.com/orbingol/NURBS-Python>`_ for details on the algorithms.

Some other advantages of this package are;

* Python 2.x and 3.x compatibility
* No external dependencies (such as NumPy)
* Uses Python properties for the data storage access
* A :code:`utilities` module containing several helper functions
* :code:`Grid` and :code:`GridWeighted` classes for generating various types of control points grids

The NURBS-Python package follows an object-oriented design as much as possible. However, in order to understand the algorithms, you might need to take a look at `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_ itself.

.. moduleauthor:: Onur Rauf Bingol

"""

__version__ = "3.0.0"

# Fixes "from geomdl import *" but this is not considered as a good practice
# @see: https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = ["BSpline.Curve",
           "BSpline.Curve2D",
           "BSpline.Surface",
           "NURBS.Curve",
           "NURBS.Curve2D",
           "NURBS.Surface",
           "CPGen.Grid",
           "CPGen.GridWeighted",
           "utilities"]
