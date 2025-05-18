NURBS-Python (geomdl)
^^^^^^^^^^^^^^^^^^^^^

|RTD|_ |PYPI|_ |PYPIDL|_

Introduction
============

NURBS-Python (geomdl) is a pure Python, self-contained, object-oriented B-Spline and NURBS spline library for Python 3.

Features
========

NURBS-Python (geomdl) provides convenient data structures and highly customizable API for rational and non-rational
splines along with the efficient and extensible implementations of the following algorithms:

* Spline evaluation
* Derivative evaluation
* Knot insertion
* Knot removal
* Knot vector refinement
* Degree elevation
* Degree reduction
* Curve and surface fitting via interpolation and least squares approximation

NURBS-Python (geomdl) also provides customizable visualization and animation options via Matplotlib, Plotly and VTK
libraries. Please refer to the `documentation <http://nurbs-python.readthedocs.io/>`_ for more details.

Further reading
===============

* Documentation: https://nurbs-python.readthedocs.io/
* Examples: https://github.com/orbingol/NURBS-Python_Examples
* Development: https://github.com/orbingol/NURBS-Python

Additional file format support
==============================

* `rw3dm <https://github.com/orbingol/rw3dm>`_
* `rwsat <https://github.com/orbingol/rwsat>`_

Citing
======

The `following article <https://doi.org/10.1016/j.softx.2018.12.005>`_ outlines the design and features of NURBS-Python
(geomdl)::

    @article{bingol2019geomdl,
      title={{NURBS-Python}: An open-source object-oriented {NURBS} modeling framework in {Python}},
      author={Bingol, Onur Rauf and Krishnamurthy, Adarsh},
      journal={{SoftwareX}},
      volume={9},
      pages={85--94},
      year={2019},
      publisher={Elsevier},
      doi={https://doi.org/10.1016/j.softx.2018.12.005}
    }

License
=======

NURBS-Python (geomdl) is licensed under the terms of `MIT License <LICENSE>`_ and it contains the following modules:

* ``six`` is licensed under the terms of `MIT License <https://github.com/benjaminp/six/blob/1.12.0/LICENSE>`_
* ``backports.functools_lru_cache`` is licensed under the terms of `MIT License <https://github.com/jaraco/backports.functools_lru_cache/blob/1.5/LICENSE>`_

.. |RTD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=5.x
.. _RTD: https://nurbs-python.readthedocs.io/en/5.x/?badge=5.x

.. |PYPI| image:: https://img.shields.io/pypi/v/geomdl.svg
.. _PYPI: https://pypi.org/project/geomdl/

.. |PYPIDL| image:: https://img.shields.io/pypi/dm/geomdl.svg
.. _PYPIDL: https://pypi.org/project/geomdl/
