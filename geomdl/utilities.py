"""
.. module:: utilities
    :platform: Unix, Windows
    :synopsis: Contains common utility functions for linear algebra, data validation, etc.

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import random
from geomdl import linalg
from geomdl.elements import Vertex, Quad

# Preserve the knot vector functions for compatibility
from . import knotvector
generate_knot_vector = knotvector.generate
check_knot_vector = knotvector.check
normalize_knot_vector = knotvector.normalize


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
                    extrapolated_edge = linalg.vector_generate(points2d[u - 1][v], points2d[u][v])
                    translated_point = linalg.point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if v + 1 < size_v:
                temp.append(points2d[u][v+1])
            else:
                if extrapolate:
                    extrapolated_edge = linalg.vector_generate(points2d[u][v - 1], points2d[u][v])
                    translated_point = linalg.point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if u - 1 >= 0:
                temp.append(points2d[u-1][v])
            else:
                if extrapolate:
                    extrapolated_edge = linalg.vector_generate(points2d[u + 1][v], points2d[u][v])
                    translated_point = linalg.point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            if v - 1 >= 0:
                temp.append(points2d[u][v-1])
            else:
                if extrapolate:
                    extrapolated_edge = linalg.vector_generate(points2d[u][v + 1], points2d[u][v])
                    translated_point = linalg.point_translate(points2d[u][v], extrapolated_edge)
                    temp.append(translated_point)
            qtree.append(tuple(temp))

    # Return generated quad-tree
    return tuple(qtree)
