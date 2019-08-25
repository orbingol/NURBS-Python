#
# doubledouble.py - Double-double aritmetic for Python
#
# https://github.com/sukop/doubledouble
#
# doubledouble.py is a library for computing with unevaluated sums of two double
# precision floating-point numbers. The so-called "double-double arithmetic"
# enables operations with at least 106-bit significand (2x53-bit) and 11-bit
# exponent, compared to 113-bit and 15-bit, respectively, of the IEEE 754-2008
# quadruple precision floating-point format.
#
# References:
# Dekker, T. J. (1971). A Floating-Point Technique for Extending the Available
# Precision. Numerische Mathematik 18, 224-242.
# Knuth, D. E. (1997). The Art of Computer Programming, Volume 2: Seminumerical
# Algorithms, 4.2.2. Accuracy of Floating Point Arithmetic.
# Hida, Y., Li, X. S., Bailey, D. H. (2000). Quad-Double Arithmetic: Algorithms,
# Implementation, and Application. Technical Report LBNL-46996.
#
# Install with `pip install doubledouble`.
#
# Copyright (c) 2017, Juraj Sukop
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

from __future__ import division
from math import exp, frexp, ldexp, log, sqrt
from numbers import Integral

def _two_sum_quick(x, y):
    r = x + y
    e = y - (r - x)
    return r, e

def _two_sum(x, y):
    r = x + y
    t = r - x
    e = (x - (r - t)) + (y - t)
    return r, e

def _two_difference(x, y):
    r = x - y
    t = r - x
    e = (x - (r - t)) - (y + t)
    return r, e

try:
    from math import fma
    def _two_product(x, y):
        r = x*y
        e = fma(x, y, -r)
        return r, e
except ImportError:
    def _two_product(x, y):
        u = x*134217729.0 # 0x8000001.0 (equivalent to shift add significand)
        v = y*134217729.0
        s = u - (u - x)
        t = v - (v - y)
        f = x - s
        g = y - t
        r = x*y
        e = ((s*t - r) + s*g + f*t) + f*g
        return r, e

