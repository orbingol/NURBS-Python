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
..    :show-inheritance:

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

nurbs.Curve module
------------------

.. automodule:: nurbs.Curve
    :members:
    :undoc-members:
..    :show-inheritance:

nurbs.Surface module
--------------------

.. automodule:: nurbs.Surface
    :members:
    :undoc-members:
..    :show-inheritance:

nurbs.utilities module
----------------------

.. automodule:: nurbs.utilities
    :members:
    :exclude-members: basis_functions, all_basis_functions, basis_functions_ders, check_uv, find_span, find_multiplicity
    :undoc-members:
..    :show-inheritance:

.. toctree::
   :maxdepth: 2

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
