.. NURBS-Python documentation master file, created by
   sphinx-quickstart on Fri Mar 10 21:16:25 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

NURBS-Python Documentation
==========================

Introduction
------------

.. automodule:: geomdl
    :members:
    :undoc-members:

Author
^^^^^^

Onur Rauf Bingol

* E-mail: contact@onurbingol.net
* Twitter: https://twitter.com/orbingol

Q&A
^^^

**What is NURBS?**

NURBS, namely *Non-Uniform Rational Basis Spline*, is a mathematical model for generation of curves and surfaces in a flexible way. It is a well-accepted industry standard and used as a basis for nearly all of the 3D modeling and CAD/CAM software packages.
Please see the `the related Wikipedia article <https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline>`_ or `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_, a very nice and informative book written by Dr. Piegl and Dr. Tiller.

**What is the purpose of this package/library?**

Implementing the well-known NURBS algorithms in native Python in an organized way and without using any converters or
wrappers, like `SWIG <http://www.swig.org/>`_ or `Boost.Python <https://github.com/boostorg/python>`_.

**What are the minimum requirements?**

NURBS-Python is tested on Python versions 2.7.13 and 3.5.3+. It doesn't require any additional packages, such as NumPy,
so that you can run it on a plain Python installation.

**How can I install NURBS-Python?**

The easiest method to install NURBS-Python is using the included setup script, i.e. ``python setup.py install``.

.. note:: Please use the issue tracker on GitHub to report bugs. If you have any questions and/or comments, please feel free to email the author.

Examples
--------

You can find the example scripts in the `Examples <https://github.com/orbingol/NURBS-Python_Examples>`_ repository.

2D Curves
^^^^^^^^^

.. image:: images/ex_curve01.png
    :alt: Curve example

.. image:: images/ex_curve03.png
    :alt: Curve example with tangents as quiver plots

.. image:: images/ex_curve04.png
    :alt: A full circle using NURBS

Surfaces
^^^^^^^^

.. image:: images/ex_surface01.png
    :alt: Surface example 1

.. image:: images/ex_surface02.png
    :alt: Surface example 2

.. image:: images/ex_surface03.png
    :alt: Surface example 3

Submodules
----------

The package name is :code:`geomdl` and it contains :code:`BSpline` and :code:`NURBS` modules along with the :code:`utilities`
module for functions common in both :code:`BSpline` and :code:`NURBS`. It also includes a simple control points generator
module, :code:`CPGen`, to use as an input to :code:`BSpline.Surface` and :code:`NURBS.Surface` classes.

B-Spline Module
^^^^^^^^^^^^^^^

:code:`BSpline` module provides data storage properties and evaluation functions for B-Spline (NUBS) 2D/3D curves and surfaces.

3D B-Spline Curve
~~~~~~~~~~~~~~~~~

.. autoclass:: geomdl.BSpline.Curve
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

2D B-Spline Curve
~~~~~~~~~~~~~~~~~

.. autoclass:: geomdl.BSpline.Curve2D
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

B-Spline Surface
~~~~~~~~~~~~~~~~

.. autoclass:: geomdl.BSpline.Surface
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

NURBS Module
^^^^^^^^^^^^

:code:`NURBS` module provides data storage properties and evaluation functions for NURBS 2D/3D curves and surfaces.

3D NURBS Curve
~~~~~~~~~~~~~~

.. autoclass:: geomdl.NURBS.Curve
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

2D NURBS Curve
~~~~~~~~~~~~~~

.. autoclass:: geomdl.NURBS.Curve2D
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

NURBS Surface
~~~~~~~~~~~~~

.. autoclass:: geomdl.NURBS.Surface
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Utilities module
^^^^^^^^^^^^^^^^

:code:`utilities` module contains common helper functions for B-spline and NURBS curve and surface evaluation.

.. automodule:: geomdl.utilities
    :members:
    :exclude-members: basis_functions, basis_functions_all, basis_functions_ders, check_uv, find_span, find_multiplicity
    :undoc-members:

Control Points Generator Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:code:`CPGen` module allows users to generate control points grids as an input to :code:`BSpline.Surface` and
:code:`NURBS.Surface` classes. This module is designed to enable more testing cases in a very simple way and it doesn't
have the capabilities of a fully-featured grid generator, but it should be enough to be used side by side with
:code:`BSpline` and :code:`NURBS` modules.

:code:`CPGen.Grid` class provides an easy way to generate control point grids for use with :code:`BSpline.Surface` class
and :code:`CPGen.GridWeighted` does the same for :code:`NURBS.Surface` class.


Grid
~~~~

.. autoclass:: geomdl.CPGen.Grid
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:


Weighted Grid
~~~~~~~~~~~~~

.. autoclass:: geomdl.CPGen.GridWeighted
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:


.. toctree::
    :maxdepth: 2

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
