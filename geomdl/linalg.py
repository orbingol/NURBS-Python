"""
.. module:: linalg
    :platform: Unix, Windows
    :synopsis: Provides linear algebra utility functions

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import os
import math
from operator import add, sub, mul, truediv
from copy import deepcopy
from functools import reduce
try:
    from functools import lru_cache
except ImportError:
    from .functools_lru_cache import lru_cache
from .base import GeomdlError, GeomdlFloat


def vector_cross(vector1, vector2):
    """ Computes the cross-product of the input vectors.

    :param vector1: input vector 1
    :type vector1: list, tuple
    :param vector2: input vector 2
    :type vector2: list, tuple
    :return: result of the cross product
    :rtype: tuple
    """
    if not 1 < len(vector1) <= 3 or not 1 < len(vector2) <= 3:
        raise GeomdlError("The input vectors should contain 2 or 3 components")

    # Convert 2-D to 3-D, if necessary
    v1 = list(vector1) + [type(vector1[0])(0.0)] if len(vector1) == 2 else vector1
    v2 = list(vector2) + [type(vector2[0])(0.0)] if len(vector2) == 2 else vector2

    # Compute cross product
    return [(v1[1] * v2[2]) - (v1[2] * v2[1]), (v1[2] * v2[0]) - (v1[0] * v2[2]), (v1[0] * v2[1]) - (v1[1] * v2[0])]


def vector_dot(vector1, vector2):
    """ Computes the dot-product of the input vectors.

    :param vector1: input vector 1
    :type vector1: list, tuple
    :param vector2: input vector 2
    :type vector2: list, tuple
    :return: result of the dot product
    """
    # Compute dot product, ref: https://docs.python.org/2/library/itertools.html#recipes
    return sum(map(mul, vector1, vector2))


def vector_multiply(vector_in, scalar):
    """ Multiplies the vector with a scalar value.

    This operation is also called *vector scaling*.

    :param vector_in: vector
    :type vector_in: list, tuple
    :param scalar: scalar value
    :return: updated vector
    :rtype: tuple
    """
    s = type(vector_in[0])(scalar)
    return [mul(v, s) for v in vector_in]


def vector_sum(vector1, vector2):
    """ Sums the vectors.

    This function computes the result of the vector operation :math:`\\overline{v}_{1} + \\overline{v}_{2}`, where
    :math:`\\overline{v}_{1}` is ``vector1`` and :math:`\\overline{v}_{2}`  is ``vector2``.

    :param vector1: vector 1
    :type vector1: list, tuple
    :param vector2: vector 2
    :type vector2: list, tuple
    :return: updated vector
    :rtype: list
    """
    return list(map(add, vector1, vector2))


def vector_normalize(vector_in):
    """ Generates a unit vector from the input.

    :param vector_in: vector to be normalized
    :type vector_in: list, tuple
    :return: the normalized vector (i.e. the unit vector)
    :rtype: list
    """
    # Calculate magnitude of the vector
    magnitude = vector_magnitude(vector_in)

    if magnitude <= 0:
        raise GeomdlError("The magnitude of the vector is zero")

    # Normalize the vector
    vector_out = [truediv(vin, magnitude) for vin in vector_in]

    # Return the normalized vector
    return vector_out


def vector_generate(start_pt, end_pt, **kwargs):
    """ Generates a vector from 2 input points.

    :param start_pt: start point of the vector
    :type start_pt: list, tuple
    :param end_pt: end point of the vector
    :type end_pt: list, tuple
    :return: a vector from start_pt to end_pt
    :rtype: list
    """
    normalize = kwargs.get('normalize', False)
    ret_vec = list(map(sub, end_pt, start_pt))
    return vector_normalize(ret_vec) if normalize else ret_vec


def vector_mean(*args, **kwargs):
    """ Computes the mean (average) of a list of vectors.

    The function computes the arithmetic mean of a list of vectors, which are also organized as a list of
    integers or floating point numbers.

    .. code-block:: python
        :linenos:

        # Create a list of vectors as an example
        vector_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        # Compute mean vector
        mean_vector = vector_mean(*vector_list)

        # Alternative usage example (same as above):
        mean_vector = vector_mean([1, 2, 3], [4, 5, 6], [7, 8, 9])

    :param args: list of vectors
    :type args: list, tuple
    :return: mean vector
    :rtype: list
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    sz = len(args)
    mean_vector = [dt(0.0) for _ in range(len(args[0]))]
    for input_vector in args:
        mean_vector = [a+b for a, b in zip(mean_vector, input_vector)]
    return [truediv(a, sz) for a in mean_vector]


