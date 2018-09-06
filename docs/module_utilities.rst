Utilities and Helpers
^^^^^^^^^^^^^^^^^^^^^

These modules contain common utility and helper functions for B-Spline / NURBS curve and surface evaluation operations.

Utilities
=========

The **Utilities** module contains several utility functions that help computation of several common linear algebra and
geometry operations.

Although most of the functions are designed for internal usage, the users can still use some of the functions for their
advantage, especially the point and vector manipulation and generation functions. Functions related to point
manipulation have ``point_`` prefix and the ones related to vectors have ``vector_`` prefix.

.. automodule:: geomdl.utilities
    :members:
    :exclude-members: init_var
    :undoc-members:


Helpers
=======

The **Helpers** module contains common functions required for evaluating both surfaces and curves, such as basis
function computations, knot vector span finding, etc.

.. automodule:: geomdl.helpers
    :members:
    :undoc-members:
