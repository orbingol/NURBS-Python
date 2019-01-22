"""
.. module:: elements
    :platform: Unix, Windows
    :synopsis: Provides classes representing geometry and topology entities

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
import copy
import six
from ._utilities import export


@six.add_metaclass(abc.ABCMeta)
class AbstractEntity(object):
    """ Abstract base class for all geometric entities. """
    def __init__(self, *args, **kwargs):
        self._id = int(kwargs.get('id', 0))  # element identifier
        self._data = []  # data storage array

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        # Don't copy self reference
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        # Copy all other attributes
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __reversed__(self):
        return reversed(self._data)

    @property
    def id(self):
        """ Identifier for the geometric entity.

        It must be an integer number, otherwise the setter will raise a *ValueError*.

        :getter: Gets the identifier
        :setter: Sets the identifier
        :type: int
        """
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("Identifier value must be an integer")
        self._id = value


@export
class Vertex(AbstractEntity):
    """ 3-dimensional Vertex entity with spatial and parametric position. """
    def __init__(self, *args, **kwargs):
        super(Vertex, self).__init__(*args, **kwargs)
        self.data = [float(arg) for arg in args] if args else [0.0, 0.0, 0.0]  # spatial coordinates
        self._uv = [0.0, 0.0]  # parametric coordinates
        self._inside = False  # flag for trimming

    def __str__(self):
        return "Vertex " + str(self._id) + " " + str(self._data)

    __repr__ = __str__

    def __cmp__(self, other):
        return (self.id > other.id) - (self.id < other.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __nonzero__(self):
        # For Python 2 compatibility
        return self.__bool__()

    def __bool__(self):
        # For Python 3 compatibility
        return self.inside

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Can only add Vertex objects")
        res_data = [0.0 for _ in range(3)]
        for idx in range(3):
            res_data[idx] = self.data[idx] + other.data[idx]
        res_uv = [0.0 for _ in range(2)]
        for idx in range(2):
            res_uv[idx] = self.uv[idx] + other.uv[idx]
        res_val = self.__class__()
        res_val.data = res_data
        res_val.uv = res_uv
        return res_val

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Can only subtract Vertex objects")
        res_data = [0.0 for _ in range(3)]
        for idx in range(3):
            res_data[idx] = self.data[idx] - other.data[idx]
        res_uv = [0.0 for _ in range(2)]
        for idx in range(2):
            res_uv[idx] = self.uv[idx] - other.uv[idx]
        res_val = self.__class__()
        res_val.data = res_data
        res_val.uv = res_uv
        return res_val

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        if not isinstance(other, (float, int)):
            raise TypeError("Can only divide by a float or an integer")
        res_data = [0.0 for _ in range(3)]
        for idx in range(3):
            res_data[idx] = self.data[idx] / float(other)
        res_uv = [0.0 for _ in range(2)]
        for idx in range(2):
            res_uv[idx] = self.uv[idx] / float(other)
        res_val = self.__class__()
        res_val.data = res_data
        res_val.uv = res_uv
        return res_val

    @property
    def x(self):
        """ x-component of the vertex

        :getter: Gets the x-component of the vertex
        :setter: Sets the x-component of the vertex
        :type: float
        """
        return self._data[0]

    @x.setter
    def x(self, value):
        self._data[0] = float(value)

    @property
    def y(self):
        """ y-component of the vertex

        :getter: Gets the y-component of the vertex
        :setter: Sets the y-component of the vertex
        :type: float
        """
        return self._data[1]

    @y.setter
    def y(self, value):
        self._data[1] = float(value)

    @property
    def z(self):
        """ z-component of the vertex

        :getter: Gets the z-component of the vertex
        :setter: Sets the z-component of the vertex
        :type: float
        """
        return self._data[2]

    @z.setter
    def z(self, value):
        self._data[2] = float(value)

    @property
    def u(self):
        """ Parametric u-component of the vertex

        :getter: Gets the u-component of the vertex
        :setter: Sets the u-component of the vertex
        :type: float
        """
        return self._uv[0]

    @u.setter
    def u(self, value):
        self._uv[0] = float(value)

    @property
    def v(self):
        """ Parametric v-component of the vertex

        :getter: Gets the v-component of the vertex
        :setter: Sets the v-component of the vertex
        :type: float
        """
        return self._uv[1]

    @v.setter
    def v(self, value):
        self._uv[1] = float(value)

    @property
    def uv(self):
        """ Parametric (u,v) pair of the vertex

        :getter: Gets the uv-component of the vertex
        :setter: Sets the uv-component of the vertex
        :type: list, tuple
        """
        return tuple(self._uv)

    @uv.setter
    def uv(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError("UV data input must be a list or tuple")
        if len(value) != 2:
            raise ValueError("UV must have 2 components")
        self._uv = list(value)

    @property
    def inside(self):
        """ Inside-outside flag

        :getter: Gets the flag
        :setter: Sets the flag
        :type: bool
        """
        return self._inside

    @inside.setter
    def inside(self, value):
        self._inside = bool(value)

    @property
    def data(self):
        """ (x,y,z) components of the vertex.

        :getter: Gets the 3-dimensional components
        :setter: Sets the 3-dimensional components
        """
        return tuple(self._data)

    @data.setter
    def data(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError("Vertex data must be a list or tuple")
        if len(value) != 3:
            raise ValueError("Vertex can only store 3 components")
        # Convert to float
        self._data = [float(val) for val in value]


@export
class Triangle(AbstractEntity):
    """ Triangle entity which represents a triangle composed of vertices. """
    def __init__(self, *args, **kwargs):
        super(Triangle, self).__init__(*args, **kwargs)
        self._inside = False  # flag for trimming
        if args:
            self.add_vertex(*args)

    def __str__(self):
        return "Triangle " + str(self._id)

    __repr__ = __str__

    @property
    def vertices(self):
        """ Vertices of the triangle

        :getter: Gets the list of vertices
        :type: tuple
        """
        return tuple(self._data)

    @property
    def vertices_raw(self):
        """ Vertices which generates a closed triangle

        Adds the first vertex as a last element of the return value (good for plotting)

        :getter: Gets the list of vertices
        :type: list
        """
        v_raw = []
        for v in self._data:
            v_raw.append(v.data)
        # Add the first vertex data as a last element (for plotting modules)
        if len(self._data) > 0:
            v_raw.append(self._data[0].data)
        return v_raw

    @property
    def vertices_uv(self):
        """ Parametric coordinates of the triangle vertices

        :getter: Gets the parametric coordinates of the vertices
        :type: list
        """
        data = self.vertices
        res = [data[idx].uv for idx in range(3)]
        return res

    @property
    def edges(self):
        """ Edges of the triangle

        :getter: Gets the list of vertices that generates the edges of the triangle
        :type: list
        """
        data = self.vertices_raw
        res = [[] for _ in range(3)]
        for idx in range(3):
            res[idx] = [data[idx], data[idx + 1]]
        return res

    @property
    def vertex_ids(self):
        """ Vertex indices

        Vertex numbering starts from 1.

        :getter: Gets the vertex indices
        :type: list
        """
        v_idx = []
        for v in self._data:
            v_idx.append(v.id)
        return v_idx

    @property
    def vertex_ids_zero(self):
        """ Zero-indexed vertex indices

        Vertex numbering starts from 0.

        :getter: Gets the vertex indices
        :type: list
        """
        v_idx = []
        for v in self._data:
            v_idx.append(v.id - 1)
        return v_idx

    @property
    def inside(self):
        """ Inside-outside flag

        :getter: Gets the flag
        :setter: Sets the flag
        :type: bool
        """
        return self._inside

    @inside.setter
    def inside(self, value):
        self._inside = bool(value)

    def add_vertex(self, *args):
        """ Adds vertices to the Triangle object.

        This method takes a single or a list of vertices as its function arguments.
        """
        if len(self._data) > 2:
            raise ValueError("Cannot add more vertices")
        res = []
        for arg in args:
            if isinstance(arg, Vertex):
                res.append(arg)
            else:
                raise TypeError("Input must be a Vertex object")
        self._data = res


@export
class Quad(AbstractEntity):
    """ Quad entity which represents a quadrilateral structure composed of vertices. """

    def __init__(self, *args, **kwargs):
        super(Quad, self).__init__(*args, **kwargs)
        if args:
            self.data = args

    def __str__(self):
        return "Quad " + str(self._id) + " V: " + str(self._data)

    __repr__ = __str__

    @property
    def data(self):
        """ Vertex indices.

        :getter: Gets the vertex indices
        :setter: Sets the vertex indices
        """
        return tuple(self._data)

    @data.setter
    def data(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError("Input data must be a list or tuple")
        if len(value) != 4:
            raise ValueError("Quad can only have 4 vertices")
        # Convert to int
        self._data = [int(val) for val in value]

    def add_vertex(self, *args):
        """ Adds vertices to the Quad object.

        This method takes a single or a list of vertices as its function arguments.
        """
        if len(self._data) > 3:
            raise ValueError("Cannot add more vertices")
        res = []
        for arg in args:
            if isinstance(arg, Vertex):
                res.append(arg.id)
            else:
                raise TypeError("Input must be a Vertex object")
        self._data = res


@export
class Face(AbstractEntity):
    """ Representation of Face entity which is composed of triangles or quads. """
    def __init__(self, *args, **kwargs):
        super(Face, self).__init__(*args, **kwargs)
        if args:
            self.add_triangle(*args)

    def __str__(self):
        return "Face " + str(self._id)

    __repr__ = __str__

    @property
    def triangles(self):
        """ Triangles of the face

        :getter: Gets the list of triangles
        :type: tuple
        """
        return tuple(self._data)

    def add_triangle(self, *args):
        """ Adds triangles to the Face object.

        This method takes a single or a list of triangles as its function arguments.
        """
        res = []
        for arg in args:
            if isinstance(arg, Triangle):
                res.append(arg)
            else:
                raise TypeError("Input must be a Triangle object")
        self._data = res


@export
class Body(AbstractEntity):
    """ Representation of Body entity which is composed of faces. """
    def __init__(self, *args, **kwargs):
        super(Body, self).__init__(*args, **kwargs)
        if args:
            self.add_face(*args)

    def __str__(self):
        return "Body " + str(self._id)

    __repr__ = __str__

    @property
    def faces(self):
        """ Faces of the body

        :getter: Gets the list of faces
        :type: tuple
        """
        return tuple(self._data)

    def add_face(self, *args):
        """ Adds faces to the Body object.

        This method takes a single or a list of faces as its function arguments.
        """
        res = []
        for arg in args:
            if isinstance(arg, Face):
                res.append(arg)
            else:
                raise TypeError("Input must be a Face object")
        self._data = res
