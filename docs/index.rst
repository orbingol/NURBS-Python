NURBS-Python v6.x Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |PYPI|_ |ANACONDA|_

|TRAVISCI|_ |APPVEYOR|_ |CIRCLECI|_

NURBS-Python (geomdl) is a object-oriented pure Python B-spline and NURBS library.
It is compatible with Python versions 3.6.x and later.
It supports rational and non-rational B-spline curves, surfaces and volumes.

NURBS-Python (geomdl) provides easy-to-use data structures for storing geometry descriptions
in addition to the fundamental and advanced evaluation algorithms.

This documentation is organized into a couple sections:

* :ref:`introduction`
* :ref:`using`
* :ref:`modules`

.. _introduction:

.. toctree::
    :maxdepth: 2
    :caption: Introduction

    introduction
    citing

.. _using:

.. toctree::
    :maxdepth: 2
    :caption: Using the Library

    install
    basics
    examples_repo
    load_save
    file_formats
    compatibility
    surface_generator
    knot_refinement
    fitting
    visualization
    visualization_splitting
    visualization_export

.. _modules:

.. toctree::
    :maxdepth: 3
    :caption: Modules

    modules
    modules_visualization
    modules_cli
    modules_rhino


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |PYPI| image:: https://img.shields.io/pypi/v/geomdl.svg
.. _PYPI: https://pypi.org/project/geomdl/

.. |ANACONDA| image:: https://anaconda.org/orbingol/geomdl/badges/version.svg
.. _ANACONDA: https://anaconda.org/orbingol/geomdl

.. |TRAVISCI| image:: https://travis-ci.org/orbingol/NURBS-Python.svg?branch=master
.. _TRAVISCI: https://travis-ci.org/orbingol/NURBS-Python

.. |APPVEYOR| image:: https://ci.appveyor.com/api/projects/status/github/orbingol/nurbs-python?branch=master&svg=true
.. _APPVEYOR: https://ci.appveyor.com/project/orbingol/nurbs-python

.. |CIRCLECI| image:: https://circleci.com/gh/orbingol/NURBS-Python/tree/master.svg?style=shield
.. _CIRCLECI: https://circleci.com/gh/orbingol/NURBS-Python/tree/master
