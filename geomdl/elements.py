"""
.. module:: elements
    :platform: Unix, Windows
    :synopsis: Provides classes representing geometry and topology elements

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import array


# Abstract class for geometry and topology elements (entities)
class AbstractElement(object):
    """ Abstract base class for all geometric entities. """
    def __init__(self):
        self._id = 0

    @property
    def id(self):
        """ Identifier for the geometric entity.

        It must be an integer number, otherwise the setter will raise a *ValueError*.

        :getter: Gets the identifier
        :setter: Sets the identifier
        """
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("Identifier value must be an integer")
        self._id = value


# Vertex class
class Vertex(AbstractElement):
    """ Representation of a 3-dimensional vertex entity with its parametric position. """
    def __init__(self):
        super(Vertex, self).__init__()
        self._value = array('f', [0.0, 0.0, 0.0, 0.0])  # x, y, z, 1.0 if inside is True
        self._uv = array('f', [0.0, 0.0])

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
        return iter(self.data)

    def __reversed__(self):
        return reversed(self._value)

    def __nonzero__(self):
        # For Python 2 compatibility
        return self.__bool__()

    def __bool__(self):
        # For Python 3 compatibility
        return self.inside

    @property
    def x(self):
        """ x-component of the vertex """
        return self._value[0]

    @x.setter
    def x(self, value):
        self._value[0] = value

    @property
    def y(self):
        """ y-component of the vertex """
        return self._value[1]

    @y.setter
    def y(self, value):
        self._value[1] = value

    @property
    def z(self):
        """ z-component of the vertex """
        return self._value[2]

    @z.setter
    def z(self, value):
        self._value[2] = value

    @property
    def u(self):
        """ Parametric u-component of the vertex """
        return self._uv[0]

    @u.setter
    def u(self, value):
        self._uv[0] = value

    @property
    def v(self):
        """ Parametric v-component of the vertex """
        return self._uv[1]

    @v.setter
    def v(self, value):
        self._uv[1] = value

    @property
    def uv(self):
        """ Parametric (u,v) pair of the vertex """
        return self._uv.tolist()

    @uv.setter
    def uv(self, value):
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            print("UV must have 2 components")
            return
        self._uv = array("d", list(value))

    @property
    def inside(self):
        """ Inside-outside flag """
        return bool(self._value[3])

    @inside.setter
    def inside(self, value):
        self._value[3] = value

    @property
    def data(self):
        """ (x,y,z) components of the vertex.

        :getter: Gets the 3-dimensional components
        :setter: Sets the 3-dimensional components
        """
        return self._value.tolist()[0:-1]

    @data.setter
    def data(self, value):
        if len(value) == 3:
            self._value = array('f', value + [0.0])
        else:
            raise ValueError("Vertex can only store 3 components")

    @property
    def data_full(self):
        """ (x,y,z,i) components of the vertex.

        (x,y,z) corresponds to 3-dimensional coordinate of the vertex. (i) value corresponds to inside-outside flag.

        :getter: Gets (x,y,z,i) components
        """
        return self._value.tolist()


# Triangle class
class Triangle(AbstractElement):
    """ Representation of a triangular geometric entity composed of vertices. """
    def __init__(self):
        super(Triangle, self).__init__()
        self._vertices = []

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
    def vertices(self):
        return self._vertices

    @property
    def vertices_raw(self):
        """ Returns the list of vertices that generates a closed triangle.

        :getter: List of vertices
        """
        v_raw = []
        for v in self._vertices:
            v_raw.append(v.data)
        # Add the first vertex data as a last element (for plotting modules)
        if len(self._vertices) > 0:
            v_raw.append(self._vertices[0].data)
        return v_raw

    @property
    def vertices_uv(self):
        data = self.vertices
        res = [data[idx].uv for idx in range(3)]
        return res

    @property
    def edges(self):
        data = self.vertices
        data.append(self.vertices[0])
        res = [[] for _ in range(3)]
        for idx in range(3):
            res[idx] = [data[idx], data[idx + 1]]
        return res

    @property
    def edges_raw(self):
        data = self.vertices_raw
        res = [[] for _ in range(3)]
        for idx in range(3):
            res[idx] = [data[idx], data[idx + 1]]
        return res

    @property
    def edges_uv(self):
        data = self.edges
        res = [[] for _ in range(3)]
        for idx in range(3):
            res[idx] = [data[idx][0].uv, data[idx][1].uv]
        return res

    @property
    def vertex_ids(self):
        """ Gets vertex number list.

        Vertex numbering starts from 1.
        """
        v_idx = []
        for v in self._vertices:
            v_idx.append(v.id)
        return v_idx

    @property
    def vertex_ids_zero(self):
        """ Gets zero-indexed vertex number list.

        Vertex numbering starts from 0.
        """
        v_idx = []
        for v in self._vertices:
            v_idx.append(v.id - 1)
        return v_idx

    @property
    def inside(self):
        res = [[] for _ in range(3)]
        for idx in range(3):
            res[idx] = self._vertices[idx].inside
        return all(res)

    def add_vertex(self, vertex):
        if len(self._vertices) > 2:
            raise ValueError("Cannot add more vertices")
        if isinstance(vertex, Vertex):
            self._vertices.append(vertex)
        elif isinstance(vertex, (list, tuple)):
            for elem in vertex:
                self.add_vertex(elem)
        else:
            raise TypeError("Input must be a Vertex object")


# Face class
class Face(AbstractElement):
    """ Representation of a face geometric entity composed of triangles. """
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
        if isinstance(triangle, Triangle):
            self._triangles.append(triangle)
        elif isinstance(triangle, (list, tuple)):
            for elem in triangle:
                self.add_triangle(elem)
        else:
            raise TypeError("Input must be a Triangle object")


# Body class
class Body(AbstractElement):
    """ Representation of a geometric body composed of faces. """
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
        if isinstance(face, Face):
            self._faces.append(face)
        elif isinstance(face, (list, tuple)):
            for elem in face:
                self.add_face(elem)
        else:
            raise TypeError("Input must be a Face object")