def vector_magnitude(vector_in):
    """ Computes square magnitude of the input vector.

    :param vector_in: input vector
    :type vector_in: list, tuple
    :return: square magnitude of the vector
    :rtype: float
    """
    mag_sq = sum([pow(vin, 2) for vin in vector_in])
    try:
        return mag_sq.sqrt()
    except AttributeError:
        return math.sqrt(mag_sq)


def vector_angle_between(vector1, vector2, **kwargs):
    """ Computes the angle between the two input vectors.

    If the keyword argument ``degrees`` is set to *True*, then the angle will be in degrees. Otherwise, it will be
    in radians. By default, ``degrees`` is set to *True*.

    :param vector1: vector
    :type vector1: list, tuple
    :param vector2: vector
    :type vector2: list, tuple
    :return: angle between the vectors
    """
    degrees = kwargs.get('degrees', True)
    magn1 = vector_magnitude(vector1)
    magn2 = vector_magnitude(vector2)
    acos_val = truediv(vector_dot(vector1, vector2), mul(magn1, magn2))
    angle_radians = math.acos(acos_val)
    return math.degrees(angle_radians) if degrees else angle_radians


def vector_is_zero(vector_in, tol=10e-8):
    """ Checks if the input vector is a zero vector.

    :param vector_in: input vector
    :type vector_in: list, tuple
    :param tol: tolerance value
    :type tol: float
    :return: True if the input vector is zero, False otherwise
    :rtype: bool
    """
    return all([True if abs(vin) < tol else False for vin in vector_in])


def point_translate(point_in, vector_in):
    """ Translates the input points using the input vector.

    :param point_in: input point
    :type point_in: list, tuple
    :param vector_in: input vector
    :type vector_in: list, tuple
    :return: translated point
    :rtype: list
    """
    return list(map(add, point_in, vector_in))


def point_distance(pt1, pt2):
    """ Computes distance between two points.

    :param pt1: point 1
    :type pt1: list, tuple
    :param pt2: point 2
    :type pt2: list, tuple
    :return: distance between input points
    """
    dist_vector = vector_generate(pt1, pt2, normalize=False)
    return vector_magnitude(dist_vector)


def point_mid(pt1, pt2):
    """ Computes the midpoint of the input points.

    :param pt1: point 1
    :type pt1: list, tuple
    :param pt2: point 2
    :type pt2: list, tuple
    :return: midpoint
    :rtype: list
    """
    dist_vector = vector_generate(pt1, pt2, normalize=False)
    half_dist_vector = vector_multiply(dist_vector, GeomdlFloat(0.5))
    return point_translate(pt1, half_dist_vector)


@lru_cache(maxsize=int(os.environ.get('GEOMDL_CACHE_SIZE', '64')))
def matrix_identity(n, **kwargs):
    """ Generates a :math:`N \\times N` identity matrix.

    :param n: size of the matrix
    :type n: int
    :return: identity matrix
    :rtype: list
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    return [[dt(1.0) if i == j else dt(0.0) for i in range(n)] for j in range(n)]


def matrix_pivot(m, sign=False, **kwargs):
    """ Computes the pivot matrix for M, a square matrix.

    This function computes

    * the permutation matrix, :math:`P`
    * the product of M and P, :math:`M \\times P`
    * determinant of P, :math:`det(P)` if ``sign = True``

    :param m: input matrix
    :type m: list, tuple
    :param sign: flag to return the determinant of the permutation matrix, P
    :type sign: bool
    :return: a tuple containing the matrix product of M x P, P and det(P)
    :rtype: tuple
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    mp = deepcopy(m)
    n = len(mp)
    p = matrix_identity(n, dtype=dt)  # permutation matrix
    num_rowswap = 0
    for j in range(0, n):
        row = j
        a_max = dt(0.0)
        for i in range(j, n):
            a_abs = abs(mp[i][j])
            if a_abs > a_max:
                a_max = a_abs
                row = i
        if j != row:
            num_rowswap += 1
            for q in range(0, n):
                # Swap rows
                p[j][q], p[row][q] = p[row][q], p[j][q]
                mp[j][q], mp[row][q] = mp[row][q], mp[j][q]
    if sign:
        return mp, p, math.pow(-1, num_rowswap)
    return mp, p


