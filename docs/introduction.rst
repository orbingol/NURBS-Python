Motivation
^^^^^^^^^^

NURBS-Python is an object-oriented Python library containing implementations of :doc:`NURBS <q_a>` curve and
surface generation and evaluation algorithms. It also provides a convenient and easy-to-use data structure for storing
curve and surface descriptions.

Some significant features of NURBS-Python are:

* Fully object-oriented API with an abstract interface for extensions
* Data structures for storing surface and curve descriptions (in all dimensions)
* Helper functions, such as automatic uniform knot vector generator and many more
* Control points grid generator for surfaces
* Visualization module for direct plotting of curves and surfaces
* Shapes component for generation common surfaces and curves
* CSV export functionality with customizable meshing options
* Python 2.7.x and 3.x compatibility
* No external C/C++ library dependencies
* No compilation steps are necessary, everything is implemented in pure python
* Easy to install via pip: ``pip install geomdl``
* Conda packages are also available for installation: ``conda install -c orbingol geomdl``

References
==========

NURBS-Python implements the following algorithms from **The NURBS Book (2nd Edition)** by Piegl & Tiller:

* A2.1 FindSpan *(page 68)*
* A2.2 BasisFuns *(page 70)*
* A2.3 DersBasisFuns *(pages 72,73)*
* A2.4 OneBasisFun *(pages 74,75)*
* A2.5 DersOneBasisFun *(pages 76-78)*
* A3.1 CurvePoint *(page 82)*
* A3.2 CurveDerivsAlg1 *(page 93)*
* A3.3 CurveDerivCpts *(page 98)*
* A3.4 CurveDerivsAlg2 *(pages 99,100)*
* A3.5 SurfacePoint *(page 103)*
* A3.6 SurfaceDerivsAlg1 *(pages 111,112)*
* A4.1 CurvePoint *(page 124)*
* A4.2 RatCurveDerivs *(page 127)*
* A4.3 SurfacePoint *(page 134)*
* A4.4 RatSurfaceDerivs *(pages 137,138)*
* A5.1 CurveKnotIns *(page 151)*
* A5.3 SurfaceKnotIns *(pages 155-157)*

Author
======

Onur Rauf Bingol

* E-mail: contact@onurbingol.net
* Twitter: https://twitter.com/orbingol
* LinkedIn: https://www.linkedin.com/in/onurraufbingol/

Acknowledgments
===============

I would like to thank my PhD adviser, `Dr. Adarsh Krishnamurthy <https://www.me.iastate.edu/faculty/?user_page=adarsh>`_,
for his guidance and supervision throughout the course of this project.


.. _DOI: https://doi.org/10.5281/zenodo.815010
