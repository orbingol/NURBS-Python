"""
.. module:: exchange_helpers
    :platform: Unix, Windows
    :synopsis: CAD exchange and interoperability helper functions and classes for NURBS-Python package

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from array import array
from . import utilities as utils


# Vertex class
class Vertex(object):
    def __init__(self, value=()):
        self._id = 0
        self._value = array('f', [0.0, 0.0, 0.0])
        if len(value) == 3:
            self._value = array('f', value)
        self._uv = None

    def __str__(self):
        return "Vertex " + str(self._id) + " " + str(self._value.tolist())

    __repr__ = __str__

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID value must be an integer")
        self._id = value

    @property
    def x(self):
        return self._value[0]

    @x.setter
    def x(self, value):
        self._value[0] = float(value)

    @property
    def y(self):
        return self._value[1]

    @y.setter
    def y(self, value):
        self._value[1] = float(value)

    @property
    def z(self):
        return self._value[2]

    @z.setter
    def z(self, value):
        self._value[2] = float(value)

    @property
    def uv(self):
        return self._uv

    @uv.setter
    def uv(self, value):
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError("UV must have 2 components")
        self._uv = array("d", list(value))

    @property
    def data(self):
        return self._value.tolist()


# Triangle class
class Triangle(object):
    def __init__(self):
        self._id = 0
        self._vertices = []
        self._normal = None

    def __str__(self):
        return "Triangular face " + str(self._id)

    __repr__ = __str__

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID value must be an integer")
        self._id = value

    @property
    def normal(self):
        if not self._normal:
            vec1 = utils.vector_generate(self._vertices[0].data, self._vertices[1].data)
            vec2 = utils.vector_generate(self._vertices[1].data, self._vertices[2].data)
            self._normal = utils.normalize(utils.vector_cross(vec1, vec2))
        return self._normal

    def add_vertex(self, vertex=None):
        if len(self._vertices) > 2:
            raise ValueError("Cannot add more vertices")
        if not isinstance(vertex, Vertex):
            raise ValueError("Input must be a Vertex object")
        self._vertices.append(vertex)

    @property
    def vertex_ids(self):
        return [self._vertices[0].id, self._vertices[1].id, self._vertices[2].id]


# Generates triangles for saving as a Wavefront OBJ file
def make_obj_triangles(points, row_size, col_size, vertex_spacing):
    points2d = []
    for i in range(0, col_size):
        row_list = []
        for j in range(0, row_size):
            row_list.append(points[j + (i * row_size)])
        points2d.append(row_list)

    u_range = 1.0 / float(col_size - 1)
    v_range = 1.0 / float(row_size - 1)
    vertices = []
    vert_id = 1
    u = 0.0
    for col_idx in range(0, col_size, vertex_spacing):
        vert_list = []
        v = 0.0
        for row_idx in range(0, row_size, vertex_spacing):
            temp = Vertex(points2d[col_idx][row_idx])
            temp.id = vert_id
            temp.uv = [u, v]
            vert_list.append(temp)
            vert_id += 1
            v += v_range
        vertices.append(vert_list)
        u += u_range

    v_col_size = len(vertices)
    v_row_size = len(vert_list)

    tri_id = 1
    forward = True
    triangles = []
    for col_idx in range(0, v_col_size - 1):
        row_idx = 0
        left_half = True
        tri_list = []
        while row_idx < v_row_size - 1:
            tri = Triangle()
            if left_half:
                tri.add_vertex(vertices[col_idx + 1][row_idx])
                tri.add_vertex(vertices[col_idx][row_idx])
                tri.add_vertex(vertices[col_idx][row_idx + 1])
                left_half = False
            else:
                tri.add_vertex(vertices[col_idx][row_idx + 1])
                tri.add_vertex(vertices[col_idx + 1][row_idx + 1])
                tri.add_vertex(vertices[col_idx + 1][row_idx])
                left_half = True
                row_idx += 1
            tri.id = tri_id
            tri_list.append(tri)
            tri_id += 1
        if forward:
            forward = False
        else:
            forward = True
            tri_list.reverse()
        triangles += tri_list

    return vertices, triangles


# Find parametric positions (u, v) of the face normals (center of mass of the triangle)
def make_obj_face_normals_uv(delta, vertex_spacing):
    if vertex_spacing <= 0 or delta <= 0:
        raise ValueError("Delta and vertex spacing cannot be less than and equal to zero")

    start_pos = 0.0
    end_pos = 1.0

    uv_list = []
    for u in utils.frange(start_pos, end_pos, delta * vertex_spacing):
        normal_u = u / 4
        for v in utils.frange(start_pos, end_pos, delta * vertex_spacing):
            normal_v = v / 4
            uv = [normal_u, normal_v]
            uv_list.append(uv)

    return uv_list
