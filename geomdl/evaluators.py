"""
.. module:: evaluators
    :platform: Unix, Windows
    :synopsis: Provides NURBS & B-Spline evaluation algorithms

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import copy
import abc
import six
from . import helpers
from . import utilities


class AbstractEvaluator(six.with_metaclass(abc.ABCMeta, object)):
    """ Evaluator abstract base class.

    The methods ``evaluate`` and ``derivative`` is intended to be used for computation over a range of values.
    The suggested usage of ``evaluate_single`` and ``derivative_single`` methods are computation of a single value.

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        self._name = kwargs.get('name', self.__class__.__name__)
        self._span_func = kwargs.get('find_span_func', None)

    @property
    def name(self):
        """ Evaluator name (as a string).

        :getter: Gets the name of the evaluator
        :type: str
        """
        return self._name

    @abc.abstractmethod
    def evaluate_single(self, **kwargs):
        """ Abstract method for computation of a single point at a single parameter. """
        pass

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Abstract method for computation of points over a range of parameters. """
        pass

    @abc.abstractmethod
    def derivatives_single(self, **kwargs):
        """ Abstract method for computation of derivatives at a single parameter. """
        pass

    @abc.abstractmethod
    def derivatives(self, **kwargs):
        """ Abstract method for computation of derivatives over a range of parameters. """
        pass


class AbstractCurveEvaluator(six.with_metaclass(abc.ABCMeta, object)):
    """ Curve customizations for Evaluator abstract base class. """

    def __init__(self, **kwargs):
        self._span_func = kwargs.get('find_span_func', None)

    @abc.abstractmethod
    def insert_knot(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm. """
        pass


