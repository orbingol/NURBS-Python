"""
.. module:: VisBase
    :platform: Unix, Windows
    :synopsis: Abstract class for NURBS-Python visualization components

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc


class VisAbstract(object):
    """ Visualization abstract class """
    __metaclass__ = abc.ABCMeta

    def __init__(self, plot_ctrlpts=True):
        self._points = []  # control points and evaluated points
        self._sizes = []  # sizes in all directions
        self._colors = []  # color information for the plots
        self._names = []  # names of the plots on the legend
        self._plot_ctrlpts = plot_ctrlpts

    def clear(self):
        """ Clears the points, colors and names lists"""
        if self._points:
            self._points[:] = []
            self._sizes[:] = []
            self._colors[:] = []
            self._names[:] = []

    def add(self, ptsarr=(), size=0, name=None, color=None):
        """ Adds points sets to the visualization instance for plotting.

        :param ptsarr: control, curve or surface points
        :type ptsarr: list, tuple
        :param size: size in all directions
        :type size: int, list
        :param name: name of the point on the legend
        :type name: str
        :param color: color of the point on the legend
        :type color: str
        :return: None
        """
        if not ptsarr or not color or not name:
            return
        # Add points, size, plot color and name on the legend
        self._points.append(ptsarr)
        self._sizes.append(size)
        self._colors.append(color)
        self._names.append(name)

    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots of the point sets """
        pass


class VisAbstractSurf(VisAbstract):
    """ Visualization abstract class for surfaces """
    __metaclass__ = abc.ABCMeta

    def __init__(self, plot_ctrlpts=True):
        super(VisAbstractSurf, self).__init__(plot_ctrlpts)
        self._ctrlpts_offset = 0.0

    def set_ctrlpts_offset(self, offset_value):
        """ Sets an offset for the control points grid plot.

        :param offset_value: offset value
        :type offset_value: float
        :return: None
        """
        self._ctrlpts_offset = float(offset_value)

    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots of the point sets """
        pass
