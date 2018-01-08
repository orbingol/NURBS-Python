"""
.. module:: VisBase
    :platform: Unix, Windows
    :synopsis: Abstract class for NURBS-Python visualization components

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc


class VisAbstract(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._points = []
        self._colors = []
        self._names = []

    def add(self, ptsarr=(), name=None, color=None):
        if not ptsarr or not color or not name:
            return
        # Add points, plot color and name on the legend
        self._points.append(ptsarr)
        self._colors.append(color)
        self._names.append(name)

    @abc.abstractmethod
    def render(self):
        pass
