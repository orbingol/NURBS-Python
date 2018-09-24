"""
.. module:: tessellate
    :platform: Unix, Windows
    :synopsis: Provides tessellation classes for surface triangulation

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import Abstract
from . import utilities


class TriangularTessellate(Abstract.Tessellate):
    """  Triangular tessellation """

    def __init__(self, **kwargs):
        super(TriangularTessellate, self).__init__(**kwargs)

    def tessellate(self, points, size_u, size_v, **kwargs):
        """  Applies triangular tessellation.

        :param points: points to be triangulated
        :type points: list, tuple
        :param size_u: number of points on the u-direction
        :type size_u: int
        :param size_v: number of points on the v-direction
        :type size_v: int
        """
        # Call parent function
        super(TriangularTessellate, self).tessellate(points, size_u, size_v, **kwargs)

        # Apply default triangular mesh generator function
        self._vertices, self._triangles = utilities.make_triangle_mesh(points, size_u, size_v, **kwargs)
