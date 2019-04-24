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
* Support for common geometric algorithms: tessellation, voxelization, ray intersection, etc.
* Construct surfaces and volumes, extract isosurfaces via ``construct`` module
* Customizable visualization and animation options with Matplotlib, Plotly and VTK modules
* Import geometry data from common CAD formats, such as 3DM and SAT.
* Export geometry data into common CAD formats, such as 3DM, STL, OBJ and VTK
* Support importing/exporting in JSON, YAML and `libconfig <https://github.com/hyperrealm/libconfig>`_ formats
* `Jinja2 <http://jinja.pocoo.org/>`_ support for file imports
* Pure Python, no external C/C++ or FORTRAN library dependencies
* Python compatibility: 2.7.x, 3.4.x and later
* For higher performance, optional *Compile with Cython* options are also available
* Easy to install via `pip <https://pypi.org/project/geomdl/>`_ or `conda <https://anaconda.org/orbingol/geomdl>`_
* `Docker images <https://hub.docker.com/r/idealabisu/nurbs-python>`_ are available
* ``geomdl-shapes`` module for generating common spline and analytic geometries
* ``geomdl-cli`` module for using the library from the command line

NURBS-Python (geomdl) contains the following fundamental geometric algorithms:

* Point evaluation
* Derivative evaluation
* Knot insertion
* Knot removal
* Knot vector refinement
* Degree elevation
* Degree reduction

References
==========

* Leslie Piegl and Wayne Tiller. The NURBS Book. Springer Science & Business Media, 2012.
* David F. Rogers. An Introduction to NURBS: With Historical Perspective. Academic Press, 2001.
* Elaine Cohen et al. Geometric Modeling with Splines: An Introduction. CRC Press, 2001.
* Mark de Berg et al. Computational Geometry: Algorithms and Applications. Springer-Verlag TELOS, 2008.
* John F. Hughes et al. Computer Graphics: Principles and Practice. Pearson Education, 2014.
* Fletcher Dunn and Ian Parberry. 3D Math Primer for Graphics and Game Development. CRC Press, 2015.
* Erwin Kreyszig. Advanced Engineering Mathematics. John Wiley & Sons, 2010.
* Erich Gamma et al. Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley, 1994.

Author
======

* Onur R. Bingol (`@orbingol <https://github.com/orbingol>`_)
