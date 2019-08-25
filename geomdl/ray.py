"""
.. module:: ray
    :platform: Unix, Windows
    :synopsis: Provides ray data structures and operations

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""
import sys

from . import linalg
from ._utilities import export


@export
class Ray(object):
    """ Representation of a n-dimensional ray generated from 2 points.

    A ray is defined by :math:`r(t)=p_{1}+t\\times\\vec{d}` where :math`t` is the parameter value,
    :math:`\\vec{d} = p_{2}-p_{1}` is the vector component of the ray, :math:`p_{1}` is the origin point and
    :math:`p_{2}` is the second point which is required to define a line segment

    :param point1: 1st point of the line segment
    :type point1:  list, tuple
    :param point2: 2nd point of the line segment
    :type point2:  list, tuple
    """
    def __init__(self, point1, point2):
        super(Ray, self).__init__()
        if not isinstance(point1, (list, tuple)):
            raise TypeError("Point 1 must be a list or a tuple")
        if not isinstance(point2, (list, tuple)):
            raise TypeError("Point 2 must be a list or a tuple")
        if len(point1) != len(point2):
            raise ValueError("THe dimensions of the input points must be equal")
        else:
            self._dim = len(point1)
        self._pt1 = [float(c) for c in point1]
        self._pt2 = [float(c) for c in point2]

    @property
    def dimension(self):
        """ Spatial dimension of the ray

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the dimension of the ray
        """
        return self._dim

    @property
    def points(self):
        """ Start and end points of the line segment that the ray was generated

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the points
        """
        return tuple(self._pt1), tuple(self._pt2)

    @property
    def p(self):
        """ Origin point of the ray (p)

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the origin point of the ray
        """
        return tuple(self._pt1)

    @property
    def d(self):
        """ Vector component of the ray (d)

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the vector component of the ray
        """
        return linalg.vector_generate(self._pt1, self._pt2, normalize=False)

    def eval(self, t=0):
        """ Finds the point on the line segment defined by the input parameter.

        :math:`t=0` returns the origin (1st) point, defined by the input argument ``point1`` and :math:`t=1` returns
        the end (2nd) point, defined by the input argument ``point2``.

        :param t: parameter
        :type t: float
        :return: point at the parameter value
        :rtype: tuple
        """
        return linalg.point_translate(self.p, linalg.vector_multiply(self.d, t))


@export
class RayIntersection(object):
    """ The status of the ray intersection operation """
    INTERSECT = 1  # only one solution
    COLINEAR = 2  # no solution (parallel) or infinitely many solutions (coincident)
    SKEW = 3  # neither parallel nor intersecting


@export
def intersect(ray1, ray2, **kwargs):
    """ Finds intersection of 2 rays.

    This functions finds the parameter values for the 1st and 2nd input rays and returns a tuple of
    ``(parameter for ray1, parameter for ray2, intersection status)``.
    ``status`` value is a enum type which reports the case which the intersection operation encounters.

    The intersection operation can encounter 3 different cases:

    * Intersecting: This is the anticipated solution. Returns ``(t1, t2, RayIntersection.INTERSECT)``
    * Colinear: The rays can be parallel or coincident. Returns ``(t1, t2, RayIntersection.COLINEAR)``
    * Skew:  The rays are neither parallel nor intersecting. Returns ``(t1, t2, RayIntersection.SKEW)``

    For the colinear case, ``t1`` and ``t2`` are the parameter values that give the starting point of the ray2 and ray1,
    respectively. Therefore;

    .. code-block:: python

        ray1.eval(t1) == ray2.p
        ray2.eval(t2) == ray1.p

    Please note that this operation is only implemented for 2- and 3-dimensional rays.

    :param ray1: 1st ray
    :param ray2: 2nd ray
    :return: a tuple of the parameter (t) for ray1 and ray2, and status of the intersection
    :rtype: tuple
    """
    if not isinstance(ray1, Ray) or not isinstance(ray2, Ray):
        raise TypeError("The input arguments must be instances of the Ray object")

    if ray1.dimension != ray2.dimension:
        raise ValueError("Dimensions of the input rays must be the same")

    # Keyword arguments
    tol = kwargs.get('tol', (1 << 8) * sys.float_info.epsilon)

    # Call intersection method
    if ray1.dimension == 2:
        return _intersect2d(ray1, ray2, tol)
    elif ray1.dimension == 3:
        return _intersect3d(ray1, ray2, tol)
    else:
        raise NotImplementedError("Intersection operation for the current type of rays has not been implemented yet")


def _intersect2d(ray1, ray2, tol):
    # Using homogeneous coordinates
    r1_pt1 = list(ray1.points[0]) + [1.0]
    r1_pt2 = list(ray1.points[1]) + [1.0]
    r2_pt1 = list(ray2.points[0]) + [1.0]
    r2_pt2 = list(ray2.points[1]) + [1.0]

    # Generate 3-dimensional rays
    ray1_3d = Ray(r1_pt1, r1_pt2)
    ray2_3d = Ray(r2_pt1, r2_pt2)

    # Do a 3-dimensional intersect
    return _intersect3d(ray1_3d, ray2_3d, tol)


def _intersect3d(ray1, ray2, tol):
    # Check for colinear case
    d_cross = linalg.vector_cross(ray1.d, ray2.d)
    if linalg.vector_is_zero(d_cross, tol):
        tmp1 = linalg.vector_sum(ray2.p, ray1.p, coeff=-1.0)
        t1 = 0.0 if abs(ray1.d[0]) < tol else tmp1[0] / ray1.d[0]
        tmp2 = linalg.vector_sum(ray1.p, ray2.p, coeff=-1.0)
        t2 = 0.0 if abs(ray2.d[0]) < tol else tmp2[0] / ray2.d[0]
        return t1, t2, RayIntersection.COLINEAR

    # Find common values
    p_diff = linalg.vector_generate(ray1.p, ray2.p)
    d_magn = linalg.vector_magnitude(d_cross)
    d_magn_square = d_magn ** 2

    # Find t1
    pd1_cross = linalg.vector_cross(p_diff, ray2.d)
    pd1_dot = linalg.vector_dot(pd1_cross, d_cross)
    t1 = pd1_dot / d_magn_square

    # Find t2
    pd2_cross = linalg.vector_cross(p_diff, ray1.d)
    pd2_dot = linalg.vector_dot(pd2_cross, d_cross)
    t2 = pd2_dot / d_magn_square

    # Check for skew case
    ray1_pt = ray1.eval(t1)
    ray2_pt = ray2.eval(t2)

    if linalg.point_distance(ray1_pt, ray2_pt) < tol:
        return t1, t2, RayIntersection.INTERSECT
    else:
        return t1, t2, RayIntersection.SKEW
