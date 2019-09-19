"""
.. module:: control_points
    :platform: Unix, Windows
    :synopsis: Provides helper classes for managing control points

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
import copy
from functools import reduce
from .exceptions import GeomdlException
from ._utilities import export, add_metaclass


@add_metaclass(abc.ABCMeta)
class AbstractManager(object):
    """ Abstract base class for control points manager classes.

    Control points manager class provides an easy way to set control points without knowing
    the internal data structure of the geometry classes. The manager class is initialized
    with the number of control points in all parametric dimensions.

    All classes extending this class should implement the following methods:

    * ``find_index``

    This class provides the following properties:

    * :py:attr:`ctrlpts`

    This class provides the following methods:

    * :py:meth:`get_ctrlpt`
    * :py:meth:`set_ctrlpt`
    * :py:meth:`get_ptdata`
    * :py:meth:`set_ptdata`
    """
    __slots__ = ('_size', '_num_ctrlpts', '_attachment', '_points', '_pt_data', '_cache', '_iter_index')

    def __init__(self, *args, **kwargs):
        self._size = [int(arg) for arg in args]  # size in all parametric dimensions
        self._num_ctrlpts = reduce(lambda x, y: x *y, self._size)  # number of control points
        self._attachment = kwargs if kwargs else dict()  # data attached to the control points
        self._points = list()  # list of control points
        self._pt_data = dict()  # dict containing lists of additional data attached to the control points
        self._cache = {}
        self.reset()  # initialize control points list

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
        memo[id(self._cache)] = self._cache.__new__(dict)
        # Deep copy all other attributes
        for var in self.__slots__:
            setattr(result, var, copy.deepcopy(getattr(self, var), memo))
        # Return updated instance
        return result

    @property
    def ctrlpts(self):
        """ Control points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._points

    @ctrlpts.setter
    def ctrlpts(self, value):
        self._points = value

    def reset(self):
        """ Resets/initializes the internal control points array. """
        self._points[:] = [[] for _ in range(self._num_ctrlpts)]
        for k, v in self._attachment.items():
            if v > 1:
                self._pt_data[k] = [[0.0 for _ in range(v)] for _ in range(self._num_ctrlpts)]
            else:
                self._pt_data[k] = [0.0 for _ in range(self._num_ctrlpts)]

    def get_ctrlpt(self, *args):
        """ Gets the control point from the given location in the array. """
        # Find the index
        idx = self.find_index(*args)
        # Return the control point
        try:
            return self._points[idx]
        except IndexError:
            return None

    def set_ctrlpt(self, pt, *args):
        """ Puts the control point to the given location in the array.

        :param pt: control point
        :type pt: list, tuple
        """
        if not isinstance(pt, (list, tuple)):
            raise GeomdlException("'pt' argument should be a list or tuple")
        if len(args) != len(self._size):
            raise GeomdlException("Input dimensions are not compatible with the geometry")
        # Find the index
        idx = self.find_index(*args)
        # Set control point
        try:
            self._points[idx] = pt
        except IndexError:
            raise GeomdlException("Index is out of range")

    def get_ptdata(self, dkey, *args):
        """ Gets the data attached to the control point.

        :param dkey: key of the attachment dictionary
        :param dkey: str
        """
        # Find the index
        idx = self.find_index(*args)
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
        idx = self.find_index(*args)
        # Attach the data to the control point
        try:
            for k, val in adct.items():
                if k in self._pt_data:
                    if isinstance(val, (list, tuple)):
                        for j, v in enumerate(val):
                            self._pt_data[k][idx][j] = v
                    else:
                        self._pt_data[k][idx] = val
                else:
                    raise GeomdlException("Invalid key: " + str(k))
        except IndexError:
            raise GeomdlException("Index is out of range")

    @abc.abstractmethod
    def find_index(self, *args):
        """ Finds the array index from the given parametric positions.

        .. note::

            This is an abstract method and it must be implemented in the subclass.
        """
        return 0


