"""
.. module:: elements
    :platform: Unix, Windows
    :synopsis: Classes representing geometry and topology elements

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from array import array
from . import utilities as utils


# Abstract class for geometry and topology elements
class AbstractElement(object):
    def __init__(self):
        self._id = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID value must be an integer")
        self._id = value


# Vertex class
class Vertex(AbstractElement):
    def __init__(self):
        super(Vertex, self).__init__()
        self._value = array('f', [0.0, 0.0, 0.0])
        self._uv = None
        self._inside = 1

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
            print("UV must have 2 components")
            return
        self._uv = array("d", list(value))

    @property
    def inside(self):
        return self._inside

    @inside.setter
    def inside(self, value):
        self._inside = value

    @property
    def data(self):
        return self._value.tolist()

    @data.setter
    def data(self, value):
        if len(value) == 3:
            raise ValueError("Vertex can only store 3 components")
        self._value = array('f', value)

    @property
    def data_full(self):
        ret_list = self.data
        ret_list.append(self._inside)
        return ret_list


# Triangle class
class Triangle(AbstractElement):
    def __init__(self):
        super(Triangle, self).__init__()
        self._vertices = []
        self._normal = None

    def __str__(self):
        return "Triangle " + str(self._id)

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
    def normal(self):
        if not self._normal:
            vec1 = utils.vector_generate(self._vertices[0].data, self._vertices[1].data)
            vec2 = utils.vector_generate(self._vertices[1].data, self._vertices[2].data)
            # self._normal = utils.vector_normalize(utils.vector_cross(vec1, vec2))
            self._normal = utils.vector_cross(vec1, vec2)
        return self._normal

    def add_vertex(self, vertex=None):
        if len(self._vertices) > 2:
            print("Cannot add more vertices")
            return
        if not isinstance(vertex, Vertex):
            print("Input must be a Vertex object")
            return
        self._vertices.append(vertex)

    @property
    def vertices(self):
        return self._vertices

    @property
    def vertex_ids(self):
        return [self._vertices[0].id, self._vertices[1].id, self._vertices[2].id]


# Face class
class Face(AbstractElement):
    def __init__(self):
        super(Face, self).__init__()
        self._triangles = []

    def __str__(self):
        return "Face " + str(self._id)

    __repr__ = __str__

    def __len__(self):
        return len(self._triangles)

    def __getitem__(self, key):
        return self._triangles[key]

    def __iter__(self):
        return iter(self._triangles)

    def __reversed__(self):
        return reversed(self._triangles)

    @property
    def triangles(self):
        return self._triangles

    def add_triangle(self, triangle):
        if not isinstance(triangle, Triangle):
            print("Input must be a Triangle object")
            return
        self._triangles.append(triangle)


# Body class
class Body(AbstractElement):
    def __init__(self):
        super(Body, self).__init__()
        self._faces = []

    def __str__(self):
        return "Body " + str(self._id)

    __repr__ = __str__

    def __len__(self):
        return len(self._faces)

    def __getitem__(self, key):
        return self._faces[key]

    def __iter__(self):
        return iter(self._faces)

    def __reversed__(self):
        return reversed(self._faces)

    @property
    def faces(self):
        return self._faces

    def add_face(self, face):
        if not isinstance(face, Face):
            print("Input must be a Face object")
            return
        self._faces.append(face)
