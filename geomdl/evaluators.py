"""
.. module:: evaluators
    :platform: Unix, Windows
    :synopsis: Provides NURBS & B-Spline evaluation algorithms

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import copy
from . import Abstract
from . import helpers
from . import utilities


class CurveEvaluator(Abstract.Evaluator, Abstract.CurveEvaluator):
    """ Sequential B-Spline curve evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.2: CurveDerivsAlg1
    * Algorithm A5.1: CurveKnotIns

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        super(CurveEvaluator, self).__init__(**kwargs)

    def evaluate_single(self, **kwargs):
        """ Evaluates a single curve point. """
        # Call parent method
        super(CurveEvaluator, self).evaluate_single(**kwargs)

        knot = kwargs.get('knot')
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.1
        span = self._span_func(degree, knot_vector, len(control_points), knot)
        basis = helpers.basis_function(degree, knot_vector, span, knot)

        crvpt = [0.0 for _ in range(dimension)]
        for i in range(0, degree + 1):
            crvpt[:] = [crv_p + (basis[i] * ctl_p) for crv_p, ctl_p in
                        zip(crvpt, control_points[span - degree + i])]

        return crvpt

    def evaluate(self, **kwargs):
        """ Evaluates the curve. """
        # Call parent method
        super(CurveEvaluator, self).evaluate(**kwargs)

        start_u = kwargs.get('start_u')
        stop_u = kwargs.get('stop_u')
        sample_size = kwargs.get('sample_size')
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')
        precision = kwargs.get('precision')

        # Algorithm A3.1
        knots = utilities.linspace(start_u, stop_u, sample_size, decimals=precision)
        spans = helpers.find_spans(degree, knot_vector, len(control_points), knots, self._span_func)
        basis = helpers.basis_functions(degree, knot_vector, spans, knots)

        eval_points = []
        for idx in range(len(knots)):
            crvpt = [0.0 for _ in range(dimension)]
            for i in range(0, degree + 1):
                crvpt[:] = [crv_p + (basis[idx][i] * ctl_p) for crv_p, ctl_p in
                            zip(crvpt, control_points[spans[idx] - degree + i])]

            eval_points.append(crvpt)

        return eval_points

    # Evaluates the curve derivative using "CurveDerivsAlg1" algorithm
    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order curve derivatives at a single parameter. """
        # Call parent method
        super(CurveEvaluator, self).derivatives_single(**kwargs)

        knot = kwargs.get('knot')
        deriv_order = kwargs.get('deriv_order', 0)
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.2
        du = min(degree, deriv_order)

        CK = [[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)]

        span = self._span_func(degree, knot_vector, len(control_points), knot)
        bfunsders = helpers.basis_function_ders(degree, tuple(knot_vector), span, knot, du)

        for k in range(0, du + 1):
            CK[k] = [0.0 for _ in range(dimension)]
            for j in range(0, degree + 1):
                CK[k][:] = [drv + (bfunsders[k][j] * ctl_pt) for drv, ctl_pt in
                            zip(CK[k], control_points[span - degree + j])]

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
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')

        # Algorithm A5.1
        k = self._span_func(degree, knot_vector, len(control_points), knot)
        mp = len(knot_vector)
        np = len(control_points)
        nq = np + r

        # Initialize new knot vector array
        UQ = [0.0 for _ in range(mp + r)]
        # Initialize new control points array (control points may be weighted or not)
        Q = [[] for _ in range(nq)]
        # Initialize a local array of length p + 1
        R = [[] for _ in range(degree + 1)]

        # Load new knot vector
        for i in range(0, k + 1):
            UQ[i] = knot_vector[i]
        for i in range(1, r + 1):
            UQ[k + i] = knot
        for i in range(k + 1, mp):
            UQ[i + r] = knot_vector[i]

        # Save unaltered control points
        for i in range(0, k - degree + 1):
            Q[i] = control_points[i]
        for i in range(k - s, np):
            Q[i + r] = control_points[i]

        # The algorithm uses R array to update control points
        for i in range(0, degree - s + 1):
            R[i] = copy.deepcopy(control_points[k - degree + i])

        # Insert the knot r times
        for j in range(1, r + 1):
            L = k - degree + j
            for i in range(0, degree - j - s + 1):
                alpha = (knot - knot_vector[L + i]) / (knot_vector[i + k + 1] - knot_vector[L + i])
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

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        super(CurveEvaluator2, self).__init__(**kwargs)

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
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.3
        r = r2 - r1
        PK = [[[None for _ in range(dimension)] for _ in range(r + 1)] for _ in range(deriv_order + 1)]
        for i in range(0, r + 1):
            PK[0][i][:] = [elem for elem in control_points[r1 + i]]

        for k in range(1, deriv_order + 1):
            tmp = degree - k + 1
            for i in range(0, r - k + 1):
                PK[k][i][:] = [tmp * (elem1 - elem2) /
                               (knot_vector[r1 + i + degree + 1] - knot_vector[r1 + i + k]) for elem1, elem2
                               in zip(PK[k - 1][i + 1], PK[k - 1][i])]

        # Return a 2-dimensional list of control points
        return PK

    # Evaluates the curve derivative using "CurveDerivsAlg2" algorithm
    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order curve derivatives at a single parameter. """
        # Call parent method
        super(CurveEvaluator2, self).derivatives_single(**kwargs)

        knot = kwargs.get('knot')
        deriv_order = kwargs.get('deriv_order', 0)
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.4
        du = min(degree, deriv_order)

        CK = [[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)]

        span = self._span_func(degree, knot_vector, len(control_points), knot)
        bfuns = helpers.basis_function_all(degree, tuple(knot_vector), span, knot)

        # "derivatives_ctrlpts" is a static method that could be called like below
        PK = CurveEvaluator2.derivatives_ctrlpts(r1=(span - degree), r2=span,
                                                 degree=degree,
                                                 knotvector=knot_vector,
                                                 ctrlpts=control_points,
                                                 dimension=dimension,
                                                 deriv_order=du)

        for k in range(0, du + 1):
            CK[k] = [0.0 for _ in range(dimension)]
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

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        super(NURBSCurveEvaluator, self).__init__(**kwargs)

    def evaluate_single(self, **kwargs):
        """ Evaluates a single curve point. """
        dimension = kwargs.get('dimension')

        # Algorithm A4.1
        crvptw = super(NURBSCurveEvaluator, self).evaluate_single(**kwargs)

        # Divide by weight
        crvpt = [float(pt / crvptw[-1]) for pt in crvptw[0:(dimension - 1)]]

        return crvpt

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


