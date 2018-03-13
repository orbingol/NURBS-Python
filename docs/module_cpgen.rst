Control Points Generator Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``CPGen`` module allows users to generate control points grids as an input to :py:class:`.BSpline.Surface` and
:py:class:`.NURBS.Surface` classes. This module is designed to enable more testing cases in a very simple way and
it doesn't have the capabilities of a fully-featured grid generator, but it should be enough to be used side by side
with ``BSpline`` and ``NURBS`` modules.

:py:class:`.CPGen.Grid` class provides an easy way to generate control point grids for use with
:py:class:`.BSpline.Surface` class and :py:class:`.CPGen.GridWeighted` does the same for :py:class:`.NURBS.Surface`
class.

Grid
====

.. autoclass:: geomdl.CPGen.Grid
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:


Weighted Grid
=============

.. autoclass:: geomdl.CPGen.GridWeighted
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