def matrix_inverse(m, **kwargs):
    """ Computes the inverse of the matrix via LUP decomposition.

    :param m: input matrix
    :type m: list, tuple
    :return: inverse of the matrix
    :rtype: list
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    mp, p = matrix_pivot(m, dtype=dt)
    m_inv = lu_solve(mp, p, dtype=dt)
    return m_inv


def matrix_determinant(m, **kwargs):
    """ Computes the determinant of the square matrix :math:`M` via LUP decomposition.

    :param m: input matrix
    :type m: list, tuple
    :return: determinant of the matrix
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    mp, p, sign = matrix_pivot(m, sign=True, dtype=dt)
    m_l, m_u = lu_decomposition(mp, dtype=dt)
    det = 1.0
    for i in range(len(m)):
        det *= m_l[i][i] * m_u[i][i]
    det *= sign
    return det


def matrix_transpose(m):
    """ Transposes the input matrix.

    The input matrix :math:`m` is a 2-dimensional array.

    :param m: input matrix with dimensions :math:`(n \\times m)`
    :type m: list, tuple
    :return: transpose matrix with dimensions :math:`(m \\times n)`
    :rtype: list
    """
    num_cols = len(m)
    num_rows = len(m[0])
    m_t = []
    for i in range(num_rows):
        temp = []
        for j in range(num_cols):
            temp.append(m[j][i])
        m_t.append(temp)
    return m_t


def matrix_multiply(mat1, mat2, **kwargs):
    """ Matrix multiplication (iterative algorithm).

    The running time of the iterative matrix multiplication algorithm is :math:`O(n^{3})`.

    :param mat1: 1st matrix with dimensions :math:`(n \\times p)`
    :type mat1: list, tuple
    :param mat2: 2nd matrix with dimensions :math:`(p \\times m)`
    :type mat2: list, tuple
    :return: resultant matrix with dimensions :math:`(n \\times m)`
    :rtype: list
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    n = len(mat1)
    p1 = len(mat1[0])
    p2 = len(mat2)
    if p1 != p2:
        raise GeomdlError("Column - row size mismatch")
    try:
        # Matrix - matrix multiplication
        m = len(mat2[0])
        mat3 = [[dt(0.0) for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for k in range(p2):
                    mat3[i][j] += mat1[i][k] * mat2[k][j]
    except TypeError:
        # Matrix - vector multiplication
        mat3 = [dt(0.0) for _ in range(n)]
        for i in range(n):
            for k in range(p2):
                mat3[i] += mat1[i][k] * mat2[k]
    return mat3


def matrix_scalar(m, sc):
    """ Matrix multiplication by a scalar value (iterative algorithm).

    The running time of the iterative matrix multiplication algorithm is :math:`O(n^{2})`.

    :param m: input matrix
    :type m: list, tuple
    :param sc: scalar value
    :return: result matrix
    :rtype: list
    """
    mm = deepcopy(m)
    for i in range(len(m)):
        for j in range(len(m[0])):
            mm[i][j] = m[i][j] * sc
    return mm


def triangle_normal(tri):
    """ Computes the (approximate) normal vector of the input triangle.

    :param tri: triangle object
    :type tri: elements.Triangle
    :return: normal vector of the triangle
    :rtype: tuple
    """
    vec1 = vector_generate(tri.vertices[0].data, tri.vertices[1].data)
    vec2 = vector_generate(tri.vertices[1].data, tri.vertices[2].data)
    return vector_cross(vec1, vec2)


def triangle_center(tri, **kwargs):
    """ Computes the center of mass of the input triangle.

    :param tri: triangle object
    :type tri: elements.Triangle
    :return: center of mass of the triangle
    :rtype: tuple
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    uv = kwargs.get('uv', False)
    data, mid = ([t.uv for t in tri], [dt(0.0) for _ in range(2)]) if uv \
        else (tri.vertices, [dt(0.0) for _ in range(3)])
    for vert in data:
        mid = [m + v for m, v in zip(mid, vert)]
    return (truediv(m, 3) for m in mid)


