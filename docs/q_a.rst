Questions and Answers
^^^^^^^^^^^^^^^^^^^^^

What is NURBS?
==============

NURBS is an acronym for *Non-Uniform Rational Basis Spline* and it represents a mathematical model for generation of
geometric shapes in a flexible way. It is a well-accepted industry standard and used as a basis for nearly all of
the 3-dimensional modeling and CAD/CAM software packages as well as modeling and visualization frameworks.

Although the mathematical theory of behind the splines dates back to early 1900s, the spline theory in the way we know
is coined by `Isaac (Iso) Schoenberg <http://pages.cs.wisc.edu/~deboor/hat/people/schoenberg.html>`_ and developed
further by various researchers around the world.

The following books are recommended for individuals who prefer to investigate the technical details of NURBS:

* `A Practical Guide to Splines <https://www.springer.com/us/book/9780387953663>`_
* `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_
* `Geometric Modeling with Splines: An Introduction <https://www.crcpress.com/p/book/9781568811376>`_

Why NURBS-Python?
=================

NURBS-Python started as a final project for *M E 625 Surface Modeling* course offered in 2016 Spring semester at Iowa
State University. The main purpose of the project was development of a free and open-source, object-oriented, pure
Python NURBS library and releasing it on the public domain. As an added challenge to the project, everything was
developed using Python Standard Library but no other external modules.

In years, NURBS-Python has grown up to a self-contained and extensible general-purpose pure Python spline library with
support for various computational geometry and linear algebra algorithms. Apart from the computational side, user
experience was also improved by introduction of visualization and CAD exchange modules.

NURBS-Python is a user-friendly library, regardless of the mathematical complexity of the splines. To give a head start,
it comes with 40+ examples for various use cases. It also provides several extension modules for

* Using the library directly from the command-line (useful for non-Python and automated systems)
* Generating common spline shapes
* Rhino .3dm file import/export support

Moreover, NURBS-Python and its extensions are free and open-source projects distributed under the MIT license.

NURBS-Python is **not** *an another NURBS library* but it is mostly considered as one of its kind. Please see the
:doc:`Motivation <introduction>` page for more details.

Why two packages on PyPI?
=========================

Prior to NURBS-Python v4.0.0, the PyPI project name was `NURBS-Python <https://pypi.org/project/NURBS-Python/>`_. The
latest version of this package is v3.9.0 which is an alias for the `geomdl <https://pypi.org/project/geomdl/>`_ package.
To get the latest features and bug fixes, please use `geomdl <https://pypi.org/project/geomdl/>`_ package and update
whenever a new version is released. The simplest way to check if you are using the latest version is

.. code-block:: console

    $ pip list --outdated

Minimum Requirements
====================

NURBS-Python is tested on Python versions 2.7.x and 3.4.x+. The core library does not depend on any additional packages
or require any compilation steps; therefore, you can run it on a plain python installation as well as on a distribution,
such as Anaconda.

Since Python `2.7.x <https://www.python.org/dev/peps/pep-0373/>`_ and `v3.4.x <https://www.python.org/dev/peps/pep-0429/>`_
are reaching their end-of-life very soon, NURBS-Python project will only support Python 3.5+ starting with v6.0.0.

Please see the following page for more details: https://python3statement.org/

Help and Support
================

Please join the `email list <https://groups.google.com/forum/#!forum/nurbs-python>`_ on Google Groups. It is open for
NURBS-Python users to ask questions, request new features and submit any other comments you may have.

Issues and Reporting
====================

Bugs and Feature Requests
-------------------------

Please use the `issue tracker on GitHub <https://github.com/orbingol/NURBS-Python/issues>`_ for bug reporting and
requesting a new feature.

Contributions
-------------

All contributions to NURBS-Python are welcomed and I appreciate your time and efforts in advance. I have posted some
`guidelines for contributing <https://github.com/orbingol/NURBS-Python/blob/master/.github/CONTRIBUTING.md>`_ and
I would be really happy if you could follow these guidelines if you would like to contribute to NURBS-Python.

API Changes
===========

I try to keep the API (name and location of the functions, class fields and member functions) backward-compatible
during minor version upgrades. During major version upgrades, the API change might not be backward-compatible.
However, these changes will be kept minor and therefore, the users can update their code to the new version without
much hassle. All of these changes, regardless of minor or major version upgrades, will be announced on the CHANGELOG
file.

Installation Issues on Mac OS
=============================

Installation of ``six`` package from PyPI might cause some issues on some Mac OS versions. Six is a Python 2 to 3
compatibility library and allows NURBS-Python to run under both Python 2 and Python 3. If you are having issues regarding
to installation of ``six`` package on Mac OS, please use the following command to install NURBS-Python (geomdl):

.. code-block:: console

    $ pip install geomdl --ignore-installed six

and to upgrade NURBS-Python (geomdl):

.. code-block:: console

    $ pip install geomdl --upgrade --ignore-installed six

or alternatively, you can use :doc:`conda <install>`.

Please refer to the following issue on pip issue tracker for more details: https://github.com/pypa/pip/issues/3165