class AbstractSurfaceEvaluator(six.with_metaclass(abc.ABCMeta, object)):
    """ Surface customizations for the Evaluator abstract base class. """

    def __init__(self, **kwargs):
        self._span_func = kwargs.get('find_span_func', None)

    @abc.abstractmethod
    def insert_knot_u(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm on the u-direction. """
        pass

    @abc.abstractmethod
    def insert_knot_v(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm on the v-direction. """
        pass


class CurveEvaluator(AbstractEvaluator, AbstractCurveEvaluator):
    """ Sequential B-Spline curve evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.2: CurveDerivsAlg1
    * Algorithm A5.1: CurveKnotIns

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(CurveEvaluator, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate_single(self, **kwargs):
        """ Evaluates a single curve point. """
        # Call parent method
        super(CurveEvaluator, self).evaluate_single(**kwargs)

        param = kwargs.get('parameter')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')
        precision = kwargs.get('precision')

        # Algorithm A3.1
        crvpt = self.evaluate(start=param, stop=param, degree=degree, knotvector=knotvector,
                              ctrlpts=ctrlpts, sample_size=1, dimension=dimension, precision=precision)

        return crvpt[0]

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
        knots = utilities.linspace(start, stop, sample_size, decimals=precision)
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

    # Evaluates the curve derivative using "CurveDerivsAlg1" algorithm
    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order curve derivatives at a single parameter. """
        # Call parent method
        super(CurveEvaluator, self).derivatives_single(**kwargs)

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

    def derivatives(self, **kwargs):
        """ Evaluates n-th order curve derivatives over a range of parameters. """
        # Call parent method
        super(CurveEvaluator, self).derivatives(**kwargs)

        # Not implemented, yet...
        raise NotImplementedError("This functionality is not implemented at the moment")

    def insert_knot(self, **kwargs):
        """ Insert knot multiple times at a single parameter. """
        # Call parent method
        super(CurveEvaluator, self).insert_knot(**kwargs)

        knot = kwargs.get('knot')
        r = kwargs.get('r')  # number of knot insertions
        s = kwargs.get('s')  # multiplicity
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')

        # Algorithm A5.1
        k = self._span_func(degree, knotvector, len(ctrlpts), knot)
        mp = len(knotvector)
        np = len(ctrlpts)
        nq = np + r

        # Initialize new knot vector array
        UQ = [0.0 for _ in range(mp + r)]
        # Initialize new control points array (control points may be weighted or not)
        Q = [[] for _ in range(nq)]
        # Initialize a local array of length p + 1
        R = [[] for _ in range(degree + 1)]

        # Load new knot vector
        for i in range(0, k + 1):
            UQ[i] = knotvector[i]
        for i in range(1, r + 1):
            UQ[k + i] = knot
        for i in range(k + 1, mp):
            UQ[i + r] = knotvector[i]

        # Save unaltered control points
        for i in range(0, k - degree + 1):
            Q[i] = ctrlpts[i]
        for i in range(k - s, np):
            Q[i + r] = ctrlpts[i]

        # The algorithm uses R array to update control points
        for i in range(0, degree - s + 1):
            R[i] = copy.deepcopy(ctrlpts[k - degree + i])

        # Insert the knot r times
        for j in range(1, r + 1):
            L = k - degree + j
            for i in range(0, degree - j - s + 1):
                alpha = (knot - knotvector[L + i]) / (knotvector[i + k + 1] - knotvector[L + i])
                R[i][:] = [alpha * elem2 + (1.0 - alpha) * elem1 for elem1, elem2 in zip(R[i], R[i + 1])]
            Q[L] = copy.deepcopy(R[0])
            Q[k + r - j - s] = copy.deepcopy(R[degree - j - s])

        # Load remaining control points
        L = k - degree + r
        for i in range(L + 1, k - s):
            Q[i] = copy.deepcopy(R[i - L])

        # Return updated knot vector and control points
        return UQ, Q


class CurveEvaluator2(CurveEvaluator):
    """ Sequential B-Spline curve evaluation algorithms (alternative).

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.4: CurveDerivsAlg2
    * Algorithm A5.1: CurveKnotIns

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(CurveEvaluator2, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Computes the control points of all derivative curves up to and including the {degree}-th derivative
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

    # Evaluates the curve derivative using "CurveDerivsAlg2" algorithm
    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order curve derivatives at a single parameter. """
        # Call parent method
        super(CurveEvaluator2, self).derivatives_single(**kwargs)

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


class NURBSCurveEvaluator(CurveEvaluator):
    """ Sequential NURBS curve evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A4.2: RatCurveDerivs
    * Algorithm A5.1: CurveKnotIns

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(NURBSCurveEvaluator, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate(self, **kwargs):
        """ Evaluates the curve. """
        dimension = kwargs.get('dimension')

        # Algorithm A4.1
        crvptw = super(NURBSCurveEvaluator, self).evaluate(**kwargs)

        # Divide by weight
        eval_points = []
        for pt in crvptw:
            cpt = [float(c / pt[-1]) for c in pt[0:(dimension - 1)]]
            eval_points.append(cpt)

        return eval_points

    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order curve derivatives at a single parameter. """
        deriv_order = kwargs.get('deriv_order')
        dimension = kwargs.get('dimension')

        # Call the parent function to evaluate A(u) and w(u) derivatives
        CKw = super(NURBSCurveEvaluator, self).derivatives_single(**kwargs)

        # Algorithm A4.2
        CK = [[0.0 for _ in range(dimension - 1)] for _ in range(deriv_order + 1)]
        for k in range(0, deriv_order + 1):
            v = [val for val in CKw[k][0:(dimension - 1)]]
            for i in range(1, k + 1):
                v[:] = [tmp - (utilities.binomial_coefficient(k, i) * CKw[i][-1] * drv) for tmp, drv in
                        zip(v, CK[k - i])]
            CK[k][:] = [tmp / CKw[0][-1] for tmp in v]

        # Return C(u) derivatives
        return CK


class SurfaceEvaluator(AbstractEvaluator, AbstractSurfaceEvaluator):
    """ Sequential B-Spline surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5: SurfacePoint
    * Algorithm A3.6: SurfaceDerivsAlg1
    * Algorithm A5.3: SurfaceKnotIns

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(SurfaceEvaluator, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate_single(self, **kwargs):
        """ Evaluates a single surface point. """
        # Call parent method
        super(SurfaceEvaluator, self).evaluate_single(**kwargs)

        param = kwargs.get('parameter')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        ctrlpts_size = kwargs.get('ctrlpts_size')
        dimension = kwargs.get('dimension')
        precision = kwargs.get('precision')

        spt = self.evaluate(start=param, stop=param, degree=degree, knotvector=knotvector, ctrlpts=ctrlpts,
                            ctrlpts_size=ctrlpts_size, sample_size=(1, 1), dimension=dimension, precision=precision)

        return spt[0]

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
            knots = utilities.linspace(start[idx], stop[idx], sample_size[idx], decimals=precision)
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

    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order surface derivatives at a (u,v) parameter. """
        # Call parent method
        super(SurfaceEvaluator, self).derivatives_single(**kwargs)

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

            dd = min(deriv_order - k, d[1])
            for l in range(0, dd + 1):
                for s in range(0, degree[1] + 1):
                    SKL[k][l][:] = [elem + (basisdrv[1][l][s] * tmp) for elem, tmp in zip(SKL[k][l], temp[s])]

        return SKL

    def derivatives(self, **kwargs):
        """ Evaluates n-th order surface derivatives over a range of (u,v) parameters. """
        # Call parent method
        super(SurfaceEvaluator, self).derivatives(**kwargs)

        # Not implemented, yet
        raise NotImplementedError("This functionality is not implemented at the moment")

    def insert_knot_u(self, **kwargs):
        """ Inserts knot(s) in u-direction. """
        # Call parent method
        super(SurfaceEvaluator, self).insert_knot_u(**kwargs)

        param = kwargs.get('parameter')
        r = kwargs.get('r')
        s = kwargs.get('s')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        ctrlpts_size = kwargs.get('ctrlpts_size')

        # Algorithm A5.3
        span = self._span_func(degree, knotvector, ctrlpts_size[0], param)

        # Initialize new knot vector array
        UQ = [0.0 for _ in range(len(knotvector) + r)]
        # Initialize new control points array (control points can be weighted or not)
        Q = [[] for _ in range((ctrlpts_size[0] + r) * ctrlpts_size[1])]
        # Initialize a local array of length p + 1
        R = [[] for _ in range(degree + 1)]

        # Load new knot vector
        for i in range(0, span + 1):
            UQ[i] = knotvector[i]
        for i in range(1, r + 1):
            UQ[span + i] = param
        for i in range(span + 1, len(knotvector)):
            UQ[i + r] = knotvector[i]

        # Update control points
        for row in range(0, ctrlpts_size[1]):
            for i in range(0, span - degree + 1):
                Q[row + (ctrlpts_size[1] * i)] = ctrlpts[row + (ctrlpts_size[1] * i)]
            for i in range(span - s, ctrlpts_size[0]):
                Q[row + (ctrlpts_size[1] * (i + r))] = ctrlpts[row + (ctrlpts_size[1] * i)]
            # Load auxiliary control points
            for i in range(0, degree - s + 1):
                R[i] = copy.deepcopy(ctrlpts[row + (ctrlpts_size[1] * (span - degree + i))])
            # Insert the knot r times
            for j in range(1, r + 1):
                L = span - degree + j
                for i in range(0, degree - j - s + 1):
                    alpha = (param - knotvector[L + i]) / (knotvector[i + span + 1] - knotvector[L + i])
                    R[i][:] = [alpha * elem2 + (1.0 - alpha) * elem1 for elem1, elem2 in zip(R[i], R[i + 1])]
                Q[row + (ctrlpts_size[1] * L)] = copy.deepcopy(R[0])
                Q[row + (ctrlpts_size[1] * (span + r - j - s))] = copy.deepcopy(R[degree - j - s])
            # Load the remaining control points
            L = span - degree + r
            for i in range(L + 1, span - s):
                Q[row + (ctrlpts_size[1] * i)] = copy.deepcopy(R[i - L])

        return UQ, Q

    def insert_knot_v(self, **kwargs):
        """ Inserts knot(s) in v-direction. """
        # Call parent method
        super(SurfaceEvaluator, self).insert_knot_v(**kwargs)

        param = kwargs.get('parameter')
        r = kwargs.get('r')
        s = kwargs.get('s')
        degree = kwargs.get('degree')
        knotvector = kwargs.get('knotvector')
        ctrlpts = kwargs.get('ctrlpts')
        ctrlpts_size = kwargs.get('ctrlpts_size')

        # Algorithm A5.3
        span = self._span_func(degree, knotvector, ctrlpts_size[1], param)

        # Initialize new knot vector array
        VQ = [0.0 for _ in range(len(knotvector) + r)]
        # Initialize new control points array (control points can be weighted or not)
        Q = [[] for _ in range(ctrlpts_size[0] * (ctrlpts_size[1] + r))]
        # Initialize a local array of length q + 1
        R = [[] for _ in range(degree + 1)]

        # Load new knot vector
        for i in range(0, span + 1):
            VQ[i] = knotvector[i]
        for i in range(1, r + 1):
            VQ[span + i] = param
        for i in range(span + 1, len(knotvector)):
            VQ[i + r] = knotvector[i]

        # Update control points
        for col in range(0, ctrlpts_size[0]):
            for i in range(0, span - degree + 1):
                Q[i + ((ctrlpts_size[1] + r) * col)] = ctrlpts[i + (ctrlpts_size[1] * col)]
            for i in range(span - s, ctrlpts_size[1]):
                Q[i + r + ((ctrlpts_size[1] + r) * col)] = ctrlpts[i + (ctrlpts_size[1] * col)]
            # Load auxiliary control points
            for i in range(0, degree - s + 1):
                R[i] = copy.deepcopy(ctrlpts[span - degree + i + (ctrlpts_size[1] * col)])
            # Insert the knot r times
            for j in range(1, r + 1):
                L = span - degree + j
                for i in range(0, degree - j - s + 1):
                    alpha = (param - knotvector[L + i]) / (knotvector[i + span + 1] - knotvector[L + i])
                    R[i][:] = [alpha * elem2 + (1.0 - alpha) * elem1 for elem1, elem2 in zip(R[i], R[i + 1])]
                Q[L + ((ctrlpts_size[1] + r) * col)] = copy.deepcopy(R[0])
                Q[span + r - j - s + ((ctrlpts_size[1] + r) * col)] = copy.deepcopy(R[degree - j - s])
            # Load the remaining control points
            L = span - degree + r
            for i in range(L + 1, span - s):
                Q[i + ((ctrlpts_size[1] + r) * col)] = copy.deepcopy(R[i - L])

        return VQ, Q


class SurfaceEvaluator2(SurfaceEvaluator):
    """ Sequential B-Spline surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5: SurfacePoint
    * Algorithm A3.7: SurfaceDerivCpts
    * Algorithm A3.8: SurfaceDerivsAlg2
    * Algorithm A5.3: SurfaceKnotIns

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

    # Evaluates the surface derivatives using "SurfaceDerivsAlg2"
    def derivatives_single(self, **kwargs):
        """ Evaluates the n-th order surface derivatives at (u,v) parameters.

        Output is SKL[k][l], derivative of the surface k times with respect to U and l times with respect to V
        """
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


class NURBSSurfaceEvaluator(SurfaceEvaluator):
    """ Sequential NURBS surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A4.3: SurfacePoint
    * Algorithm A4.4: RatSurfaceDerivs
    * Algorithm A5.3: SurfaceKnotIns

    Please note that knot vector span finding function may be changed by setting ``find_span_func`` keyword argument
    during the initialization. By default, this function is set to :py:func:`.helpers.find_span_linear`.
    Please see :doc:`Helpers Module Documentation <module_utilities>` for more details.
    """

    def __init__(self, **kwargs):
        super(NURBSSurfaceEvaluator, self).__init__(**kwargs)
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    def evaluate(self, **kwargs):
        """ Evaluates the surface. """
        dimension = kwargs.get('dimension')

        # Algorithm A4.3
        cptw = super(NURBSSurfaceEvaluator, self).evaluate(**kwargs)

        # Divide by weight
        eval_points = []
        for pt in cptw:
            cpt = [float(c / pt[-1]) for c in pt[0:(dimension - 1)]]
            eval_points.append(cpt)

        return eval_points

    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order surface derivatives at a (u, v) parameter. """
        deriv_order = kwargs.get('deriv_order')
        dimension = kwargs.get('dimension')

        # Call the parent function to evaluate A(u) and w(u) derivatives
        SKLw = super(NURBSSurfaceEvaluator, self).derivatives_single(**kwargs)

        # Generate an empty list of derivatives
        SKL = [[[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        # Algorithm A4.4
        for k in range(0, deriv_order + 1):
            for l in range(0, deriv_order - k + 1):
                # Deep copying might seem a little overkill but we also want to avoid same pointer issues too
                v = copy.deepcopy(SKLw[k][l])

                for j in range(1, l + 1):
                    v[:] = [tmp - (utilities.binomial_coefficient(l, j) * SKLw[0][j][-1] * drv) for tmp, drv in
                            zip(v, SKL[k][l - j])]
                for i in range(1, k + 1):
                    v[:] = [tmp - (utilities.binomial_coefficient(k, i) * SKLw[i][0][-1] * drv) for tmp, drv in
                            zip(v, SKL[k - i][l])]
                    v2 = [0.0 for _ in range(dimension - 1)]
                    for j in range(1, l + 1):
                        v2[:] = [tmp + (utilities.binomial_coefficient(l, j) * SKLw[i][j][-1] * drv) for tmp, drv in
                                 zip(v2, SKL[k - i][l - j])]
                    v[:] = [tmp - (utilities.binomial_coefficient(k, i) * tmp2) for tmp, tmp2 in zip(v, v2)]

                SKL[k][l][:] = [tmp / SKLw[0][0][-1] for tmp in v[0:(dimension - 1)]]

        # Return S(u,v) derivatives
        return SKL
