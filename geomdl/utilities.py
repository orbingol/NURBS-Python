"""
.. module:: utilities
    :platform: Unix, Windows
    :synopsis: Contains common utility functions and some helper functions for data conversion, integration, etc.

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import random
from . import math


def linspace(start, stop, num, decimals=6):
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
    num = int(num)
    div = num - 1
    delta = stop - start
    return [float(("%0." + str(decimals) + "f") % (start + (float(x) * float(delta) / float(div)))) for x in range(num)]


def vector_cross(vector1, vector2):
    """ Computes the cross-product of the input vectors.

    :param vector1: input vector 1
    :type vector1: list, tuple
    :param vector2: input vector 2
    :type vector2: list, tuple
    :return: result of the cross product
    :rtype: list
    """
    try:
        if vector1 is None or len(vector1) == 0 or vector2 is None or len(vector2) == 0:
            raise ValueError("Input vectors cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Input must be a list or tuple")
    except Exception:
        raise

    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Input should contain 3 elements")

    # Compute cross product
    vector_out = [(vector1[1] * vector2[2]) - (vector1[2] * vector2[1]),
                  (vector1[2] * vector2[0]) - (vector1[0] * vector2[2]),
                  (vector1[0] * vector2[1]) - (vector1[1] * vector2[0])]

    # Return the cross product of the input vectors
    return vector_out


def vector_dot(vector1, vector2):
    """ Computes the dot-product of the input vectors.

    :param vector1: input vector 1
    :type vector1: list, tuple
    :param vector2: input vector 2
    :type vector2: list, tuple
    :return: result of the dot product
    :rtype: list
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
    prod = 0
    for v1, v2 in zip(vector1, vector2):
        prod += v1 * v2

    # Return the dot product of the input vectors
    return prod


# Normalizes the input vector
def vector_normalize(vector_in, decimals=6):
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
    sq_sum = 0
    for vin in vector_in:
        sq_sum += vin**2
    magnitude = math.sqrt(sq_sum)

    # Normalize the vector
    if magnitude > 0:
        vector_out = []
        for vin in vector_in:
            vector_out.append(vin / magnitude)

        # Return the normalized vector and consider the number of significands
        return [float(("%0." + str(decimals) + "f") % vout) for vout in vector_out]
    else:
        raise ValueError("The magnitude of the vector is zero")


def vector_generate(start_pt, end_pt, normalize=False):
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


def point_translate(point_in, vector_in):
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


def binomial_coefficient(k, i):
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


def check_uv(u=None, v=None):
    """ Checks if the parameter values are valid, i.e. between 0 and 1.

    :param u: u parameter
    :type u: float
    :param v: v parameter
    :type v: float
    """
    # Check u value
    if u is not None:
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')

    # Check v value, if necessary
    if v is not None:
        if v < 0.0 or v > 1.0:
            raise ValueError('"v" value should be between 0 and 1.')


def evaluate_bounding_box(ctrlpts):
    """ Evaluates the bounding box of a curve or a surface.

    :param ctrlpts: control points
    :type ctrlpts: list, tuple
    :return: bounding box
    :rtype: list
    """
    # Estimate dimension from the first element of the control points
    dimension = len(ctrlpts[0])

    # Evaluate bounding box
    bbmin = [float('inf') for _ in range(0, dimension)]
    bbmax = [0.0 for _ in range(0, dimension)]
    for cpt in ctrlpts:
        for i, arr in enumerate(zip(cpt, bbmin)):
            if arr[0] < arr[1]:
                bbmin[i] = arr[0]
        for i, arr in enumerate(zip(cpt, bbmax)):
            if arr[0] > arr[1]:
                bbmax[i] = arr[0]

    return [tuple(bbmin), tuple(bbmax)]


# Changes linearly ordered list of points into a zig-zag shape
def make_zigzag(points, num_cols):
    """ Changes linearly ordered list of points into a zig-zag shape.

    This function is designed to create input for the visualization software. It orders the points to draw a zig-zag
    shape which enables generating properly connected lines without any scanlines. Please see the below sketch on the
    functionality of the ``num_cols`` parameter::

             num cols
        <-=============->
        ------->>-------|
        |------<<-------|
        |------>>-------|
        -------<<-------|

    Please note that this function does not detect the ordering of the input points to detect the input points have
    already been processed to generate a zig-zag shape.

    :param points: list of points to be ordered
    :type points: list
    :param num_cols: number of elements in a row which the zig-zag is generated
    :param num_cols: int
    :return: re-ordered points
    :rtype: list
    """
    new_points = []
    points_size = len(points)
    forward = True
    idx = 0
    rev_idx = -1
    while idx < points_size:
        if forward:
            new_points.append(points[idx])
        else:
            new_points.append(points[rev_idx])
            rev_idx -= 1
        idx += 1
        if idx % num_cols == 0:
            forward = False if forward else True
            rev_idx = idx + num_cols - 1

    return new_points


