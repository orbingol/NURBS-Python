NURBS-Python (geomdl)
^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |PYPI|_ |PYPIDL|_ |ANACONDA|_

|RTD|_ |TRAVISCI|_ |APPVEYOR|_ |CIRCLECI|_ |CODECOV|_

|WAFFLEIO|_

Introduction
============

NURBS-Python (geomdl) is an object-oriented B-Spline and NURBS surface and curve library for Python with
implementations of advanced computation algorithms in an extensible way. It comes with various features, such as
on-the-fly visualization options, knot vector and surface grid generators, tessellation, voxelization and more.

NURBS-Python is a pure Python library, therefore there are no external C/C++ or FORTRAN dependencies or any compilation
steps during installation. A Cython-compiled option also is provided for better performance. Moreover, the core library
is self-contained; and therefore, it can be easily used with systems using embedded Python.

NURBS-Python is tested with Python v2.7.x, Python v3.4.x and later.

Citing NURBS-Python
-------------------

The following article outlines the design and features of NURBS-Python (geomdl). I would be glad if you would cite it
if you have used NURBS-Python (geomdl) in your research::

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

Please refer to the `Citing <http://nurbs-python.readthedocs.io/en/latest/citing.html>`_ section of the documentation
for more details.

Examples, Documentation and Extras
----------------------------------

* **Examples**: https://github.com/orbingol/NURBS-Python_Examples
* **Documentation**: http://nurbs-python.readthedocs.io/
* **Wiki**: https://github.com/orbingol/NURBS-Python/wiki
* **Command line application**: https://github.com/orbingol/geomdl-cli
* **rw3dm**: https://github.com/orbingol/rw3dm

Using NURBS-Python (geomdl)
===========================

Installation and Testing
------------------------

Please refer to the `Installation and Testing <http://nurbs-python.readthedocs.io/en/latest/install.html>`_ section
of the documentation for details.

Contributions and Issues
------------------------

All contributions are welcome. For details, please refer to the
`Issues and Reporting <http://nurbs-python.readthedocs.io/en/latest/q_a.html#issues-and-reporting>`_ section of the
documentation for details.

Author
======

* Onur Rauf Bingol (`@orbingol <https://github.com/orbingol>`_)

License
=======

NURBS-Python (geomdl) is a free and open-source software and it is licensed under the `MIT License <LICENSE>`_.

Acknowledgments
===============

I would like to thank my PhD adviser, `Dr. Adarsh Krishnamurthy <https://www.me.iastate.edu/faculty/?user_page=adarsh>`_,
for his guidance and supervision throughout the course of this project.

In addition, I would like to thank `all NURBS-Python contributors <CONTRIBUTORS.rst>`_ for their time and effort in
supporting this project.


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |RTD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=latest
.. _RTD: http://nurbs-python.readthedocs.io/en/latest/?badge=latest

.. |WAFFLEIO| image:: https://badge.waffle.io/orbingol/NURBS-Python.svg?columns=all
.. _WAFFLEIO: https://waffle.io/orbingol/NURBS-Python

.. |TRAVISCI| image:: https://travis-ci.org/orbingol/NURBS-Python.svg?branch=master
.. _TRAVISCI: https://travis-ci.org/orbingol/NURBS-Python

.. |APPVEYOR| image:: https://ci.appveyor.com/api/projects/status/github/orbingol/nurbs-python?branch=master&svg=true
.. _APPVEYOR: https://ci.appveyor.com/project/orbingol/nurbs-python

.. |CIRCLECI| image:: https://circleci.com/gh/orbingol/NURBS-Python/tree/master.svg?style=shield
.. _CIRCLECI: https://circleci.com/gh/orbingol/NURBS-Python/tree/master

.. |PYPI| image:: https://img.shields.io/pypi/v/geomdl.svg
.. _PYPI: https://pypi.org/project/geomdl/

.. |PYPIDL| image:: https://img.shields.io/pypi/dm/geomdl.svg
.. _PYPIDL: https://pypi.org/project/geomdl/

.. |ANACONDA| image:: https://anaconda.org/orbingol/geomdl/badges/version.svg
.. _ANACONDA: https://anaconda.org/orbingol/geomdl

.. |CODECOV| image:: https://codecov.io/gh/orbingol/NURBS-Python/branch/master/graph/badge.svg
.. _CODECOV: https://codecov.io/gh/orbingol/NURBS-Python
