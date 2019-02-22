"""
.. module:: utilities
    :platform: Unix, Windows
    :synopsis: Contains common utility functions for linear algebra, data validation, etc.

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import random
from .linalg import vector_cross, vector_generate, point_translate
from .elements import Vertex, Triangle, Quad

# Preserve the knot vector functions for compatibility
from . import knotvector
generate_knot_vector = knotvector.generate
check_knot_vector = knotvector.check
normalize_knot_vector = knotvector.normalize


def evaluate_bounding_box(ctrlpts):
    """ Computes the minimum bounding box of the point set.

    The (minimum) bounding box is the smallest enclosure in which all the input points lie.

    :param ctrlpts: points
    :type ctrlpts: list, tuple
    :return: bounding box in the format [min, max]
    :rtype: tuple
    """
    # Estimate dimension from the first element of the control points
    dimension = len(ctrlpts[0])

    # Evaluate bounding box
    bbmin = [float('inf') for _ in range(0, dimension)]
    bbmax = [float('-inf') for _ in range(0, dimension)]
    for cpt in ctrlpts:
        for i, arr in enumerate(zip(cpt, bbmin)):
            if arr[0] < arr[1]:
                bbmin[i] = arr[0]
        for i, arr in enumerate(zip(cpt, bbmax)):
            if arr[0] > arr[1]:
                bbmax[i] = arr[0]

    return tuple(bbmin), tuple(bbmax)


# Changes linearly ordered list of points into a zig-zag shape
def make_zigzag(points, num_cols):
    """ Converts linear sequence of points into a zig-zag shape.

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


def make_quad(points, size_u, size_v):
    """ Converts linear sequence of input points into a quad structure.

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


def make_quad_mesh(points, size_u, size_v):
    """ Generates a mesh of quadrilateral elements.

    :param points: list of points
    :type points: list, tuple
    :param size_u: number of points on the u-direction (column)
    :type size_u: int
    :param size_v: number of points on the v-direction (row)
    :return: a tuple containing lists of vertices and quads
    :rtype: tuple
    """
    # Generate vertices
    vertex_idx = 1
    vertices = []
    for pt in points:
        vrt = Vertex(*pt, id=vertex_idx)
        vertices.append(vrt)
        vertex_idx += 1

    # Generate quads
    quad_idx = 1
    quads = []
    for i in range(0, size_u - 1):
        for j in range(0, size_v - 1):
            idx1 = j + (size_v * i)
            idx2 = j + (size_v * (i + 1))
            idx3 = j + 1 + (size_v * (i + 1))
            idx4 = j + 1 + (size_v * i)
            qd = Quad(idx1, idx2, idx3, idx4, id=quad_idx)
            quads.append(qd)
            quad_idx += 1

    return vertices, quads


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
    :type args: elements.Vertex
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
    for vert in data:
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
                    extrapolated_edge = vector_generate(points2d[u - 1][v], points2d[u][v])
                    translated_point = point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if v + 1 < size_v:
                temp.append(points2d[u][v+1])
            else:
                if extrapolate:
                    extrapolated_edge = vector_generate(points2d[u][v - 1], points2d[u][v])
                    translated_point = point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if u - 1 >= 0:
                temp.append(points2d[u-1][v])
            else:
                if extrapolate:
                    extrapolated_edge = vector_generate(points2d[u + 1][v], points2d[u][v])
                    translated_point = point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if v - 1 >= 0:
                temp.append(points2d[u][v-1])
            else:
                if extrapolate:
                    extrapolated_edge = vector_generate(points2d[u][v + 1], points2d[u][v])
                    translated_point = point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            qtree.append(tuple(temp))

    # Return generated quad-tree
    return tuple(qtree)


def check_params(params):
    """ Checks if the parameters are defined in the domain [0, 1].

    :param params: parameters (u, v, w)
    :type params: list, tuple
    :return: True if defined in the domain [0, 1]. False, otherwise.
    :rtype: bool
    """
    tol = 10e-8
    # Check parameters
    for prm in params:
        if prm is not None:
            if not (0.0 - tol) <= prm <= (1.0 + tol):
                return False
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
