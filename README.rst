NURBS-Python
^^^^^^^^^^^^

|DOI|_

|PYPI|_ |RTD|_ |TRAVISCI|_ |APPVEYOR|_ |WAFFLEIO|_

Introduction
============

This project aims to implement Non-Uniform Rational B-Spline (NURBS) curve and surface computation algorithms in native
Python with minimum possible dependencies. The library is fully object-oriented and does *not* depend on any external
C/C++ libraries.

Implementation
--------------

NURBS-Python is a high-level Python library following the object-oriented design principles.
In its core, it implements the algorithms from **The NURBS Book (2nd Edition)** by Piegl & Tiller and combines
these algorithms with other useful features. Please see the documentation for function reference
and details on how to use the library: https://nurbs-python.readthedocs.io/en/3.x/

Examples
--------

The Examples_ repository contains example scripts describing how to use NURBS-Python with advanced visualization
examples. Please see the documentation for more details.

Citing NURBS-Python
-------------------

I would be glad if you cite this repository using the DOI_ provided as a badge at the top.

Features
========

NURBS-Python consists of the following modules:

* Core library
* Multi module
* Exchange module
* Visualization module

In addition, it also contains the following experimental components:

* Matplotlib visualization component
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

Starting from version 3.2, NURBS-Python provides abstract *Curve* and *Surface* base classes with ``geomdl.Abstract``
module.

Multi Module
------------

NURBS-Python provides container-like classes for visualization of multiple curves and surfaces with ``geomdl.Multi``
module. Please see the documentation for details.

Exchange Module
---------------

NURBS-Python can export `Surface` types in OBJ and STL format using ``geomdl.exchange`` module. This module contains 2
major functions:

* ``save_obj()`` for saving surfaces as .obj files
* ``save_stl()`` for saving surfaces as .stl files in ascii or binary format (default is binary)

Visualization Module
--------------------

NURBS-Python provides a visualization module, ``geomdl.VisBase`` to serve as a basis for all possible visualization
components, such as OpenGL, for plotting 2D/3D curves and surfaces directly using ``render()`` method.

NURBS-Python comes with an experimental visualization component, ``geomdl.visualization`` which implements Matplotlib.
This component provides a variety of visualization options for surfaces and 2D/3D curves.

Shapes Component
----------------

Starting from NURBS-Python v3.1, a new experimental component ``geomdl.shapes`` is shipped with the NURBS-Python
package. The aim of this component is providing an easy way to generate the most common curves and surfaces,
such as circles and cylinders.

Installation
============

Using Pip
---------

You can find the NURBS-Python library on `Python Package Index <https://pypi.python.org/pypi/NURBS-Python>`_ and install
using the following command:

``pip install NURBS-Python``

Manual Method
-------------

Included *setup.py* script will take care of the installation and automatically copy the required files to
*site-packages* directory. Please run the following from the command line:

``python setup.py install``

If you don't want to put the files into your Python distribution's *site-packages* directory for some reason (e.g.
extension development or bug fixing), you can run

``python setup.py develop``

from the command line to generate a link to the package directory inside *site-packages*.

Testing
-------

``tests/`` directory contains the testing scripts. In order to execute the tests which comes with NURBS-Python,
you need to install `pytest <https://pytest.readthedocs.io/en/latest>`_ on your Python distribution.
After installing the required packages, execute the following from your favorite IDE or from the command line:

``pytest``

pytest will automatically find the tests under ``tests/`` directory, execute them and show the results.

Branch Information
==================

* ``3.x`` branch contains code for NURBS-Python v3.x series
* ``2.x`` branch contains code for NURBS-Python v2.x series

There are some API changes between *v2.x* and *v3.x* series and all updates will be added to the latest version. Old
versions won't be receiving any new features and updates.

Issues and Reporting
====================

Contributions to NURBS-Python
-----------------------------

All contributions to NURBS-Python are welcomed. I would recommend you reading `CONTRIBUTING <.github/CONTRIBUTING.md>`_
file for more details.

Bugs and Issues
---------------

Please use the issue tracker for reporting bugs and other related issues.

Comments and Questions
----------------------

If you have any questions or comments related to the NURBS-Python package, please don't hesitate to contact the
developers by email.

Author
======

* Onur Rauf Bingol (`@orbingol <https://github.com/orbingol>`_)

Contributors
============

I would like to thank all contributors for their help and support in testing, bug fixing and improvement of the
NURBS-Python_ project.

* Luke Frisken (`@kellpossible <https://github.com/kellpossible>`_)
* John-Eric Dufour (`@jedufour <https://github.com/jedufour>`_)
* Jan Heczko (`@heczis <https://github.com/heczis>`_)
* Pavel Vlasanek (`@tucna <https://github.com/tucna>`_)
* Xuefeng Zhao

License
=======

NURBS-Python is licensed under `The MIT License <LICENSE>`_.

Acknowledgments
===============

I would like to thank my PhD adviser, `Dr. Adarsh Krishnamurthy <https://www.me.iastate.edu/faculty/?user_page=adarsh>`_,
for his guidance and supervision throughout the course of this project.


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |RTD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=stable
.. _RTD: http://nurbs-python.readthedocs.io/en/stable/?badge=stable

.. |WAFFLEIO| image:: https://badge.waffle.io/orbingol/NURBS-Python.svg?columns=all
.. _WAFFLEIO: https://waffle.io/orbingol/NURBS-Python

.. |PYPI| image:: https://img.shields.io/pypi/v/NURBS-Python.svg
.. _PYPI: https://pypi.python.org/pypi/NURBS-Python

.. |TRAVISCI| image:: https://travis-ci.org/orbingol/NURBS-Python.svg?branch=master
.. _TRAVISCI: https://travis-ci.org/orbingol/NURBS-Python

.. |APPVEYOR| image:: https://ci.appveyor.com/api/projects/status/github/orbingol/nurbs-python?branch=master&svg=true
.. _APPVEYOR: https://ci.appveyor.com/project/orbingol/nurbs-python

.. _NURBS-Python: https://github.com/orbingol/NURBS-Python
.. _Examples: https://github.com/orbingol/NURBS-Python_Examples