@lru_cache(maxsize=int(os.environ.get('GEOMDL_CACHE_SIZE', '128')))
def binomial_coefficient(k, i, **kwargs):
    """ Computes the binomial coefficient (denoted by *k choose i*).

    Please see the following website for details: http://mathworld.wolfram.com/BinomialCoefficient.html

    :param k: size of the set of distinct elements
    :type k: int
    :param i: size of the subsets
    :type i: int
    :return: combination of *k* and *i*
    :rtype: float
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    # Special case
    if i > k:
        return dt(0.0)
    # Compute binomial coefficient
    k_fact = math.factorial(k)
    i_fact = math.factorial(i)
    k_i_fact = math.factorial(k - i)
    return dt(truediv(k_fact, (k_i_fact * i_fact)))


def lu_decomposition(matrix_a, **kwargs):
    """ LU-Factorization method using Doolittle's Method for solution of linear systems.

    Decomposes the matrix :math:`A` such that :math:`A = LU`.

    The input matrix is represented by a list or a tuple. The input matrix is **2-dimensional**, i.e. list of lists of
    integers and/or floats.

    :param matrix_a: input matrix (must be a square matrix)
    :type matrix_a: list, tuple
    :return: a tuple containing matrices L and U
    :rtype: tuple
    """
    def _doolittle(ma, dt):
        """ Doolittle's Method for LU-factorization.

        :param ma: Input matrix (must be a square matrix)
        :type ma: list, tuple
        :param dt: data type
        :type dt: type
        :return: a tuple containing matrices (L,U)
        :rtype: tuple
        """
        # Initialize L and U matrices
        mu = [[dt(0.0) for _ in range(len(ma))] for _ in range(len(ma))]
        ml = [[dt(0.0) for _ in range(len(ma))] for _ in range(len(ma))]

        # Doolittle Method
        for i in range(0, len(ma)):
            for k in range(i, len(ma)):
                # Upper triangular (U) matrix
                mu[i][k] = ma[i][k] - sum([ml[i][j] * mu[j][k] for j in range(0, i)])
                # Lower triangular (L) matrix
                if i == k:
                    ml[i][i] = dt(1.0)
                else:
                    ml[k][i] = ma[k][i] - sum([ml[k][j] * mu[j][i] for j in range(0, i)])
                    # Handle zero division error
                    try:
                        ml[k][i] = truediv(ml[k][i], mu[i][i])
                    except ZeroDivisionError:
                        ml[k][i] = dt(0.0)

        return ml, mu

    # Data type, e.g. float, Decimal, etc.
    dt = kwargs.get('dtype', GeomdlFloat)

    # Check if the 2-dimensional input matrix is a square matrix
    q = len(matrix_a)
    for idx, m_a in enumerate(matrix_a):
        if len(m_a) != q:
            raise GeomdlError("The input must be a square matrix. " +
                              "Row " + str(idx + 1) + " has a size of " + str(len(m_a)) + ".")

    # Return L and U matrices
    return _doolittle(matrix_a, dt)


def forward_substitution(matrix_l, matrix_b, **kwargs):
    """ Forward substitution method for the solution of linear systems.

    Solves the equation :math:`Ly = b` using forward substitution method
    where :math:`L` is a lower triangular matrix and :math:`b` is a column matrix.

    :param matrix_l: L, lower triangular matrix
    :type matrix_l: list, tuple
    :param matrix_b: b, column matrix
    :type matrix_b: list, tuple
    :return: y, column matrix
    :rtype: list
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    q = len(matrix_b)
    matrix_y = [dt(0.0) for _ in range(q)]
    matrix_y[0] = truediv(matrix_b[0], matrix_l[0][0])
    for i in range(1, q):
        matrix_y[i] = matrix_b[i] - sum([matrix_l[i][j] * matrix_y[j] for j in range(0, i)])
        matrix_y[i] = truediv(matrix_y[i], matrix_l[i][i])
    return matrix_y


