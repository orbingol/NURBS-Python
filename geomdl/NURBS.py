"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: Provides data storage and evaluation functionality for rational spline geometries

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import BSpline, evaluators
from .base import export, GeomdlError, GeomdlTypeSequence
from .control_points import CPManager, separate_ctrlpts_weights, combine_ctrlpts_weights


@export
class Curve(BSpline.Curve):
    """ Data storage and evaluation class for n-variate NURBS (rational) curves.

    The rational shapes have some minor differences between the non-rational ones. This class is designed to operate
    with weighted control points (Pw) as described in *The NURBS Book* by Piegl and Tiller. Therefore, it provides
    a different set of properties (i.e. getters and setters):

        * ``ctrlptsw``: 1-dimensional array of weighted control points
        * ``ctrlpts``: 1-dimensional array of control points
        * ``weights``: 1-dimensional array of weights
    """

    @classmethod
    def from_bspline(cls, obj):
        """ Creates a rational B-spline curve from a non-rational B-spline curve

        :param obj: B-spline curve
        :type obj: BSpline.Curve
        """
        if obj.pdimension != 1:
            raise GeomdlError("Parametric dimension mismatch")
        rspl = cls()
        rspl.degree = obj.degree
        rspl.knotvector = obj.knotvector
        rspl.ctrlpts = obj.ctrlpts
        rspl.delta = obj.delta
        return rspl

    def __init__(self, *args, **kwargs):
        super(Curve, self).__init__(*args, **kwargs)
        self._rational = True
        self._evaluator = evaluators.CurveEvaluatorRational()

    @property
    def ctrlptsw(self):
        """ Weighted control points (Pw)

        Weighted control points are in (x*w, y*w, z*w, w) format; where x,y,z are the coordinates and w is the weight.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the weighted control points
        :setter: Sets the weighted control points
        """
        return self._control_points

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")
        self._control_points = value
        # Clear caches
        self.reset()

    @property
    def ctrlpts(self):
        """ Control points (P)

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets unweighted control points. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets unweighted control points
        :type: list
        """
        # Populate the cache, if necessary
        if not self._cache['ctrlpts']:
            self._cache['ctrlpts'], self._cache['weights'] = separate_ctrlpts_weights(self._control_points.points)
        return self._cache['ctrlpts']

    @ctrlpts.setter
    def ctrlpts(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")

        # Check if we can retrieve the existing weights. If not, generate a weights vector of 1.0s.
        if not self.weights:
            weights = [1.0 for _ in range(len(value))]
        else:
            weights = self.weights

        # Generate weighted control points using the new control points
        value.points  = combine_ctrlpts_weights(value.points, weights)

        # Set new weighted control points
        self._control_points = value

        # Clear caches
        self.reset()


@export
class Surface(BSpline.Surface):
    """ Data storage and evaluation class for NURBS (rational) surfaces.

    The rational shapes have some minor differences between the non-rational ones. This class is designed to operate
    with weighted control points (Pw) as described in *The NURBS Book* by Piegl and Tiller. Therefore, it provides
    a different set of properties (i.e. getters and setters):

        * ``ctrlptsw``: 1-dimensional array of weighted control points
        * ``ctrlpts``: 1-dimensional array of control points
        * ``weights``: 1-dimensional array of weights
    """

    def __init__(self, *args, **kwargs):
        super(Surface, self).__init__(*args, **kwargs)
        self._rational = True
        self._evaluator = evaluators.SurfaceEvaluatorRational()

    @classmethod
    def from_bspline(cls, obj):
        """ Creates a rational B-spline surface from a non-rational B-spline surface

        :param obj: B-spline surface
        :type obj: BSpline.Surface
        """
        if obj.pdimension != 2:
            raise GeomdlError("Parametric dimension mismatch")
        rspl = cls()
        rspl.degree = obj.degree
        rspl.knotvector = obj.knotvector
        rspl.ctrlpts = obj.ctrlpts
        rspl.delta = obj.delta
        return rspl

    @property
    def ctrlptsw(self):
        """ Weighted control points (Pw)

        Weighted control points are in (x*w, y*w, z*w, w) format; where x,y,z are the coordinates and w is the weight.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the weighted control points
        :setter: Sets the weighted control points
        """
        return self._control_points

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")
        self._control_points = value
        # Clear caches
        self.reset()

    @property
    def ctrlpts(self):
        """ Control points (P)

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets unweighted control points. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets unweighted control points
        :type: list
        """
        # Populate the cache, if necessary
        if not self._cache['ctrlpts']:
            self._cache['ctrlpts'], self._cache['weights'] = separate_ctrlpts_weights(self._control_points.data)
        return self._cache['ctrlpts']

    @ctrlpts.setter
    def ctrlpts(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")

        # Check if we can retrieve the existing weights. If not, generate a weights vector of 1.0s.
        if not self.weights:
            weights = [1.0 for _ in range(len(value))]
        else:
            weights = self.weights

        # Generate weighted control points using the new control points
        value.points  = combine_ctrlpts_weights(value.points, weights)

        # Set new weighted control points
        self._control_points = value

        # Clear caches
        self.reset()


@export
class Volume(BSpline.Volume):
    """ Data storage and evaluation class for NURBS (rational) volumes.

    The rational shapes have some minor differences between the non-rational ones. This class is designed to operate
    with weighted control points (Pw) as described in *The NURBS Book* by Piegl and Tiller. Therefore, it provides
    a different set of properties (i.e. getters and setters):

        * ``ctrlptsw``: 1-dimensional array of weighted control points
        * ``ctrlpts``: 1-dimensional array of control points
        * ``weights``: 1-dimensional array of weights
    """

    def __init__(self, *args, **kwargs):
        super(Volume, self).__init__(*args, **kwargs)
        self._rational = True
        self._evaluator = evaluators.VolumeEvaluatorRational()

    @classmethod
    def from_bspline(cls, obj):
        """ Creates a rational B-spline volume from a non-rational B-spline volume

        :param obj: B-spline volume
        :type obj: BSpline.Volume
        """
        if obj.pdimension != 3:
            raise GeomdlError("Parametric dimension mismatch")
        rspl = cls()
        rspl.degree = obj.degree
        rspl.knotvector = obj.knotvector
        rspl.ctrlpts = obj.ctrlpts
        rspl.delta = obj.delta
        return rspl

    @property
    def ctrlptsw(self):
        """ Weighted control points (Pw)

        Weighted control points are in (x*w, y*w, z*w, w) format; where x,y,z are the coordinates and w is the weight.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the weighted control points
        :setter: Sets the weighted control points
        """
        return self._control_points

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")
        self._control_points = value
        # Clear caches
        self.reset()

    @property
    def ctrlpts(self):
        """ Control points (P)

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets unweighted control points. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets unweighted control points
        :type: list
        """
        # Populate the cache, if necessary
        if not self._cache['ctrlpts']:
            self._cache['ctrlpts'], self._cache['weights'] = separate_ctrlpts_weights(self._control_points.data)
        return self._cache['ctrlpts']

    @ctrlpts.setter
    def ctrlpts(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")

        # Check if we can retrieve the existing weights. If not, generate a weights vector of 1.0s.
        if not self.weights:
            weights = [1.0 for _ in range(len(value))]
        else:
            weights = self.weights

        # Generate weighted control points using the new control points
        value.points  = combine_ctrlpts_weights(value.points, weights)

        # Set new weighted control points
        self._control_points = value

        # Clear caches
        self.reset()
