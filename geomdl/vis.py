"""
.. module:: vis
    :platform: Unix, Windows
    :synopsis: Provides abstract base classes for visualization modules

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
from . import _utilities as utl
from .exceptions import GeomdlException


# Initialize an empty __all__ for controlling imports
__all__ = []


@utl.add_metaclass(abc.ABCMeta)
class VisConfigAbstract(object):
    """ Abstract base class for user configuration of the visualization module

    Defines an abstract base for NURBS-Python (geomdl) visualization configuration.
    """

    def __init__(self, **kwargs):
        pass


@utl.add_metaclass(abc.ABCMeta)
class VisAbstract(object):
    """ Abstract base class for visualization

    Defines an abstract base for NURBS-Python (geomdl) visualization modules.

    :param config: configuration class
    :type config: VisConfigAbstract
    """

    def __init__(self, config, **kwargs):
        if not isinstance(config, VisConfigAbstract):
            raise TypeError("Config variable must be an instance of vis.VisAbstractConfig")
        self._user_config = config.__class__(**kwargs) if kwargs else config
        self._module_config = {'ctrlpts': 'points', 'evalpts': 'points', 'others': None}
        self._plots = []
        self._ctrlpts_offset = 0.0

    def clear(self):
        """ Clears the points, colors and names lists. """
        self._plots[:] = []

    def add(self, ptsarr, plot_type, name="", color="", idx=0):
        """ Adds points sets to the visualization instance for plotting.

        :param ptsarr: control or evaluated points
        :type ptsarr: list, tuple
        :param plot_type: type of the plot, e.g. ctrlpts, evalpts, bbox, etc.
        :type plot_type: str
        :param name: name of the plot displayed on the legend
        :type name: str
        :param color: plot color
        :type color: str
        :param color: plot index
        :type color: int
        """
        # ptsarr can be a list, a tuple or an array
        if ptsarr is None or len(ptsarr) == 0:
            return
        # Add points, size, plot color and name on the legend
        plt_name = " ".join([str(n) for n in name]) if isinstance(name, (list, tuple)) else name
        elem = {'ptsarr': ptsarr, 'name': plt_name, 'color': color, 'type': plot_type, 'idx': idx}
        self._plots.append(elem)

    @property
    def vconf(self):
        """ User configuration class for visualization

        :getter: Gets the user configuration class
        :type: vis.VisConfigAbstract
        """
        return self._user_config

    @property
    def mconf(self):
        """ Configuration directives for the visualization module (internal).

        This property controls the internal configuration of the visualization module. It is for advanced use and
        testing only.

        The visualization module is mainly designed to plot the control points (*ctrlpts*) and the surface points
        (*evalpts*). These are called as *plot types*. However, there is more than one way to plot the control points
        and the surface points. For instance, a control points plot can be a scatter plot or a quad mesh, and a
        surface points plot can be a scatter plot or a tessellated surface plot.

        This function allows you to change the type of the plot, e.g. from scatter plot to tessellated surface plot.
        On the other than, some visualization modules also defines some specialized classes for this purpose as it might
        not be possible to change the type of the plot at the runtime due to visualization library internal API
        differences (i.e. different backends for 2- and 3-dimensional plots).

        By default, the following plot types and values are available:

        Curve:
            * For control points (*ctrlpts*): points
            * For evaluated points (*evalpts*): points

        Surface:
            * For control points (*ctrlpts*): points, quads
            * For evaluated points (*evalpts*): points, quads, triangles

        Volume:
            * For control points (*ctrlpts*): points
            * For evaluated points (*evalpts*): points, voxels

        :getter: Gets the visualization module configuration
        :setter: Sets the visualization module configuration
        """
        return self._module_config

    @mconf.setter
    def mconf(self, value):
        try:
            if not isinstance(value[0], str) or not isinstance(value[1], str):
                raise GeomdlException("Plot type and its value should be string type")

            if value[0] not in self._module_config.keys():
                raise GeomdlException(value[0] + " is not a configuration directive. Possible directives: " +
                                      ", ".join([k for k in self._module_config.keys()]))

            self._module_config[value[0]] = value[1]
        except TypeError:
            raise GeomdlException("The input should be  a list or a tuple")

    @property
    def ctrlpts_offset(self):
        """ Defines an offset value for the control points grid plots

        Only makes sense to use with surfaces with dense control points grid.

        :getter: Gets the offset value
        :setter: Sets the offset value
        :type: float
        """
        return self._ctrlpts_offset

    @ctrlpts_offset.setter
    def ctrlpts_offset(self, offset_value):
        self._ctrlpts_offset = float(offset_value)

    def size(self, plot_type):
        """ Returns the number of plots defined by the plot type.

        :param plot_type: plot type
        :type plot_type: str
        :return: number of plots defined by the plot type
        :rtype: int
        """
        count = 0
        for plot in self._plots:
            if plot['type'] == plot_type:
                count += 1
        return count

    def animate(self, **kwargs):
        """ Generates animated plots (if supported).

        If the implemented visualization module supports animations, this function will create an animated figure.
        Otherwise, it will call :py:meth:`render` method by default.
        """
        # Call render() by default
        self.render(**kwargs)

    @abc.abstractmethod
    def render(self, **kwargs):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstract`` class.
        """
        # We need something to plot
        if self._plots is None or len(self._plots) == 0:
            raise GeomdlException("Nothing to plot")
