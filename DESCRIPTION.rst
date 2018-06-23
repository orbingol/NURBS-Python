NURBS-Python
^^^^^^^^^^^^

|DOI|_ |RTD|_ |TRAVISCI|_ |APPVEYOR|_ |WAFFLEIO|_


.. note::

    Starting from v4.0, this package will be renamed to `geomdl <https://pypi.org/project/geomdl/>`_.
    Please see the `documentation <http://nurbs-python.readthedocs.io/en/latest/install.html>`_ for more details.


Description
===========

NURBS-Python provides Non-Uniform Rational B-Spline (NURBS) surface and 2D/3D curve data structures and computation
algorithms in native Python. The library is fully object-oriented and does *not* depend on any external libraries.

Features
========

NURBS-Python consists of the following modules and components:

* Core library
* Multi module
* Exchange module
* Visualization component
* Shapes component

Core Library
------------

The core library contains 4 modules:

* ``geomdl.BSpline`` contains Non-Uniform B-Spline (NUBS) evaluation and storage functionality
* ``geomdl.NURBS`` contains Non-Uniform Rational B-Spline (NURBS) evaluation and storage functionality
* ``geomdl.CPGen`` contains simple control points grid generation algorithms
* ``geomdl.utilities`` contains helper functions for generating and altering knot vectors and control points

``geomdl.BSpline`` and ``geomdl.NURBS`` modules contain the following classes:

* **Curve** for evaluating curves (in any dimension)
* **Surface** for evaluating surfaces

``geomdl.CPGen`` module contains 2 classes for grid generation:

* **Grid** for generating inputs for ``geomdl.BSpline.Surface`` class
* **GridWeighted** for generating inputs for ``geomdl.NURBS.Surface`` class

NURBS-Python provides abstract *Curve* and *Surface* base classes in ``geomdl.Abstract`` module.

Multi Module
------------

NURBS-Python provides container-like classes for working with multiple curves and surfaces in ``geomdl.Multi`` module.
Please see the documentation for details.

Exchange Module
---------------

NURBS-Python can export `Surface` types in OBJ and STL format using ``geomdl.exchange`` module. This module contains 2
major functions:

* ``save_obj`` for saving surfaces as .obj files
* ``save_stl`` for saving surfaces as .stl files in ascii or binary format (default is binary)

Visualization Component
-----------------------

NURBS-Python comes with an experimental visualization module, ``geomdl.visualization``, for plotting generated
2D/3D curves and surfaces directly.

Shapes Component
----------------

A new experimental module ``geomdl.shapes`` is also shipped with the NURBS-Python package.
The aim of this component is providing an easy way to generate the most common curves and surfaces, such as circles and
cylinders.

Further Reading
===============

* Github repository: https://github.com/orbingol/NURBS-Python/tree/3.x
* Examples: https://github.com/orbingol/NURBS-Python_Examples/tree/3.x
* Documentation: https://nurbs-python.readthedocs.io/en/3.x/

License
=======

NURBS-Python is licensed under The MIT License.


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |RTD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=stable
.. _RTD: http://nurbs-python.readthedocs.io/en/stable/?badge=stable

.. |WAFFLEIO| image:: https://badge.waffle.io/orbingol/NURBS-Python.svg?columns=all
.. _WAFFLEIO: https://waffle.io/orbingol/NURBS-Python

.. |TRAVISCI| image:: https://travis-ci.org/orbingol/NURBS-Python.svg?branch=master
.. _TRAVISCI: https://travis-ci.org/orbingol/NURBS-Python

.. |APPVEYOR| image:: https://ci.appveyor.com/api/projects/status/github/orbingol/nurbs-python?branch=master&svg=true
.. _APPVEYOR: https://ci.appveyor.com/project/orbingol/nurbs-python

.. _NURBS-Python: https://github.com/orbingol/NURBS-Python
.. _Examples: https://github.com/orbingol/NURBS-Python_Examples
