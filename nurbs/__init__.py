""" Native Python implementation of several **The NURBS Book** algorithms.

**What is NURBS?**

NURBS, namely *Non-Uniform Rational Basis Spline*, is a mathematical model for generation of curves and surfaces in a flexible way. It is a well-accepted industry standard and used as a basis for nearly all of the 3D modeling and CAD/CAM software packages.
Please see the `the related Wikipedia article <https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline>`_ or `The NURBS Book <http://www.springer.com/gp/book/9783642973857>`_, a very nice and informative book written by Dr. Piegl and Dr. Tiller.

**What is the purpose of this package/library?**

Very simple: Implementing the well-known NURBS algorithms in native Python, i.e. without using any converters or wrappers, like `SWIG <http://www.swig.org/>`_ or `Boost.Python <https://github.com/boostorg/python>`_. This approach comes with some advantages in debugging and implementing new algorithms.

Current version of the library doesn't require any additional packages, such as NumPy, so that you can run **NURBS-Python** on a plain Python installation.

The first version of the library was very complicated to use (I developed that version as a class project), so I started developing an alternative, easy-to-use NURBS library with simple data storage functionality, and now, here we are :-)

**Can I request a new feature?**

Of course you can :-) Please feel free to contact me about the NURBS-Python package anytime you want.

* `Github <https://github.com/orbingol>`_ (you can find my email there)
* Twitter: `@orbingol <https://twitter.com/orbingol>`_

.. moduleauthor:: Onur Rauf Bingol

"""

__version__ = "2.2.3"
