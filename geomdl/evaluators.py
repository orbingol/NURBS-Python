"""
.. module:: evaluators
    :platform: Unix, Windows
    :synopsis: NURBS & B-Spline evaluation algorithms

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import copy
from . import Abstract
from . import helpers
from . import utilities


class CurveEvaluator(Abstract.Evaluator):
    """ Sequential B-Spline curve evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.2: CurveDerivsAlg1
    * Algorithm A5.1: CurveKnotIns

    """

    def __init__(self):
        super(CurveEvaluator, self).__init__()
        self._name = "Curve Evaluator"

    def evaluate_single(self, **kwargs):
        """ Evaluates a single curve point. """
        knot = kwargs.get('knot')
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.1
        span = helpers.find_span(knot_vector, len(control_points), knot)
        basis = helpers.basis_function(degree, knot_vector, span, knot)

        crvpt = [0.0 for _ in range(dimension)]
        for i in range(0, degree + 1):
            crvpt[:] = [crv_p + (basis[i] * ctl_p) for crv_p, ctl_p in
                        zip(crvpt, control_points[span - degree + i])]

        return crvpt

    def evaluate(self, **kwargs):
        """ Evaluates the curve. """
        knots = kwargs.get('knots')
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.1
        spans = helpers.find_spans(knot_vector, len(control_points), knots)
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
        knot = kwargs.get('knot')
        deriv_order = kwargs.get('deriv_order', 0)
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.2
        du = min(degree, deriv_order)

        CK = [[None for _ in range(dimension)] for _ in range(deriv_order + 1)]
        for k in range(degree + 1, deriv_order + 1):
            CK[k] = [0.0 for _ in range(dimension)]

        span = helpers.find_span(knot_vector, len(control_points), knot)
        bfunsders = helpers.basis_function_ders(degree, tuple(knot_vector), span, knot, du)

        for k in range(0, du + 1):
            CK[k] = [0.0 for _ in range(dimension)]
            for j in range(0, degree + 1):
                CK[k][:] = [drv + (bfunsders[k][j] * ctl_pt) for drv, ctl_pt in
                            zip(CK[k], control_points[span - degree + j])]

        # Return the derivatives
        return CK

    def derivatives(self, **kwargs):
        pass

    def insert_knot(self, **kwargs):
        knot = kwargs.get('knot')
        r = kwargs.get('r')  # number of knot insertions
        s = kwargs.get('s')  # multiplicity
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')

        # Algorithm A5.1
        k = helpers.find_span(knot_vector, len(control_points), knot)
        mp = len(knot_vector)
        np = len(control_points)
        nq = np + r

        # Initialize new knot vector array
        UQ = [None for _ in range(mp + r)]
        # Initialize new control points array (control points may be weighted or not)
        Q = [None for _ in range(nq)]
        # Initialize a local array of length p + 1
        R = [None for _ in range(degree + 1)]

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
    """ Sequential B-Spline curve evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.1: CurvePoint
    * Algorithm A3.3: CurveDerivCpts
    * Algorithm A3.4: CurveDerivsAlg2
    * Algorithm A5.1: CurveKnotIns

    """

    def __init__(self):
        super(CurveEvaluator2, self).__init__()
        self._name = "Curve Evaluator using A3.4 CurveDerivsAlg2"

    # Computes the control points of all derivative curves up to and including the d-th derivative
    def _derivatives_ctrlpts(self, **kwargs):
        """ Computes the control points of all derivative curves up to and including the {degree}-th derivative.

        Output is PK[k][i], i-th control point of the k-th derivative curve where 0 <= k <= degree and r1 <= i <= r2-k

        :param order: derivative order
        :type order: integer
        :param r1: minimum span
        :type r1: integer
        :param r2: maximum span
        :type r2: integer
        :return: PK, a 2D list of control points
        :rtype: list
        """
        r1 = kwargs.get('r1', 0)  # minimum span
        r2 = kwargs.get('r2', 0)  # maximum span
        deriv_order = kwargs.get('deriv_order', 0)
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
                PK[k][i][:] = [tmp * (elem1 - elem2) / (
                    knot_vector[r1 + i + degree + 1] - knot_vector[r1 + i + k]) for elem1, elem2
                               in zip(PK[k - 1][i + 1], PK[k - 1][i])]

        # Return a 2-dimensional list of control points
        return PK

    # Evaluates the curve derivative using "CurveDerivsAlg2" algorithm
    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order curve derivatives at the given parameter value. """
        knot = kwargs.get('knot')
        deriv_order = kwargs.get('deriv_order')
        degree = kwargs.get('degree')
        knot_vector = kwargs.get('knotvector')
        control_points = kwargs.get('ctrlpts')
        dimension = kwargs.get('dimension')

        # Algorithm A3.4
        du = min(degree, deriv_order)

        CK = [[None for _ in range(dimension)] for _ in range(deriv_order + 1)]
        for k in range(degree + 1, deriv_order + 1):
            CK[k] = [0.0 for _ in range(dimension)]

        span = helpers.find_span(knot_vector, len(control_points), knot)
        bfuns = helpers.basis_function_all(degree, tuple(knot_vector), span, knot)
        PK = self._derivatives_ctrlpts(order=du, r1=(span - degree), r2=span, **kwargs)

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

    """

    def __init__(self):
        super(NURBSCurveEvaluator, self).__init__()
        self._name = "NURBS Curve Evaluator"

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

    # Evaluates the rational curve derivative
    def derivatives_single(self, **kwargs):
        """ Evaluates n-th order curve derivatives at the given parameter value. """
        deriv_order = kwargs.get('deriv_order')
        dimension = kwargs.get('dimension')

        # Call the parent function to evaluate A(u) and w(u) derivatives
        CKw = super(NURBSCurveEvaluator, self).derivatives_single(**kwargs)

        # Algorithm A4.2
        CK = [[None for _ in range(dimension - 1)] for _ in range(deriv_order + 1)]
        for k in range(0, deriv_order + 1):
            v = [val for val in CKw[k][0:(dimension - 1)]]
            for i in range(1, k + 1):
                v[:] = [tmp - (utilities.binomial_coefficient(k, i) * CKw[i][-1] * drv) for tmp, drv in
                        zip(v, CK[k - i])]
            CK[k][:] = [tmp / CKw[0][-1] for tmp in v]

        # Return C(u) derivatives
        return CK


class SurfaceEvaluator(Abstract.Evaluator):
    """ Sequential B-Spline surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A3.5

    """

    def __init__(self):
        super(SurfaceEvaluator, self).__init__()
        self._name = "Surface Evaluator"

    def evaluate_single(self, **kwargs):
        """ Evaluates a single surface point. """
        knot_u = kwargs.get('knot_u')
        knot_v = kwargs.get('knot_v')
        degree_u = kwargs.get('degree_u')
        degree_v = kwargs.get('degree_v')
        knot_vector_u = kwargs.get('knotvector_u')
        knot_vector_v = kwargs.get('knotvector_v')
        control_points2D = kwargs.get('ctrlpts')
        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')
        dimension = kwargs.get('dimension')

        # Algorithm A3.5
        span_u = helpers.find_span(knot_vector_u, ctrlpts_size_u, knot_u)
        span_v = helpers.find_span(knot_vector_v, ctrlpts_size_v, knot_v)

        basis_u = helpers.basis_function(degree_u, knot_vector_u, span_u, knot_u)
        basis_v = helpers.basis_function(degree_v, knot_vector_v, span_v, knot_v)

        idx_u = span_u - degree_u
        spt = [0.0 for _ in range(dimension)]

        for l in range(0, degree_v + 1):
            temp = [0.0 for _ in range(dimension)]
            idx_v = span_v - degree_v + l
            for k in range(0, degree_u + 1):
                temp[:] = [tmp + (basis_u[k] * cp) for tmp, cp in zip(temp, control_points2D[idx_u + k][idx_v])]
            spt[:] = [pt + (basis_v[l] * tmp) for pt, tmp in zip(spt, temp)]

        return spt

    def evaluate(self, **kwargs):
        """ Evaluates the surface. """
        knots_u = kwargs.get('knots_u')
        knots_v = kwargs.get('knots_v')
        degree_u = kwargs.get('degree_u')
        degree_v = kwargs.get('degree_v')
        knot_vector_u = kwargs.get('knotvector_u')
        knot_vector_v = kwargs.get('knotvector_v')
        control_points2D = kwargs.get('ctrlpts')
        ctrlpts_size_u = kwargs.get('ctrlpts_size_u')
        ctrlpts_size_v = kwargs.get('ctrlpts_size_v')
        dimension = kwargs.get('dimension')

        # Algorithm A3.5
        spans_u = helpers.find_spans(knot_vector_u, ctrlpts_size_u, knots_u)
        spans_v = helpers.find_spans(knot_vector_v, ctrlpts_size_v, knots_v)

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
                                   zip(temp, control_points2D[idx_u + k][idx_v])]
                    spt[:] = [pt + (basis_v[j][l] * tmp) for pt, tmp in zip(spt, temp)]

                eval_points.append(spt)

        return eval_points

    def derivatives_single(self, **kwargs):
        pass

    def derivatives(self, **kwargs):
        pass

    def insert_knot(self, **kwargs):
        pass


class NURBSSurfaceEvaluator(SurfaceEvaluator):
    """ Sequential NURBS surface evaluation algorithms.

    This evaluator implements the following algorithms from **The NURBS Book**:

    * Algorithm A4.3

    """

    def __init__(self):
        super(NURBSSurfaceEvaluator, self).__init__()
        self._name = "NURBS Surface Evaluator"

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
        pass

    def derivatives(self, **kwargs):
        pass
