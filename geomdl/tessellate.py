"""
.. module:: tessellate
    :platform: Unix, Windows
    :synopsis: Provides tessellation classes for surface triangulation

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
from . import utilities
from . import _tessellate
from .exceptions import GeomdlException
from ._utilities import add_metaclass, export


@add_metaclass(abc.ABCMeta)
class AbstractTessellate(object):
    """ Abstract base class for tessellation algorithms. """

    def __init__(self, **kwargs):
        self._vertices = []
        self._faces = []
        self._arguments = dict()

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

        :getter: Gets the tessellation arguments (as a dict)
        :setter: Sets the tessellation arguments (as a dict)
        """
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        if not isinstance(value, dict):
            raise GeomdlException("Tessellation arguments must be a dict object")
        self._arguments = value

    @arguments.deleter
    def arguments(self):
        self._arguments = dict()

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


@export
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

        :param points: array of points
        :type points: list, tuple
        """
        # Call parent function
        super(TriangularTessellate, self).tessellate(points, **kwargs)

        # Apply default triangular mesh generator function
        self._vertices, self._faces = utilities.make_triangle_mesh(points, **kwargs)


class TrimTessellate(AbstractTessellate):
    """  Triangular tessellation algorithm for trimmed surfaces. """

    def __init__(self, **kwargs):
        super(TrimTessellate, self).__init__(**kwargs)

    def tessellate(self, points, **kwargs):
        """ Applies triangular tessellation w/ trimming curves.

        Keyword Arguments:
            * ``size_u``: number of points on the u-direction
            * ``size_v``: number of points on the v-direction

        :param points: array of points
        :type points: list, tuple
        """
        # Call parent function
        super(TrimTessellate, self).tessellate(points, **kwargs)

        # Extract trims for pre-processing
        trims = kwargs.pop('trims', [])

        # Add "sense" if it doesn't exist
        for idx in range(len(trims)):
            if trims[idx].opt_get('sense') is None:
                trims[idx].opt = ['sense', 0]

        # Apply default triangular mesh generator function with trimming customization
        self._vertices, self._faces = utilities.make_triangle_mesh(points, trims=trims,
                                                                   tessellate_func=_tessellate.surface_trim_tessellate,
                                                                   tessellate_args=self.arguments,
                                                                   **kwargs)
