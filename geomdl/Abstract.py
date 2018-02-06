"""
.. module:: Abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract classes for all BSpline / NURBS curves and surfaces using Python's ABC module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
from warnings import warn

from .visualization import VisBase


class Curve(object):
    """ Abstract class for all curves. """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._degree = 0  # degree
        self._knot_vector = None  # knot vector
        self._control_points = None  # control points
        self._delta = 0.1  # evaluation delta
        self._curve_points = None  # evaluated points
        self._vis_component = None  # visualization component

    @abc.abstractmethod
    def _get_degree(self):
        return False

    @abc.abstractmethod
    def _set_degree(self, value):
        pass

    @abc.abstractmethod
    def _get_knot_vector(self):
        return False

    @abc.abstractmethod
    def _set_knot_vector(self, value):
        pass

    @abc.abstractmethod
    def _get_control_points(self):
        return False

    @abc.abstractmethod
    def _set_control_points(self, value):
        pass

    @abc.abstractmethod
    def _get_curve_points(self):
        return False

    def _del_degree(self):
        self._degree = 0

    def _del_knot_vector(self):
        self._knot_vector = None

    def _del_control_points(self):
        self._control_points = None

    def _del_curve_points(self):
        self._curve_points = None

    def _get_order(self):
        return self._degree + 1

    def _del_order(self):
        self._degree = 0

    def _get_delta(self):
        return self._delta

    def _set_delta(self, value):
        self._delta = value

    def _del_delta(self):
        self._delta = 0.1

    def _get_visualization_component(self):
        return self._vis_component

    def _set_visualization_component(self, value):
        if not isinstance(value, VisBase.VisAbstract):
            warn("Visualization component is NOT an instance of VisAbstract class")
            return
        self._vis_component = value

    delta = property(fget=_get_delta, fset=_set_delta, fdel=_del_delta, doc="Evaluation delta")
    order = property(fget=_get_order, fdel=_del_order, doc="Order of the curve")
    degree = property(fget=_get_degree, fset=_set_degree, fdel=_del_degree, doc="Degree of the curve")
    knotvector = property(fget=_get_knot_vector, fset=_set_knot_vector, fdel=_del_knot_vector, doc="Knot vector")
    ctrlpts = property(fget=_get_control_points, fset=_set_control_points,
                       fdel=_del_control_points, doc="Control points")
    curvepts = property(fget=_get_curve_points, fdel=_del_curve_points, doc="Evaluated curve points")

    @abc.abstractmethod
    def evaluate(self):
        pass


class Surface(object):
    """ Abstract class for all surfaces. """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        # U-direction
        self._degree_u = 0  # degree
        self._knot_vector_u = None  # knot vector
        self._control_points_size_u = 0  # control points array length
        # V-direction
        self._degree_v = 0  # degree
        self._knot_vector_v = None  # knot vector
        self._control_points_size_v = 0  # control points array length
        # Common
        self._delta = 0.1  # evaluation delta
        self._control_points = None  # control points, 1-D array (v-order)
        self._control_points2D = None  # control points, 2-D array [u][v]
        self._surface_points = None  # evaluated points
        self._vis_component = None  # visualization component
