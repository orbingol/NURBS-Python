"""
.. module:: tessellate.quadrilateral
    :platform: Unix, Windows
    :synopsis: Quadrilateral tessellation

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from ..entity import Vertex, Quad

def make_quad_mesh(points, size_u, size_v):
    """ Generates a mesh of quadrilateral elements.

    :param points: list of points
    :type points: list, tuple
    :param size_u: number of points on the u-direction (column)
    :type size_u: int
    :param size_v: number of points on the v-direction (row)
    :type size_v: int
    :return: a tuple containing lists of vertices and quads
    :rtype: tuple
    """
    # Numbering
    vertex_idx = 0
    quad_idx = 0

    # Generate vertices
    vertices = []
    for pt in points:
        vrt = Vertex(*pt, id=vertex_idx)
        vertices.append(vrt)
        vertex_idx += 1

    # Generate quads
    quads = []
    for j in range(0, size_v - 1):
        for i in range(0, size_u - 1):
            v1 = vertices[i + (size_u * j)]
            v2 = vertices[i + (size_u * (j + 1))]
            v3 = vertices[i + 1 + (size_u * (j + 1))]
            v4 = vertices[i + 1 + (size_u * j)]
            qd = Quad(v1, v2, v3, v4, id=quad_idx)
            quads.append(qd)
            quad_idx += 1

    return vertices, quads
