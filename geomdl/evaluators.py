"""
.. module:: evaluators
    :platform: Unix, Windows
    :synopsis: Provides spline evaluator classes

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from . import linalg, helpers
from .base import export, GeomdlFloat, GeomdlEvaluator


@export
class CurveEvaluator(GeomdlEvaluator):
    """ Sequential curve evaluation algorithms

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.2: CurveDerivsAlg1
    """

    def evaluate(self, datadict, **kwargs):
        """ Evaluates the curve.

        Keyword Arguments:
            * ``start``: starting parametric position for evaluation
            * ``stop``: ending parametric position for evaluation

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :return: evaluated points
        :rtype: list
        """
        # Geometry data from datadict
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Keyword arguments
        start = kwargs.get('start', [GeomdlFloat(0.0) for _ in range(datadict['pdimension'])])
        stop = kwargs.get('stop', [GeomdlFloat(1.0) for _ in range(datadict['pdimension'])])

        # Algorithm A3.1
        spans = [[] for _ in range(datadict['pdimension'])]
        basis = [[] for _ in range(datadict['pdimension'])]
        for idx in range(datadict['pdimension']):
            knots = linalg.linspace(start[idx], stop[idx], datadict['sample_size'][idx])
            spans[idx] = helpers.find_spans(datadict['degree'][idx], datadict['knotvector'][idx], datadict['size'][idx], knots)
            basis[idx] = helpers.basis_functions(datadict['degree'][idx], datadict['knotvector'][idx], spans[idx], knots)

        eval_points = []
        for im, su in enumerate(spans[0]):
            idx_u = su - datadict['degree'][0]
            spt = [0.0 for _ in range(dimension)]
            for k in range(0, datadict['degree'][0] + 1):
                spt[:] = [tmp + (basis[0][im][k] * cp) for tmp, cp in zip(spt, datadict['control_points'][idx_u + k])]
            eval_points.append(spt)

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
        # Geometry data from datadict
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Algorithm A3.2
        du = min(datadict['degree'][0], deriv_order)

        CK = [[GeomdlFloat(0.0) for _ in range(dimension)] for _ in range(deriv_order + 1)]

        span = helpers.find_span_linear(datadict['degree'][0], datadict['knotvector'][0], datadict['size'][0], parpos[0])
        bfunsders = helpers.basis_function_ders(datadict['degree'][0], datadict['knotvector'][0], span, parpos[0], du)

        for k in range(0, du + 1):
            idx_u = span - datadict['degree'][0]
            for j in range(0, datadict['degree'][0] + 1):
                CK[k][:] = [drv + (bfunsders[k][j] * pt) for drv, pt in
                            zip(CK[k], datadict['control_points'][idx_u + j])]

        # Return the derivatives
        return CK


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
class SurfaceEvaluator(GeomdlEvaluator):
    """ Sequential surface evaluation algorithms

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5: SurfacePoint
    * Algorithm A3.6: SurfaceDerivsAlg1
    """

    def evaluate(self, datadict, **kwargs):
        """ Evaluates the surface.

        Keyword Arguments:
            * ``start``: starting parametric position for evaluation
            * ``stop``: ending parametric position for evaluation

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :return: evaluated points
        :rtype: list
        """
        # Geometry data from datadict
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Keyword arguments
        start = kwargs.get('start', [GeomdlFloat(0.0) for _ in range(datadict['pdimension'])])
        stop = kwargs.get('stop', [GeomdlFloat(1.0) for _ in range(datadict['pdimension'])])

        # Algorithm A3.5
        spans = [[] for _ in range(datadict['pdimension'])]
        basis = [[] for _ in range(datadict['pdimension'])]
        for idx in range(datadict['pdimension']):
            knots = linalg.linspace(start[idx], stop[idx], datadict['sample_size'][idx])
            spans[idx] = helpers.find_spans(datadict['degree'][idx], datadict['knotvector'][idx], datadict['size'][idx], knots)
            basis[idx] = helpers.basis_functions(datadict['degree'][idx], datadict['knotvector'][idx], spans[idx], knots)

        eval_points = []
        for j, sv in enumerate(spans[1]):
            idx_v = sv - datadict['degree'][1]
            for i, su in enumerate(spans[0]):
                idx_u = su - datadict['degree'][0]
                spt = [GeomdlFloat(0.0) for _ in range(dimension)]
                for k in range(0, datadict['degree'][0] + 1):
                    temp = [GeomdlFloat(0.0) for _ in range(dimension)]
                    for l in range(0, datadict['degree'][1] + 1):
                        temp[:] = [tmp + (basis[1][j][l] * cp) for tmp, cp in
                                   zip(temp, datadict['control_points'][idx_u + k, idx_v + l])]
                    spt[:] = [pt + (basis[0][i][k] * tmp) for pt, tmp in zip(spt, temp)]
                eval_points.append(spt)

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
        # Geometry data from datadict
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Algorithm A3.6
        d = [min(p, deriv_order) for p in datadict['degree']]
        SKL = [[[GeomdlFloat(0.0) for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        span = [0 for _ in range(datadict['pdimension'])]
        basisdrv = [[] for _ in range(datadict['pdimension'])]
        for idx in range(datadict['pdimension']):
            span[idx] = helpers.find_span_linear(datadict['degree'][idx], datadict['knotvector'][idx], datadict['size'][idx], parpos[idx])
            basisdrv[idx] = helpers.basis_function_ders(datadict['degree'][idx], datadict['knotvector'][idx], span[idx], parpos[idx], d[idx])

        for k in range(0, d[0] + 1):
            temp = [[GeomdlFloat(0.0) for _ in range(dimension)] for _ in range(datadict['degree'][1] + 1)]
            for s in range(0, datadict['degree'][1] + 1):
                for r in range(0, datadict['degree'][0] + 1):
                    cu = span[0] - datadict['degree'][0] + r
                    cv = span[1] - datadict['degree'][1] + s
                    temp[s][:] = [tmp + (basisdrv[0][k][r] * cp) for tmp, cp in
                                  zip(temp[s], datadict['control_points'][cu, cv])]

            # dd = min(deriv_order - k, d[1])
            dd = min(deriv_order, d[1])
            for l in range(0, dd + 1):
                for s in range(0, datadict['degree'][1] + 1):
                    SKL[k][l][:] = [elem + (basisdrv[1][l][s] * tmp) for elem, tmp in zip(SKL[k][l], temp[s])]

        return SKL


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
class VolumeEvaluator(GeomdlEvaluator):
    """ Sequential volume evaluation algorithms """

    def evaluate(self, datadict, **kwargs):
        """ Evaluates the volume

        Keyword Arguments:
            * ``start``: starting parametric position for evaluation
            * ``stop``: ending parametric position for evaluation

        :param datadict: data dictionary containing the necessary variables
        :type datadict: dict
        :return: evaluated points
        :rtype: list
        """
        # Geometry data from datadict
        dimension = datadict['dimension'] + 1 if datadict['rational'] else datadict['dimension']

        # Keyword arguments
        start = kwargs.get('start', [GeomdlFloat(0.0) for _ in range(datadict['pdimension'])])
        stop = kwargs.get('stop', [GeomdlFloat(1.0) for _ in range(datadict['pdimension'])])

        # Algorithm A3.5 (modified)
        spans = [[] for _ in range(datadict['pdimension'])]
        basis = [[] for _ in range(datadict['pdimension'])]
        for idx in range(datadict['pdimension']):
            knots = linalg.linspace(start[idx], stop[idx], datadict['sample_size'][idx])
            spans[idx] = helpers.find_spans(datadict['degree'][idx], datadict['knotvector'][idx], datadict['size'][idx], knots)
            basis[idx] = helpers.basis_functions(datadict['degree'][idx], datadict['knotvector'][idx], spans[idx], knots)

        eval_points = []
        for k, sw in enumerate(spans[2]):
            iw = sw - datadict['degree'][2]
            for j, sv in enumerate(spans[1]):
                iv = sv - datadict['degree'][1]
                for i, su in enumerate(spans[0]):
                    iu = su - datadict['degree'][0]
                    spt = [GeomdlFloat(0.0) for _ in range(dimension)]
                    for du in range(0, datadict['degree'][0] + 1):
                        temp2 = [GeomdlFloat(0.0) for _ in range(dimension)]
                        for dv in range(0, datadict['degree'][1] + 1):
                            temp = [GeomdlFloat(0.0) for _ in range(dimension)]
                            for dw in range(0, datadict['degree'][2] + 1):
                                temp[:] = [tmp + (basis[2][k][dw] * cp) for tmp, cp in
                                           zip(temp, datadict['control_points'][iu + du, iv + dv, iw + dw])]
                            temp2[:] = [pt + (basis[1][j][dv] * tmp) for pt, tmp in zip(temp2, temp)]
                        spt[:] = [pt + (basis[0][i][du] * tmp) for pt, tmp in zip(spt, temp2)]
                    eval_points.append(spt)

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
        # TO-DO: Complete volume derivatives
        return list()


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


# Don't export alternative curve evalutator
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

        span = helpers.find_span_linear(datadict['degree'][0], datadict['knotvector'][0], datadict['size'][0], parpos)
        bfuns = helpers.basis_function_all(datadict['degree'][0], datadict['knotvector'][0], datadict['size'][0], parpos)

        # Algorithm A3.3
        PK = helpers.curve_deriv_cpts(dimension, datadict['degree'][0], datadict['knotvector'][0], ctrlpts = datadict['control_points'].data,
                                      rs=((span - datadict['degree'][0]), span), deriv_order=du)

        for k in range(0, du + 1):
            for j in range(0, datadict['degree'][0] - k + 1):
                CK[k][:] = [elem + (bfuns[j][datadict['degree'][0] - k] * pt) for elem, pt in
                            zip(CK[k], PK[k][j])]

        # Return the derivatives
        return CK


# Don't export alternative surface evaluator
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
        ctrlpts = datadict['control_points'].data
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
