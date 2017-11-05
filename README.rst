B-Spline and NURBS Evaluation Library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |RTFD|_

Introduction
============

This project implements Non-Uniform Rational B-Spline (NURBS) curve and surface computation algorithms in native Python
with minimum possible dependencies. The package contains 3 modules:

* :code:`BSpline` contains Non-Uniform B-Spline (NUBS) algorithms
* :code:`NURBS` contains Non-Uniform Rational B-Spline (NURBS) algorithms
* :code:`CPGen` contains simple control points grid generation algorithms

:code:`BSpline` and :code:`NURBS` modules contain 3 classes for geometric evaluation:

* **Curve** for evaluating 3D curves
* **Curve2D** for evaluating 2D curves
* **Surface** for evaluating surfaces

:code:`CPGen` module contains 2 classes for grid generation:

* **Grid** for generating inputs for :code:`BSpline.Surface` class
* **GridWeighted** for generating inputs for :code:`NURBS.Surface` class

Information for Researchers
---------------------------

I would be glad if you cite this repository using the DOI_ provided as a badge at the top.

Example Scripts
===============

Please see `NURBS-Python Examples <https://github.com/orbingol/NURBS-Python_Examples>`_ repository for examples.

Algorithms Implemented
======================

NURBS-Python currently implements the following algorithms from **The NURBS Book (2nd Edition)** by Piegl & Tiller:

* **Algorithm A2.1:** FindSpan *(page 68)*
* **Algorithm A2.2:** BasisFuns *(page 70)*
* **Algorithm A2.3:** DersBasisFuns *(pages 72,73)*
* **Algorithm A3.1:** CurvePoint *(page 82)*
* **Algorithm A3.2:** CurveDerivsAlg1 *(page 93)*
* **Algorithm A3.3:** CurveDerivCpts *(page 98)*
* **Algorithm A3.4:** CurveDerivsAlg2 *(pages 99,100)*
* **Algorithm A3.5:** SurfacePoint *(page 103)*
* **Algorithm A3.6:** SurfaceDerivsAlg1 *(pages 111,112)*
* **Algorithm A4.1:** CurvePoint *(page 124)*
* **Algorithm A4.2:** RatCurveDerivs *(page 127)*
* **Algorithm A4.3:** SurfacePoint *(page 134)*
* **Algorithm A4.4:** RatSurfaceDerivs *(pages 137,138)*
* **Algorithm A5.1:** CurveKnotIns *(page 151)*
* **Algorithm A5.3:** SurfaceKnotIns *(pages 155-157)*

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

* John-Eric Dufour (`@jedufour <https://github.com/jedufour>`_)
* Jan Heczko (`@heczis <https://github.com/heczis>`_)

License
=======

NURBS-Python is licensed under `The MIT License <LICENSE>`_.

Acknowledgments
===============

I would like to thank my PhD adviser, `Dr. Adarsh Krishnamurthy <https://www.me.iastate.edu/faculty/?user_page=adarsh>`_
, for his guidance and supervision throughout the course of this project.

.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |RTFD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=latest
.. _RTFD: http://nurbs-python.readthedocs.io/en/latest/?badge=latest
