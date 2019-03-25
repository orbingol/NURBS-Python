"""
.. module:: elements
    :platform: Unix, Windows
    :synopsis: Provides classes representing geometry and topology entities

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import copy
import abc
from .exceptions import GeomdlException
from . import _utilities as utl


@utl.add_metaclass(abc.ABCMeta)
class AbstractEntity(object):
    """ Abstract base class for all geometric entities. """
    def __init__(self, *args, **kwargs):
        self._name = "entity"  # object name
        self._id = int(kwargs.get('id', 0))  # object ID
        self._opt_data = dict()  # custom data dict
        self._cache = {}  # cache dict
        self._data = []  # data storage array

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

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._iter_index < len(self._data):
            result = self._data[self._iter_index]
            self._iter_index += 1
            return result
        raise StopIteration

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __reversed__(self):
        return reversed(self._data)

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
        # Don't copy the cache
        memo[id(self._cache)] = self._cache.__new__(dict)
        # Copy all other attributes
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __str__(self):
        return self.name + " " + str(self.id) + " " + str(self.data)

    __repr__ = __str__

    @property
    def id(self):
        """ Object ID (as an integer).

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the object ID
        :setter: Sets the object ID
        :type: int
        """
        return self._id

    @id.setter
    def id(self, value):
        self._id = int(value)

    @id.deleter
    def id(self):
        self._id = 0

    @property
    def name(self):
        """ Object name (as a string)

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the object name
        :setter: Sets the object name
        :type: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @name.deleter
    def name(self):
        self._name = ""

    @property
    def opt(self):
        """ Dictionary for storing custom data in the current geometry object.

        ``opt`` is a wrapper to a dict in *key => value* format, where *key* is string, *value* is any Python object.
        You can use ``opt`` property to store custom data inside the geometry object. For instance:

        .. code-block:: python

            geom.opt = ["face_id", 4]  # creates "face_id" key and sets its value to an integer
            geom.opt = ["contents", "data values"]  # creates "face_id" key and sets its value to a string
            print(geom.opt)  # will print: {'face_id': 4, 'contents': 'data values'}

            del geom.opt  # deletes the contents of the hash map
            print(geom.opt)  # will print: {}

            geom.opt = ["body_id", 1]  # creates "body_id" key  and sets its value to 1
            geom.opt = ["body_id", 12]  # changes the value of "body_id" to 12
            print(geom.opt)  # will print: {'body_id': 12}

            geom.opt = ["body_id", None]  # deletes "body_id"
            print(geom.opt)  # will print: {}

        :getter: Gets the dict
        :setter: Adds key and value pair to the dict
        :deleter: Deletes the contents of the dict
        """
        return self._opt_data

    @opt.setter
    def opt(self, key_value):
        if not isinstance(key_value, (list, tuple)):
            raise GeomdlException("opt input must be a list or a tuple")
        if len(key_value) != 2:
            raise GeomdlException("opt input must have a size of 2, corresponding to [0:key] => [1:value]")
        if not isinstance(key_value[0], str):
            raise GeomdlException("key must be string")

        if key_value[1] is None:
            self._opt_data.pop(*key_value)
        else:
            self._opt_data[key_value[0]] = key_value[1]

    @opt.deleter
    def opt(self):
        self._opt_data = dict()

    def opt_get(self, value):
        """ Safely query for the value from the :py:attr:`opt` property.

        :param value: a key in the :py:attr:`opt` property
        :type value: str
        :return: the corresponding value, if the key exists. ``None``, otherwise.
        """
        try:
            return self._opt_data[value]
        except KeyError:
            return None


@utl.export
class Vertex(AbstractEntity):
    """ 3-dimensional Vertex entity with spatial and parametric position. """
    def __init__(self, *args, **kwargs):
        super(Vertex, self).__init__(*args, **kwargs)
        self._name = "vertex"
        self.data = [float(arg) for arg in args] if args else [0.0, 0.0, 0.0]  # spatial coordinates
        self._uv = [0.0, 0.0]  # parametric coordinates
        self._opt_data['inside'] = False  # flag for trimming

    def __nonzero__(self):
        # For Python 2 compatibility
        return self.__bool__()

    def __bool__(self):
        # For Python 3 compatibility
        return self.opt_get("inside")

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise GeomdlException("Can only add Vertex objects")
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
            raise GeomdlException("Can only subtract Vertex objects")
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
            raise GeomdlException("Can only divide by a float or an integer")
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
            raise GeomdlException("UV data input must be a list or tuple")
        if len(value) != 2:
            raise GeomdlException("UV must have 2 components")
        self._uv = list(value)

    @property
    def inside(self):
        """ Inside-outside flag

        :getter: Gets the flag
        :setter: Sets the flag
        :type: bool
        """
        return self.opt_get("inside")

    @inside.setter
    def inside(self, value):
        self.opt = ["inside", bool(value)]

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
            raise GeomdlException("Vertex data must be a list or tuple")
        if len(value) != 3:
            raise GeomdlException("Vertex can only store 3 components")
        # Convert to float
        self._data = [float(val) for val in value]