def backward_substitution(matrix_u, matrix_y, **kwargs):
    """ Backward substitution method for the solution of linear systems.

    Solves the equation :math:`Ux = y` using backward substitution method
    where :math:`U` is a upper triangular matrix and :math:`y` is a column matrix.

    :param matrix_u: U, upper triangular matrix
    :type matrix_u: list, tuple
    :param matrix_y: y, column matrix
    :type matrix_y: list, tuple
    :return: x, column matrix
    :rtype: list
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    q = len(matrix_y)
    matrix_x = [dt(0.0) for _ in range(q)]
    matrix_x[q - 1] = truediv(matrix_y[q - 1], matrix_u[q - 1][q - 1])
    for i in range(q - 2, -1, -1):
        matrix_x[i] = matrix_y[i] - sum([matrix_u[i][j] * matrix_x[j] for j in range(i, q)])
        matrix_x[i] = truediv(matrix_x[i], matrix_u[i][i])
    return matrix_x


def lu_solve(matrix_a, b, **kwargs):
    """ Computes the solution to a system of linear equations.

    This function solves :math:`Ax = b` using LU decomposition. :math:`A` is a
    :math:`N \\times N` matrix, :math:`b` is :math:`N \\times M` matrix of
    :math:`M` column vectors. Each column of :math:`x` is a solution for
    corresponding column of :math:`b`.

    :param matrix_a: matrix A
    :type m_l: list
    :param b: matrix of M column vectors
    :type b: list
    :return: x, the solution matrix
    :rtype: list
    """
    # Data type, e.g. float, Decimal, etc.
    dt = kwargs.get('dtype', GeomdlFloat)
    # Variable initialization
    dim = len(b[0])
    num_x = len(b)
    x = [[dt(0.0) for _ in range(dim)] for _ in range(num_x)]

    # LU decomposition
    ml, mu = lu_decomposition(matrix_a, dtype=dt)

    # Solve the system of linear equations
    for i in range(dim):
        bt = [b1[i] for b1 in b]
        y = forward_substitution(ml, bt, dtype=dt)
        xt = backward_substitution(mu, y, dtype=dt)
        for j in range(num_x):
            x[j][i] = xt[j]

    # Return the solution
    return x


def lu_factor(matrix_a, b, **kwargs):
    """ Computes the solution to a system of linear equations with partial pivoting.

    This function solves :math:`Ax = b` using LUP decomposition. :math:`A` is a
    :math:`N \\times N` matrix, :math:`b` is :math:`N \\times M` matrix of
    :math:`M` column vectors. Each column of :math:`x` is a solution for
    corresponding column of :math:`b`.

    :param matrix_a: matrix A
    :type m_l: list
    :param b: matrix of M column vectors
    :type b: list
    :return: x, the solution matrix
    :rtype: list
    """
    # Data type, e.g. float, Decimal, etc.
    dt = kwargs.get('dtype', GeomdlFloat)
    # Variable initialization
    dim = len(b[0])
    num_x = len(b)
    x = [[dt(0.0) for _ in range(dim)] for _ in range(num_x)]

    # LUP decomposition
    mp, p = matrix_pivot(matrix_a, dtype=dt)
    ml, mu = lu_decomposition(mp, dtype=dt)

    # Solve the system of linear equations
    for i in range(dim):
        bt = [b1[i] for b1 in b]
        y = forward_substitution(ml, bt)
        xt = backward_substitution(mu, y)
        for j in range(num_x):
            x[j][i] = xt[j]

    # Return the solution
    return x


def linspace(start, stop, num, **kwargs):
    """ Returns a list of evenly spaced numbers over a specified interval.

    Inspired from Numpy's linspace function: https://github.com/numpy/numpy/blob/master/numpy/core/function_base.py

    :param start: starting value
    :param stop: end value
    :param num: number of samples to generate
    :type num: int
    :param dtype: data type
    :type dtype: type
    :return: a list of equally spaced numbers
    :rtype: list
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    start = dt(start)
    stop = dt(stop)
    if abs(start - stop) <= 10e-8:
        return [start]
    num = int(num)
    if num > 1:
        div = num - 1
        delta = stop - start
        return [start + truediv(x * delta, div) for x in range(num)]
    return [start]


