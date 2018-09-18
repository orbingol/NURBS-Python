"""
.. module:: utilities
    :platform: Unix, Windows
    :synopsis: Contains common utility functions for linear algebra, data validation, etc.

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import random
from . import math
from .elements import Vertex, Triangle


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

    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Input should contain 3 elements")

    # Compute cross product
    vector_out = [(vector1[1] * vector2[2]) - (vector1[2] * vector2[1]),
                  (vector1[2] * vector2[0]) - (vector1[0] * vector2[2]),
                  (vector1[0] * vector2[1]) - (vector1[1] * vector2[0])]

    # Return the cross product of the input vectors
    return tuple(vector_out)


def vector_dot(vector1, vector2):
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
    prod = 0
    for v1, v2 in zip(vector1, vector2):
        prod += v1 * v2

    # Return the dot product of the input vectors
    return prod


# Multiplies the input vector with a scalar value
def vector_multiply(vector_in, scalar):
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
    return tuple(scaled_vector)


# Normalizes the input vector
def vector_normalize(vector_in, decimals=6):
    """ Generates a unit vector from the input.

    :param vector_in: vector to be normalized
    :type vector_in: list, tuple
    :param decimals: number of significands
    :type decimals: int
    :return: the normalized vector (i.e. the unit vector)
    :rtype: tuple
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
        return tuple([float(("%0." + str(decimals) + "f") % vout) for vout in vector_out])
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
    :rtype: tuple
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
    return tuple(ret_vec)


def vector_mean(*args):
    """ Computes the mean (average) of a list of vectors.

    The function computes the arithmetic mean of a list of vectors, which are also organized as a list of
    integers or floating point numbers.

    .. code-block:: python

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
    :rtype: tuple
    """
    sz = len(args)
    mean_vector = [0.0 for _ in range(len(args[0]))]
    for input_vector in args:
        mean_vector = [a+b for a, b in zip(mean_vector, input_vector)]
    mean_vector = [a / sz for a in mean_vector]
    return tuple(mean_vector)


def vector_magnitude(vector_in):
    """ Computes the magnitude of the input vector.

    :param vector_in: input vector
    :type vector_in: list, tuple
    :return: magnitude of the vector
    :rtype: float
    """
    sq_sum = 0
    for vin in vector_in:
        sq_sum += vin**2
    return math.sqrt(sq_sum)


def vector_angle_between(vector1, vector2, **kwargs):
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


