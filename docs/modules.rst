Modules
^^^^^^^

The package name is :code:`geomdl` and it contains :code:`BSpline` and :code:`NURBS` modules along with the :code:`utilities`
module for functions common in both :code:`BSpline` and :code:`NURBS`. It also includes a simple control points generator
module, :code:`CPGen`, to use as an input to :code:`BSpline.Surface` and :code:`NURBS.Surface` classes.

B-Spline Module
===============

:code:`BSpline` module provides data storage properties and evaluation functions for B-Spline (NUBS) 2D/3D curves and surfaces.

3D B-Spline Curve
-----------------

.. autoclass:: geomdl.BSpline.Curve
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

2D B-Spline Curve
-----------------

.. autoclass:: geomdl.BSpline.Curve2D
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

B-Spline Surface
----------------

.. autoclass:: geomdl.BSpline.Surface
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

NURBS Module
============

:code:`NURBS` module provides data storage properties and evaluation functions for NURBS 2D/3D curves and surfaces.

3D NURBS Curve
--------------

.. autoclass:: geomdl.NURBS.Curve
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

2D NURBS Curve
--------------

.. autoclass:: geomdl.NURBS.Curve2D
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

NURBS Surface
-------------

.. autoclass:: geomdl.NURBS.Surface
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Utilities module
================

:code:`utilities` module contains common helper functions for B-spline and NURBS curve and surface evaluation.

.. automodule:: geomdl.utilities
    :members:
    :exclude-members: basis_functions, basis_functions_all, basis_functions_ders, check_uv, find_span, find_multiplicity
    :undoc-members:

Control Points Generator Module
===============================

:code:`CPGen` module allows users to generate control points grids as an input to :code:`BSpline.Surface` and
:code:`NURBS.Surface` classes. This module is designed to enable more testing cases in a very simple way and it doesn't
have the capabilities of a fully-featured grid generator, but it should be enough to be used side by side with
:code:`BSpline` and :code:`NURBS` modules.

:code:`CPGen.Grid` class provides an easy way to generate control point grids for use with :code:`BSpline.Surface` class
and :code:`CPGen.GridWeighted` does the same for :code:`NURBS.Surface` class.


Grid
----

.. autoclass:: geomdl.CPGen.Grid
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:


Weighted Grid
-------------

.. autoclass:: geomdl.CPGen.GridWeighted
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
