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

    @property
    def order(self):
        """ Curve order.

        Defined as order = degree + 1

        :getter: Gets the curve order
        :setter: Sets the curve order
        :type: integer
        """
        return self._degree + 1

    @order.setter
    def order(self, value):
        self._degree = value - 1

    @property
    @abc.abstractmethod
    def degree(self):
        return False

    @degree.setter
    @abc.abstractmethod
    def degree(self, value):
        pass

    @property
    @abc.abstractmethod
    def knotvector(self):
        return False

    @knotvector.setter
    @abc.abstractmethod
    def knotvector(self, value):
        pass

    @property
    @abc.abstractmethod
    def ctrlpts(self):
        return False

    @ctrlpts.setter
    @abc.abstractmethod
    def ctrlpts(self, value):
        pass

    @property
    @abc.abstractmethod
    def curvepts(self):
        return False

    @property
    @abc.abstractmethod
    def delta(self):
        return self._delta

    @delta.setter
    @abc.abstractmethod
    def delta(self, value):
        self._delta = value

    @property
    def vis(self):
        """ Visualization component.

        .. note:: The visualization component is completely optional to use.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        :type: float
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisBase.VisAbstract):
            warn("Visualization component is NOT an instance of VisAbstract class")
            return
        self._vis_component = value

    # Checks whether the curve evaluation is possible or not
    def _check_variables(self):
        works = True
        # Check degree values
        if self._degree == 0:
            works = False
        if not self._control_points:
            works = False
        if not self._knot_vector:
            works = False
        if not works:
            raise ValueError("Some required parameters for curve evaluation are not set")

    @abc.abstractmethod
    def curvept(self, u=-1, check_vars=True, get_ctrlpts=False):
        pass

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

    @property
    def order_u(self):
        """ Surface order for U direction.

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for U direction
        :setter: Sets the surface order for U direction
        :type: integer
        """
        return self._degree_u + 1

    @order_u.setter
    def order_u(self, value):
        self._degree_u = value - 1

    @property
    def order_v(self):
        """ Surface order for V direction.

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for V direction
        :setter: Sets the surface order for V direction
        :type: integer
        """
        return self._degree_v + 1

    @order_v.setter
    def order_v(self, value):
        self._degree_v = value - 1

    @property
    @abc.abstractmethod
    def degree_u(self):
        return False

    @degree_u.setter
    @abc.abstractmethod
    def degree_u(self, value):
        pass

    @property
    @abc.abstractmethod
    def degree_v(self):
        return False

    @degree_v.setter
    @abc.abstractmethod
    def degree_v(self, value):
        pass

    @property
    @abc.abstractmethod
    def knotvector_u(self):
        return False

    @knotvector_u.setter
    @abc.abstractmethod
    def knotvector_u(self, value):
        pass

    @property
    @abc.abstractmethod
    def knotvector_v(self):
        return False

    @knotvector_v.setter
    @abc.abstractmethod
    def knotvector_v(self, value):
        pass

    @property
    @abc.abstractmethod
    def ctrlpts(self):
        return False

    @ctrlpts.setter
    @abc.abstractmethod
    def ctrlpts(self, value):
        pass

    @property
    @abc.abstractmethod
    def ctrlpts2d(self):
        return False

    @ctrlpts2d.setter
    @abc.abstractmethod
    def ctrlpts2d(self, value):
        pass

    @property
    def ctrlpts_size_u(self):
        return self._control_points_size_u

    @ctrlpts_size_u.setter
    def ctrlpts_size_u(self, value):
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size_u = value

    @property
    def ctrlpts_size_v(self):
        return self._control_points_size_v

    @ctrlpts_size_v.setter
    def ctrlpts_size_v(self, value):
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size_v = value

    @property
    @abc.abstractmethod
    def surfpts(self):
        return False

    @property
    @abc.abstractmethod
    def delta(self):
        return self._delta

    @delta.setter
    @abc.abstractmethod
    def delta(self, value):
        self._delta = value

    @property
    def vis(self):
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisBase.VisAbstract):
            warn("Visualization component is NOT an instance of VisAbstract class")
            return
        self._vis_component = value

    # Checks whether the surface evaluation is possible or not
    def _check_variables(self):
        works = True
        if self._degree_u == 0 or self._degree_v == 0:
            works = False
        if not self._control_points:
            works = False
        if not self._knot_vector_u or not self._knot_vector_v:
            works = False
        if not works:
            raise ValueError("Some required parameters for surface evaluation are not set.")

    @abc.abstractmethod
    def surfpt(self, u=-1, v=-1, check_vars=True, get_ctrlpts=False):
        pass

    @abc.abstractmethod
    def evaluate(self):
        pass
