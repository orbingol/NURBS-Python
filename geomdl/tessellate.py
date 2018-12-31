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
        self._vertices = []
        self._faces = []
        self._arguments = None

    @property
    def vertices(self):
        """ Vertex objects generated after tessellation.

        :getter: Gets the vertices
        :type: elements.AbstractEntity
        """
        return self._vertices

    @property
    def faces(self):
        """ Objects generated after tessellation.

        :getter: Gets the faces
        :type: elements.AbstractEntity
        """
        return self._faces

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
        """ Clears stored vertices and faces. """
        self._vertices[:] = []
        self._faces[:] = []

    def is_tessellated(self):
        """ Checks if vertices and faces are generated.

        :return: tessellation status
        :rtype: bool
        """
        return all((self.vertices, self.faces))

    @abc.abstractmethod
    def tessellate(self, points, **kwargs):
        """ Abstract method for the implementation of the tessellation algorithm.

        This algorithm should update :py:attr:`~vertices` and :py:attr:`~faces` properties.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param points: points to be tessellated
        """
        pass


class TriangularTessellate(AbstractTessellate):
    """  Triangular tessellation algorithm for surfaces.

    This class provides the default triangular tessellation algorithm for surfaces.
    """

    def __init__(self, **kwargs):
        super(TriangularTessellate, self).__init__(**kwargs)

    def tessellate(self, points, **kwargs):
        """ Applies triangular tessellation.

        This function does not check if the points have already been tessellated.

        Keyword Arguments:
            * ``size_u``: number of points on the u-direction
            * ``size_v``: number of points on the v-direction

        :param points: list of points
        :type points: list or tuple
        """
        # Call parent function
        super(TriangularTessellate, self).tessellate(points, **kwargs)

        # Apply default triangular mesh generator function
        self._vertices, self._faces = utilities.make_triangle_mesh(points, **kwargs)
