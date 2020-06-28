"""
.. module:: evaluators.default_rational
    :platform: Unix, Windows
    :synopsis: Default evaluation algorithms (rational)

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import linalg
from ..base import export, GeomdlFloat
from .default import CurveEvaluator, SurfaceEvaluator, VolumeEvaluator


@export
class CurveEvaluatorRational(CurveEvaluator):
    """ Sequential rational curve evaluation algorithms

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A4.2: RatCurveDerivs
    """

    def evaluate(self, datadict, **kwargs):
        """ Evaluates the rational curve.

        Keyword Arguments:
            * ``start``: starting parametric position for evaluation
            * ``stop``: ending parametric position for evaluation

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :return: evaluated points
        :rtype: list
        """
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Algorithm A4.1
        crvptw = super(CurveEvaluatorRational, self).evaluate(datadict, **kwargs)

        # Divide by weight
        eval_points = []
        for pt in crvptw:
            cpt = [GeomdlFloat(c / pt[-1]) for c in pt[0:(dimension - 1)]]
            eval_points.append(cpt)

        return eval_points

    def derivatives(self, datadict, parpos, deriv_order=0, **kwargs):
        """ Evaluates the n-th order derivatives at the input parametric position

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :param parpos: parametric position where the derivatives will be computed
        :type parpos: list, tuple
        :param deriv_order: derivative order; to get the i-th derivative
        :type deriv_order: int
        :return: evaluated derivatives
        :rtype: list
        """
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Call the parent function to evaluate A(u) and w(u) derivatives
        CKw = super(CurveEvaluatorRational, self).derivatives(datadict, parpos, deriv_order, **kwargs)

        # Algorithm A4.2
        CK = [[GeomdlFloat(0.0) for _ in range(dimension - 1)] for _ in range(deriv_order + 1)]
        for k in range(0, deriv_order + 1):
            v = [val for val in CKw[k][0:(dimension - 1)]]
            for i in range(1, k + 1):
                v[:] = [tmp - (linalg.binomial_coefficient(k, i) * CKw[i][-1] * drv) for tmp, drv in
                        zip(v, CK[k - i])]
            CK[k][:] = [tmp / CKw[0][-1] for tmp in v]

        # Return C(u) derivatives
        return CK


@export
class SurfaceEvaluatorRational(SurfaceEvaluator):
    """ Sequential rational surface evaluation algorithms

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A4.3: SurfacePoint
    * Algorithm A4.4: RatSurfaceDerivs
    """

    def evaluate(self, datadict, **kwargs):
        """ Evaluates the rational surface.

        Keyword Arguments:
            * ``start``: starting parametric position for evaluation
            * ``stop``: ending parametric position for evaluation

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :return: evaluated points
        :rtype: list
        """
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Algorithm A4.3
        cptw = super(SurfaceEvaluatorRational, self).evaluate(datadict, **kwargs)

        # Divide by weight
        eval_points = []
        for pt in cptw:
            cpt = [GeomdlFloat(c / pt[-1]) for c in pt[0:(dimension - 1)]]
            eval_points.append(cpt)

        return eval_points

    def derivatives(self, datadict, parpos, deriv_order=0, **kwargs):
        """ Evaluates the n-th order derivatives at the input parametric position

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :param parpos: parametric position where the derivatives will be computed
        :type parpos: list, tuple
        :param deriv_order: derivative order; to get the i-th derivative
        :type deriv_order: int
        :return: evaluated derivatives
        :rtype: list
        """
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Call the parent function to evaluate A(u) and w(u) derivatives
        SKLw = super(SurfaceEvaluatorRational, self).derivatives(datadict, parpos, deriv_order, **kwargs)

        # Generate an empty list of derivatives
        SKL = [[[GeomdlFloat(0.0) for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        # Algorithm A4.4
        for k in range(0, deriv_order + 1):
            # for l in range(0, deriv_order - k + 1):
            for l in range(0, deriv_order + 1):
                # Deep copying might seem a little overkill but we also want to avoid same pointer issues too
                v = copy.deepcopy(SKLw[k][l])

                for j in range(1, l + 1):
                    v[:] = [tmp - (linalg.binomial_coefficient(l, j) * SKLw[0][j][-1] * drv) for tmp, drv in
                            zip(v, SKL[k][l - j])]
                for i in range(1, k + 1):
                    v[:] = [tmp - (linalg.binomial_coefficient(k, i) * SKLw[i][0][-1] * drv) for tmp, drv in
                            zip(v, SKL[k - i][l])]
                    v2 = [0.0 for _ in range(dimension - 1)]
                    for j in range(1, l + 1):
                        v2[:] = [tmp + (linalg.binomial_coefficient(l, j) * SKLw[i][j][-1] * drv) for tmp, drv in
                                 zip(v2, SKL[k - i][l - j])]
                    v[:] = [tmp - (linalg.binomial_coefficient(k, i) * tmp2) for tmp, tmp2 in zip(v, v2)]
                SKL[k][l][:] = [tmp / SKLw[0][0][-1] for tmp in v[0:(dimension - 1)]]

        # Return S(u,v) derivatives
        return SKL


@export
class VolumeEvaluatorRational(VolumeEvaluator):
    """ Sequential rational volume evaluation algorithms """

    def evaluate(self, datadict, **kwargs):
        """ Evaluates the rational volume

        Keyword Arguments:
            * ``start``: starting parametric position for evaluation
            * ``stop``: ending parametric position for evaluation

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :return: evaluated points
        :rtype: list
        """
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Algorithm A4.3 (modified)
        cptw = super(VolumeEvaluatorRational, self).evaluate(datadict, **kwargs)

        # Divide by weight
        eval_points = []
        for pt in cptw:
            cpt = [GeomdlFloat(c / pt[-1]) for c in pt[0:(dimension - 1)]]
            eval_points.append(cpt)

        return eval_points

    def derivatives(self, datadict, parpos, deriv_order=0, **kwargs):
        """ Evaluates the n-th order derivatives at the input parametric position

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :param parpos: parametric position where the derivatives will be computed
        :type parpos: list, tuple
        :param deriv_order: derivative order; to get the i-th derivative
        :type deriv_order: int
        :return: evaluated derivatives
        :rtype: list
        """
        # Call the parent function to evaluate A(u) and w(u) derivatives
        SKLw = super(VolumeEvaluatorRational, self).derivatives(datadict, parpos, deriv_order, **kwargs)

        # TO-DO: Complete rational volume derivatives
        return SKLw
