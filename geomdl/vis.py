"""
.. module:: vis
    :platform: Unix, Windows
    :synopsis: Provides abstract base classes for visualization modules

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
import six
from typing import Any, Sequence, List


class VisConfigAbstract(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class for visualization configuration

    Defines an abstract base for NURBS-Python visualization configuration.
    """

    def __init__(self, **kwargs):
        # type: (**Any) -> None
        pass


class VisAbstract(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class for visualization

    Defines an abstract base for NURBS-Python visualization modules.

    :param config: configuration class
    :type config: VisConfigAbstract
    """

    def __init__(self, config):
        # type: (VisConfigAbstract) -> None
        if not isinstance(config, VisConfigAbstract):
            raise TypeError("Config variable must be an instance of vis.VisAbstractConfig")
        self._config = config
        self._plots = []  # type: List[dict]
        self._plot_types = {'ctrlpts': 'points', 'evalpts': 'points', 'others': None}
        self._ctrlpts_offset = 0.0

    def clear(self):
        # type: () -> None
        """ Clears the points, colors and names lists. """
        self._plots[:] = []

    def add(self, ptsarr, plot_type, name="", color=""):
        # type: (Sequence[Sequence[float]], str, str, str) -> None
        """ Adds points sets to the visualization instance for plotting.

        :param ptsarr: control or evaluated points
        :type ptsarr: list, tuple
        :param plot_type: type of the plot, e.g. ctrlpts, evalpts, bbox, etc.
        :type plot_type: str
        :param name: name of the plot displayed on the legend
        :type name: str
        :param color: plot color
        :type color: str
        """
        # ptsarr can be a list, a tuple or an array
        if ptsarr is None or len(ptsarr) == 0:
            return
        # Add points, size, plot color and name on the legend
        elem = {'ptsarr': ptsarr, 'name': name, 'color': color, 'type': plot_type}
        self._plots.append(elem)

    @property
    def plot_types(self):
        # type: () -> dict
        """ Plot types

        :getter: Gets the plot types
        :type: tuple
        """
        return self._plot_types

    def set_plot_type(self, plot_type, type_value):
        # type: (str, str) -> None
        """ Sets the plot type.

        The visualization module is mainly designed to plot the control points (*ctrlpts*) and the surface points
        (*evalpts*). These are called as *plot types*. However, there is more than one way to plot the control points
        and the surface points. For instance, a control points plot can be a scatter plot or a quad mesh, and a
        surface points plot can be a scatter plot or a tessellated surface plot.

        This function allows you to change the type of the plot, e.g. from scatter plot to tessellated surface plot.
        On the other than, some visualization modules also defines some specialized classes for this purpose as it might
        not be possible to change the type of the plot at the runtime due to visualization library internal API
        differences (i.e. different backends for 2- and 3-dimensional plots).

        By default, the following plot types and values are available:

        **Curve**:

        * For control points (*ctrlpts*): points
        * For evaluated points (*evalpts*): points

        **Surface**:

        * For control points (*ctrlpts*): points, quads, quadmesh
        * For evaluated points (*evalpts*): points, quads, triangles

        **Volume**:

        * For control points (*ctrlpts*): points
        * For evaluated points (*evalpts*): points, voxels

        :param plot_type: plot type
        :type plot_type: str
        :param type_value: type value
        :type type_value: str
        """
        if not isinstance(plot_type, str) or not isinstance(type_value, str):
            raise TypeError("Plot type and its value should be string type")

        if plot_type not in self._plot_types.keys():
            raise KeyError(plot_type + " is not a type. Possible types: " +
                           ", ".join([k for k in self._plot_types.keys()]))

        self._plot_types[plot_type] = type_value

    def set_ctrlpts_offset(self, offset_value):
        # type: (float) -> None
        """ Sets an offset value for the control points plots.

        :param offset_value: offset value
        :type offset_value: float
        """
        self._ctrlpts_offset = float(offset_value)

    @abc.abstractmethod
    def render(self, **kwargs):
        # type: (**Any) -> None
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstract`` class.
        """
        # We need something to plot
        if self._plots is None or len(self._plots) == 0:
            raise ValueError("Nothing to plot")

        # Remaining should be implemented
        pass