class CurveManager(AbstractManager):
    """ Curve control points manager.

    Control points manager class provides an easy way to set control points without knowing
    the internal data structure of the geometry classes. The manager class is initialized
    with the number of control points in all parametric dimensions.

    B-spline curves are defined in one parametric dimension. Therefore, this manager class
    should be initialized with a single integer value.

    .. code-block:: python

        # Assuming that the curve has 10 control points
        manager = CurveManager(10)

    Getting the control points:

    .. code-block:: python

        # Number of control points in all parametric dimensions
        size_u = spline.ctrlpts_size_u

        # Generate control points manager
        cpt_manager = control_points.SurfaceManager(size_u)
        cpt_manager.ctrlpts = spline.ctrlpts

        # Control points array to be used externally
        control_points = []

        # Get control points from the spline geometry
        for u in range(size_u):
            pt = cpt_manager.get_ctrlpt(u)
            control_points.append(pt)

    Setting the control points:

    .. code-block:: python

        # Number of control points in all parametric dimensions
        size_u = 5

        # Create control points manager
        points = control_points.SurfaceManager(size_u)

        # Set control points
        for u in range(size_u):
            # 'pt' is the control point, e.g. [10, 15, 12]
            points.set_ctrlpt(pt, u, v)

        # Create spline geometry
        curve = BSpline.Curve()

        # Set control points
        curve.ctrlpts = points.ctrlpts
    """
    def __init__(self, *args, **kwargs):
        super(CurveManager, self).__init__(*args, **kwargs)

    def find_index(self, *args):
        super(CurveManager, self).find_index(*args)
        return args[0]


class SurfaceManager(AbstractManager):
    """ Surface control points manager.

    Control points manager class provides an easy way to set control points without knowing
    the internal data structure of the geometry classes. The manager class is initialized
    with the number of control points in all parametric dimensions.

    B-spline surfaces are defined in one parametric dimension. Therefore, this manager class
    should be initialized with two integer values.

    .. code-block:: python

        # Assuming that the surface has size_u = 5 and size_v = 7 control points
        manager = SurfaceManager(5, 7)

    Getting the control points:

    .. code-block:: python

        # Number of control points in all parametric dimensions
        size_u = spline.ctrlpts_size_u
        size_v = spline.ctrlpts_size_v

        # Generate control points manager
        cpt_manager = control_points.SurfaceManager(size_u, size_v)
        cpt_manager.ctrlpts = spline.ctrlpts

        # Control points array to be used externally
        control_points = []

        # Get control points from the spline geometry
        for u in range(size_u):
            for v in range(size_v):
                pt = cpt_manager.get_ctrlpt(u, v)
                control_points.append(pt)

    Setting the control points:

    .. code-block:: python

        # Number of control points in all parametric dimensions
        size_u = 5
        size_v = 3

        # Create control points manager
        points = control_points.SurfaceManager(size_u, size_v)

        # Set control points
        for u in range(size_u):
            for v in range(size_v):
                # 'pt' is the control point, e.g. [10, 15, 12]
                points.set_ctrlpt(pt, u, v)

        # Create spline geometry
        surf = BSpline.Surface()

        # Set control points
        surf.ctrlpts = points.ctrlpts
    """
    def __init__(self, *args, **kwargs):
        super(SurfaceManager, self).__init__(*args, **kwargs)

    def find_index(self, *args):
        super(SurfaceManager, self).find_index(*args)
        return args[1] + (args[0] * self._size[1])


class VolumeManager(AbstractManager):
    """ Volume control points manager.

    Control points manager class provides an easy way to set control points without knowing
    the internal data structure of the geometry classes. The manager class is initialized
    with the number of control points in all parametric dimensions.

    B-spline volumes are defined in one parametric dimension. Therefore, this manager class
    should be initialized with there integer values.

    .. code-block:: python

        # Assuming that the volume has size_u = 5, size_v = 12 and size_w = 3 control points
        manager = VolumeManager(5, 12, 3)

    Gettting the control points:

    .. code-block:: python

        # Number of control points in all parametric dimensions
        size_u = spline.ctrlpts_size_u
        size_v = spline.ctrlpts_size_v
        size_w = spline.ctrlpts_size_w

        # Generate control points manager
        cpt_manager = control_points.SurfaceManager(size_u, size_v, size_w)
        cpt_manager.ctrlpts = spline.ctrlpts

        # Control points array to be used externally
        control_points = []

        # Get control points from the spline geometry
        for u in range(size_u):
            for v in range(size_v):
                for w in range(size_w):
                    pt = cpt_manager.get_ctrlpt(u, v, w)
                    control_points.append(pt)

    Setting the control points:

    .. code-block:: python

        # Number of control points in all parametric dimensions
        size_u = 5
        size_v = 3
        size_w = 2

        # Create control points manager
        points = control_points.VolumeManager(size_u, size_v, size_w)

        # Set control points
        for u in range(size_u):
            for v in range(size_v):
                for w in range(size_w):
                    # 'pt' is the control point, e.g. [10, 15, 12]
                    points.set_ctrlpt(pt, u, v, w)

        # Create spline geometry
        volume = BSpline.Volume()

        # Set control points
        volume.ctrlpts = points.ctrlpts
    """
    def __init__(self, *args, **kwargs):
        super(VolumeManager, self).__init__(*args, **kwargs)

    def find_index(self, *args):
        super(VolumeManager, self).find_index(*args)
        return args[1] + (args[0] * self._size[1]) + (args[2] * self._size[0] * self._size[1])
