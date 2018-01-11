Non-Uniform Rational Basis Spline (NURBS) Python Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |RTFD|_

Introduction
============

This project aims to implement Non-Uniform Rational B-Spline (NURBS) curve and surface computation algorithms in native
Python with minimum possible dependencies. The library is fully object-oriented and does *not* depend on any external
C/C++ libraries.

Information for Researchers
---------------------------

I would be glad if you cite this repository using the DOI_ provided as a badge at the top.

Description of the Package
==========================

Algorithms
----------

NURBS-Python currently implements the following algorithms from **The NURBS Book** by Piegl & Tiller:

* Algorithm A2.1: FindSpan
* Algorithm A2.2: BasisFuns
* Algorithm A2.3: DersBasisFuns
* Algorithm A3.1: CurvePoint
* Algorithm A3.2: CurveDerivsAlg1
* Algorithm A3.3: CurveDerivCpts
* Algorithm A3.4: CurveDerivsAlg2
* Algorithm A3.5: SurfacePoint
* Algorithm A3.6: SurfaceDerivsAlg1
* Algorithm A4.1: CurvePoint (from weighted control points)
* Algorithm A4.3: SurfacePoint (from weighted control points)

Data Structure
--------------

The data structure in ``Curve`` and ``Surface`` classes is implemented using `Python properties <https://docs.python.org/2/library/functions.html#property>`_.
The following table shows the properties defined in these classes:

+------------------+-----------------------------+--------------------------------------+
| Curve Properties | Surface Properties          | Notes                                |
+==================+=============================+======================================+
| degree           | degree_u / degree_v         | degree(s)                            |
+------------------+-----------------------------+--------------------------------------+
| knotvector       | knotvector_u / knotvector_v | knot vector(s)                       |
+------------------+-----------------------------+--------------------------------------+
| ctrlpts          | ctrlpts                     | 1-D array of control points          |
+------------------+-----------------------------+--------------------------------------+
| ctrlptsw         | ctrlptsw                    | 1-D array of weighted control points |
+------------------+-----------------------------+--------------------------------------+
|                  | ctrlpts2D                   | 2-D array of control points          |
+------------------+-----------------------------+--------------------------------------+
| weights          | weights                     | weights vector                       |
+------------------+-----------------------------+--------------------------------------+
| delta            | delta                       | evaluation delta                     |
+------------------+-----------------------------+--------------------------------------+
| curvepts         | surfpts                     | evaluated points                     |
+------------------+-----------------------------+--------------------------------------+

Evaluation Methods
------------------

After setting the required parameters, the curve or the surface can be evaluated using ``evaluate()`` or
``evaluate_rational()`` methods. Then, the evaluated curve points can be obtained from ``curvepts`` property and the
evaluated surface points can be obtained from ``surfpts`` property. The curve and surface derivatives can be evaluated
using ``derivatives()`` method. An easy way to get the 1st derivatives using ``tangent()`` method is available in both
classes.

``Surface`` class has methods for transposing the surface by swapping U and V directions, ``tranpose()``,
and finding surface normals, ``normal()``.

Reading Control Points
----------------------

Both classes have ``read_ctrlpts()`` and ``read_ctrlptsw()`` methods for reading control points and weighted control
points, respectively, from a text file. The details on the file format are explained in `FORMATS.md <FORMATS.md>`_ file.

Additional Features
-------------------

``utilities`` module has some extra features for several mathematical operations:

* ``autogen_knotvector()`` generates a uniform knot vector according to the input degree and number of control points
* ``normalize_knotvector()`` normalizes the knot vector between 0 and 1
* ``cross_vector()`` computes the cross production of the input vectors
* ``normalize_vector()`` generates a unit vector from the input vector

Other functions in the ``utilities`` module are used as helper functions in evaluation methods of ``Curve`` and
``Surface`` classes.

2D Grid Generation
------------------

``Grid`` module is capable of generating simple 2D control point grids for use with the ``Surface`` class.
Please check the examples repository on how to use the ``Grid`` class and its features.

Minimum Requirements
====================

One of the major goals of this project is implementing all these algorithms with minimum dependencies.
Currently, the NURBS-Python package can run with plain Python and therefore, it has no extra dependencies,
like NumPy or similar. The code was tested with Python versions 2.7.12 and 3.5.3.

On the other hand, the plotting part of the examples requires Matplotlib installed in your Python distribution.
If you don't need any plotting, you basically won't need Matplotlib at all.

Installation
============

Included *setup.py* script will take care of the installation and automatically copy the required files to
*site-packages* directory. Please run the following from the command line:

``python setup.py install``

If you don't want to put the files into your Python distribution's *site-packages* directory for some reason,
you can run

``python setup.py develop``

from the command line to generate a link to the package directory inside *site-packages*.

Example Scripts
===============

Please see `NURBS-Python Examples <https://github.com/orbingol/NURBS-Python_Examples/tree/2.x>`_ repository for examples.

Issues and Reporting
====================

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

License
=======

NURBS-Python is licensed under `The MIT License <LICENSE>`_.

Acknowledgments
===============

I would like to thank my PhD adviser, `Dr. Adarsh Krishnamurthy <https://www.me.iastate.edu/faculty/?user_page=adarsh>`_,
for his guidance and supervision throughout the course of this project.


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |RTFD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=2.x
.. _RTFD: http://nurbs-python.readthedocs.io/en/2.x/

.. _NURBS-Python: https://github.com/orbingol/NURBS-Python
