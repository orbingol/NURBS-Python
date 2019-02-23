NURBS-Python (geomdl)
^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |PYPI|_ |PYPIDL|_ |ANACONDA|_

|RTD|_ |TRAVISCI|_ |APPVEYOR|_ |CIRCLECI|_ |CODECOV|_

|WAFFLEIO|_

Introduction
============

NURBS-Python (geomdl) is a pure Python, self-contained, object-oriented B-Spline and NURBS spline library for Python
versions 2.7.x, 3.4.x and later.

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

Installation
============

The easiest way to install NURBS-Python (geomdl) is using ``pip``:

.. code-block:: console

    $ pip install geomdl

If you are getting permission errors on Linux, you can use ``--user`` switch to install to current user's package
directory.

.. code-block:: console

    $ pip install --user geomdl

It is also possible to install NURBS-Python (geomdl) using ``conda``:

.. code-block:: console

    $ conda install -c orbingol geomdl

Please refer to the `Installation and Testing <http://nurbs-python.readthedocs.io/en/latest/install.html>`_ section
of the documentation for alternative installation methods.

Examples and Documentation
==========================

* **Examples**: https://github.com/orbingol/NURBS-Python_Examples
* **Documentation**: http://nurbs-python.readthedocs.io/
* **Wiki**: https://github.com/orbingol/NURBS-Python/wiki

Extra Modules
=============

* **Command line application**: https://github.com/orbingol/geomdl-cli
* **Rhino importer/exporter**: https://github.com/orbingol/rw3dm
* **Shapes module**: https://github.com/orbingol/geomdl-shapes

Author
======

* Onur R. Bingol (`@orbingol <https://github.com/orbingol>`_)

Acknowledgments
===============

Please see `CONTRIBUTORS.rst <CONTRIBUTORS.rst>`_ file for the acknowledgements.

License
=======

NURBS-Python (geomdl) is a free and open-source software and it is licensed under the `MIT License <LICENSE>`_.


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |RTD| image:: https://readthedocs.org/projects/nurbs-python/badge/?version=latest
.. _RTD: https://nurbs-python.readthedocs.io/en/latest/?badge=latest

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