def point_translate(point_in, vector_in):
    """ Translates the input points using the input vector.

    :param point_in: input point
    :type point_in: list, tuple
    :param vector_in: input vector
    :type vector_in: list, tuple
    :return: translated point
    :rtype: tuple
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

    return tuple(point_out)


def point_distance(pt1, pt2):
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
    """ Computes the midpoint of the two points.

    :param pt1: point 1
    :type pt1: list, tuple
    :param pt2: point 2
    :type pt2: list, tuple
    :return: midpoint
    :rtype: tuple
    """
    if len(pt1) != len(pt2):
        raise ValueError("The input points should have the same dimension")

    dist_vector = vector_generate(pt1, pt2, normalize=False)
    half_dist_vector = vector_multiply(dist_vector, 0.5)
    return point_translate(pt1, half_dist_vector)


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
    """ Checks if the parameter values are valid.

    :param u: u parameter
    :type u: float
    :param v: v parameter
    :type v: float
    :raises ValueError: u and/or v is not in the interval [0, 1]
    """
    tol = 10e-8
    # Check u value
    if u is not None:
        if not (0.0 - tol) <= u <= (1.0 + tol):
            raise ValueError('"u" value should be between 0 and 1.')

    # Check v value, if necessary
    if v is not None:
        if not (0.0 - tol) <= v <= (1.0 + tol):
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
    :type num_cols: int
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


def make_quad_mesh(points, size_u, size_v):
    """ Generates a quad mesh from linearly ordered list of points.

    :param points: list of points to be ordered
    :type points: list, tuple
    :param size_v: number of elements in a row
    :type size_v: int
    :param size_u: number of elements in a column
    :type size_u: int
    :return: re-ordered points
    :rtype: list
    """
    # Start with generating a zig-zag shape in row direction and then take its reverse
    new_points = make_zigzag(points, size_v)
    new_points.reverse()

    # Start generating a zig-zag shape in col direction
    forward = True
    for row in range(0, size_v):
        temp = []
        for col in range(0, size_u):
            temp.append(points[row + (col * size_v)])
        if forward:
            forward = False
        else:
            forward = True
            temp.reverse()
        new_points += temp

    return new_points


def make_triangle_mesh(points, size_u, size_v, **kwargs):
    """ Generates a triangular mesh from an array of points.

    This function simply generates a triangular mesh for a NURBS or B-Spline surface on its parametric space.
    The input is the surface points and the number of points on the parametric dimensions u and v,
    indicated as row and column sizes in the function signature. This function should operate correctly if row and
    column sizes are input correctly, no matter what the points are v-ordered or u-ordered. Please see the
    documentation of ``ctrlpts`` and ``ctrlpts2d`` properties of the Surface class for more details on
    point ordering for the surfaces.

    This function accepts the following keyword arguments:

    * ``vertex_spacing``: Defines the size of the triangles via setting the jump value between points
    * ``vertex_postprocess_func``: Function called after generating the vertex list
    * ``vertex_postprocess_args``: Arguments passed to the vertex post-processing function
    * ``triangle_postprocess_func``: Function called after generating the triangle list
    * ``triangle_postprocess_args``: Arguments passed to the triangle post-processing function

    Post-processing functions are designed to modify the vertices and triangles. They take a list of vertices and
    triangles as instances of :py:class:`.Vertex` and  :py:class:`.Triangle` classes. They should return a list of
    vertices and triangles. Prototypes of the post-processing functions can be found in the source code of this
    function.

    The return value of this function is a tuple containing two lists. First one is the list of vertices and the second
    one is the list of triangles.

    :param points: input points
    :type points: list, tuple
    :param size_u: number of elements on the u-direction
    :type size_u: int
    :param size_v: number of elements on the v-direction
    :type size_v: int
    :return: a tuple containing lists of vertices and triangles
    :rtype: tuple
    """
    def process_vertices(vertex_list, postprocess_args):
        # Default function for vertex post-processing
        return vertex_list

    def process_triangles(triangle_list, postprocess_args):
        # Default function for triangle post-processing
        return triangle_list

    # Get keyword arguments
    vertex_spacing = kwargs.get('vertex_spacing', 1)  # defines the size of the triangles
    # Vertex and triangle post-processing functions
    vertex_postprocess_func = kwargs.get('vertex_postprocess_func', process_vertices)
    triangle_postprocess_func = kwargs.get('triangle_postprocess_func', process_triangles)
    # Vertex and triangle post-processing function arguments
    vertex_postprocess_args = kwargs.get('vertex_postprocess_args', None)
    triangle_postprocess_args = kwargs.get('triangle_postprocess_args', None)

    # Variable initialization
    vrt_idx = 0  # vertex array index numbering start
    tri_id = 1  # triangle ID numbering start
    u_range = 1.0 / float(size_u - 1)  # for computing vertex parametric u value
    v_range = 1.0 / float(size_v - 1)  # for computing vertex parametric v value

    # Vertex array size (also used for traversing triangulation loop)
    varr_size_u = int(round((size_u / vertex_spacing) + 10e-8) + (size_u % vertex_spacing))
    varr_size_v = int(round((size_v / vertex_spacing) + 10e-8) + (size_v % vertex_spacing))

    # Start vertex generation loop
    vertices = [Vertex() for _ in range(varr_size_v * varr_size_u)]
    u = 0.0
    for i in range(0, size_u, vertex_spacing):
        v = 0.0
        for j in range(0, size_v, vertex_spacing):
            idx = j + (i * size_v)
            vertices[vrt_idx].data = points[idx]
            vertices[vrt_idx].id = vrt_idx + 1
            vertices[vrt_idx].uv = [u, v]
            vrt_idx += 1
            v += (v_range * vertex_spacing)
        u += (u_range * vertex_spacing)

    # Execute vertex post-processing function
    if vertex_postprocess_func is not None:
        vertices = vertex_postprocess_func(vertices, vertex_postprocess_args)

    # Start triangulation loop
    forward = True
    triangles = []
    for i in range(0, varr_size_u - 1):
        j = 0
        left_half = True
        tri_list = []
        while j < varr_size_v - 1:
            if left_half:
                vertex1 = vertices[((i + 1) * varr_size_v) + j]
                vertex2 = vertices[(i * varr_size_v) + j]
                vertex3 = vertices[(i * varr_size_v) + j + 1]
                left_half = False
            else:
                vertex1 = vertices[(i * varr_size_v) + j + 1]
                vertex2 = vertices[((i + 1) * varr_size_v) + j + 1]
                vertex3 = vertices[((i + 1) * varr_size_v) + j]
                left_half = True
                j += 1

            # Generate triangle
            tri = Triangle()
            tri.add_vertex((vertex1, vertex2, vertex3))
            tri.id = tri_id
            tri_list.append(tri)
            tri_id += 1
        if forward:
            forward = False
        else:
            forward = True
            tri_list.reverse()
        triangles += tri_list

    # Execute triangle post-processing function
    if triangle_postprocess_func is not None:
        triangles = triangle_postprocess_func(triangles, triangle_postprocess_args)

    return vertices, triangles


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


def triangle_center(tri, uv=False):
    """ Computes the center of mass of the input triangle.

    :param tri: triangle object
    :type tri: elements.Triangle
    :param uv: if True, then finds parametric position of the center of mass
    :type uv: bool
    :return: center of mass of the triangle
    :rtype: tuple
    """
    if uv:
        data = tri.vertices_uv
        mid = [0.0, 0.0]
        sz = 2
    else:
        data = tri.vertices
        mid = [0.0, 0.0, 0.0]
        sz = 3
    for idx, vert in enumerate(data):
        mid = [m + v for m, v in zip(mid, vert)]
    mid = [m / sz for m in mid]
    return tuple(mid)


def make_quadtree(points, size_u, size_v, **kwargs):
    """ Generates a quadtree-like structure from surface control points.

    This function generates a 2-dimensional list of control point coordinates. Considering the object-oriented
    representation of a quadtree data structure, first dimension of the generated list corresponds to a list of
    *QuadTree* classes. Second dimension of the generated list corresponds to a *QuadTree* data structure. The first
    element of the 2nd dimension is the mid-point of the bounding box and the remaining elements are corner points of
    the bounding box organized in counter-clockwise order.

    To maintain stability for the data structure on the edges and corners, the function accepts ``extrapolate``
    keyword argument. If it is *True*, then the function extrapolates the surface on the corners and edges to complete
    the quad-like structure for each control point. If it is *False*, no extrapolation will be applied.
    By default, ``extrapolate`` is set to *True*.

    Please note that this function's intention is not generating a real quadtree structure but reorganizing the
    control points in a very similar fashion to make them available for various geometric operations.

    :param points: 1-dimensional array of surface control points
    :type points: list, tuple
    :param size_u: number of control points on the u-direction
    :type size_u: int
    :param size_v: number of control points on the v-direction
    :type size_v: int
    :return: control points organized in a quadtree-like structure
    :rtype: tuple
    """
    # Get keyword arguments
    extrapolate = kwargs.get('extrapolate', True)

    # Convert control points array into 2-dimensional form
    points2d = []
    for i in range(0, size_u):
        row_list = []
        for j in range(0, size_v):
            row_list.append(points[j + (i * size_v)])
        points2d.append(row_list)

    # Traverse 2-dimensional control points to find neighbors
    qtree = []
    for u in range(size_u):
        for v in range(size_v):
            temp = [points2d[u][v]]
            # Note: negative indexing actually works in Python, so we need explicit checking
            if u + 1 < size_u:
                temp.append(points2d[u+1][v])
            else:
                if extrapolate:
                    extrapolated_edge = vector_generate(points2d[u-1][v], points2d[u][v])
                    translated_point = point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if v + 1 < size_v:
                temp.append(points2d[u][v+1])
            else:
                if extrapolate:
                    extrapolated_edge = vector_generate(points2d[u][v-1], points2d[u][v])
                    translated_point = point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if u - 1 >= 0:
                temp.append(points2d[u-1][v])
            else:
                if extrapolate:
                    extrapolated_edge = vector_generate(points2d[u+1][v], points2d[u][v])
                    translated_point = point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if v - 1 >= 0:
                temp.append(points2d[u][v-1])
            else:
                if extrapolate:
                    extrapolated_edge = vector_generate(points2d[u][v+1], points2d[u][v])
                    translated_point = point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            qtree.append(tuple(temp))

    # Return the array generated.
    return tuple(qtree)


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
def generate_knot_vector(degree, num_ctrlpts, **kwargs):
    """ Generates a uniformly-spaced knot vector using the degree and the number of control points.

    It uses the following equation to generate knot vector:

    m = n + p + 1

    where;

    p: degree, n+1: number of control points, m+1: number of knots

    Keyword Arguments:

        * ``clamped``: flag to choose from clamped or unclamped knot vector options. *Default: True*

    :param degree: degree
    :type degree: integer
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: integer
    :return: uniform knot vector
    :rtype: list
    """
    if degree == 0 or num_ctrlpts == 0:
        raise ValueError("Input values should be different than zero.")

    # Get keyword arguments
    clamped = kwargs.get('clamped', True)

    # Number of repetitions at the start and end of the array
    num_repeat = degree

    # Number of knots in the middle
    num_segments = num_ctrlpts - (degree + 1)

    if not clamped:
        # No repetitions at the start and end
        num_repeat = 0
        # Should conform the rule: m = n + p + 1
        num_segments = degree + num_ctrlpts - 1

    # First knots
    knot_vector = [0.0 for _ in range(0, num_repeat)]

    # Middle knots
    knot_vector += linspace(0.0, 1.0, num_segments + 2)

    # Last knots
    knot_vector += [1.0 for _ in range(0, num_repeat)]

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
    def r_int():
        return random.randint(0, 255)
    if seed is not None:
        random.seed(seed)
    color_string = '#%02X%02X%02X'
    return [color_string % (r_int(), r_int(), r_int()), color_string % (r_int(), r_int(), r_int())]


def init_var(instance):
    if callable(instance):
        return instance()
    else:
        return None