class SurfaceEvaluator(Abstract.Evaluator, Abstract.SurfaceEvaluator):
    """ Sequential B-Spline surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5: SurfacePoint
    * Algorithm A3.6: SurfaceDerivsAlg1
    * Algorithm A5.3: SurfaceKnotIns

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        super(SurfaceEvaluator, self).__init__(**kwargs)

    def evaluate_single(self, **kwargs):
        """ Evaluates a single surface point. """
        # Call parent method
        super(SurfaceEvaluator, self).evaluate_single(**kwargs)

        knot_u = kwargs.get('knot_u')
        knot_v = kwargs.get('knot_v')
        degree_u = kwargs.get('degree_u')
        degree_v = kwargs.get('degree_v')
        knot_vector_u = kwargs.get('knotvector_u')
        knot_vector_v = kwargs.get('knotvector_v')
        control_points2d = kwargs.get('ctrlpts')
        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')
        dimension = kwargs.get('dimension')

        # Algorithm A3.5
        span_u = self._span_func(degree_u, knot_vector_u, ctrlpts_size_u, knot_u)
        span_v = self._span_func(degree_v, knot_vector_v, ctrlpts_size_v, knot_v)

        basis_u = helpers.basis_function(degree_u, knot_vector_u, span_u, knot_u)
        basis_v = helpers.basis_function(degree_v, knot_vector_v, span_v, knot_v)

        idx_u = span_u - degree_u
        spt = [0.0 for _ in range(dimension)]

        for l in range(0, degree_v + 1):
            temp = [0.0 for _ in range(dimension)]
            idx_v = span_v - degree_v + l
            for k in range(0, degree_u + 1):
                temp[:] = [tmp + (basis_u[k] * cp) for tmp, cp in zip(temp, control_points2d[idx_u + k][idx_v])]
            spt[:] = [pt + (basis_v[l] * tmp) for pt, tmp in zip(spt, temp)]

        return spt

    def evaluate(self, **kwargs):
        """ Evaluates the surface. """
        # Call parent method
        super(SurfaceEvaluator, self).evaluate(**kwargs)

        start_u = kwargs.get('start_u')
        stop_u = kwargs.get('stop_u')
        start_v = kwargs.get('start_v')
        stop_v = kwargs.get('stop_v')
        sample_size = kwargs.get('sample_size')
        degree_u = kwargs.get('degree_u')
        degree_v = kwargs.get('degree_v')
        knot_vector_u = kwargs.get('knotvector_u')
        knot_vector_v = kwargs.get('knotvector_v')
        control_points2d = kwargs.get('ctrlpts')
        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')
        dimension = kwargs.get('dimension')
        precision = kwargs.get('precision')

        # Algorithm A3.5
        knots_u = utilities.linspace(start_u, stop_u, sample_size[0], decimals=precision)
        knots_v = utilities.linspace(start_v, stop_v, sample_size[1], decimals=precision)

        spans_u = helpers.find_spans(degree_u, knot_vector_u, ctrlpts_size_u, knots_u, self._span_func)
        spans_v = helpers.find_spans(degree_v, knot_vector_v, ctrlpts_size_v, knots_v, self._span_func)

        basis_u = helpers.basis_functions(degree_u, knot_vector_u, spans_u, knots_u)
        basis_v = helpers.basis_functions(degree_v, knot_vector_v, spans_v, knots_v)

        eval_points = []
        for i in range(len(knots_u)):
            idx_u = spans_u[i] - degree_u
            for j in range(len(knots_v)):
                spt = [0.0 for _ in range(dimension)]
                for l in range(0, degree_v + 1):
                    temp = [0.0 for _ in range(dimension)]
                    idx_v = spans_v[j] - degree_v + l
                    for k in range(0, degree_u + 1):
                        temp[:] = [tmp + (basis_u[i][k] * cp) for tmp, cp in
                                   zip(temp, control_points2d[idx_u + k][idx_v])]
                    spt[:] = [pt + (basis_v[j][l] * tmp) for pt, tmp in zip(spt, temp)]

                eval_points.append(spt)

        return eval_points

    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order surface derivatives at a (u,v) parameter. """
        # Call parent method
        super(SurfaceEvaluator, self).derivatives_single(**kwargs)

        deriv_order = kwargs.get('deriv_order')
        knot_u = kwargs.get('knot_u')
        knot_v = kwargs.get('knot_v')
        degree_u = kwargs.get('degree_u')
        degree_v = kwargs.get('degree_v')
        knot_vector_u = kwargs.get('knotvector_u')
        knot_vector_v = kwargs.get('knotvector_v')
        control_points2d = kwargs.get('ctrlpts')
        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')
        dimension = kwargs.get('dimension')

        # Algorithm A3.6
        du = min(degree_u, deriv_order)
        dv = min(degree_v, deriv_order)

        SKL = [[[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        span_u = self._span_func(degree_u, knot_vector_u, ctrlpts_size_u, knot_u)
        bfunsders_u = helpers.basis_function_ders(degree_u, knot_vector_u, span_u, knot_u, du)
        span_v = self._span_func(degree_v, knot_vector_v, ctrlpts_size_v, knot_v)
        bfunsders_v = helpers.basis_function_ders(degree_v, knot_vector_v, span_v, knot_v, dv)

        for k in range(0, du + 1):
            temp = [[] for _ in range(degree_v + 1)]
            for s in range(0, degree_v + 1):
                temp[s] = [0.0 for _ in range(dimension)]
                for r in range(0, degree_u + 1):
                    cu = span_u - degree_u + r
                    cv = span_v - degree_v + s
                    temp[s][:] = [tmp + (bfunsders_u[k][r] * cp) for tmp, cp in
                                  zip(temp[s], control_points2d[cu][cv])]

            dd = min(deriv_order - k, dv)
            for l in range(0, dd + 1):
                for s in range(0, degree_v + 1):
                    SKL[k][l][:] = [elem + (bfunsders_v[l][s] * tmp) for elem, tmp in zip(SKL[k][l], temp[s])]

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

        u = kwargs.get('knot')
        r = kwargs.get('r')
        s = kwargs.get('s')
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points2d = kwargs.get('ctrlpts')
        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')

        # Algorithm A5.3
        span = self._span_func(degree, knot_vector, ctrlpts_size_u, u)

        # Initialize new knot vector array
        UQ = [0.0 for _ in range(len(knot_vector) + r)]
        # Initialize new control points array (control points can be weighted or not)
        Q = [[[] for _ in range(ctrlpts_size_v)] for _ in range(ctrlpts_size_u + r)]
        # Initialize a local array of length p + 1
        R = [[] for _ in range(degree + 1)]

        # Load new knot vector
        for i in range(0, span + 1):
            UQ[i] = knot_vector[i]
        for i in range(1, r + 1):
            UQ[span + i] = u
        for i in range(span + 1, len(knot_vector)):
            UQ[i + r] = knot_vector[i]

        # Save the alphas
        alpha = [[0.0 for _ in range(r + 1)] for _ in range(degree - s)]
        for j in range(1, r + 1):
            L = span - degree + j
            for i in range(0, degree - j - s + 1):
                alpha[i][j] = (u - knot_vector[L + i]) / (knot_vector[i + span + 1] - knot_vector[L + i])

        # Update control points
        for row in range(0, ctrlpts_size_v):
            for i in range(0, span - degree + 1):
                Q[i][row] = control_points2d[i][row]
            for i in range(span - s, ctrlpts_size_u):
                Q[i + r][row] = control_points2d[i][row]
            # Load auxiliary control points
            for i in range(0, degree - s + 1):
                R[i] = copy.deepcopy(control_points2d[span - degree + i][row])
            # Insert the knot r times
            for j in range(1, r + 1):
                L = span - degree + j
                for i in range(0, degree - j - s + 1):
                    R[i][:] = [alpha[i][j] * elem2 + (1.0 - alpha[i][j]) * elem1
                               for elem1, elem2 in zip(R[i], R[i + 1])]
                Q[L][row] = copy.deepcopy(R[0])
                Q[span + r - j - s][row] = copy.deepcopy(R[degree - j - s])
            # Load the remaining control points
            L = span - degree + r
            for i in range(L + 1, span - s):
                Q[i][row] = copy.deepcopy(R[i - L])

        return UQ, Q

    def insert_knot_v(self, **kwargs):
        """ Inserts knot(s) in v-direction. """
        # Call parent method
        super(SurfaceEvaluator, self).insert_knot_v(**kwargs)

        v = kwargs.get('knot')
        r = kwargs.get('r')
        s = kwargs.get('s')
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points2d = kwargs.get('ctrlpts')
        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')

        # Algorithm A5.3
        span = self._span_func(degree, knot_vector, ctrlpts_size_v, v)

        # Initialize new knot vector array
        VQ = [0.0 for _ in range(len(knot_vector) + r)]
        # Initialize new control points array (control points can be weighted or not)
        Q = [[[] for _ in range(ctrlpts_size_v + r)] for _ in range(ctrlpts_size_u)]
        # Initialize a local array of length q + 1
        R = [[] for _ in range(degree + 1)]

        # Load new knot vector
        for i in range(0, span + 1):
            VQ[i] = knot_vector[i]
        for i in range(1, r + 1):
            VQ[span + i] = v
        for i in range(span + 1, len(knot_vector)):
            VQ[i + r] = knot_vector[i]

        # Save the alphas
        alpha = [[0.0 for _ in range(r + 1)] for _ in range(degree - s)]
        for j in range(1, r + 1):
            L = span - degree + j
            for i in range(0, degree - j - s + 1):
                alpha[i][j] = (v - knot_vector[L + i]) / (knot_vector[i + span + 1] - knot_vector[L + i])

        # Update control points
        for col in range(0, ctrlpts_size_u):
            for i in range(0, span - degree + 1):
                Q[col][i] = control_points2d[col][i]
            for i in range(span - s, ctrlpts_size_v):
                Q[col][i + r] = control_points2d[col][i]
            # Load auxiliary control points
            for i in range(0, degree - s + 1):
                R[i] = copy.deepcopy(control_points2d[col][span - degree + i])
            # Insert the knot r times
            for j in range(1, r + 1):
                L = span - degree + j
                for i in range(0, degree - j - s + 1):
                    R[i][:] = [alpha[i][j] * elem2 + (1.0 - alpha[i][j]) * elem1
                               for elem1, elem2 in zip(R[i], R[i + 1])]
                Q[col][L] = copy.deepcopy(R[0])
                Q[col][span + r - j - s] = copy.deepcopy(R[degree - j - s])
            # Load the remaining control points
            L = span - degree + r
            for i in range(L + 1, span - s):
                Q[col][i] = copy.deepcopy(R[i - L])

        return VQ, Q


class SurfaceEvaluator2(SurfaceEvaluator):
    """ Sequential B-Spline surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5: SurfacePoint
    * Algorithm A3.7: SurfaceDerivCpts
    * Algorithm A3.8: SurfaceDerivsAlg2
    * Algorithm A5.3: SurfaceKnotIns

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        super(SurfaceEvaluator2, self).__init__(**kwargs)

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

        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        degree_u = kwargs.get('degree_u')
        knot_vector_u = kwargs.get('knotvector_u')

        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')
        degree_v = kwargs.get('degree_v')
        knot_vector_v = kwargs.get('knotvector_v')

        ctrlpts2d = kwargs.get('ctrlpts')
        deriv_order = kwargs.get('deriv_order')

        dimension = kwargs.get('dimension')

        PKL = [[[[[None for _ in range(dimension)]
                  for _ in range(ctrlpts_size_v)] for _ in range(ctrlpts_size_u)]
                for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        du = min(degree_u, deriv_order)
        dv = min(degree_v, deriv_order)

        r = r2 - r1
        s = s2 - s1

        # Control points of the U derivatives of every U-curve
        for j in range(s1, s2 + 1):
            PKu = CurveEvaluator2.derivatives_ctrlpts(r1=r1, r2=r2,
                                                      degree=degree_u,
                                                      knotvector=knot_vector_u,
                                                      ctrlpts=[ctrlpts2d[_][j] for _ in range(len(ctrlpts2d))],
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
                                                           degree=degree_v,
                                                           knotvector=knot_vector_v[s1:],
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
        knot_u = kwargs.get('knot_u')
        knot_v = kwargs.get('knot_v')
        degree_u = kwargs.get('degree_u')
        degree_v = kwargs.get('degree_v')
        knot_vector_u = kwargs.get('knotvector_u')
        knot_vector_v = kwargs.get('knotvector_v')
        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')
        dimension = kwargs.get('dimension')

        SKL = [[[0.0 for _ in range(dimension)] for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

        du = min(degree_u, deriv_order)
        dv = min(degree_v, deriv_order)

        span_u = self._span_func(degree_u, knot_vector_u, ctrlpts_size_u, knot_u)
        bfuns_u = helpers.basis_function_all(degree_u, tuple(knot_vector_u), span_u, knot_u)
        span_v = self._span_func(degree_v, knot_vector_v, ctrlpts_size_v, knot_v)
        bfuns_v = helpers.basis_function_all(degree_v, tuple(knot_vector_v), span_v, knot_v)

        PKL = self.derivatives_ctrlpts(r1=span_u - degree_u, r2=span_u,
                                       s1=span_v - degree_v, s2=span_v,
                                       **kwargs)

        # Evaluating the derivative at parameters (u,v) using its control points
        for k in range(0, du + 1):
            dd = min(deriv_order - k, dv)

            for l in range(0, dd + 1):
                SKL[k][l] = [0.0 for _ in range(dimension)]

                for i in range(0, degree_v - l + 1):
                    temp = [0.0 for _ in range(dimension)]

                    for j in range(0, degree_u - k + 1):
                        temp[:] = [elem + (bfuns_u[j][degree_u - k] * drv_ctl_p) for elem, drv_ctl_p in
                                   zip(temp, PKL[k][l][j][i])]

                    SKL[k][l][:] = [elem + (bfuns_v[i][degree_v - l] * drv_ctl_p) for elem, drv_ctl_p in
                                    zip(SKL[k][l], temp)]

        return SKL


class NURBSSurfaceEvaluator(SurfaceEvaluator):
    """ Sequential NURBS surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A4.3: SurfacePoint
    * Algorithm A4.4: RatSurfaceDerivs
    * Algorithm A5.3: SurfaceKnotIns

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        super(NURBSSurfaceEvaluator, self).__init__(**kwargs)

    def evaluate_single(self, **kwargs):
        """ Evaluates a single surface point. """
        dimension = kwargs.get('dimension')

        # Algorithm A4.3
        cptw = super(NURBSSurfaceEvaluator, self).evaluate_single(**kwargs)

        # Divide by weight
        cpt = [float(pt / cptw[-1]) for pt in cptw[0:(dimension - 1)]]

        return cpt

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
