"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: Provides data storage and evaluation functionality for rational B-spline geometries

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import BSpline
from .base import export, GeomdlError
from .evaluators import default_rational as defeval


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
        self._evaluator = defeval.CurveEvaluatorRational()


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
        self._evaluator = defeval.SurfaceEvaluatorRational()

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
        self._evaluator = defeval.VolumeEvaluatorRational()

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
