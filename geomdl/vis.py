"""
.. module:: vis
    :platform: Unix, Windows
    :synopsis: Provides abstract base classes for visualization modules

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
import six


class VisConfigAbstract(six.with_metaclass(abc.ABCMeta, object)):
    """ Visualization configuration abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all visualization configurations
    in NURBS-Python package.
    """

    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass


class VisAbstract(six.with_metaclass(abc.ABCMeta, object)):
    """ Visualization abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all common visualization options
    in NURBS-Python package.
    """

    def __init__(self, config=None):
        self._plots = []
        self._config = config

    def clear(self):
        """ Clears the points, colors and names lists. """
        self._plots[:] = []

    def add(self, ptsarr=(), name=None, color=None, plot_type=0):
        """ Adds points sets to the visualization instance for plotting.

        :param ptsarr: control, curve or surface points
        :type ptsarr: list, tuple
        :param name: name of the point on the legend
        :type name: str
        :param color: color of the point on the legend
        :type color: str
        :param plot_type: type of the plot, control points (type = 1) or evaluated points (type = 0)
        :type plot_type: int
        """
        if ptsarr is None or len(ptsarr) == 0:
            return
        if not color or not name:
            return
        # Add points, size, plot color and name on the legend
        elem = {'ptsarr': ptsarr, 'name': name, 'color': color, 'type': plot_type}
        self._plots.append(elem)

    @abc.abstractmethod
    def render(self, **kwargs):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstract`` class.
        """
        # We need something to plot
        if self._plots is None or len(self._plots) == 0:
            raise ValueError("Nothing to plot")

        # Remaining should be implemented
        pass


class VisAbstractSurf(six.with_metaclass(abc.ABCMeta, VisAbstract)):
    """ Visualization abstract class for surfaces

    Implements ``VisAbstract`` class and also uses Python's *Abstract Base Class* implementation to define a base
    for **surface** visualization options in NURBS-Python package.
    """

    def __init__(self, config=None):
        super(VisAbstractSurf, self).__init__(config=config)
        self._ctrlpts_offset = 0.0
        self._plot_types = {'ctrlpts': 'points', 'evalpts': 'points'}

    @property
    def plot_types(self):
        """ Plot types

        :getter: Gets the plot types
        :type: tuple
        """
        return self._plot_types

    def set_plot_type(self, plot_type, type_value):
        """ Sets the plot type.

        By default, the following plot types are possible: *ctrlpts*, *evalpts*

        By default, the following plot type values are possible:

        * For control points (*ctrlpts*): points, quads
        * For surface points (*evalpts*): points, quads, triangles

        :param plot_type: plot type
        :type plot_type: str
        :param type_value: type value
        :type type_value: str
        :return:
        """
        if not isinstance(plot_type, str) or not isinstance(type_value, str):
            raise TypeError("Plot type and its value should be string type")

        if plot_type not in self._plot_types.keys():
            raise KeyError(plot_type + " is not a type. Possible types: " +
                           ", ".join([k for k in self._plot_types.keys()]))

        self._plot_types[plot_type] = type_value

    def set_ctrlpts_offset(self, offset_value):
        """ Sets an offset for the control points grid plot.

        :param offset_value: offset value
        :type offset_value: float
        """
        self._ctrlpts_offset = float(offset_value)

    @abc.abstractmethod
    def render(self, **kwargs):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstractSurf`` class.
        """
        # Calling parent function
        super(VisAbstractSurf, self).render()

        # Remaining should be implemented
        pass
