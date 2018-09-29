"""
.. module:: elements
    :platform: Unix, Windows
    :synopsis: Provides classes representing geometry and topology elements

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import copy


# Abstract class for geometry and topology elements (entities)
class AbstractElement(object):
    """ Abstract base class for all geometric entities. """
    def __init__(self):
        self._id = 0  # element ID
        self._data = []  # data storage array

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
        self._data = [0.0, 0.0, 0.0]  # spatial coordinates
        self._uv = [0.0, 0.0]  # parametric coordinates
        self._inside = False  # flag for trimming

    def __str__(self):
        return "Vertex " + str(self._id) + " " + str(self._data)

    __repr__ = __str__

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

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self.data)

    def __reversed__(self):
        return reversed(self._data)

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
        """ x-component of the vertex """
        return self._data[0]

    @x.setter
    def x(self, value):
        self._data[0] = float(value)

    @property
    def y(self):
        """ y-component of the vertex """
        return self._data[1]

    @y.setter
    def y(self, value):
        self._data[1] = float(value)

    @property
    def z(self):
        """ z-component of the vertex """
        return self._data[2]

    @z.setter
    def z(self, value):
        self._data[2] = float(value)

    @property
    def u(self):
        """ Parametric u-component of the vertex """
        return self._uv[0]

    @u.setter
    def u(self, value):
        self._uv[0] = float(value)

    @property
    def v(self):
        """ Parametric v-component of the vertex """
        return self._uv[1]

    @v.setter
    def v(self, value):
        self._uv[1] = float(value)

    @property
    def uv(self):
        """ Parametric (u,v) pair of the vertex """
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
        """ Inside-outside flag """
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
        self._data = list(value)


# Triangle class
class Triangle(AbstractElement):
    """ Representation of a triangular geometric entity composed of vertices. """
    def __init__(self):
        super(Triangle, self).__init__()
        self._inside = False  # flag for trimming

    def __str__(self):
        return "Triangle " + str(self._id)

    __repr__ = __str__

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
    def vertices(self):
        return tuple(self._data)

    @property
    def vertices_raw(self):
        """ Returns the list of vertices that generates a closed triangle.

        :getter: List of vertices
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
        data = self.vertices
        res = [data[idx].uv for idx in range(3)]
        return res

    @property
    def edges(self):
        data = self.vertices
        res = [[] for _ in range(3)]
        for idx in range(3):
            if idx == 2:
                lv = 0
            else:
                lv = idx + 1
            res[idx] = [data[idx], data[lv]]
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
        for v in self._data:
            v_idx.append(v.id)
        return v_idx

    @property
    def vertex_ids_zero(self):
        """ Gets zero-indexed vertex number list.

        Vertex numbering starts from 0.
        """
        v_idx = []
        for v in self._data:
            v_idx.append(v.id - 1)
        return v_idx

    @property
    def inside(self):
        return self._inside

    @inside.setter
    def inside(self, value):
        self._inside = bool(value)

    def add_vertex(self, *args):
        if len(self._data) > 2:
            raise ValueError("Cannot add more vertices")
        res = []
        for arg in args:
            if isinstance(arg, Vertex):
                res.append(arg)
            else:
                raise TypeError("Input must be a Vertex object")
        self._data = res


# Face class
class Face(AbstractElement):
    """ Representation of a face geometric entity composed of triangles. """
    def __init__(self):
        super(Face, self).__init__()

    def __str__(self):
        return "Face " + str(self._id)

    __repr__ = __str__

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
    def triangles(self):
        return tuple(self._data)

    def add_triangle(self, *args):
        res = []
        for arg in args:
            if isinstance(arg, Triangle):
                res.append(arg)
            else:
                raise TypeError("Input must be a Triangle object")
        self._data = res


# Body class
class Body(AbstractElement):
    """ Representation of a geometric body composed of faces. """
    def __init__(self):
        super(Body, self).__init__()

    def __str__(self):
        return "Body " + str(self._id)

    __repr__ = __str__

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
    def faces(self):
        return tuple(self._data)

    def add_face(self, *args):
        res = []
        for arg in args:
            if isinstance(arg, Face):
                res.append(arg)
            else:
                raise TypeError("Input must be a Face object")
        self._data = res
