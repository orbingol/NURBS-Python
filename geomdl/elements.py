"""
.. module:: elements
    :platform: Unix, Windows
    :synopsis: Classes representing the geometry and topology elements

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

    def __len__(self):
        return len(self._value)

    def __getitem__(self, key):
        return self._value[key]

    def __setitem__(self, key, value):
        self._value[key] = value

    def __delitem__(self, key):
        del self._value[key]

    def __iter__(self):
        return iter(self._value)

    def __reversed__(self):
        return reversed(self._value)

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

    def __len__(self):
        return len(self._vertices)

    def __getitem__(self, key):
        return self._vertices[key]

    def __iter__(self):
        return iter(self._vertices)

    def __reversed__(self):
        return reversed(self._vertices)

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
            # self._normal = utils.vector_normalize(utils.vector_cross(vec1, vec2))
            self._normal = utils.vector_cross(vec1, vec2)
        return self._normal

    def add_vertex(self, vertex=None):
        if len(self._vertices) > 2:
            raise ValueError("Cannot add more vertices")
        if not isinstance(vertex, Vertex):
            raise ValueError("Input must be a Vertex object")
        self._vertices.append(vertex)

    @property
    def vertices(self):
        return self._vertices

    @property
    def vertex_ids(self):
        return [self._vertices[0].id, self._vertices[1].id, self._vertices[2].id]
