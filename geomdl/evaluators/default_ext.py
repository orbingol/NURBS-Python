"""
.. module:: evaluators.default_ext
    :platform: Unix, Windows
    :synopsis: Default evaluation algorithms - extended version

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from .. import linalg, helpers
from ..base import GeomdlFloat
from .default import CurveEvaluator, SurfaceEvaluator

__all__ = []


class CurveEvaluator2(CurveEvaluator):
    """ Sequential curve evaluation algorithms (alternative)

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.3: CurveDerivCpts
    * Algorithm A3.4: CurveDerivsAlg2
    """

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
        # Geometry data from datadict
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Algorithm A3.4
        du = min(datadict['degree'][0], deriv_order)

        CK = [[GeomdlFloat(0.0) for _ in range(dimension)] for _ in range(deriv_order + 1)]

        span = helpers.find_span_linear(datadict['degree'][0], datadict['knotvector'][0], datadict['size'][0], parpos[0])
        bfuns = helpers.basis_function_all(datadict['degree'][0], datadict['knotvector'][0], span, parpos[0])

        # Algorithm A3.3
        PK = helpers.curve_deriv_cpts(dimension, datadict['degree'][0], datadict['knotvector'][0], datadict['control_points'].points,
                                      rs=((span - datadict['degree'][0]), span), deriv_order=du)

        for k in range(0, du + 1):
            for j in range(0, datadict['degree'][0] - k + 1):
                CK[k][:] = [elem + (bfuns[j][datadict['degree'][0] - k] * pt) for elem, pt in
                            zip(CK[k], PK[k][j])]

        # Return the derivatives
        return CK


class SurfaceEvaluator2(SurfaceEvaluator):
    """ Sequential surface evaluation algorithms (alternative)

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5: SurfacePoint
    * Algorithm A3.7: SurfaceDerivCpts
    * Algorithm A3.8: SurfaceDerivsAlg2
    """

    def derivatives(self, datadict, parpos, deriv_order=0, **kwargs):
        """ Evaluates the n-th order derivatives at the input parametric position.

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :param parpos: parametric position where the derivatives will be computed
        :type parpos: list, tuple
        :param deriv_order: derivative order; to get the i-th derivative
        :type deriv_order: int
        :return: evaluated derivatives
        :rtype: list
        """
        # Geometry data from datadict
        degree = datadict['degree']
        knotvector = datadict['knotvector']
        ctrlpts = datadict['control_points'].points
        size = datadict['size']
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']
        pdimension = datadict['pdimension']

        SKL = [[[GeomdlFloat(0.0) for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        d = (min(degree[0], deriv_order), min(degree[1], deriv_order))

        span = [0 for _ in range(pdimension)]
        basis = [[] for _ in range(pdimension)]
        for idx in range(pdimension):
            span[idx] = helpers.find_span_linear(degree[idx], knotvector[idx], size[idx], parpos[idx])
            basis[idx] = helpers.basis_function_all(degree[idx], knotvector[idx], span[idx], parpos[idx])

        # Algorithm A3.7
        # rs: (minimum, maximum) span on the u-direction., ss: (minimum, maximum) span on the v-direction
        PKL = helpers.surface_deriv_cpts(dimension, degree, knotvector, ctrlpts, size,
                                         rs=(span[0] - degree[0], span[0]), ss=(span[1] - degree[1], span[1]),
                                         deriv_order=deriv_order)

        # Evaluating the derivative at parameters (u,v) using its control points
        for k in range(0, d[0] + 1):
            dd = min(deriv_order - k, d[1])
            for l in range(0, dd + 1):
                #SKL[k][l] = [GeomdlFloat(0.0) for _ in range(dimension)]
                for i in range(0, degree[1] - l + 1):
                    temp = [GeomdlFloat(0.0) for _ in range(dimension)]
                    for j in range(0, degree[0] - k + 1):
                        temp[:] = [elem + (basis[0][j][degree[0] - k] * drv_ctl_p) for elem, drv_ctl_p in
                                   zip(temp, PKL[k][l][j][i])]
                    SKL[k][l][:] = [elem + (basis[1][i][degree[1] - l] * drv_ctl_p) for elem, drv_ctl_p in
                                    zip(SKL[k][l], temp)]
        return SKL
