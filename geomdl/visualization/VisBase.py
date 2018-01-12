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

    def __init__(self):
        self._points = []  # control points and evaluated points
        self._colors = []  # color information for the plots
        self._names = []  # names of the plots on the legend

    def clear(self):
        """ Clears the points, colors and names lists"""
        if self._points:
            self._points[:] = []
            self._colors[:] = []
            self._names[:] = []

    def add(self, ptsarr=(), name=None, color=None):
        """ Adds points sets to the visualization instance for plotting.

        :param ptsarr: control, curve or surface points
        :type ptsarr: list, tuple
        :param name: name of the point on the legend
        :type name: str
        :param color: color of the point on the legend
        :type color: str
        :return: None
        """
        if not ptsarr or not color or not name:
            return
        # Add points, plot color and name on the legend
        self._points.append(ptsarr)
        self._colors.append(color)
        self._names.append(name)

    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots of the point sets """
        pass
