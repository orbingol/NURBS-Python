"""
.. module:: base
    :platform: Unix, Windows
    :synopsis: Provides common base functionality for geomdl and its extensions

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>
.. moduleauthor:: Chris Horler

"""

import sys
import abc
import copy
from .six import add_metaclass

# Initialize an empty __all__ for controlling imports
__all__ = []

# Get Python version
_pyversion = sys.version_info[0]


def export(fn):
    """ Export decorator

    Please refer to the following SO article for details: https://stackoverflow.com/a/35710527
    """
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        mod.__all__.append(fn.__name__)
    else:
        mod.__all__ = [fn.__name__]
    return fn


@export
class GeomdlError(Exception):
    """ Custom exception for library-wide errors

    The error details can be retrieved by querying ``data`` class member. The following snippet illustrates a sample
    usage of this exception.

    .. code-example: python

        from geomdl.base import GeomdlError

        DEBUG = True

        # Catch exception
        try:
            # Do something which can raise this exception
        except GeomdlError as e:
            print(e)
            if DEBUG:
                print(e.data)
            # Stop execution of the function
            return
    """
    EXCEPTION_PREFIX = "GEOMDL ERROR: "

    def __init__(self, msg, data=None):
        super(GeomdlError, self).__init__(GeomdlError.EXCEPTION_PREFIX + msg)
        self.data = data


@export
class GeomdlWarning(Warning):
    """ Custom exception for library-wide warnings

    The warning details can be retrieved by querying ``data`` class member. The following snippet illustrates a sample
    usage of this exception.

    .. code-example: python

        from geomdl.base import GeomdlWarning

        DEBUG = True

        # Catch exception
        try:
            # Do something which can raise this exception
        except GeomdlWarning as e:
            print(e)
            if DEBUG:
                print(e.data)
            # Stop execution of the function
            return
    """
    EXCEPTION_PREFIX = "GEOMDL WARNING: "

    def __init__(self, msg, data=None):
        super(GeomdlWarning, self).__init__(GeomdlWarning.EXCEPTION_PREFIX + msg)
        self.data = data


class GeomdlFloat(float):
    """ A customizable float class """
    def __new__(cls, value):
        return float.__new__(cls, value)


class GeomdlDict(dict):
    """ A weak referencable dict class """


# Ref: https://stackoverflow.com/a/13259435/1162349
def notifylist_callback(func):
    """ Callback function for GeomdlNotifyList

    Contributed by Chris Horler.
    """
    def notify(self, *args, **kwargs):
        for _, callback in self.callbacks:
            callback()
        return func(self, *args, **kwargs)
    return notify


# Ref: https://stackoverflow.com/a/13259435/1162349
class GeomdlNotifyList(list):
    """ A list class with callback handlers for list modification

    Contributed by Chris Horler.
    """
    extend = notifylist_callback(list.extend)
    append = notifylist_callback(list.append)
    remove = notifylist_callback(list.remove)
    pop = notifylist_callback(list.pop)
    __delitem__ = notifylist_callback(list.__delitem__)
    __setitem__ = notifylist_callback(list.__setitem__)
    __iadd__ = notifylist_callback(list.__iadd__)
    __imul__ = notifylist_callback(list.__imul__)

    # Take care to return a new NotifyList if we slice it.
    if _pyversion < 3:
        __setslice__ = notifylist_callback(list.__setslice__)
        __delslice__ = notifylist_callback(list.__delslice__)

        def __getslice__(self, *args):
            return self.__class__(list.__getslice__(self, *args))

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__class__(list.__getitem__(self, item))
        return list.__getitem__(self, item)

    def __init__(self, *args):
        list.__init__(self, *args)
        self._callbacks = []
        self._callback_cntr = 0

    def register_callback(self, cb):
        self._callbacks.append((self._callback_cntr, cb))
        self._callback_cntr += 1
        return self._callback_cntr - 1

    def unregister_callback(self, cbid):
        for idx, (i, cb) in enumerate(self._callbacks):
            if i == cbid:
                self._callbacks.pop(idx)
                return cb
            return None

    @property
    def callbacks(self):
        return self._callbacks


