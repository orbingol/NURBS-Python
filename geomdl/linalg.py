"""
.. module:: linalg
    :platform: Unix, Windows
    :synopsis: Provides linear algebra utility functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import os
import math
from typing import cast, Sequence, List, Tuple, Generator
from . import _linalg
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


def linspace(start, stop, num, decimals=18):
    # type: (float, float, int, int) -> List[float]
    """ Returns a list of evenly spaced numbers over a specified interval.

    Inspired from Numpy's linspace function: https://github.com/numpy/numpy/blob/master/numpy/core/function_base.py

    :param start: starting value
    :type start: float
    :param stop: end value
    :type stop: float
    :param num: number of samples to generate
    :type num: int
    :param decimals: number of significands
    :type decimals: int
    :return: a list of equally spaced numbers
    :rtype: list
    """
    start = float(start)
    stop = float(stop)
    if abs(start - stop) <= 10e-8:
        return [start]
    num = int(num)
    if num > 1:
        div = num - 1
        delta = stop - start
        return [float(("{:." + str(decimals) + "f}").format((start + (float(x) * float(delta) / float(div)))))
                for x in range(num)]
    return [float(("{:." + str(decimals) + "f}").format(start))]


def vector_cross(vector1, vector2):
    # type: (Sequence[float], Sequence[float]) -> List[float]
    """ Computes the cross-product of the input vectors.

    :param vector1: input vector 1
    :type vector1: list, tuple
    :param vector2: input vector 2
    :type vector2: list, tuple
    :return: result of the cross product
    :rtype: tuple
    """
    try:
        if vector1 is None or len(vector1) == 0 or vector2 is None or len(vector2) == 0:
            raise ValueError("Input vectors cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Input must be a list or tuple")
    except Exception:
        raise

    if not 1 < len(vector1) <= 3 or not 1 < len(vector2) <= 3:
        raise ValueError("The input vectors should contain 2 or 3 elements")

    # Convert 2-D to 3-D, if necessary
    if len(vector1) == 2:
        v1 = cast(Sequence, [float(v) for v in vector1] + [0.0])
    else:
        v1 = vector1

    if len(vector2) == 2:
        v2 = cast(Sequence, [float(v) for v in vector2] + [0.0])
    else:
        v2 = vector2

    # Compute cross product
    vector_out = [(v1[1] * v2[2]) - (v1[2] * v2[1]),
                  (v1[2] * v2[0]) - (v1[0] * v2[2]),
                  (v1[0] * v2[1]) - (v1[1] * v2[0])]

    # Return the cross product of the input vectors
    return vector_out


def vector_dot(vector1, vector2):
    # type: (Sequence[float], Sequence[float]) -> float
    """ Computes the dot-product of the input vectors.

    :param vector1: input vector 1
    :type vector1: list, tuple
    :param vector2: input vector 2
    :type vector2: list, tuple
    :return: result of the dot product
    :rtype: float
    """
    try:
        if vector1 is None or len(vector1) == 0 or vector2 is None or len(vector2) == 0:
            raise ValueError("Input vectors cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Input must be a list or tuple")
    except Exception:
        raise

    # Compute dot product
    prod = 0.0
    for v1, v2 in zip(vector1, vector2):
        prod += v1 * v2

    # Return the dot product of the input vectors
    return prod


def vector_multiply(vector_in, scalar):
    # type: (Sequence[float], float) -> List[float]
    """ Multiplies the vector with a scalar value.

    This operation is also called *vector scaling*.

    :param vector_in: vector
    :type vector_in: list, tuple
    :param scalar: scalar value
    :type scalar: int, float
    :return: updated vector
    :rtype: tuple
    """
    scaled_vector = [v * scalar for v in vector_in]
    return scaled_vector


def vector_sum(vector1, vector2, coeff=1.0):
    # type: (Sequence[float], Sequence[float], float) -> List[float]
    """ Sums the vectors.

    This function computes the result of the vector operation :math:`\\overline{v}_{1} + c * \\overline{v}_{2}`, where
    :math:`\\overline{v}_{1}` is ``vector1``, :math:`\\overline{v}_{2}`  is ``vector2`` and :math:`c` is ``coeff``.

    :param vector1: vector 1
    :type vector1: list, tuple
    :param vector2: vector 2
    :type vector2: list, tuple
    :param coeff: multiplier for vector 2
    :type coeff: float
    :return: updated vector
    :rtype: list
    """
    summed_vector = [v1 + (coeff * v2) for v1, v2 in zip(vector1, vector2)]
    return summed_vector


def vector_normalize(vector_in, decimals=18):
    # type: (Sequence[float], int) -> List[float]
    """ Generates a unit vector from the input.

    :param vector_in: vector to be normalized
    :type vector_in: list, tuple
    :param decimals: number of significands
    :type decimals: int
    :return: the normalized vector (i.e. the unit vector)
    :rtype: list
    """
    try:
        if vector_in is None or len(vector_in) == 0:
            raise ValueError("Input vector cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Input must be a list or tuple")
    except Exception:
        raise

    # Calculate magnitude of the vector
    magnitude = vector_magnitude(vector_in)

    # Normalize the vector
    if magnitude > 0:
        vector_out = []
        for vin in vector_in:
            vector_out.append(vin / magnitude)

        # Return the normalized vector and consider the number of significands
        return [float(("{:." + str(decimals) + "f}").format(vout)) for vout in vector_out]
    else:
        raise ValueError("The magnitude of the vector is zero")


def vector_generate(start_pt, end_pt, normalize=False):
    # type: (Sequence[float], Sequence[float], bool) -> List[float]
    """ Generates a vector from 2 input points.

    :param start_pt: start point of the vector
    :type start_pt: list, tuple
    :param end_pt: end point of the vector
    :type end_pt: list, tuple
    :param normalize: if True, the generated vector is normalized
    :type normalize: bool
    :return: a vector from start_pt to end_pt
    :rtype: list
    """
    try:
        if start_pt is None or len(start_pt) == 0 or end_pt is None or len(end_pt) == 0:
            raise ValueError("Input points cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Input must be a list or tuple")
    except Exception:
        raise

    ret_vec = []
    for sp, ep in zip(start_pt, end_pt):
        ret_vec.append(ep - sp)

    if normalize:
        ret_vec = vector_normalize(ret_vec)
    return ret_vec


def vector_mean(*args):
    # type: (*Sequence[float]) -> List[float]
    """ Computes the mean (average) of a list of vectors.

    The function computes the arithmetic mean of a list of vectors, which are also organized as a list of
    integers or floating point numbers.

    .. code-block:: python
        :linenos:

        # Import geomdl.utilities module
        from geomdl import utilities

        # Create a list of vectors as an example
        vector_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        # Compute mean vector
        mean_vector = utilities.vector_mean(*vector_list)

        # Alternative usage example (same as above):
        mean_vector = utilities.vector_mean([1, 2, 3], [4, 5, 6], [7, 8, 9])

    :param args: list of vectors
    :type args: list, tuple
    :return: mean vector
    :rtype: list
    """
    sz = len(args)
    mean_vector = [0.0 for _ in range(len(args[0]))]
    for input_vector in args:
        mean_vector = [a+b for a, b in zip(mean_vector, input_vector)]
    mean_vector = [a / sz for a in mean_vector]
    return mean_vector


def vector_magnitude(vector_in):
    # type: (Sequence[float]) -> float
    """ Computes the magnitude of the input vector.

    :param vector_in: input vector
    :type vector_in: list, tuple
    :return: magnitude of the vector
    :rtype: float
    """
    sq_sum = 0.0
    for vin in vector_in:
        sq_sum += vin**2
    return math.sqrt(sq_sum)


def vector_angle_between(vector1, vector2, **kwargs):
    # type: (Sequence[float], Sequence[float], **bool) -> float
    """ Computes the angle between the two input vectors.

    If the keyword argument ``degrees`` is set to *True*, then the angle will be in degrees. Otherwise, it will be
    in radians. By default, ``degrees`` is set to *True*.

    :param vector1: vector
    :type vector1: list, tuple
    :param vector2: vector
    :type vector2: list, tuple
    :return: angle between the vectors
    :rtype: float
    """
    degrees = kwargs.get('degrees', True)
    magn1 = vector_magnitude(vector1)
    magn2 = vector_magnitude(vector2)
    acos_val = vector_dot(vector1, vector2) / (magn1 * magn2)
    angle_radians = math.acos(acos_val)
    if degrees:
        return math.degrees(angle_radians)
    else:
        return angle_radians


def vector_is_zero(vector_in, tol=10e-8):
    # type: (Sequence[float], float) -> bool
    """ Checks if the input vector is a zero vector.

    :param vector_in: input vector
    :type vector_in: list, tuple
    :param tol: tolerance value
    :type tol: float
    :return: True if the input vector is zero, False otherwise
    :rtype: bool
    """
    if not isinstance(vector_in, (list, tuple)):
        raise TypeError("Input vector must be a list or a tuple")

    res = [False for _ in range(len(vector_in))]
    for idx in range(len(vector_in)):
        if abs(vector_in[idx]) < tol:
            res[idx] = True
    return all(res)


def point_translate(point_in, vector_in):
    # type: (Sequence[float], Sequence[float]) -> List[float]
    """ Translates the input points using the input vector.

    :param point_in: input point
    :type point_in: list, tuple
    :param vector_in: input vector
    :type vector_in: list, tuple
    :return: translated point
    :rtype: list
    """
    try:
        if point_in is None or len(point_in) == 0 or vector_in is None or len(vector_in) == 0:
            raise ValueError("Input arguments cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Input must be a list or tuple")
    except Exception:
        raise

    # Translate the point using the input vector
    point_out = [coord + comp for coord, comp in zip(point_in, vector_in)]

    return point_out


def point_distance(pt1, pt2):
    # type: (Sequence[float], Sequence[float]) -> float
    """ Computes distance between two points.

    :param pt1: point 1
    :type pt1: list, tuple
    :param pt2: point 2
    :type pt2: list, tuple
    :return: distance between input points
    :rtype: float
    """
    if len(pt1) != len(pt2):
        raise ValueError("The input points should have the same dimension")

    dist_vector = vector_generate(pt1, pt2, normalize=False)
    distance = vector_magnitude(dist_vector)
    return distance


def point_mid(pt1, pt2):
    # type: (Sequence[float], Sequence[float]) -> List[float]
    """ Computes the midpoint of the input points.

    :param pt1: point 1
    :type pt1: list, tuple
    :param pt2: point 2
    :type pt2: list, tuple
    :return: midpoint
    :rtype: list
    """
    if len(pt1) != len(pt2):
        raise ValueError("The input points should have the same dimension")

    dist_vector = vector_generate(pt1, pt2, normalize=False)
    half_dist_vector = vector_multiply(dist_vector, 0.5)
    return point_translate(pt1, half_dist_vector)


def matrix_transpose(m):
    # type: (Sequence[Sequence[float]]) -> Sequence[Sequence[float]]
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


def matrix_multiply(m1, m2):
    # type: (Sequence[Sequence[float]], Sequence[Sequence[float]]) -> Sequence[Sequence[float]]
    """ Matrix multiplication (iterative algorithm).

    The running time of the iterative matrix multiplication algorithm is :math:`O(n^{3})`.

    :param m1: 1st matrix with dimensions :math:`(n \\times p)`
    :type m1: list, tuple
    :param m2: 2nd matrix with dimensions :math:`(p \\times m)`
    :type m2: list, tuple
    :return: resultant matrix with dimensions :math:`(n \\times m)`
    :rtype: list
    """
    mm = [[0.0 for _ in range(len(m2[0]))] for _ in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                mm[i][j] += float(m1[i][k] * m2[k][j])
    return mm


@lru_cache(maxsize=os.environ['GEOMDL_CACHE_SIZE'] if "GEOMDL_CACHE_SIZE" in os.environ else 128)
def binomial_coefficient(k, i):
    # type: (int, int) -> float
    """ Computes the binomial coefficient (denoted by *k choose i*).

    Please see the following website for details: http://mathworld.wolfram.com/BinomialCoefficient.html

    :param k: size of the set of distinct elements
    :type k: int
    :param i: size of the subsets
    :type i: int
    :return: combination of *k* and *i*
    :rtype: float
    """
    # Special case
    if i > k:
        return float(0)
    # Compute binomial coefficient
    k_fact = math.factorial(k)
    i_fact = math.factorial(i)
    k_i_fact = math.factorial(k - i)
    return float(k_fact / (k_i_fact * i_fact))


def lu_decomposition(matrix_a):
    # type: (Sequence[Sequence[float]]) -> Tuple[Sequence[Sequence[float]], Sequence[Sequence[float]]]
    """ LU-Factorization method using Doolittle's Method for solution of linear systems.

    Decomposes the matrix :math:`A` such that :math:`A = LU`.

    The input matrix is represented by a list or a tuple. The input matrix is **2-dimensional**, i.e. list of lists of
    integers and/or floats.

    :param matrix_a: Input matrix (must be a square matrix)
    :type matrix_a: list, tuple
    :return: a tuple containing matrices L and U
    :rtype: tuple
    """
    # Check if the 2-dimensional input matrix is a square matrix
    q = len(matrix_a)
    for idx, m_a in enumerate(matrix_a):
        if len(m_a) != q:
            raise ValueError("The input must be a square matrix. " +
                             "Row " + str(idx + 1) + " has a size of " + str(len(m_a)) + ".")

    # Return L and U matrices
    return _linalg.doolittle(matrix_a)


def forward_substitution(matrix_l, matrix_b):
    # type: (Sequence[Sequence[float]], Sequence[float]) -> Sequence[float]
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
    q = len(matrix_b)
    matrix_y = [0.0 for _ in range(q)]
    matrix_y[0] = float(matrix_b[0]) / float(matrix_l[0][0])
    for i in range(1, q):
        matrix_y[i] = float(matrix_b[i]) - sum([matrix_l[i][j] * matrix_y[j] for j in range(0, i)])
        matrix_y[i] /= float(matrix_l[i][i])
    return matrix_y


def backward_substitution(matrix_u, matrix_y):
    # type: (Sequence[Sequence[float]], Sequence[float]) -> Sequence[float]
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
    q = len(matrix_y)
    matrix_x = [0.0 for _ in range(q)]
    matrix_x[q - 1] = float(matrix_y[q - 1]) / float(matrix_u[q - 1][q - 1])
    for i in range(q - 2, -1, -1):
        matrix_x[i] = float(matrix_y[i]) - sum([matrix_u[i][j] * matrix_x[j] for j in range(i, q)])
        matrix_x[i] /= float(matrix_u[i][i])
    return matrix_x


def frange(start, stop, step=1.0):
    # type: (float, float, float) -> Generator
    """ Implementation of Python's ``range()`` function which works with floats.

    Reference to this implementation: https://stackoverflow.com/a/36091634

    :param start: start value
    :type start: float
    :param stop: end value
    :type stop: float
    :param step: increment
    :type step: float
    :return: float
    :rtype: generator
    """
    i = 0.0
    x = float(start)  # Prevent yielding integers.
    x0 = x
    epsilon = step / 2.0
    yield x  # always yield first value
    while x + epsilon < stop:
        i += 1.0
        x = x0 + i * step
        yield x
    if stop > x:
        yield stop  # for yielding last value of the knot vector if the step is a large value, like 0.1
