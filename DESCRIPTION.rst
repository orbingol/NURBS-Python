NURBS-Python (geomdl)
^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |ANACONDA|_

|RTD|_ |TRAVISCI|_ |APPVEYOR|_ |CODECOV|_

|WAFFLEIO|_

Introduction
============

NURBS-Python (geomdl) provides fully object-oriented Non-Uniform Rational B-Spline (NURBS) surface and curve data
structures and extensible advanced computation algorithms in pure python. It allows users to directly visualize the
computed curves and surfaces using various visualization libraries. Additionally, it comes with a surface generator.

Features
========

NURBS-Python consists of the following modules and components:

* Core library
* Exchange module
* Visualization component
* Shapes component

Core Library
------------

The core library is responsible for data storage and evaluation. It is capable of handling B-Spline (NUBS) and NURBS
curves and surfaces (single via ``geomdl.BSpline`` and ``geomdl.NURBS``, multiple via ``geomdl.Multi`` modules).
It provides an abstraction layer for easy extensibility (``geomdl.Abstract``), allows a variety of customizations and
helper functionality, such as surface (``geomdl.CPGen`` module) and uniform knot vector
(``geomdl.utilities.generate_knot_vector``) generators.

Exchange Module
---------------

``geomdl.exchange`` module can export control points and evaluated points of the ``Curve`` and ``Surface`` objects
in common formats such as CSV, VTK, OBJ, OFF and STL.

Visualization Component
-----------------------

``geomdl.visualization`` component contains customizable classes for plotting curves and surfaces directly.

Shapes Component
----------------

``geomdl.shapes`` component provides an easy way to generate the most common curves and surfaces, such as circles and
cylinders.

Further Reading
===============

* Github repository: https://github.com/orbingol/NURBS-Python
* Examples: https://github.com/orbingol/NURBS-Python_Examples
* Documentation: http://nurbs-python.readthedocs.io/

License
=======

NURBS-Python is licensed under the MIT License.


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |RTD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=latest
.. _RTD: http://nurbs-python.readthedocs.io/en/stable/?badge=latest

.. |WAFFLEIO| image:: https://badge.waffle.io/orbingol/NURBS-Python.svg?columns=all
.. _WAFFLEIO: https://waffle.io/orbingol/NURBS-Python

.. |TRAVISCI| image:: https://travis-ci.org/orbingol/NURBS-Python.svg?branch=master
.. _TRAVISCI: https://travis-ci.org/orbingol/NURBS-Python

.. |APPVEYOR| image:: https://ci.appveyor.com/api/projects/status/github/orbingol/nurbs-python?branch=master&svg=true
.. _APPVEYOR: https://ci.appveyor.com/project/orbingol/nurbs-python

.. |ANACONDA| image:: https://anaconda.org/orbingol/geomdl/badges/version.svg
.. _ANACONDA: https://anaconda.org/orbingol/geomdl

.. |CODECOV| image:: https://codecov.io/gh/orbingol/NURBS-Python/branch/master/graph/badge.svg
.. _CODECOV: https://codecov.io/gh/orbingol/NURBS-Python
