"""
.. module:: evaluators
    :platform: Unix, Windows
    :synopsis: Provides spline evaluator classes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import copy
import abc
from . import linalg, helpers
from ._utilities import add_metaclass, export


@add_metaclass(abc.ABCMeta)
class AbstractEvaluator(object):
    """ Abstract base class for implementations of fundamental spline algorithms, such as evaluate and derivative.

    **Abstract Methods**:

    * ``evaluate`` is used for computation of the complete spline shape
    * ``derivative_single`` is used for computation of derivatives at a single parametric coordinate

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see :py:mod:`helpers` module for details.
    """

    def __init__(self, **kwargs):
        self._name = kwargs.get('name', self.__class__.__name__)
        self._span_func = kwargs.get('find_span_func', None)

    @property
    def name(self):
        """ Evaluator name.

        :getter: Gets the name of the evaluator
        :type: str
        """
        return self._name

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Abstract method for computation of points over a range of parameters.

        .. note::

            This is an abstract method and it must be implemented in the subclass.
        """
        pass

    @abc.abstractmethod
    def derivatives(self, **kwargs):
        """ Abstract method for computation of derivatives at a single parameter.

        .. note::

            This is an abstract method and it must be implemented in the subclass.
        """
        pass


@export
class CurveEvaluator(AbstractEvaluator):
    """ Sequential curve evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.2: CurveDerivsAlg1

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(CurveEvaluator, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate(self, **kwargs):
        """ Evaluates the curve. """
        # Call parent method
        super(CurveEvaluator, self).evaluate(**kwargs)

        start = kwargs.get('start')
        stop = kwargs.get('stop')
        sample_size = kwargs.get('sample_size')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')
        precision = kwargs.get('precision')

        # Algorithm A3.1
        knots = linalg.linspace(start, stop, sample_size, decimals=precision)
        spans = helpers.find_spans(degree, knotvector, len(ctrlpts), knots, self._span_func)
        basis = helpers.basis_functions(degree, knotvector, spans, knots)

        eval_points = []
        for idx in range(len(knots)):
            crvpt = [0.0 for _ in range(dimension)]
            for i in range(0, degree + 1):
                crvpt[:] = [crv_p + (basis[idx][i] * ctl_p) for crv_p, ctl_p in
                            zip(crvpt, ctrlpts[spans[idx] - degree + i])]

            eval_points.append(crvpt)

        return eval_points

    def derivatives(self, **kwargs):
        """ Evaluates the derivatives at the input parameter. """
        # Call parent method
        super(CurveEvaluator, self).derivatives(**kwargs)

        param = kwargs.get('parameter')
        deriv_order = kwargs.get('deriv_order', 0)
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.2
        du = min(degree, deriv_order)

        CK = [[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)]

        span = self._span_func(degree, knotvector, len(ctrlpts), param)
        bfunsders = helpers.basis_function_ders(degree, knotvector, span, param, du)

        for k in range(0, du + 1):
            for j in range(0, degree + 1):
                CK[k][:] = [drv + (bfunsders[k][j] * ctl_pt) for drv, ctl_pt in
                            zip(CK[k], ctrlpts[span - degree + j])]

        # Return the derivatives
        return CK


class CurveEvaluator2(CurveEvaluator):
    """ Sequential curve evaluation algorithms (alternative).

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.4: CurveDerivsAlg2

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(CurveEvaluator2, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    @staticmethod
    def derivatives_ctrlpts(**kwargs):
        """ Computes the control points of all derivative curves up to and including the {degree}-th derivative.

        Implementation of Algorithm A3.3 from The NURBS Book by Piegl & Tiller.

        Output is PK[k][i], i-th control point of the k-th derivative curve where 0 <= k <= degree and r1 <= i <= r2-k.
        """
        # r1 - minimum span, r2 - maximum span
        r1 = kwargs.get('r1')
        r2 = kwargs.get('r2')
        deriv_order = kwargs.get('deriv_order')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.3
        r = r2 - r1
        PK = [[[None for _ in range(dimension)] for _ in range(r + 1)] for _ in range(deriv_order + 1)]
        for i in range(0, r + 1):
            PK[0][i][:] = [elem for elem in ctrlpts[r1 + i]]

        for k in range(1, deriv_order + 1):
            tmp = degree - k + 1
            for i in range(0, r - k + 1):
                PK[k][i][:] = [tmp * (elem1 - elem2) /
                               (knotvector[r1 + i + degree + 1] - knotvector[r1 + i + k]) for elem1, elem2
                               in zip(PK[k - 1][i + 1], PK[k - 1][i])]

        # Return a 2-dimensional list of control points
        return PK

    def derivatives(self, **kwargs):
        """ Evaluates the derivatives at the input parameter. """
        # Call parent method
        super(CurveEvaluator2, self).derivatives(**kwargs)

        param = kwargs.get('parameter')
        deriv_order = kwargs.get('deriv_order', 0)
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.4
        du = min(degree, deriv_order)

        CK = [[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)]

        span = self._span_func(degree, knotvector, len(ctrlpts), param)
        bfuns = helpers.basis_function_all(degree, tuple(knotvector), span, param)

        # "derivatives_ctrlpts" is a static method that could be called like below
        PK = CurveEvaluator2.derivatives_ctrlpts(r1=(span - degree), r2=span,
                                                 degree=degree,
                                                 knotvector=knotvector,
                                                 ctrlpts=ctrlpts,
                                                 dimension=dimension,
                                                 deriv_order=du)

        for k in range(0, du + 1):
            for j in range(0, degree - k + 1):
                CK[k][:] = [elem + (bfuns[j][degree - k] * drv_ctl_p) for elem, drv_ctl_p in
                            zip(CK[k], PK[k][j])]

        # Return the derivatives
        return CK


@export
class CurveEvaluatorRational(CurveEvaluator):
    """ Sequential rational curve evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A4.2: RatCurveDerivs

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(CurveEvaluatorRational, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate(self, **kwargs):
        """ Evaluates the rational curve. """
        dimension = kwargs.get('dimension')

        # Algorithm A4.1
        crvptw = super(CurveEvaluatorRational, self).evaluate(**kwargs)

        # Divide by weight
        eval_points = []
        for pt in crvptw:
            cpt = [float(c / pt[-1]) for c in pt[0:(dimension - 1)]]
            eval_points.append(cpt)

        return eval_points

    def derivatives(self, **kwargs):
        """ Evaluates the derivatives at the input parameter. """
        deriv_order = kwargs.get('deriv_order')
        dimension = kwargs.get('dimension')

        # Call the parent function to evaluate A(u) and w(u) derivatives
        CKw = super(CurveEvaluatorRational, self).derivatives(**kwargs)

        # Algorithm A4.2
        CK = [[0.0 for _ in range(dimension - 1)] for _ in range(deriv_order + 1)]
        for k in range(0, deriv_order + 1):
            v = [val for val in CKw[k][0:(dimension - 1)]]
            for i in range(1, k + 1):
                v[:] = [tmp - (linalg.binomial_coefficient(k, i) * CKw[i][-1] * drv) for tmp, drv in
                        zip(v, CK[k - i])]
            CK[k][:] = [tmp / CKw[0][-1] for tmp in v]

        # Return C(u) derivatives
        return CK


@export
class SurfaceEvaluator(AbstractEvaluator):
    """ Sequential surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5: SurfacePoint
    * Algorithm A3.6: SurfaceDerivsAlg1

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(SurfaceEvaluator, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate(self, **kwargs):
        """ Evaluates the surface. """
        # Call parent method
        super(SurfaceEvaluator, self).evaluate(**kwargs)

        start = kwargs.get('start')
        stop = kwargs.get('stop')
        sample_size = kwargs.get('sample_size')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        ctrlpts_size = kwargs.get('ctrlpts_size')
        dimension = kwargs.get('dimension')
        precision = kwargs.get('precision')

        # Algorithm A3.5
        spans = [[] for _ in range(len(degree))]
        basis = [[] for _ in range(len(degree))]
        for idx in range(len(degree)):
            knots = linalg.linspace(start[idx], stop[idx], sample_size[idx], decimals=precision)
            spans[idx] = helpers.find_spans(degree[idx], knotvector[idx], ctrlpts_size[idx], knots, self._span_func)
            basis[idx] = helpers.basis_functions(degree[idx], knotvector[idx], spans[idx], knots)

        eval_points = []
        for i in range(len(spans[0])):
            idx_u = spans[0][i] - degree[0]
            for j in range(len(spans[1])):
                idx_v = spans[1][j] - degree[1]
                spt = [0.0 for _ in range(dimension)]
                for k in range(0, degree[0] + 1):
                    temp = [0.0 for _ in range(dimension)]
                    for l in range(0, degree[1] + 1):
                        temp[:] = [tmp + (basis[1][j][l] * cp) for tmp, cp in
                                   zip(temp, ctrlpts[idx_v + l + (ctrlpts_size[1] * (idx_u + k))])]
                    spt[:] = [pt + (basis[0][i][k] * tmp) for pt, tmp in zip(spt, temp)]

                eval_points.append(spt)

        return eval_points

    def derivatives(self, **kwargs):
        """ Evaluates the derivatives at the input parameter. """
        # Call parent method
        super(SurfaceEvaluator, self).derivatives(**kwargs)

        deriv_order = kwargs.get('deriv_order')
        param = kwargs.get('parameter')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        ctrlpts_size = kwargs.get('ctrlpts_size')
        dimension = kwargs.get('dimension')

        # Algorithm A3.6
        d = (min(degree[0], deriv_order), min(degree[1], deriv_order))

        SKL = [[[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        span = [0 for _ in range(len(degree))]
        basisdrv = [[] for _ in range(len(degree))]
        for idx in range(len(degree)):
            span[idx] = self._span_func(degree[idx], knotvector[idx], ctrlpts_size[idx], param[idx])
            basisdrv[idx] = helpers.basis_function_ders(degree[idx], knotvector[idx], span[idx], param[idx], d[idx])

        for k in range(0, d[0] + 1):
            temp = [[0.0 for _ in range(dimension)] for _ in range(degree[1] + 1)]
            for s in range(0, degree[1] + 1):
                for r in range(0, degree[0] + 1):
                    cu = span[0] - degree[0] + r
                    cv = span[1] - degree[1] + s
                    temp[s][:] = [tmp + (basisdrv[0][k][r] * cp) for tmp, cp in
                                  zip(temp[s], ctrlpts[cv + (ctrlpts_size[1] * cu)])]

            # dd = min(deriv_order - k, d[1])
            dd = min(deriv_order, d[1])
            for l in range(0, dd + 1):
                for s in range(0, degree[1] + 1):
                    SKL[k][l][:] = [elem + (basisdrv[1][l][s] * tmp) for elem, tmp in zip(SKL[k][l], temp[s])]

        return SKL


class SurfaceEvaluator2(SurfaceEvaluator):
    """ Sequential surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5: SurfacePoint
    * Algorithm A3.7: SurfaceDerivCpts
    * Algorithm A3.8: SurfaceDerivsAlg2

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(SurfaceEvaluator2, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    @staticmethod
    def derivatives_ctrlpts(**kwargs):
        """ Computes the control points of all derivative surfaces up to and including the {degree}-th derivative.

        Output is PKL[k][l][i][j], i,j-th control point of the surface differentiated k times w.r.t to u and
        l times w.r.t v.
        """
        r1 = kwargs.get('r1')  # minimum span on the u-direction
        r2 = kwargs.get('r2')  # maximum span on the u-direction
        s1 = kwargs.get('s1')  # minimum span on the v-direction
        s2 = kwargs.get('s2')  # maximum span on the v-direction

        deriv_order = kwargs.get('deriv_order')
        ctrlpts_size = kwargs.get('ctrlpts_size')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        PKL = [[[[[None for _ in range(dimension)]
                  for _ in range(ctrlpts_size[1])] for _ in range(ctrlpts_size[0])]
                for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        du = min(degree[0], deriv_order)
        dv = min(degree[1], deriv_order)

        r = r2 - r1
        s = s2 - s1

        # Control points of the U derivatives of every U-curve
        for j in range(s1, s2 + 1):
            PKu = CurveEvaluator2.derivatives_ctrlpts(r1=r1, r2=r2,
                                                      degree=degree[0],
                                                      knotvector=knotvector[0],
                                                      ctrlpts=[ctrlpts[j + (ctrlpts_size[1] * i)] for i in range(ctrlpts_size[0])],
                                                      dimension=dimension,
                                                      deriv_order=du)

            # Copy into output as the U partial derivatives
            for k in range(0, du + 1):
                for i in range(0, r - k + 1):
                    PKL[k][0][i][j - s1] = PKu[k][i]

        # Control points of the V derivatives of every U-differentiated V-curve
        for k in range(0, du):
            for i in range(0, r - k + 1):
                dd = min(deriv_order - k, dv)

                PKuv = CurveEvaluator2.derivatives_ctrlpts(r1=0, r2=s,
                                                           degree=degree[1],
                                                           knotvector=knotvector[1][s1:],
                                                           ctrlpts=PKL[k][0][i],
                                                           dimension=dimension,
                                                           deriv_order=dd)

                # Copy into output
                for l in range(1, dd + 1):
                    for j in range(0, s - l + 1):
                        PKL[k][l][i][j] = PKuv[l][j]

        return PKL

    def derivatives(self, **kwargs):
        """ Evaluates the derivatives at the input parameter. """
        deriv_order = kwargs.get('deriv_order')
        param = kwargs.get('parameter')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts_size = kwargs.get('ctrlpts_size')
        dimension = kwargs.get('dimension')

        SKL = [[[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        d = (min(degree[0], deriv_order), min(degree[1], deriv_order))

        span = [0 for _ in range(len(degree))]
        basis = [[] for _ in range(len(degree))]
        for idx in range(len(degree)):
            span[idx] = self._span_func(degree[idx], knotvector[idx], ctrlpts_size[idx], param[idx])
            basis[idx] = helpers.basis_function_all(degree[idx], knotvector[idx], span[idx], param[idx])

        PKL = self.derivatives_ctrlpts(r1=span[0] - degree[0], r2=span[0],
                                       s1=span[1] - degree[1], s2=span[1],
                                       **kwargs)

        # Evaluating the derivative at parameters (u,v) using its control points
        for k in range(0, d[0] + 1):
            dd = min(deriv_order - k, d[1])

            for l in range(0, dd + 1):
                SKL[k][l] = [0.0 for _ in range(dimension)]

                for i in range(0, degree[1] - l + 1):
                    temp = [0.0 for _ in range(dimension)]

                    for j in range(0, degree[0] - k + 1):
                        temp[:] = [elem + (basis[0][j][degree[0] - k] * drv_ctl_p) for elem, drv_ctl_p in
                                   zip(temp, PKL[k][l][j][i])]

                    SKL[k][l][:] = [elem + (basis[1][i][degree[1] - l] * drv_ctl_p) for elem, drv_ctl_p in
                                    zip(SKL[k][l], temp)]

        return SKL


@export
class SurfaceEvaluatorRational(SurfaceEvaluator):
    """ Sequential rational surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A4.3: SurfacePoint
    * Algorithm A4.4: RatSurfaceDerivs

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(SurfaceEvaluatorRational, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate(self, **kwargs):
        """ Evaluates the rational surface. """
        dimension = kwargs.get('dimension')

        # Algorithm A4.3
        cptw = super(SurfaceEvaluatorRational, self).evaluate(**kwargs)

        # Divide by weight
        eval_points = []
        for pt in cptw:
            cpt = [float(c / pt[-1]) for c in pt[0:(dimension - 1)]]
            eval_points.append(cpt)

        return eval_points

    def derivatives(self, **kwargs):
        """ Evaluates the derivatives at the input parameter. """
        deriv_order = kwargs.get('deriv_order')
        dimension = kwargs.get('dimension')

        # Call the parent function to evaluate A(u) and w(u) derivatives
        SKLw = super(SurfaceEvaluatorRational, self).derivatives(**kwargs)

        # Generate an empty list of derivatives
        SKL = [[[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

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
class VolumeEvaluator(AbstractEvaluator):
    """ Sequential volume evaluation algorithms.

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(VolumeEvaluator, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate(self, **kwargs):
        """ Evaluates the volume. """
        # Call parent method
        super(VolumeEvaluator, self).evaluate(**kwargs)

        start = kwargs.get('start')
        stop = kwargs.get('stop')
        sample_size = kwargs.get('sample_size')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        size = kwargs.get('ctrlpts_size')
        dimension = kwargs.get('dimension')
        precision = kwargs.get('precision')

        spans = [[] for _ in range(len(degree))]
        basis = [[] for _ in range(len(degree))]
        for idx in range(len(degree)):
            knots = linalg.linspace(start[idx], stop[idx], sample_size[idx], decimals=precision)
            spans[idx] = helpers.find_spans(degree[idx], knotvector[idx], size[idx], knots, self._span_func)
            basis[idx] = helpers.basis_functions(degree[idx], knotvector[idx], spans[idx], knots)

        eval_points = []
        for i in range(len(spans[0])):
            iu = spans[0][i] - degree[0]
            for j in range(len(spans[1])):
                iv = spans[1][j] - degree[1]
                for k in range(len(spans[2])):
                    iw = spans[2][k] - degree[2]
                    spt = [0.0 for _ in range(dimension)]
                    for du in range(0, degree[0] + 1):
                        temp2 = [0.0 for _ in range(dimension)]
                        for dv in range(0, degree[1] + 1):
                            temp = [0.0 for _ in range(dimension)]
                            for dw in range(0, degree[2] + 1):
                                # flattening algorithm 1: x + (WIDTH * y) + (WIDTH * DEPTH) * z
                                # flattening algorithm 2: x + (WIDTH * (y + (DEPTH * z))
                                temp[:] = [tmp + (basis[2][k][dw] * cp) for tmp, cp in
                                           zip(temp, ctrlpts[iv + dv + (size[1] * (iu + du + (size[0] * (iw + dw))))])]
                            temp2[:] = [pt + (basis[1][j][dv] * tmp) for pt, tmp in zip(temp2, temp)]
                        spt[:] = [pt + (basis[0][i][du] * tmp) for pt, tmp in zip(spt, temp2)]
                    eval_points.append(spt)

        return eval_points

    def derivatives(self, **kwargs):
        """ Evaluates the derivative at the given parametric coordinate. """
        pass


@export
class VolumeEvaluatorRational(VolumeEvaluator):
    """ Sequential rational volume evaluation algorithms.

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(VolumeEvaluatorRational, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate(self, **kwargs):
        """ Evaluates the rational volume. """
        dimension = kwargs.get('dimension')

        cptw = super(VolumeEvaluatorRational, self).evaluate(**kwargs)

        # Divide by weight
        eval_points = []
        for pt in cptw:
            cpt = [float(c / pt[-1]) for c in pt[0:(dimension - 1)]]
            eval_points.append(cpt)

        return eval_points

    def derivatives(self, **kwargs):
        """ Evaluates the derivatives at the input parameter. """
        pass
