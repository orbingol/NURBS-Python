"""
.. module:: freeform
    :platform: Unix, Windows
    :synopsis: Provides freeform geometry classes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from geomdl import abstract


class Freeform(abstract.Geometry):
    """ n-dimensional freeform geometry """
    def __init__(self, **kwargs):
        super(Freeform, self).__init__(**kwargs)
        self._geometry_type = "freeform"
        self.name = "freeform geometry"

    def evaluate(self, **kwargs):
        """ Sets points that form the geometry.

        Keyword Arguments:
            * ``points``: sets the points
        """
        self._eval_points = kwargs.get('points', self._init_array())
        self._dimension = len(self._eval_points[0])
