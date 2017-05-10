.. NURBS-Python documentation master file, created by
   sphinx-quickstart on Fri Mar 10 21:16:25 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

NURBS-Python Documentation
==========================

Module contents
---------------

.. automodule:: nurbs
    :members:
    :undoc-members:

Graphical Outputs
-----------------

The following 2D and 3D plots are generated using `Matplotlib <http://matplotlib.org/>`_. You can find the scripts generating these graphical outputs in the `NURBS-Python Repository <https://github.com/orbingol/NURBS-Python>`_.

Curves
^^^^^^

.. image:: ../ex_curve01.png
    :width: 30%
    :alt: Curve example 1

.. image:: ../ex_curve02.png
    :width: 30%
    :alt: Curve example 2

.. image:: ../ex_curve03.png
    :width: 30%
    :alt: Curve example 3

Surfaces
^^^^^^^^

.. image:: ../ex_surface01.png
    :width: 30%
    :alt: Surface example 1

.. image:: ../ex_surface02.png
    :width: 30%
    :alt: Surface example 2

.. image:: ../ex_surface03.png
    :width: 30%
    :alt: Surface example 3

Submodules
----------

The :code:`nurbs` package contains :code:`Curve` and :code:`Surface` classes along with the :code:`utilities` module for functions common in both :code:`Curve` and :code:`Surface` classes.

This package also includes a very simple grid generator class, :code:`Grid`, to generate rectangular control point grids for use with the :code:`Surface` class.

nurbs.Curve module
------------------

:code:`Curve` class provides data storage properties and evaluation functions for NURBS and B-spline curves.

.. automodule:: nurbs.Curve
    :members:
    :undoc-members:

nurbs.Surface module
--------------------

:code:`Surface` class provides data storage properties and evaluation functions for NURBS and B-spline surfaces.

.. automodule:: nurbs.Surface
    :members:
    :undoc-members:

nurbs.utilities module
----------------------

:code:`utilities` module contains common helper functions for B-spline and NURBS curve and surface evaluation.

.. automodule:: nurbs.utilities
    :members:
    :exclude-members: basis_functions, basis_functions_all, basis_functions_ders, check_uv, find_span, find_multiplicity
    :undoc-members:

nurbs.Grid module
--------------------

:code:`Grid` class provides an easy way to generate control point grids for use with :code:`Surface` module.

This class is designed minimally just to enable more testing cases for the :code:`Surface` module. It is not a fully-featured grid generator which can fit to any purpose, but as always, contributions are welcome!

.. automodule:: nurbs.Grid
    :members:
    :undoc-members:


.. toctree::
   :maxdepth: 2

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
