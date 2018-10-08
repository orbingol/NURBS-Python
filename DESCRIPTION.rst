NURBS-Python (geomdl)
^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |ANACONDA|_

|RTD|_ |TRAVISCI|_ |APPVEYOR|_ |CODECOV|_

|WAFFLEIO|_

Introduction
============

NURBS-Python (geomdl) is an object-oriented B-Spline and NURBS surface and curve library for Python with implementations
of advanced computation algorithms in an extensible way. It comes with on-the-fly shape visualization options,
knot vector and surface grid generators, and more.

NURBS-Python (geomdl) is a pure Python library, therefore there are no external C/C++ or FORTRAN dependencies or any
compilation steps during installation. It is tested with Python v2.7.x, Python v3.3.x and later versions. The Python 2
and 3 compatibility library ``six`` will be automatically installed during NURBS-Python setup.

Please see the `Examples Repository <https://github.com/orbingol/NURBS-Python_Examples>`_ for details on library usage
and integration scenarios.

**Note:** This package replaces the old `NURBS-Python <https://pypi.org/project/NURBS-Python/>`_ with new and improved
features. Please see the `Installation <https://nurbs-python.readthedocs.io/en/latest/install.html>`_ documentation
page on removing the old package and installing the new package.

Features
========

Core Library
------------

The core library is responsible for data storage and evaluation. It is capable of handling B-Spline (NUBS) and NURBS
curves and surfaces (single via ``geomdl.BSpline`` and ``geomdl.NURBS``, multiple via ``geomdl.Multi`` modules).
It provides an abstraction layer for easy extensibility (``geomdl.Abstract``), allows a variety of customizations and
helper functionality, such as surface (``geomdl.CPGen`` module) and uniform knot vector
(``geomdl.utilities.generate_knot_vector``) generators.

The Core Library module of NURBS-Python is self-contained. It implements all the necessary maths and linear algebra
operations without needing any other external modules.

Exchange Module
---------------

``geomdl.exchange`` module can export control points and evaluated points of the ``Curve``, ``Surface`` and ``Multi``
objects in common formats such as CSV, VTK, OBJ, OFF and STL.

Visualization Component
-----------------------

``geomdl.visualization`` component contains extensible and customizable classes for plotting curves and surfaces
on-the-fly. The users have options to use Matplotlib and/or Plotly visualization libraries. These libraries are not
automatically installed during NURBS-Python setup and left for users' discretion.

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
