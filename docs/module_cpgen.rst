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
