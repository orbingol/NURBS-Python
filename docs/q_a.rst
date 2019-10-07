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

NURBS-Python started as a final project for *M E 625 Surface Modeling* course offered in 2016 Spring semester at
Iowa State University. The main purpose of the project was development of a free and open-source, object-oriented,
pure Python NURBS library and releasing it on the public domain. As an added challenge to the project, everything
was developed using Python Standard Library but no other external modules.

In years, NURBS-Python has grown up to a self-contained and extensible general-purpose pure Python spline library with
support for various computational geometry and linear algebra algorithms. Apart from the computational side, user
experience was also improved by introduction of visualization and CAD exchange modules.

NURBS-Python is a user-friendly library, regardless of the mathematical complexity of the splines.
To give a head start, it comes with 40+ examples for various use cases.
It also provides several extension modules for

* Using the library directly from the command-line
* Generating common spline shapes
* Rhino .3dm file import/export support
* ACIS .sat file import support

Moreover, NURBS-Python and its extensions are free and open-source projects distributed under the MIT license.

NURBS-Python is **not** *an another NURBS library* but it is mostly considered as one of its kind. Please see the
:doc:`Motivation <introduction>` page for more details.

Why two packages on PyPI?
=========================

Prior to NURBS-Python v4.0.0, the PyPI project name was `NURBS-Python <https://pypi.org/project/NURBS-Python/>`_.
The latest version of this package is v3.9.0 which is an alias for the `geomdl <https://pypi.org/project/geomdl/>`_
package. To get the latest features and bug fixes, please use `geomdl <https://pypi.org/project/geomdl/>`_ package
and update whenever a new version is released. The simplest way to check if you are using the latest version is

.. code-block:: console

    $ pip list --outdated

Minimum Requirements
====================

NURBS-Python (geomdl) is tested with Python versions 2.7.x, 3.4.x and higher.

Help and Support
================

Please join the `email list <https://groups.google.com/forum/#!forum/nurbs-python>`_ on Google Groups.
It is open for NURBS-Python users to ask questions, request new features and submit any other comments
you may have.

Alternatively, you may send an email to ``nurbs-python@googlegroups.com``.

Issues and Reporting
====================

Bugs and Feature Requests
-------------------------

NURBS-Python project uses the `issue tracker on GitHub <https://github.com/orbingol/NURBS-Python/issues>`_ for
reporting bugs and requesting for a new feature. Please use the provided templates on GitHub.

Contributions
-------------

All contributions to NURBS-Python are welcomed and I appreciate your time and efforts in advance. I have posted
some `guidelines for contributing <https://github.com/orbingol/NURBS-Python/blob/master/.github/CONTRIBUTING.md>`_
and I would be really happy if you could follow these guidelines if you would like to contribute to NURBS-Python.

It is suggested to open `a new ticket <https://github.com/orbingol/NURBS-Python/issues/new>`_ GitHub to discuss what
you would like to fix or add as a new feature, as it may already been fixed/implemented in some of the development
branches.

How can I add a new feature?
============================

The library is designed to be extensible in mind. It provides a set of :doc:`abstract classes <module_abstract>`
for creating new geometry types. All classes use :doc:`evaluators <module_evaluators>` which contain the evaluation
algorithms. Evaluator classes can be extended for new type of algorithms. Please refer to ``BSpline`` and ``NURBS``
modules for implementation examples. It would be also a good idea to refer to the constructors of the abstract
classes for more details.

Why doesn't NURBS-Python have XYZ feature?
==========================================

NURBS-Python tries to keep the geometric operations on the parametric space without any conversion to other
representations. This approach makes some operations and queries hard to implement. Keeping NURBS-Python independent of
libraries that require compilation caused including implementations some well-known geometric queries and computations,
as well as a simple linear algebra module. However, **the main purpose is providing a base for NURBS data and fundamental
operations while keeping the external dependencies at minimum**. It is users' choice to extend the library and add new
more advanced features (e.g. intersection computations) or capabilities (e.g. a new file format import/export support).

All advanced features should be packaged separately. If you are developing a feature to replace an existing feature,
it might be a good idea to package it separately.

NURBS-Python may seem to keep very high standards by means of accepting contributions. For instance, if you implement a
feature applicable to curves but not surfaces and volumes, such a pull request won't be accepted till you add that
feature to surfaces and volumes. Similarly, if you change a single module and/or the function you use most frequently,
but that change is affecting the library as a whole, your pull request will be put on hold.

If you are not interested in such level of contributions, it is suggested to create a separate module and add ``geomdl``
as its dependency. If you create a module which uses ``geomdl``, please let the developers know via emailing
``nurbs-python@googlegroups.com`` and you may be credited as a contributor.

Documentation references to the text books
==========================================

NURBS-Python contains implementations of several algorithms and equations from the references stated in the
:doc:`Introduction <introduction>` section. Please be aware that there is always a difference between an algorithm and
an implementation. Depending on the function/method documentation you are looking, it might be an implementation of
an algorithm, an equation, a set of equations or the concept/the idea discussed in the given page range.

Why doesn't NURBS-Python follow the algorithms?
===============================================

Actually, NURBS-Python does follow the algorithms pretty much all the time. However, as stated above, the implementation
that you are looking at might not belong to an algorithm, but an equation or a concept.

NURBS-Python API changes
========================

Please refer to `CHANGELOG <https://github.com/orbingol/NURBS-Python/blob/master/CHANGELOG.md>`_ file for details.

Plotly v4 API changes
=====================

As of Plotly release v4.0, the package ``plotly`` is now an offline-only package (which is all fine for ``geomdl``).
However, The online functionality, e.g. uploading charts to Plotly servers, has been moved to ``chart-studio`` package.

To install Plotly v4.x, please follow the instructions below or refer to
`Plotly website <https://plot.ly/python/v4-migration/>`_:

Using pip
---------

.. code-block:: console

    $ pip install plotly chart-studio

Using conda
-----------

.. code-block:: console

    $ conda install -c plotly plotly chart-studio

Activating online mode
----------------------

``geomdl`` comes with the offline functionality by default. It also supports the online functionality as an option.
A keyword argument ``online`` should be passed while initializing :class:`.VisPlotly.VisConfig` class.

.. code-block:: python

    from geomdl.visualization import VisPlotly

    # Enable Plotly online functionality
    vconf = VisPlotly.VisConfig(online=True)

    # Alternatively, the keyword argument may be used during the initialization of the visualization class
    vmodule = VisPlotly.VisSurface(online=True)

    # Update a hypothetical "surf" object which corresponds to a B-spline or NURBS surface
    surf.vis = vmodule
