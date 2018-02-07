"""
.. module:: VisBase
    :platform: Unix, Windows
    :synopsis: Abstract classes for NURBS-Python visualization components

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc


class VisAbstract(object):
    """ Visualization abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all common visualization options
    in NURBS-Python package.

    :param plot_ctrlpts: enables/disables display of control points plot on the final figure
    :type plot_ctrlpts: bool
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, plot_ctrlpts=True, display_legend=True):
        self._plots = []
        self._plot_ctrlpts = plot_ctrlpts
        self._plot_legend = display_legend
        self._figure_size = [10.67, 8]
        self._figure_dpi = 96

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

    def figure_size(self, size=None):
        """ Sets the figure/window size.

        :param size: size of the figure/window as (x, y) values
        :type size: list, tuple
        """
        if not size or not isinstance(size, (tuple, list)):
            return
        if not len(size) == 2:
            return
        self._figure_size = size

    def figure_dpi(self, dpi=None):
        """ Sets the resolution of the figure.

        :param dpi: resolution value; 96 by default
        :type dpi: int
        """
        if not dpi or not isinstance(dpi, int):
            return
        self._figure_dpi = dpi

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

    :param plot_ctrlpts: enables/disables display of control points plot on the final figure
    :type plot_ctrlpts: bool
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, plot_ctrlpts=True, display_legend=True):
        super(VisAbstractSurf, self).__init__(plot_ctrlpts, display_legend)
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
