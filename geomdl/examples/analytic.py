"""
.. module:: examples.analytic
    :platform: Unix, Windows
    :synopsis: Common analytic geometry examples

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
import math
from . import abstract
from . import linalg


class Circle(abstract.AnalyticGeometry):
    r""" Analytic circle geometry

    Finds the points on a circle using the following equation:

    .. math::

        x &= x_{0} + r \cos{\theta} \\
        y &= y_{0} + r \sin{\theta}

    Keyword Arguments:
        * ``radius``: radius of the circle. *Default: 1*
        * ``origin``: coordinates of the circle center. *Default: (0, 0)*
    """
    def __init__(self, **kwargs):
        super(Circle, self).__init__(**kwargs)
        self._dimension = 2
        self.name = "analytic circle"
        self._radius = kwargs.get('radius', 1.0)
        self._origin = kwargs.get('origin', (0.0, 0.0))

    def reverse(self):
        """ Reverses the evaluated points """
        if not self._eval_points:
            self.evaluate()
        self._eval_points = list(reversed(self._eval_points))

    def evaluate(self, **kwargs):
        r""" Evaluates the circle.

        Keyword Arguments:
            * ``start``: start angle :math:`\theta` in degrees. *Default: 0*
            * ``stop``: stop angle :math:`\theta` in degrees. *Default: 360*
            * ``jump``: angle :math:`\theta` increment in degrees. *Default: 0.5*
        """
        start = kwargs.get('start', 0.0)
        stop = kwargs.get('stop', 360.0)
        jump = kwargs.get('jump', 0.5)
        points = []
        for t in linalg.frange(start, stop, jump):
            t_r = math.radians(t)
            pt = [
                self._origin[0] + (self._radius * math.cos(t_r)),
                self._origin[1] + (self._radius * math.sin(t_r))
            ]
            points.append(pt)
        self._eval_points = points


class Sphere(abstract.AnalyticGeometry):
    r""" Analytic sphere geometry

    Finds the points on a sphere using the following equation:

    .. math::

        x &= x_{0} + r \sin{\phi} \cos{\theta} \\
        y &= y_{0} + r \sin{\phi} \sin{\theta} \\
        z &= z_{0} + r \cos{\phi}

    Keyword Arguments:
        * ``radius``: radius of the sphere. *Default: 1*
        * ``origin``: coordinates of the sphere center. *Default: (0, 0, 0)*
    """
    def __init__(self, **kwargs):
        super(Sphere, self).__init__(**kwargs)
        self._dimension = 3
        self.name = "analytic sphere"
        self._radius = kwargs.get('radius', 1.0)
        self._origin = kwargs.get('origin', (0.0, 0.0, 0.0))

    def evaluate(self, **kwargs):
        r""" Evaluates the sphere.

        Keyword Arguments:
            * ``start_theta``: start angle :math:`\theta` in degrees. *Default: 0*
            * ``stop_theta``: stop angle :math:`\theta` in degrees. *Default: 360*
            * ``jump_theta``: angle :math:`\theta` increment in degrees. *Default: 0.5*
            * ``start_phi``: start angle :math:`\phi` in degrees. *Default: 0*
            * ``stop_phi``: stop angle :math:`\phi` in degrees. *Default: 180*
            * ``jump_phi``: angle :math:`\phi` increment in degrees. *Default: 0.25*
        """
        start_theta = kwargs.get('start_theta', 0.0)
        stop_theta = kwargs.get('stop_theta', 360.0)
        jump_theta = kwargs.get('jump_theta', 0.5)
        start_phi = kwargs.get('start_phi', 0.0)
        stop_phi = kwargs.get('stop_phi', 180.0)
        jump_phi = kwargs.get('jump_phi', 0.25)
        points = []
        for tt in linalg.frange(start_theta, stop_theta, jump_theta):
            tt_rad = math.radians(tt)
            for tp in linalg.frange(start_phi, stop_phi, jump_phi):
                tp_rad = math.radians(tp)
                pt = [
                    self._origin[0] + (self._radius * math.sin(tp_rad) * math.cos(tt_rad)),
                    self._origin[1] + (self._radius * math.sin(tp_rad) * math.sin(tt_rad)),
                    self._origin[2] + (self._radius * math.cos(tp_rad))
                ]
                points.append(pt)
        self._eval_points = points


class Rectangle(abstract.AnalyticGeometry):
    r""" Analytic rectangle geometry

    Finds the points on a rectangle with the size of :math:`2p \times 2q` using the following equation:

    .. math::

        x &= a (\lvert \cos{\theta} \rvert \cos{\theta} + \lvert \sin{\theta} \rvert \sin{\theta}) \\
        y &= b (\lvert \cos{\theta} \rvert \cos{\theta} - \lvert \sin{\theta} \rvert \sin{\theta})

    Keyword Arguments:
        * ``a``: length of the side on the u-direction. *Default: 1*
        * ``b``: length of the side on the v-direction. *Default: 1*
        * ``origin``: coordinates of the rectangle center. *Default: (0, 0)*
    """
    def __init__(self, **kwargs):
        super(Rectangle, self).__init__(**kwargs)
        self._dimension = 2
        self.name = "analytic rectangle"
        self._a = kwargs.get('a', 1.0)
        self._b = kwargs.get('b', 1.0)
        self._origin = kwargs.get('origin', (0.0, 0.0))

    def reverse(self):
        """ Reverses the evaluated points """
        if not self._eval_points:
            self.evaluate()
        self._eval_points = list(reversed(self._eval_points))

    def evaluate(self, **kwargs):
        r""" Evaluates the rectangle.

        Keyword Arguments:
            * ``start``: start angle :math:`\theta` in degrees. *Default: 0*
            * ``stop``: stop angle :math:`\theta` in degrees. *Default: 360*
            * ``jump``: angle :math:`\theta` increment in degrees. *Default: 0.5*
        """
        start = kwargs.get('start', 0.0)
        stop = kwargs.get('stop', 360.0)
        jump = kwargs.get('jump', 0.5)
        points = []
        for t in linalg.frange(start, stop, jump):
            ct = math.cos(math.radians(t))
            st = math.sin(math.radians(t))
            pt = [
                self._origin[0] + self._a * ((abs(ct) * ct) + (abs(st) * st)),
                self._origin[1] + self._b * ((abs(ct) * ct) - (abs(st) * st)),
            ]
            points.append(pt)
        self._eval_points = points
