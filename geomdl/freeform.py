"""
.. module:: freeform
    :platform: Unix, Windows
    :synopsis: Provides freeform geometry classes

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .base import GeomdlDict
from .abstract import Geometry


class Freeform(Geometry):
    """ n-dimensional freeform geometry """
    def __init__(self, *args, **kwargs):
        super(Freeform, self).__init__(*args, **kwargs)
        self._geom_type = "freeform"

    @property
    def data(self):
        """ Returns a dict which contains the geometry information

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the geometry information
        """
        data = super(Freeform, self).data
        data.update(GeomdlDict(points=tuple(self.evalpts)))
        return data

    def evaluate(self, **kwargs):
        """ Sets points that form the geometry.

        Keyword Arguments:
            * ``points``: sets the points
        """
        self._eval_points = kwargs.get('points', self._init_array())
        self._dimension = len(self._eval_points[0])
