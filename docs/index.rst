NURBS-Python Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |PYPI|_ |ANACONDA|_

.. note::

    The version of the documentation that you are currently reading belongs to **NURBS-Python v4.x** series.
    Please see the following links, if you are using a different version of NURBS-Python:

    * `NURBS-Python v3.x <http://nurbs-python.readthedocs.io/en/3.x/>`_
    * `NURBS-Python v2.x <http://nurbs-python.readthedocs.io/en/2.x/>`_

    Please note that there might be small API changes between the versions listed above.


Welcome to the NURBS-Python (geomdl) documentation! NURBS-Python contains native Python implementations of several
`The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_ algorithms. These algorithms are used for generating
Non-Uniform Rational B-Spline (NURBS) curves and surfaces.

NURBS-Python also provides a convenient and easy-to-use data structure for storing curve and surface descriptions. All
elements of the provided data structures are documented under :ref:`modules`.

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

.. _using:

.. toctree::
    :maxdepth: 2
    :caption: Using the Library

    install
    examples_repo
    load_save
    file_formats
    compatibility
    surface_generator
    visualization
    visualization_splitting
    visualization_export

.. _modules:

.. toctree::
    :maxdepth: 3
    :caption: Modules

    modules
    modules_visualization
    modules_experimental


NURBS-Python is developed by `Onur Rauf Bingol <https://github.com/orbingol>`_ and all the code released under the
`MIT License <https://github.com/orbingol/NURBS-Python/blob/master/LICENSE>`_.


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |PYPI| image:: https://img.shields.io/pypi/v/geomdl.svg
.. _PYPI: https://pypi.org/project/geomdl/

.. |ANACONDA| image:: https://anaconda.org/orbingol/geomdl/badges/version.svg
.. _ANACONDA: https://anaconda.org/orbingol/geomdl
