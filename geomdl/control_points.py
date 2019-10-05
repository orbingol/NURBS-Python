"""
.. module:: control_points
    :platform: Unix, Windows
    :synopsis: Provides helper classes for managing control points

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from functools import reduce
from .base import GeomdlDict, GeomdlTypeSequence, GeomdlError, export

# Parametric dimension names for dynamical generation of the attributes
GEOMDL_PDIM_ATTRS = GeomdlDict(size_u=0, size_v=1, size_w=2)

# Initialize an empty __all__ for controlling imports
__all__ = []


def default_ctrlpts_init(num_ctrlpts, **kwargs):
    """ Default control points initialization function.

    :param num_ctrlpts: total number of control points
    :type num_ctrlpts: int
    :return: a tuple containing initialized control points (as a ``list``) and data dictionary (as a ``dict``)
    :rtype: tuple
    """
    points = [[] for _ in range(num_ctrlpts)]
    points_data = GeomdlDict()
    for k, v in kwargs.items():
        if v > 1:
            points_data[k] = [[0.0 for _ in range(v)] for _ in range(num_ctrlpts)]
        else:
            points_data[k] = [0.0 for _ in range(num_ctrlpts)]
    return points, points_data


def default_ctrlpts_set(pts_in, dim, pts_out):
    """ Default control points set function.

    :param pts_in: input list of control points
    :type pts_in: list, tuple
    :param dim: spatial dimension
    :type dim: int
    :param pts_out: output list of control points
    :type pts_out: list
    :return: ``pts_out`` will be returned
    :rtype: list
    """
    for idx, cpt in enumerate(pts_in):
        if not isinstance(cpt, GeomdlTypeSequence):
            raise GeomdlError("input[" + str(idx) + "] not valid. Must be a sequence.")
        if len(cpt) != dim:
            raise GeomdlError(str(cpt) + " not valid. Must be a " + str(dim) + "-dimensional list.")
        # Convert to list of floats
        pts_out[idx] = [float(coord) for coord in cpt]
    return pts_out


@export
class CPManager(object):
    """ Control points manager class.

    Control points manager class provides an easy way to set control points without knowing
    the internal data structure of the geometry classes. The manager class is initialized
    with the number of control points in all parametric dimensions.

    This class provides the following properties:

    * :py:attr:`points`
    * :py:attr:`points_data`
    * :py:attr:`size`
    * :py:attr:`count`
    * :py:attr:`dimension`

    This class provides the following methods:

    * :py:meth:`get_ctrlpt`
    * :py:meth:`set_ctrlpt`
    * :py:meth:`get_ptdata`
    * :py:meth:`set_ptdata`
    * :py:meth:`reset`
    """
    __slots__ = ('_idt', '_pt_data', '_cache', '_func_init', '_func_set', '_iter_index')

    def __init__(self, *args, **kwargs):
        # Define control points initialization function
        self._func_init = kwargs.pop('ctrlpts_init_function', default_ctrlpts_init)
        # Define control points initialization function
        self._func_set = kwargs.pop('ctrlpts_set_function', default_ctrlpts_set)
        # Start constructing the internal data structures
        self._idt = GeomdlDict(
            size=tuple([int(arg) for arg in args]),  # size in all parametric dimensions
        )
        self._idt['count'] = reduce(lambda x, y: x * y, self.size)  # total number of control points
        # Initialize control points
        self._idt['control_points'], self._pt_data = self._func_init(self.count, **kwargs)
        # Set spatial dimension
        self._idt['dimension'] = int(kwargs.pop('ctrlpts_dimension', 0))
        # Initialize cache
        self._cache = GeomdlDict()

    def __call__(self, pdim=-1):
        if pdim < 0:
            return self.points

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            result = self._points[self._iter_index]
        except IndexError:
            raise StopIteration
        self._iter_index += 1
        return result

    def __len__(self):
        return len(self._points)

    def __reversed__(self):
        return reversed(self._points)

    def __getitem__(self, idx):
        return self._points[idx]

    def __setitem__(self, idx, val):
        self._points[idx] = val

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

    def __getattr__(self, attr):
        if attr in GEOMDL_PDIM_ATTRS:
            try:
                return self.size[GEOMDL_PDIM_ATTRS[attr]]
            except IndexError:
                raise AttributeError(attr)
        if attr not in self.__slots__:
            raise AttributeError(attr)
        return self.__slots__[attr]

    def _find_index(self, *args):
        """ Finds the array index from the given parametric positions."""
        idx = 0
        for i, arg in enumerate(args):
            mul_res = 1
            if i > 0:
                for j in self._size[:i]:
                    mul_res *= j
            idx += arg * mul_res
        return idx

    @property
    def dimension(self):
        """ Spatial dimension of the control points.

        :getter: Gets the spatial dimension
        """
        return self._idt['dimension']

    @property
    def points(self):
        """ Control points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return tuple(self._idt['control_points'])

    @points.setter
    def points(self, value):
        # Check input type
        if not isinstance(value, GeomdlTypeSequence):
            raise GeomdlError("Control points input must be a sequence")
        # Check input length
        if len(value) != self.count:
            raise GeomdlError("Number of control points must be " + str(self.count))
        # Determine dimension, if required
        if self.dimension < 1:
            self._idt['dimension'] = len(value[0])
        # Set control points
        self._func_set(value, self.dimension, self._idt['control_points'])

    @property
    def points_data(self):
        return self._pt_data

    @property
    def size(self):
        """ Number of the control points in all parametric dimensions.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the number of the control points (as a ``tuple``)
        """
        return self._idt['size']

    @property
    def count(self):
        """ Total number of the control points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the total number of the control points (as an ``int``)
        """
        return self._idt['count']

    def reset(self, **kwargs):
        """ Resets the control points and the attached data contents """
        self._func_init(self.count, **kwargs)

    def get_ctrlpt(self, *args):
        """ Gets the control point from the input position. """
        # Find the index
        idx = self._find_index(*args)
        # Return the control point
        try:
            return tuple(self._idt['control_points'][idx])
        except IndexError:
            return None

    def set_ctrlpt(self, pt, *args):
        """ Puts the control point to the input position.

        :param pt: control point
        :type pt: list, tuple
        """
        if not isinstance(pt, GeomdlTypeSequence):
            raise GeomdlError("'pt' argument should be a list or tuple")
        if len(args) != len(self.size):
            raise GeomdlError("Input dimensions are not compatible with the geometry")
        # Find the index
        idx = self._find_index(*args)
        # Set control point
        try:
            self._idt['control_points'][idx] = pt
        except IndexError:
            raise GeomdlError("Index is out of range")

    def get_ptdata(self, dkey, *args):
        """ Gets the data attached to the control point.

        :param dkey: key of the attachment dictionary
        :param dkey: str
        """
        # Find the index
        idx = self._find_index(*args)
        # Return the attached data
        try:
            return self._pt_data[dkey][idx]
        except IndexError:
            return None
        except KeyError:
            return None

    def set_ptdata(self, adct, *args):
        """ Attaches the data to the control point.

        :param adct: attachment dictionary
        :param adct: dict
        """
        # Find the index
        idx = self._find_index(*args)
        # Attach the data to the control point
        try:
            for k, val in adct.items():
                if k in self._pt_data:
                    if isinstance(val, GeomdlTypeSequence):
                        for j, v in enumerate(val):
                            self._pt_data[k][idx][j] = v
                    else:
                        self._pt_data[k][idx] = val
                else:
                    raise GeomdlError("Invalid key: " + str(k))
        except IndexError:
            raise GeomdlError("Index is out of range")
