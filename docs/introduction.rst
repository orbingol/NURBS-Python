Motivation
^^^^^^^^^^

NURBS-Python is an object-oriented Python library containing implementations of :doc:`NURBS <q_a>` 2D/3D curve and
surface generation and evaluation algorithms. It also provides a convenient and easy-to-use data structure for storing
curve and surface descriptions as Python properties.

Some of the significant features of the NURBS-Python Library are:

* Python 2.x and 3.x compatibility
* No external dependencies (such as NumPy)
* Implements Python properties (using *property* decorator)
* A :code:`utilities` module containing several helper functions
* :code:`Grid` and :code:`GridWeighted` classes for generating various types of control points grids

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

Citing NURBS-Python
===================

I would be glad if you cite this repository using the DOI_ provided. You can also find it as a badge on the
:doc:`main page <index>` of this documentation.

Author
======

Onur Rauf Bingol

* E-mail: contact@onurbingol.net
* Twitter: https://twitter.com/orbingol

Acknowledgments
===============

I would like to thank my PhD adviser, `Dr. Adarsh Krishnamurthy <https://www.me.iastate.edu/faculty/?user_page=adarsh>`_,
for his guidance and supervision throughout the course of this project.


.. _DOI: https://doi.org/10.5281/zenodo.815010
