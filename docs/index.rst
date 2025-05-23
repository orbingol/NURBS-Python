NURBS-Python v5.x Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|GHACTIONS|_ |PYPI|_ |PYPIDL|_

Welcome to the **NURBS-Python (geomdl) v5.x** documentation!

NURBS-Python (geomdl) is a cross-platform (pure Python), object-oriented B-Spline and NURBS library.
It is compatible with Python versions 2.7.x, 3.4.x and later.
It supports rational and non-rational curves, surfaces and volumes.

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
    q_a
    contributing

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
    modules_rhino
    modules_acis

.. |PYPI| image:: https://img.shields.io/pypi/v/geomdl.svg
.. _PYPI: https://pypi.org/project/geomdl/

.. |PYPIDL| image:: https://img.shields.io/pypi/dm/geomdl.svg
.. _PYPIDL: https://pypi.org/project/geomdl/

.. |GHACTIONS| image:: https://img.shields.io/github/actions/workflow/status/orbingol/NURBS-Python/build.yml
.. _GHACTIONS: https://github.com/orbingol/NURBS-Python/actions/workflows/build.yml
