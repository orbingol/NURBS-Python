"""
.. module:: tessellate
    :platform: Unix, Windows
    :synopsis: Provides tessellation classes for surface triangulation

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
import six
from . import utilities


class AbstractTessellate(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class for tessellation algorithms. """

    def __init__(self, **kwargs):
        self._vertices = None
        self._triangles = None
        self._arguments = None

    @property
    def vertices(self):
        """ Vertex objects generated after tessellation.

        :getter: Gets the vertices
        """
        return self._vertices

    @property
    def triangles(self):
        """ Triangle objects generated after tessellation.

        :getter: Gets the triangles
        """
        return self._triangles

    @property
    def arguments(self):
        """ Arguments passed to the tessellation function.

        This property allows customization of the tessellation algorithm, and mainly designed to allow users to pass
        additional arguments to the tessellation function or change the behavior of the algorithm at runtime. This
        property can be thought as a way to input and store extra data for the tessellation functionality.

        :getter: Gets the tessellation arguments
        :setter: Sets the tessellation arguments
        """
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value

    def reset(self):
        """ Clears stored vertices and triangles. """
        self._vertices = None
        self._triangles = None

    @abc.abstractmethod
    def tessellate(self, points, size_u, size_v, **kwargs):
        """ Abstract method for the implementation of the tessellation algorithm.

        This algorithm should update :py:attr:`~vertices` and :py:attr:`~triangles` properties.

        :param points: 1-dimensional array of surface points
        :param size_u: number of surface points on the u-direction
        :param size_v: number of surface points on the v-direction
        """
        pass


class TriangularTessellate(AbstractTessellate):
    """  Triangular tessellation algorithm for surfaces.

    This class provides the default triangular tessellation algorithm for surfaces.
    """

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