def make_quad(points, row_size, col_size):
    """ Generates a quad mesh from linearly ordered list of points.

    :param points: list of points to be ordered
    :type points: list, tuple
    :param row_size: number of elements in a row
    :param row_size: int
    :param col_size: number of elements in a column
    :param col_size: int
    :return: re-ordered points
    :rtype: list
    """
    # Start with generating a zig-zag shape in row direction and then take its reverse
    new_points = make_zigzag(points, row_size)
    new_points.reverse()

    # Start generating a zig-zag shape in col direction
    forward = True
    for row in range(0, row_size):
        temp = []
        for col in range(0, col_size):
            temp.append(points[row + (col * row_size)])
        if forward:
            forward = False
        else:
            forward = True
            temp.reverse()
        new_points += temp

    return new_points


def make_triangle(points, row_size, col_size):
    """ Generates a triangular mesh from  linearly ordered list of points.

    :param points: list of points to be ordered
    :type points: list, tuple
    :param row_size: number of elements in a row
    :param row_size: int
    :param col_size: number of elements in a column
    :param col_size: int
    :return: re-ordered points
    :rtype: list
    """
    points2d = []
    for i in range(0, col_size):
        row_list = []
        for j in range(0, row_size):
            row_list.append(points[j + (i * row_size)])
        points2d.append(row_list)

    forward = True
    triangles = []
    for col_idx in range(0, col_size - 1):
        row_idx = 0
        left_half = True
        tri_list = []
        while row_idx < row_size - 1:
            if left_half:
                tri_list.append(points2d[col_idx + 1][row_idx])
                tri_list.append(points2d[col_idx][row_idx])
                tri_list.append(points2d[col_idx][row_idx + 1])
                tri_list.append(points2d[col_idx + 1][row_idx])
                left_half = False
            else:
                tri_list.append(points2d[col_idx][row_idx + 1])
                tri_list.append(points2d[col_idx + 1][row_idx + 1])
                tri_list.append(points2d[col_idx + 1][row_idx])
                left_half = True
                row_idx += 1
        if forward:
            forward = False
        else:
            forward = True
            tri_list.reverse()
        triangles += tri_list

    return triangles


# A float range function, implementation of https://stackoverflow.com/a/47877721
def frange(start, stop, step=1.0):
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


# Normalizes knot vector
def normalize_knot_vector(knot_vector, decimals=4):
    """ Normalizes the input knot vector between 0 and 1.

    :param knot_vector: knot vector to be normalized
    :type knot_vector: list, tuple
    :param decimals: rounding number
    :type decimals: int
    :return: normalized knot vector
    :rtype: list
    """
    try:
        if knot_vector is None or len(knot_vector) == 0:
            raise ValueError("Input knot vector cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Knot vector must be a list or tuple")
    except Exception:
        raise

    first_knot = float(knot_vector[0])
    last_knot = float(knot_vector[-1])
    denominator = last_knot - first_knot

    knot_vector_out = [(float(("%0." + str(decimals) + "f") % ((float(kv) - first_knot) / denominator)))
                       for kv in knot_vector]

    return knot_vector_out


# Generates a uniform knot vector using the given degree and the number of control points
def generate_knot_vector(degree, num_ctrlpts):
    """ Generates a uniformly-spaced knot vector using the degree and the number of control points.

    It uses the following equation to generate knot vector:

    m = n + p + 1

    where;

    p: degree, n+1: number of control points, m+1: number of knots

    :param degree: degree
    :type degree: integer
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: integer
    :return: uniform knot vector
    :rtype: list
    """
    if degree == 0 or num_ctrlpts == 0:
        raise ValueError("Input values should be different than zero.")

    # First knots
    knot_vector = [0.0 for _ in range(0, degree)]

    # Number of knots in the middle
    num_segments = num_ctrlpts - (degree + 1)

    # Middle knots
    knot_vector += linspace(0.0, 1.0, num_segments + 2)

    # Last knots
    knot_vector += [1.0 for _ in range(0, degree)]

    # Return auto-generated knot vector
    return knot_vector


# Checks if the input knot vector follows the mathematical rules
def check_knot_vector(degree, knot_vector, num_ctrlpts):
    """ Checks if the input knot vector follows the mathematical rules.

    :param degree: degree of the curve or the surface
    :type degree: int
    :param knot_vector: knot vector to be checked
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: int
    :return: True if the knot vector is valid, False otherwise
    :rtype: bool
    """
    try:
        if knot_vector is None or len(knot_vector) == 0:
            raise ValueError("Input knot vector cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Knot vector must be a list or tuple")
    except Exception:
        raise

    # Check the formula; m = p + n + 1
    if len(knot_vector) != degree + num_ctrlpts + 1:
        return False

    # Check ascending order
    prev_knot = knot_vector[0]
    for knot in knot_vector:
        if prev_knot > knot:
            return False
        prev_knot = knot

    return True


def color_generator(seed=None):
    """ Generates random colors for control and evaluated curve/surface points plots.

    The ``seed`` argument is used to set the random seed by directly passing the value to ``random.seed()`` function.
    Please see the Python documentation for more details on the ``random`` module .

    Inspired from https://stackoverflow.com/a/14019260

    :param seed: Sets the random seed
    :return: list of color strings in hex format
    :rtype: list
    """
    if seed is not None:
        random.seed(seed)
    r = lambda: random.randint(0, 255)
    color_string = '#%02X%02X%02X'
    return [color_string % (r(), r(), r()), color_string % (r(), r(), r())]
