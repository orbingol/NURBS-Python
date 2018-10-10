"""
.. module:: utilities
    :platform: Unix, Windows
    :synopsis: Contains common utility functions for linear algebra, data validation, etc.

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import random
import math
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


def vector_is_zero(vector_in, tol=10e-8):
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


def lu_decomposition(matrix_in, q=0):
    """ LU-Factorization method using Doolittle's Method for solution of linear systems.

    Decomposes the matrix :math:`A` such that :math:`A = LU`.

    The input matrix is represented by a list or a tuple. If the input matrix is 1-dimensional, i.e. a list or tuple of
    integers and/or floats, then the second function argument ``q`` must be bigger than zero. If the input matrix is
    2-dimensional, i.e. list of lists of integers and/or floats, then there is no need to input ``q`` as it will be
    automatically computed.

    :param matrix_in: Input matrix (must be a square matrix)
    :type matrix_in: list, tuple
    :param q: matrix size (not used if the input matrix is 2-dimensional)
    :type q: int
    :return: a tuple containing matrices (L,U)
    :rtype: tuple
    """
    if not isinstance(q, int):
        raise TypeError("Matrix size must be an integer")

    if q < 0:
        raise ValueError("Matrix size should be bigger than zero")

    # Flag for converting return values into 1-dimensional list
    convert_res = False
    if q > 0:
        # Check if the 1-dimensional input matrix is a square matrix
        if len(matrix_in) != q ** 2:
            raise ValueError("The input matrix must be a square matrix")

        # Convert 1-dimensional matrix to 2-dimensional
        matrix_a = [[0.0 for _ in range(q)] for _ in range(q)]
        for i in range(0, q):
            for j in range(0, q):
                matrix_a[i][j] = matrix_in[j + (q * i)]

        # The input is 1-dimensional, so the return values should be
        convert_res = True
    else:
        matrix_a = matrix_in
        # Check if the 2-dimensional input matrix is a square matrix
        q = len(matrix_a)
        for idx, m_a in enumerate(matrix_a):
            if len(m_a) != q:
                raise ValueError("The input must be a square matrix. " +
                                 "Row " + str(idx + 1) + " has a size of " + str(len(m_a)) + ".")

    # Initialize L and U matrices
    matrix_u = [[0.0 for _ in range(q)] for _ in range(q)]
    matrix_l = [[0.0 for _ in range(q)] for _ in range(q)]

    # Doolittle Method
    for i in range(0, q):
        for k in range(i, q):
            # Upper triangular (U) matrix
            matrix_u[i][k] = float(matrix_a[i][k] - sum([matrix_l[i][j] * matrix_u[j][k] for j in range(0, i)]))
            # Lower triangular (L) matrix
            if i == k:
                matrix_l[i][i] = 1.0
            else:
                matrix_l[k][i] = float(matrix_a[k][i] - sum([matrix_l[k][j] * matrix_u[j][i] for j in range(0, i)]))
                matrix_l[k][i] /= float(matrix_u[i][i])

    # Prepare and return the L and U matrices
    if convert_res:
        m_u = []
        m_l = []
        for upper, lower in zip(matrix_u, matrix_l):
            m_u.extend(upper)
            m_l.extend(lower)
        return m_l, m_u
    return matrix_l, matrix_u


def forward_substitution(matrix_l, matrix_b):
    """ Forward substitution method for solution of linear systems.

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
    """ Backward substitution method for solution of linear systems.

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

    This function generates a triangular mesh for a NURBS or B-Spline surface on its parametric space.
    The input is the surface points and the number of points on the parametric dimensions u and v,
    indicated as row and column sizes in the function signature. This function should operate correctly if row and
    column sizes are input correctly, no matter what the points are v-ordered or u-ordered. Please see the
    documentation of ``ctrlpts`` and ``ctrlpts2d`` properties of the Surface class for more details on
    point ordering for the surfaces.

    This function accepts the following keyword arguments:

    * ``vertex_spacing``: Defines the size of the triangles via setting the jump value between points
    * ``trims``: List of trim curves passed to the tessellation function
    * ``tessellate_func``: Function called for tessellation (default is ``triangular_tessellation``)
    * ``tessellate_args``: Arguments passed to the tessellation function

    The tessellation function is designed to generate triangles from 4 vertices. It takes 4 :py:class:`.Vertex` objects,
    index values for setting the triangle and vertex IDs and additional parameters as its function arguments.
    It returns a tuple of :py:class:`.Vertex` and :py:class:`.Triangle` object lists generated from the input vertices.
    A default triangle generator is provided as a prototype for implementation in the source code.

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
    def triangular_tessellation(v1, v2, v3, v4, vidx, tidx, trim_curves, tessellate_args):
        """ Default tessellation algorithm (triangular tessellation).

        :param v1: vertex 1
        :type v1: Vertex
        :param v2: vertex 2
        :type v2: Vertex
        :param v3: vertex 3
        :type v3: Vertex
        :param v4: vertex 4
        :type v4: Vertex
        :param vidx: vertex numbering start value
        :type vidx: int
        :param tidx: triangle numbering start value
        :type tidx: int
        :param trim_curves: trim curves
        :type: list, tuple
        :param tessellate_args: tessellation arguments
        :type tessellate_args: list, tuple
        :return: lists of vertex and triangle objects in (vertex_list, triangle_list) format
        :type: tuple
        """
        # Triangulate vertices
        tris = polygon_triangulate(tidx, v1, v2, v3, v4)

        # Return vertex and triangle lists
        return [], tris

    def fix_numbering(vertex_list, triangle_list):
        # Initialize variables
        final_vertices = []

        # Get all vertices inside the triangle list
        tri_vertex_ids = []
        for tri in triangle_list:
            tri_vertex_ids += tri.vertex_ids

        # Find vertices used in triangles
        for vertex in vertex_list:
            if vertex.id in tri_vertex_ids:
                final_vertices.append(vertex)

        # Fix vertex numbering (automatically fixes triangle vertex numbering)
        vert_new_id = 1
        for vertex in final_vertices:
            vertex.id = vert_new_id
            vert_new_id += 1

        return final_vertices, triangle_list

    # Vertex spacing for triangulation
    vertex_spacing = kwargs.get('vertex_spacing', 1)  # defines the size of the triangles
    trim_curves = kwargs.get('trims', [])

    # Tessellation algorithm
    tsl_func = kwargs.get('tessellate_func')
    if tsl_func is None:
        tsl_func = triangular_tessellation
    tsl_args = kwargs.get('tessellate_args', None)

    # Variable initialization
    vrt_idx = 1  # vertex index numbering start
    tri_idx = 1  # triangle index numbering start
    u_jump = (1.0 / float(size_u - 1)) * vertex_spacing  # for computing vertex parametric u value
    v_jump = (1.0 / float(size_v - 1)) * vertex_spacing  # for computing vertex parametric v value
    varr_size_u = int(round((float(size_u) / float(vertex_spacing)) + 10e-8))  # vertex array size on the u-direction
    varr_size_v = int(round((float(size_v) / float(vertex_spacing)) + 10e-8))  # vertex array size on the v-direction

    # Generate vertices directly from input points (preliminary evaluation)
    vertices = [Vertex() for _ in range(varr_size_v * varr_size_u)]
    u = 0.0
    for i in range(0, size_u, vertex_spacing):
        v = 0.0
        for j in range(0, size_v, vertex_spacing):
            idx = j + (i * size_v)
            vertices[vrt_idx - 1].id = vrt_idx
            vertices[vrt_idx - 1].data = points[idx]
            vertices[vrt_idx - 1].uv = [u, v]
            vrt_idx += 1
            v += v_jump
        u += u_jump

    #
    # Organization of vertices in a quad element on the parametric space:
    #
    # v4      v3
    # o-------o         i
    # |       |          |
    # |       |          |
    # |       |          |_ _ _
    # o-------o                 j
    # v1      v2
    #

    # Generate triangles and final vertices
    triangles = []
    for i in range(varr_size_u - 1):
        for j in range(varr_size_v - 1):
            # Find vertex indices for a quad element
            vertex1 = vertices[j + (i * varr_size_v)]
            vertex2 = vertices[j + 1 + (i * varr_size_v)]
            vertex3 = vertices[j + 1 + ((i + 1) * varr_size_v)]
            vertex4 = vertices[j + ((i + 1) * varr_size_v)]

            # Call tessellation function
            vlst, tlst = tsl_func(vertex1, vertex2, vertex3, vertex4, vrt_idx, tri_idx, trim_curves, tsl_args)

            # Add tessellation results to the return lists
            vertices += vlst
            triangles += tlst

            # Increment index values
            vrt_idx += len(vlst)
            tri_idx += len(tlst)

    # Fix vertex and triangle numbering (ID values)
    vertices, triangles = fix_numbering(vertices, triangles)

    return vertices, triangles


def polygon_triangulate(tri_idx, *args):
    """ Triangulates a monotone polygon defined by a list of vertices.

    The input vertices must form a convex polygon and must be arranged in counter-clockwise order.

    :param tri_idx: triangle numbering start value
    :type tri_idx: int
    :param args: list of Vertex objects
    :type args: tuple
    :return: list of Triangle objects
    :rtype: list
    """
    # Initialize variables
    tidx = 0
    triangles = []

    # Generate triangles
    for idx in range(1, len(args) - 1):
        tri = Triangle()
        tri.id = tri_idx + tidx
        tri.add_vertex(args[0], args[idx], args[idx + 1])
        triangles.append(tri)
        tidx += 1

    # Return generated triangles
    return triangles


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
    else:
        data = tri.vertices
        mid = [0.0, 0.0, 0.0]
    for idx, vert in enumerate(data):
        mid = [m + v for m, v in zip(mid, vert)]
    mid = [float(m) / 3.0 for m in mid]
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
