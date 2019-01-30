Motivation
^^^^^^^^^^

NURBS-Python (geomdl) is a self-contained, object-oriented pure Python B-Spline and NURBS library with implementations
of curve, surface and volume generation and evaluation algorithms. It also provides convenient and easy-to-use data
structures for storing curve, surface and volume descriptions.

Some significant features of NURBS-Python (geomdl):

* Self-contained, object-oriented, extensible and highly customizable API
* Convenient data structures for storing curve, surface and volume descriptions
* Surface and curve fitting with interpolation and least squares approximation
* Knot vector and surface grid generators
* Customizable visualization and animation options with Matplotlib, Plotly and VTK modules
* Exporting curve, surface and volume data into various file formats, such as JSON, YAML, Libconfig, STL, OBJ and VTK
* Support for common algorithms: tessellation, voxelization, ray intersection, etc.
* Shapes component for generation common surfaces and curves
* Pure Python, no external C/C++ or FORTRAN library dependencies
* Python compatibility: 2.7.x, 3.4.x and later
* No compilation steps are necessary, everything is implemented in pure Python
* For higher performance, optional *Compile with Cython* options are also available via ``setup.py``
* Easy to install via **pip**: ``pip install geomdl`` or **conda**: ``conda install -c orbingol geomdl``
* `Docker images <https://hub.docker.com/r/idealabisu/nurbs-python>`_ are available

NURBS-Python (geomdl) contains the following fundamental geometric algorithms:

* Point evaluation
* Derivative evaluation
* Knot insertion
* Knot removal
* Degree elevation
* Degree reduction

References
==========

* Piegl, Les, and Wayne Tiller. The NURBS book. Springer Science & Business Media, 2012.
* Berg, Mark de, et al. Computational Geometry: Algorithms and Applications. Springer-Verlag TELOS, 2008.
* Hughes, John F., et al. Computer Graphics: Principles and Practice. Pearson Education, 2014.
* Dunn, Fletcher, and Ian Parberry. 3D Math Primer for Graphics and Game Development. CRC Press, 2015.
* Kreyszig, Erwin. Advanced Engineering Mathematics. John Wiley & Sons, 2010.
* Gamma, Erich. Design Patterns: Elements of Reusable Object-Oriented Software. Pearson Education India, 1995.

Author
======

Onur Rauf Bingol

* E-mail: contact@onurbingol.net
* Twitter: https://twitter.com/orbingol
* LinkedIn: https://www.linkedin.com/in/onurraufbingol/


.. _DOI: https://doi.org/10.5281/zenodo.815010