@utl.export
class Triangle(AbstractEntity):
    """ Triangle entity which represents a triangle composed of vertices.

    A Triangle entity stores the vertices in its data structure. :attr:`data` returns the vertex IDs and :attr:`vertices`
    return the :class:`Vertex` instances that compose the triangular structure.
    """
    def __init__(self, *args, **kwargs):
        super(Triangle, self).__init__(*args, **kwargs)
        self._name = "triangle"
        self._opt_data['inside'] = False  # flag for trimming
        if args:
            self.add_vertex(*args)

    def __nonzero__(self):
        # For Python 2 compatibility
        return self.__bool__()

    def __bool__(self):
        # For Python 3 compatibility
        return self.opt_get("inside")

    @property
    def vertices(self):
        """ Vertices of the triangle

        :getter: Gets the list of vertices
        :type: tuple
        """
        return tuple(self._data)

    @property
    def vertices_closed(self):
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
    def edges(self):
        """ Edges of the triangle

        :getter: Gets the list of vertices that generates the edges of the triangle
        :type: list
        """
        data = self.vertices_closed
        res = [[] for _ in range(3)]
        for idx in range(3):
            res[idx] = [data[idx], data[idx + 1]]
        return res

    @property
    def vertex_ids(self):
        """ Vertex indices

        .. note:: Please use :attr:`data` instead of this property.

        :getter: Gets the vertex indices
        :type: list
        """
        return self.data

    @property
    def inside(self):
        """ Inside-outside flag

        :getter: Gets the flag
        :setter: Sets the flag
        :type: bool
        """
        return self.opt_get("inside")

    @inside.setter
    def inside(self, value):
        self.opt = ["inside", bool(value)]

    @property
    def data(self):
        """ Vertices composing the triangular structure.

        :getter: Gets the vertex indices (as int values)
        :setter: Sets the vertices (as Vertex objects)
        """
        return [v.id for v in self._data]

    @data.setter
    def data(self, value):
        if not isinstance(value, (list, tuple)):
            raise GeomdlException("Input must be a list or tuple")
        if len(value) != 3:
            raise GeomdlException("Triangle can only have 3 vertices")
        self.add_vertex(*value)

    def add_vertex(self, *args):
        """ Adds vertices to the Triangle object.

        This method takes a single or a list of vertices as its function arguments.
        """
        if len(self._data) > 2:
            raise GeomdlException("Cannot add more vertices")
        res = []
        for arg in args:
            if isinstance(arg, Vertex):
                res.append(arg)
            else:
                raise GeomdlException("Input must be a Vertex object")
        self._data = res


@utl.export
class Quad(AbstractEntity):
    """ Quad entity which represents a quadrilateral structure composed of vertices.

    A Quad entity stores the vertices in its data structure. :attr:`data` returns the vertex IDs and :attr:`vertices`
    return the :class:`Vertex` instances that compose the quadrilateral structure.
    """

    def __init__(self, *args, **kwargs):
        super(Quad, self).__init__(*args, **kwargs)
        self._name = "quad"
        if args:
            self.data = args

    @property
    def vertices(self):
        """ Vertices composing the quadrilateral structure.

        :getter: Gets the vertices
        """
        return tuple(self._data)

    @property
    def data(self):
        """ Vertices composing the quadrilateral structure.

        :getter: Gets the vertex indices (as int values)
        :setter: Sets the vertices (as Vertex objects)
        """
        return [v.id for v in self._data]

    @data.setter
    def data(self, value):
        if not isinstance(value, (list, tuple)):
            raise GeomdlException("Input must be a list or tuple")
        if len(value) != 4:
            raise GeomdlException("Quad can only have 4 vertices")
        self.add_vertex(*value)

    def add_vertex(self, *args):
        """ Adds vertices to the Quad object.

        This method takes a single or a list of vertices as its function arguments.
        """
        if len(self._data) > 3:
            raise GeomdlException("Cannot add more vertices")
        res = []
        for arg in args:
            if isinstance(arg, Vertex):
                res.append(arg)
            else:
                raise GeomdlException("Input must be a Vertex object")
        self._data = res


@utl.export
class Face(AbstractEntity):
    """ Representation of Face entity which is composed of triangles or quads. """
    def __init__(self, *args, **kwargs):
        super(Face, self).__init__(*args, **kwargs)
        self._name = "face"
        if args:
            self.add_triangle(*args)

    def __str__(self):
        return self.name + " " + str(self.id)

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
                raise GeomdlException("Input must be a Triangle object")
        self._data = res


@utl.export
class Body(AbstractEntity):
    """ Representation of Body entity which is composed of faces. """
    def __init__(self, *args, **kwargs):
        super(Body, self).__init__(*args, **kwargs)
        self._name = "body"
        if args:
            self.add_face(*args)

    def __str__(self):
        return self.name + " " + str(self.id)

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
                raise GeomdlException("Input must be a Face object")
        self._data = res
