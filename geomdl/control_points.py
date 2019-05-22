"""
.. module:: control_points
    :platform: Unix, Windows
    :synopsis: Provides helper classes for managing control points

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
from functools import reduce
from .exceptions import GeomdlException
from ._utilities import export, add_metaclass


@add_metaclass(abc.ABCMeta)
class AbstractManager(object):
    """ Abstract base class for control points manager classes. """
    def __init__(self, *args):
        self._size = [int(arg) for arg in args]
        self._points = []
        self.reset()

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

    @property
    def ctrlpts(self):
        """ Control points

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._points
    
    @ctrlpts.setter
    def ctrlpts(self, value):
        self._points = value

    def reset(self):
        """ Resets/initializes the internal control points array. """
        num = reduce(lambda x, y: x *y, self._size)
        self._points[:] = [[] for _ in range(num)]

    @abc.abstractmethod
    def get_ctrlpt(self, *args):
        """ Gets the input control point from the input location in the array. """
        pass

    @abc.abstractmethod
    def set_ctrlpt(self, pt, *args):
        """ Puts the input control point to the input location in the array.

        :param pt: control point
        :type pt: list, tuple        
        """
        if not isinstance(pt, (list, tuple)):
            raise GeomdlException("'pt' argument should be a list or tuple")
        if len(args) != len(self._size):
            raise GeomdlException("Input dimensions are not compatible with the geometry")
        pass


class CurveManager(AbstractManager):
    """ Curve control points manager. """
    def __init__(self, *args):
        super(CurveManager, self).__init__(*args)

    def get_ctrlpt(self, *args):
        """ Gets the input control point from the input location in the array.

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
        """
        super(CurveManager, self).get_ctrlpt(*args)
        idx = args[0]
        try:
            return self._points[idx]
        except KeyError:
            return None

    def set_ctrlpt(self, pt, *args):
        """ Puts the input control point to the input location in the array.

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

        :param pt: control point
        :type pt: list, tuple        
        """
        super(CurveManager, self).set_ctrlpt(pt, *args)
        idx = args[0]
        try:
            self._points[idx] = pt
        except IndexError:
            raise GeomdlException("Index is out of range")


class SurfaceManager(AbstractManager):
    """ Surface control points manager. """
    def __init__(self, *args):
        super(SurfaceManager, self).__init__(*args)

    def get_ctrlpt(self, *args):
        """ Gets the input control point from the input location in the array.

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
        """
        super(SurfaceManager, self).get_ctrlpt(*args)
        idx = args[1] + (args[0] * self._size[1])
        try:
            return self._points[idx]
        except IndexError:
            return None

    def set_ctrlpt(self, pt, *args):
        """ Puts the input control point to the input location in the array.

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

        :param pt: control point
        :type pt: list, tuple        
        """
        super(SurfaceManager, self).set_ctrlpt(pt, *args)
        idx = args[1] + (args[0] * self._size[1])
        try:
            self._points[idx] = pt
        except IndexError:
            raise GeomdlException("Index is out of range")


class VolumeManager(AbstractManager):
    """ Volume control points manager. """
    def __init__(self, *args):
        super(VolumeManager, self).__init__(*args)

    def get_ctrlpt(self, *args):
        """ Gets the input control point from the input location in the array.
        
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
        """
        super(VolumeManager, self).get_ctrlpt(*args)
        idx = args[1] + (args[0] * self._size[1]) + (args[2] * self._size[0] * self._size[1])
        try:
            return self._points[idx]
        except IndexError:
            return None

    def set_ctrlpt(self, pt, *args):
        """ Puts the input control point to the input location in the array.

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

        :param pt: control point
        :type pt: list, tuple        
        """
        super(VolumeManager, self).set_ctrlpt(pt, *args)
        idx = args[1] + (args[0] * self._size[1]) + (args[2] * self._size[0] * self._size[1])
        try:
            self._points[idx] = pt
        except IndexError:
            raise GeomdlException("Index is out of range")
