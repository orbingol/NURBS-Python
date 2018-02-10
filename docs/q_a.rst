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
system works. It takes so much time when you are not well-acquainted with the low-level programming or not willing to
learn a programming language's internals.

On the other hand, NURBS-Python is designed to get the things done in a fast way. I used object-oriented approach
throughout the library and tried to make the code look more pythonic and optimized. Since all the code is implemented
in Python natively with no external dependencies, it is possible to use this library in every platform which core python
programming language is supported or integrate into embedded systems/distributions. Using native implementation
approach also allows users to debug and extend the library in a convenient way.

Minimum Requirements
====================

NURBS-Python is tested on Python versions 2.7.13 and 3.5.3+. It doesn't require any additional packages, such as NumPy,
so that you can run it even on a plain Python installation as well as on a scientific distribution, such as Anaconda.

.. note::

    Please use the issue tracker on GitHub to report bugs. If you have any questions and/or comments,
    please feel free to email the author.