def frange(start, stop, step=1.0, **kwargs):
    """ Implementation of Python's ``range()`` function which works non-int numeric types.

    Reference to this implementation: https://stackoverflow.com/a/36091634

    :param start: start value
    :param stop: end value
    :param step: increment
    :return: Python generator instance
    :rtype: generator
    """
    dt = kwargs.get('dtype', GeomdlFloat)
    i = dt(0.0)
    x = dt(start)  # Prevent yielding integers.
    x0 = x
    epsilon = truediv(step, 2)
    yield x  # always yield first value
    while x + epsilon < stop:
        i += dt(1.0)
        x = x0 + i * step
        yield x
    if stop > x:
        yield stop  # for yielding last value of the knot vector if the step is a large value, like 0.1


def convex_hull(points):
    """ Returns points on convex hull in counterclockwise order according to Graham's scan algorithm.

    Reference: https://gist.github.com/arthur-e/5cf52962341310f438e96c1f3c3398b8

    .. note:: This implementation only works in 2-dimensional space.

    :param points: list of 2-dimensional points
    :type points: list, tuple
    :return: convex hull of the input points
    :rtype: list
    """
    turn_left, turn_right, turn_none = (1, -1, 0)

    def cmp(a, b):
        return (a > b) - (a < b)

    def turn(p, q, r):
        return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

    def keep_left(hull, r):
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != turn_left:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull

    points = sorted(points)
    l = reduce(keep_left, points, [])
    u = reduce(keep_left, reversed(points), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l


def is_left(point0, point1, point2):
    """ Tests if a point is Left|On|Right of an infinite line.

    Ported from the C++ version: on http://geomalgorithms.com/a03-_inclusion.html

    .. note:: This implementation only works in 2-dimensional space.

    :param point0: Point P0
    :param point1: Point P1
    :param point2: Point P2
    :return:
        >0 for P2 left of the line through P0 and P1
        =0 for P2 on the line
        <0 for P2 right of the line
    """
    return ((point1[0] - point0[0]) * (point2[1] - point0[1])) - ((point2[0] - point0[0]) * (point1[1] - point0[1]))


def wn_poly(point, vertices):
    """ Winding number test for a point in a polygon.

    Ported from the C++ version: http://geomalgorithms.com/a03-_inclusion.html

    .. note:: This implementation only works in 2-dimensional space.

    :param point: point to be tested
    :type point: list, tuple
    :param vertices: vertex points of a polygon vertices[n+1] with vertices[n] = vertices[0]
    :type vertices: list, tuple
    :return: True if the point is inside the input polygon, False otherwise
    :rtype: bool
    """
    wn = 0  # the winding number counter

    v_size = len(vertices) - 1
    # loop through all edges of the polygon
    for i in range(v_size):  # edge from V[i] to V[i+1]
        if vertices[i][1] <= point[1]:  # start y <= P.y
            if vertices[i + 1][1] > point[1]:  # an upward crossing
                if is_left(vertices[i], vertices[i + 1], point) > 0:  # P left of edge
                    wn += 1  # have a valid up intersect
        else:  # start y > P.y (no test needed)
            if vertices[i + 1][1] <= point[1]:  # a downward crossing
                if is_left(vertices[i], vertices[i + 1], point) < 0:  # P right of edge
                    wn -= 1  # have a valid down intersect
    # return wn
    return bool(wn)