class GeomdlList(object):
    """ A list-like container class which allows dynamically created attributes """
    __slots__ = ('_data', '_attribs', '_cb', '_cb_dynamic', '_iter_index')

    def __init__(self, *args, **kwargs):
        self._data = list(args)  # container object
        self._attribs = kwargs.get('attribs', tuple())  # dynamic attributes
        self._cb = kwargs.get('cb', [lambda: None])  # callbacks for setters
        self._cb_dynamic = kwargs.get('cbd', [lambda k, v: None])  # callbacks for dynamic atribute setters

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            result = self._data[self._iter_index]
        except IndexError:
            raise StopIteration
        self._iter_index += 1
        return result

    def __len__(self):
        return len(self._data)

    def __reversed__(self):
        return reversed(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        # Run callback functions
        for c in self._cb: c()
        for cd in self._cb_dynamic: cd(key, value)

    def __getattr__(self, name):
        try:
            idx = object.__getattribute__(self, '_attribs').index(name)
            return object.__getattribute__(self, '_data')[idx]
        except ValueError:
            raise AttributeError("'" + self.__class__.__name__ + "' object has no attribute '" + name + "'")
        except AttributeError:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in object.__getattribute__(self, '__slots__'):
            object.__setattr__(self, name, value)
        else:
            try:
                idx = object.__getattribute__(self, '_attribs').index(name)
                temp = object.__getattribute__(self, '_data')
                temp[idx] = value
                object.__setattr__(self, '_data', temp)
                # Run callback functions
                for c in self._cb: c()
                for cd in self._cb_dynamic: cd(name, value)
            except ValueError:
                raise AttributeError("'" + self.__class__.__name__ + "' object has no attribute '" + name + "'")

    @property
    def data(self):
        """ Elements of the list

        :getter: get the elements of the list
        :setter: set the elements of the list
        """
        return self._data

    @data.setter
    def data(self, val):
        if not isinstance(val, GeomdlTypeSequence):
            raise TypeError("Input for 'data' attribute should be a GeomdlTypeSequence")
        self._data = list(val)
        # Run callback function (no need to run callback functions for dynamic attributes)
        for c in self._cb: c()

    @property
    def attribs(self):
        """ Attributes of the list elements

        :getter: get the attributes
        :setter: set the attributes
        """
        return self._attribs

    @attribs.setter
    def attribs(self, val):
        if not isinstance(val, GeomdlTypeSequence):
            raise TypeError("Input for 'attribs' attribute should be a GeomdlTypeSequence")
        self._attribs = tuple(val)


@add_metaclass(abc.ABCMeta)
class GeomdlObject(object):
    """ Abstract base class for defining simple objects in geomdl

    This class provides the following properties:

    * :py:attr:`id`
    * :py:attr:`name`

    This class provides the following keyword arguments:

    * ``id``: object ID. *Default: 0*
    * ``name``: object name. *Default: name of the class*
    """
    __slots__ = ('_name', '_id', '_cfg', '_iter_index')

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', self.__class__.__name__)  # object name
        self._id = int(kwargs.get('id', 0))  # object ID
        self._cfg = GeomdlDict()  # dict for storing configuration variables

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._iter_index > 0:
            raise StopIteration
        self._iter_index += 1
        return self

    def __len__(self):
        return 1

    def __getitem__(self, index):
        return self

    def __copy__(self):
        # Create a new instance
        cls = self.__class__
        result = cls.__new__(cls)
        # Copy all attributes
        for var in self.__slots__:
            setattr(result, var, copy.copy(getattr(self, var)))
        # Return updated instance
        return result

    def __deepcopy__(self, memo):
        # Create a new instance
        cls = self.__class__
        result = cls.__new__(cls)
        # Don't copy self reference
        memo[id(self)] = result
        # Don't copy the cache
        memo[id(self._cache)] = self._cache.__new__(GeomdlDict)
        # Deep copy all other attributes
        for var in self.__slots__:
            setattr(result, var, copy.deepcopy(getattr(self, var), memo))
        # Return updated instance
        return result

    def __str__(self):
        return self.name

    __repr__ = __str__

    @property
    def id(self):
        """ Object ID (as an integer)

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
        self._name = str()


@add_metaclass(abc.ABCMeta)
class GeomdlBase(GeomdlObject):
    """ Abstract base class for defining geomdl objects

    This class provides the following properties:

    * :py:attr:`id`
    * :py:attr:`name`
    * :py:attr:`type`
    * :py:attr:`dimension`
    * :py:attr:`opt`

    This class provides the following methods:

    * :py:meth:`get_opt`
    * :py:meth:`reset`

    This class provides the following keyword arguments:

    * ``id``: object ID (as an integer). *Default: 0*
    * ``name``: object name. *Default: name of the class*
    """
    __slots__ = ('_dimension', '_geom_type', '_opt_data', '_cache')

    def __init__(self, *args, **kwargs):
        super(GeomdlBase, self).__init__(*args, **kwargs)
        self._dimension = 0  # spatial dimension
        self._geom_type = str()  # geometry type
        self._opt_data = GeomdlDict()  # dict for storing arbitrary data
        self._cache = GeomdlDict()  # cache dict

    @property
    def dimension(self):
        """ Spatial dimension

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the spatial dimension, e.g. 2D, 3D, etc.
        :type: int
        """
        return self._dimension

    @property
    def type(self):
        """ Geometry type

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the geometry type
        :type: str
        """
        return self._geom_type

    @property
    def opt(self):
        """ Dictionary for storing custom data in the current geometry object

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

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the dict
        :setter: Adds key and value pair to the dict
        :deleter: Deletes the contents of the dict
        """
        return self._opt_data

    @opt.setter
    def opt(self, key_value):
        if not isinstance(key_value, GeomdlTypeSequence):
            raise GeomdlError("opt input must be a GeomdlTypeSequence")
        if len(key_value) != 2:
            raise GeomdlError("opt input must have a size of 2, corresponding to [0:key] => [1:value]")
        if not isinstance(key_value[0], GeomdlTypeString):
            raise GeomdlError("key must be GeomdlTypeString")

        if key_value[1] is None:
            self._opt_data.pop(*key_value)
        else:
            self._opt_data[key_value[0]] = key_value[1]

    @opt.deleter
    def opt(self):
        self._opt_data = GeomdlDict()

    def get_opt(self, value):
        """ Safely query for the value from the :py:attr:`opt` property

        :param value: a key in the :py:attr:`opt` property
        :type value: str
        :return: the corresponding value, if the key exists. ``None``, otherwise.
        """
        try:
            return self._opt_data[value]
        except KeyError:
            return None

    def reset(self):
        """ Clears computed/generated data, such as caches """
        self._opt_data = GeomdlDict()
        self._cache = GeomdlDict()


@add_metaclass(abc.ABCMeta)
class GeomdlEvaluator(GeomdlObject):
    """ Abstract base class for implementations of fundamental algorithms

    This class provides the following properties:

    * :py:attr:`id`
    * :py:attr:`name`

    This class provides the following ABSTRACT methods:

    * :py:meth:`evaluate`
    * :py:meth:`derivatives_single`

    This class provides the following keyword arguments:

    * ``id``: object ID (as an integer). *Default: 0*
    * ``name``: object name. *Default: name of the class*
    """

    def __init__(self, *args, **kwargs):
        super(GeomdlEvaluator, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def evaluate(self, datadict, **kwargs):
        """ Abstract method for evaluation of points

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        """

    @abc.abstractmethod
    def derivatives(self, datadict, parpos, deriv_order=0, **kwargs):
        """ Abstract method for evaluation of the n-th order derivatives at the input parametric position

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :param parpos: parametric position where the derivatives will be computed
        :type parpos: list, tuple
        :param deriv_order: derivative order; to get the i-th derivative
        :type deriv_order: int
        """


# Following classes allows extensibility via registering additional input types.
@add_metaclass(abc.ABCMeta)
class GeomdlTypeSequence(object):
    """ Abstract base class for supported sequence types """


@add_metaclass(abc.ABCMeta)
class GeomdlTypeString(object):
    """ Abstract base class for supported string types """
