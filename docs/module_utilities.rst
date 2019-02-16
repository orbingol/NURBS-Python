Utility Functions
^^^^^^^^^^^^^^^^^

These modules contain common utility and helper functions for B-Spline / NURBS curve and surface evaluation operations.

Utilities
=========

The ``utilities`` module contains common utility functions for NURBS-Python library and its extensions.

.. automodule:: geomdl.utilities
    :members:


Helpers
=======

The ``helpers`` module contains common functions required for evaluating both surfaces and curves, such as basis
function computations, knot vector span finding, etc.

.. automodule:: geomdl.helpers
    :members:


Linear Algebra
==============

The ``linalg`` module contains some basic functions for point, vector and matrix operations.

Although most of the functions are designed for internal usage, the users can still use some of the functions for their
advantage, especially the point and vector manipulation and generation functions. Functions related to point
manipulation have ``point_`` prefix and the ones related to vectors have ``vector_`` prefix.

.. automodule:: geomdl.linalg
    :members:
