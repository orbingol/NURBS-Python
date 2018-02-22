"""
.. module:: Abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract classes for all BSpline / NURBS curves and surfaces using Python's ABC module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
from warnings import warn


class Curve(object):
    """ Abstract class for all curves. """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._degree = 0  # degree
        self._knot_vector = None  # knot vector
        self._control_points = None  # control points
        self._delta = 0.1  # evaluation delta
        self._curve_points = None  # evaluated points
        self._dimension = 0  # dimension of the curve
        self._vis_component = None  # visualization component

    @property
    def dimension(self):
        """ Dimension of the curve.

        Dimension will be automatically estimated from the first element of the control points array.

        :getter: Gets the dimension of the curve, e.g. 2D, 3D, etc.
        """
        return self._dimension

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
    def degree(self):
        """ Curve degree.

        :getter: Gets the curve degree
        :setter: Sets the curve degree
        """
        return self._degree

    @degree.setter
    def degree(self, value):
        self._degree = value

    @property
    def knotvector(self):
        """ Knot vector.

        :getter: Gets the knot vector
        :setter: Sets the knot vector
        """
        return self._knot_vector

    @knotvector.setter
    def knotvector(self, value):
        self._knot_vector = value

    @property
    def ctrlpts(self):
        """ Control points.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        self._control_points = value

    @property
    def curvepts(self):
        """ Curve points.

        :getter: Coordinates of the evaluated surface points
        """
        return self._curve_points

    @property
    def delta(self):
        """ Evaluation delta.

        .. note:: The delta value is 0.1 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        self._delta = value

    @property
    def vis(self):
        """ Visualization component.

        .. note::

            The visualization component is completely optional to use. ``render()`` method should also be implemented,
            if the visualization component is planned to be used in the implementation.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisAbstract):
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

    # Resets the control points
    def _reset_ctrlpts(self):
        self._control_points = None

    # Resets the evaluated points
    def _reset_evalpts(self):
        self._curve_points = None

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Evaluates the curve. """
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
        self._dimension = 0  # dimension of the surface
        self._vis_component = None  # visualization component

    @property
    def dimension(self):
        """ Dimension of the surface.

        Dimension will be automatically estimated from the first element of the control points array.

        :getter: Gets the dimension of the surface
        """
        return self._dimension

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
    def degree_u(self):
        """ Surface degree for U direction.

        :getter: Gets the surface degree for U direction
        :setter: Sets the surface degree for U direction
        :type: integer
        """
        return self._degree_u

    @degree_u.setter
    def degree_u(self, value):
        self._degree_u = value

    @property
    def degree_v(self):
        """ Surface degree for V direction.

        :getter: Gets the surface degree for V direction
        :setter: Sets the surface degree for V direction
        :type: integer
        """
        return self._degree_v

    @degree_v.setter
    def degree_v(self, value):
        self._degree_v = value

    @property
    def knotvector_u(self):
        """ Knot vector for U direction.

        :getter: Gets the knot vector for U direction
        :setter: Sets the knot vector for U direction
        """
        return self._knot_vector_u

    @knotvector_u.setter
    def knotvector_u(self, value):
        self._knot_vector_u = value

    @property
    def knotvector_v(self):
        """ Knot vector for V direction.

        :getter: Gets the knot vector for V direction
        :setter: Sets the knot vector for V direction
        """
        return self._knot_vector_v

    @knotvector_v.setter
    def knotvector_v(self, value):
        self._knot_vector_v = value

    @property
    def ctrlpts(self):
        """ 1-D control points.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        self._control_points = value

    @property
    def ctrlpts2d(self):
        """ 2-D control points.

        :getter: Gets the control points in U and V directions
        :setter: Sets the control points in U and V directions
        """
        return self._control_points2D

    @ctrlpts2d.setter
    def ctrlpts2d(self, value):
        self._control_points2D = value

    @property
    def ctrlpts_size_u(self):
        """ Size of the control points array in U-direction.

        :getter: Gets number of control points in U-direction
        :setter: Sets number of control points in U-direction
        """
        return self._control_points_size_u

    @ctrlpts_size_u.setter
    def ctrlpts_size_u(self, value):
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size_u = value

    @property
    def ctrlpts_size_v(self):
        """ Size of the control points array in V-direction.

        :getter: Gets number of control points in V-direction
        :setter: Sets number of control points in V-direction
        """
        return self._control_points_size_v

    @ctrlpts_size_v.setter
    def ctrlpts_size_v(self, value):
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size_v = value

    @property
    def surfpts(self):
        """ Surface points.

        :getter: Coordinates of evaluated surface points
        """
        return self._surface_points

    @property
    def delta(self):
        """ Evaluation delta.

        .. note:: The delta value is 0.1 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        self._delta = value

    @property
    def vis(self):
        """ Visualization component.

        .. note::

            The visualization component is completely optional to use. ``render()`` method should also be implemented,
            if the visualization component is planned to be used in the implementation.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisAbstract):
            warn("Visualization component is NOT an instance of VisAbstract class")
            return
        self._vis_component = value

    # Resets the control points
    def _reset_ctrlpts(self):
        self._control_points = None

    # Resets the evaluated points
    def _reset_evalpts(self):
        self._surface_points = None

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
    def evaluate(self, **kwargs):
        """ Evaluates the surface. """
        pass


class Multi(object):
    """ Abstract class for curve and surface containers. """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._elements = []
        self._delta = 0.1
        self._vis_component = None
        self._iter_index = 0
        self._instance = None

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            result = self._elements[self._iter_index]
        except IndexError:
            raise StopIteration
        self._iter_index += 1
        return result

    def __reversed__(self):
        return reversed(self._elements)

    def __getitem__(self, index):
        return self._elements[index]

    def __len__(self):
        return len(self._elements)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Cannot add non-matching types of Multi containers")
        ret = self.__class__()
        new_elems = self._elements + other._elements
        ret.add_list(new_elems)
        return ret

    @property
    def delta(self):
        """ Evaluation delta.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta should be between 0.0 and 1.0")

        # Set a new delta value
        self._delta = float(value)

    @property
    def vis(self):
        """ Visualization component.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        :type: float
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisAbstract):
            warn("Visualization component is NOT an instance of the abstract class")
            return
        self._vis_component = value

    def add(self, element):
        """ Abstract method for adding surface or curve objects to the container.

        :param element: the curve or surface object to be added
        :type element:
        """
        if not isinstance(element, self._instance):
            warn("Cannot add, incompatible type.")
            return
        self._elements.append(element)

    def add_list(self, elements):
        """ Adds curve objects to the container.

        :param elements: curve objects to be added
        :type elements: list, tuple
        """
        if not isinstance(elements, (list, tuple)):
            warn("Input must be a list or a tuple")
            return

        for element in elements:
            self.add(element)

    def translate(self, vec=()):
        """ Translates the elements in the container by the input vector.

        :param vec: translation vector
        :type vec: list, tuple
        """
        for elem in self._elements:
            elem.translate(vec)

    # Runs visualization component to render the surface
    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots using the visualization component. """
        pass


class VisConfigAbstract(object):
    """ Visualization configuration abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all visualization configurations
    in NURBS-Python package.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass


class VisAbstract(object):
    """ Visualization abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all common visualization options
    in NURBS-Python package.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, config=None):
        self._plots = []
        self._config = config

    def clear(self):
        """ Clears the points, colors and names lists. """
        self._plots[:] = []

    def add(self, ptsarr=(), size=0, name=None, color=None, plot_type=0):
        """ Adds points sets to the visualization instance for plotting.

        :param ptsarr: control, curve or surface points
        :type ptsarr: list, tuple
        :param size: size in all directions, e.g. in U- and V-direction
        :type size: int, tuple, list
        :param name: name of the point on the legend
        :type name: str
        :param color: color of the point on the legend
        :type color: str
        :param plot_type: type of the plot, control points (type = 1) or evaluated points (type = 0)
        :type plot_type: int
        """
        if not ptsarr or not color or not name:
            return
        # Add points, size, plot color and name on the legend
        elem = {'ptsarr': ptsarr, 'size': size, 'name': name, 'color': color, 'type': plot_type}
        self._plots.append(elem)

    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstract`` class.
        """
        pass


class VisAbstractSurf(VisAbstract):
    """ Visualization abstract class for surfaces

    Implements ``VisABstract`` class and also uses Python's *Abstract Base Class* implementation to define a base
    for **surface** visualization options in NURBS-Python package.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, config=None):
        super(VisAbstractSurf, self).__init__(config=config)
        self._ctrlpts_offset = 0.0

    def set_ctrlpts_offset(self, offset_value):
        """ Sets an offset for the control points grid plot.

        :param offset_value: offset value
        :type offset_value: float
        """
        self._ctrlpts_offset = float(offset_value)

    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstractSurf`` class.
        """
        pass