class DoubleDouble(object):

    __slots__ = 'x', 'y'

    def __init__(self, x, y=0.0):
        self.x, self.y = float(x), float(y)

    def __copy__(self):
        return self

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, DoubleDouble):
            return self.x == other and self.y == 0.0
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        if not isinstance(other, DoubleDouble):
            return self.x != other or self.y != 0.0
        return self.x != other.x or self.y != other.y

    def __lt__(self, other):
        if not isinstance(other, DoubleDouble):
            return self.x < other or self.x == other and self.y < 0.0
        return self.x < other.x or self.x == other.x and self.y < other.y

    def __gt__(self, other):
        if not isinstance(other, DoubleDouble):
            return self.x > other or self.x == other and self.y > 0.0
        return self.x > other.x or self.x == other.x and self.y > other.y

    def __le__(self, other):
        if not isinstance(other, DoubleDouble):
            return self.x < other or self.x == other and self.y <= 0.0
        return self.x < other.x or self.x == other.x and self.y <= other.y

    def __ge__(self, other):
        if not isinstance(other, DoubleDouble):
            return self.x > other or self.x == other and self.y >= 0.0
        return self.x > other.x or self.x == other.x and self.y >= other.y

    def __bool__(self):
        return self.x != 0.0 or self.y != 0.0

    __nonzero__ = __bool__

    def __pos__(self):
        return self

    def __neg__(self):
        return DoubleDouble(-self.x, -self.y)

    def __abs__(self):
        if self.x < 0.0:
            return -self
        return self

    def __add__(self, other):
        if not isinstance(other, DoubleDouble):
            return other + self
        r, e = _two_sum(self.x, other.x)
        e += self.y + other.y
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    def __radd__(self, other):
        r, e = _two_sum(other, self.x)
        e += self.y
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    def __sub__(self, other):
        if not isinstance(other, DoubleDouble):
            return -other + self
        r, e = _two_difference(self.x, other.x)
        e += self.y - other.y
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    def __rsub__(self, other):
        r, e = _two_difference(other, self.x)
        e -= self.y
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    def __mul__(self, other):
        if not isinstance(other, DoubleDouble):
            return other*self
        r, e = _two_product(self.x, other.x)
        e += self.x*other.y + self.y*other.x
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    def __rmul__(self, other):
        r, e = _two_product(other, self.x)
        e += other*self.y
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    def __truediv__(self, other):
        if not isinstance(other, DoubleDouble):
            other = DoubleDouble(other)
        r = self.x/other.x
        s, f = _two_product(r, other.x)
        e = (self.x - s - f + self.y - r*other.y)/other.x
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    def __rtruediv__(self, other):
        r = other/self.x
        s, f = _two_product(r, self.x)
        e = (other - s - f - r*self.y)/self.x
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    __div__ = __truediv__

    __rdiv__ = __rtruediv__

    def __pow__(self, other):
        if isinstance(other, Integral):
            return self.power(other)
        return (self.log()*other).exp()

    def __rpow__(self, other):
        return DoubleDouble(other)**self

    def power(self, n):
        b, i = self, abs(n)
        r = _one
        while True:
            if i & 1 == 1:
                r *= b
            if i <= 1:
                break
            i >>= 1
            b *= b
        if n < 0:
            return 1.0/r
        return r

    def sqrt(self):
        if self.x == 0.0:
            return _zero
        r = sqrt(self.x)
        s, f = _two_product(r, r)
        e = (self.x - s - f + self.y)*0.5/r
        r, e = _two_sum_quick(r, e)
        return DoubleDouble(r, e)

    def root(self, n):
        if self.x < 0.0 and n%2 == 0:
            raise ValueError
        if self.x == 0.0:
            return _zero
        r = DoubleDouble(exp(log(abs(self.x))/n))
        if self.x < 0.0:
            r = -r
        w = r.power(n)
        u = (n - 1)*w + (n + 1)*self
        v = (n + 1)*w + (n - 1)*self
        return r*(u/v)

    def exp(self):
        n = int(round(self.x))
        x = self - n
        # the Pade approximate for e^x: R[L=12/M=12] = (u/v), expressed using Horner's rule
        u = (((((((((((x +
            156)*x + 12012)*x +
            600600)*x + 21621600)*x +
            588107520)*x + 12350257920)*x +
            201132771840)*x + 2514159648000)*x +
            23465490048000)*x + 154872234316800)*x +
            647647525324800)*x + 1295295050649600
        v = (((((((((((x -
            156)*x + 12012)*x -
            600600)*x + 21621600)*x -
            588107520)*x + 12350257920)*x -
            201132771840)*x + 2514159648000)*x -
            23465490048000)*x + 154872234316800)*x -
            647647525324800)*x + 1295295050649600
        return e.power(n)*(u/v)

    def log(self):
        r = DoubleDouble(log(self.x))
        u = r.exp()
        r -= 2.0*(u - self)/(u + self)
        return r

    def ldexp(self, n):
        r = ldexp(self.x, n)
        e = ldexp(self.y, n)
        return DoubleDouble(r, e)

    def frexp(self):
        r, n = frexp(self.x)
        e = self.y/2**n
        return DoubleDouble(r, e), n

    def __float__(self):
        return self.x

    def __str__(self):
        return str(float(self))

    def __repr__(self):
        if self.y < 0.0:
            return '%s(%r - %r)' % (self.__class__.__name__, self.x, -self.y)
        return '%s(%r + %r)' % (self.__class__.__name__, self.x, self.y)

    def hex(self):
        if self.y < 0.0:
            return '(%s - %s)' % (self.x.hex(), (-self.y).hex())
        return '(%s + %s)' % (self.x.hex(), self.y.hex())

_zero, _one = DoubleDouble(0.0), DoubleDouble(1.0)

e, ln2, pi = \
    DoubleDouble(2.718281828459045, 1.4456468917292502e-16), \
    DoubleDouble(0.6931471805599453, 2.3190468138462996e-17), \
    DoubleDouble(3.141592653589793, 1.2246467991473532e-16)
