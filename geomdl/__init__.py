""" NURBS-Python Library contains native Python implementations of several
`The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_ algorithms for generating Non-Uniform Rational
B-Spline (NURBS) 2D/3D curves and surfaces. It also provides a data structure for storing elements, such as degrees,
knot vectors, which are required for evaluation of NURBS curves and surfaces. Please follow the README_ file included
in the repository_ for details on the algorithms.

Some of the significant features of the NURBS-Python Library are;

* Python 2.x and 3.x compatibility
* No external dependencies (such as NumPy)
* Implements Python properties (using *property* decorator)
* A :code:`utilities` module containing several helper functions
* :code:`Grid` and :code:`GridWeighted` classes for generating various types of control points grids

NURBS-Python Library follows object-oriented design principles as much as possible. However, in order to understand
the algorithms, you might want to check *The NURBS Book* itself. All references to the implemented algorithms are given
in the README_ file.

.. moduleauthor:: Onur Rauf Bingol

.. _README: https://github.com/orbingol/NURBS-Python/blob/master/README.rst
.. _repository: https://github.com/orbingol/NURBS-Python

"""

__version__ = "3.0.0"
