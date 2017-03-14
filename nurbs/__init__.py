""" Native Python implementation of several **The NURBS Book** algorithms.

**What is NURBS?**

NURBS, namely *Non-Uniform Rational Basis Spline*, is a mathematical model for generation of curves and surfaces in a flexible way. It is a well-accepted industry standard and used as a basis for nearly all of the 3D modeling and CAD/CAM software packages.
Please see the `the related Wikipedia article <https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline>`_ or `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_, a very nice and informative book written by Dr. Piegl and Dr. Tiller.

**What is the purpose of this package/library?**

As you might have noticed, you have a huge list of alternative NURBS implementations in various programming languages. Some of them are free, some of them are not and some of them have a huge set of functions, but nearly none of them are developed in native Python.

Considering this situation, I started coding native Python implementation of a NURBS library for M E 625 Surface Modeling class project, offered in Spring 2015 semester by Dr. James Oliver at Iowa State University. My purpose was developing the package without using any wrappers, like `SWIG <http://www.swig.org/>`_ or `Boost.Python <https://github.com/boostorg/python>`_. I also have SWIG- and Boost.Python-wrapped versions of a custom C++ NURBS library, but I find them hard to debug, compile and explain how they work.

The first version of the library was very complicated to use, so I started developing an alternative, easy-to-use NURBS library with simple data storage functionality, and now, here we are :-)

**Can I request a new feature?**

Of course you can :-) Please feel free to contact me about the NURBS-Python package anytime you want.

* `Github <https://github.com/orbingol>`_ (you can find my email there)
* Twitter: `@orbingol <https://twitter.com/orbingol>`_

.. moduleauthor:: Onur Rauf Bingol

"""

__version__ = "2.2.2"
