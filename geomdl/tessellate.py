"""
.. module:: tessellate
    :platform: Unix, Windows
    :synopsis: Provides tessellation classes for surface triangulation

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
from .exceptions import GeomdlException
from . import _tessellate as tsl
from ._utilities import add_metaclass, export


# Add some aliases
make_triangle_mesh = tsl.make_triangle_mesh
make_quad_mesh = tsl.make_quad_mesh
polygon_triangulate = tsl.polygon_triangulate
surface_tessellate = tsl.surface_tessellate
surface_trim_tessellate = tsl.surface_trim_tessellate


@add_metaclass(abc.ABCMeta)
class AbstractTessellate(object):
    """ Abstract base class for tessellation algorithms. """

    def __init__(self, **kwargs):
        self._tsl_func = None
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
    """  Triangular tessellation algorithm for surfaces. """

    def __init__(self, **kwargs):
        super(TriangularTessellate, self).__init__(**kwargs)
        self._tsl_func = tsl.make_triangle_mesh

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
        self._vertices, self._faces = self._tsl_func(points, **kwargs)


@export
class TrimTessellate(AbstractTessellate):
    """  Triangular tessellation algorithm for trimmed surfaces. """

    def __init__(self, **kwargs):
        super(TrimTessellate, self).__init__(**kwargs)
        self._tsl_func = tsl.make_triangle_mesh
        self._tsl_trim_func = tsl.surface_trim_tessellate

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

        # Get trims from the keyword arguments
        trims = kwargs.pop('trims', [])

        # Update sense if it is not set
        for trim in trims:
            if trim.opt_get('reversed') is None:
                trim.opt = ['reversed', 0]  # always trim the enclosed area by the curve

        # Apply default triangular mesh generator function with trimming customization
        self._vertices, self._faces = self._tsl_func(points, trims=trims, tessellate_func=self._tsl_trim_func,
                                                     tessellate_args=self.arguments, **kwargs)


@export
class QuadTessellate(AbstractTessellate):
    """  Quadrilateral tessellation algorithm for surfaces. """

    def __init__(self, **kwargs):
        super(QuadTessellate, self).__init__(**kwargs)
        self._tsl_func = tsl.make_quad_mesh

    def tessellate(self, points, **kwargs):
        """ Applies quadrilateral tessellation.

        This function does not check if the points have already been tessellated.

        Keyword Arguments:
            * ``size_u``: number of points on the u-direction
            * ``size_v``: number of points on the v-direction

        :param points: array of points
        :type points: list, tuple
        """
        # Call parent function
        super(QuadTessellate, self).tessellate(points, **kwargs)

        # Apply default triangular mesh generator function
        self._vertices, self._faces = self._tsl_func(points, **kwargs)
