Questions and Answers
^^^^^^^^^^^^^^^^^^^^^

What is NURBS?
==============

NURBS is an acronym for *Non-Uniform Rational Basis Spline* and it represents a mathematical model for generation of
curves and surfaces in a flexible way. It is a well-accepted industry standard and used as a basis for nearly all of
the 3D modeling and CAD/CAM software packages as well as modeling and visualization frameworks.

Please see the `related Wikipedia article <https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline>`_
or `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_, a very nice and informative book written by
Les A. Piegl and Wayne Tiller.

Why NURBS-Python?
=================

The main purpose is implementing the well-known NURBS algorithms in native Python in an organized way and without using
any converters or wrappers, like `SWIG <http://www.swig.org/>`_ or `Boost.Python <https://github.com/boostorg/python>`_.

Although these wrappers are lifesavers by means of converting C++ code to Python when there are too many deadlines,
their support on the source language might be limited or you might need to learn the wrapper's own language to get the
things done in your way. Personally speaking, I had to learn a part of Python's C API to understand how SWIG's typemap
system works. It takes so much time if you are not well-acquainted with the low-level programming or not willing to
learn the inner details of the programming languages (and their interpreters, compilers, etc.).

On the other hand, NURBS-Python is designed to get the things done in a fast way. I used object-oriented approach
throughout the library and tried to make the code look more pythonic and optimized. Since all the code is implemented
in Python natively with no external dependencies, it is possible to use this library in every platform which core python
programming language is supported or integrate into embedded systems/distributions. Using native implementation
approach also allows users to debug and extend the library in a convenient way.

Minimum Requirements
====================

NURBS-Python is tested on Python versions 2.7.13 and 3.5.3+. The core library doesn't depend on any additional packages,
so that you can run it on a plain python installation as well as on a scientific distribution, such as Anaconda.

Issues and Reporting
====================

Contributions to NURBS-Python
-----------------------------

All contributions to NURBS-Python are welcomed. I have posted some
`guidelines for contributing <https://github.com/orbingol/NURBS-Python/blob/master/.github/CONTRIBUTING.md>`_ and
I would be really happy if you could follow these guidelines if you would like to contribute to NURBS-Python.

Bugs and Issues
---------------

Please use the `issue tracker on GitHub <https://github.com/orbingol/NURBS-Python/issues>`_
for reporting bugs and other related issues.

I would be glad if you could provide as much detail as you can for pinpointing the problem. You don't have to provide
a solution for the issue but it would be good if you could provide steps to reproduce the issue. If required,
you can privately share your data by sending me an email or directly upload to the issue tracker.

Please note that the issue tracker is public and all written text and uploaded data will be visible to everybody.

Comments, Questions and Feature Requests
----------------------------------------

You can use the `issue tracker on GitHub <https://github.com/orbingol/NURBS-Python/issues>`_ for your questions and
comments. I would be glad if you could use the appropriate label (``comment``, ``question`` or ``feature request``) to
label your question or comment for convenience.

I also would like to leave the email communication open for NURBS-Python users. The issue tracker is still the primary
method for communication but I know some users don't feel confident asking questions or commenting on a public system.
I will try my best to reply back to your emails as soon as possible.
