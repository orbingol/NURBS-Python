"""
.. module:: evaluators
    :platform: Unix, Windows
    :synopsis: NURBS & B-Spline evaluation algorithms

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import Abstract
from . import helpers


class CurveEvaluator(Abstract.Evaluator):
    """ Sequential B-Spline curve evaluation algorithms.

    This evaluator implements the following algorithms from The NURBS Book:

    * Algorithm A3.1

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

        cpt = [0.0 for _ in range(dimension)]
        for i in range(0, degree + 1):
            cpt[:] = [crvpt + (basis[i] * ctrlpt) for crvpt, ctrlpt in zip(cpt, control_points[span - degree + i])]

        return cpt

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
            cpt = [0.0 for _ in range(dimension)]
            for i in range(0, degree + 1):
                cpt[:] = [crvpt + (basis[idx][i] * ctrlpt) for crvpt, ctrlpt in
                          zip(cpt, control_points[spans[idx] - degree + i])]

            eval_points.append(cpt)

        return eval_points

    def derivatives_single(self, **kwargs):
        pass

    def derivatives(self, **kwargs):
        pass

    def insert_knot(self, **kwargs):
        pass


class SurfaceEvaluator(Abstract.Evaluator):
    """ Sequential B-Spline surface evaluation algorithms.

    This evaluator implements the following algorithms from The NURBS Book:

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


class NURBSCurveEvaluator(CurveEvaluator):
    """ Sequential NURBS curve evaluation algorithms.

    This evaluator implements the following algorithms from The NURBS Book:

    * Algorithm A4.1

    """

    def __init__(self):
        super(NURBSCurveEvaluator, self).__init__()
        self._name = "NURBS Curve Evaluator"

    def evaluate_single(self, **kwargs):
        """ Evaluates a single curve point. """
        dimension = kwargs.get('dimension')

        # Algorithm A4.1
        cptw = super(NURBSCurveEvaluator, self).evaluate_single(**kwargs)

        # Divide by weight
        cpt = [float(pt / cptw[-1]) for pt in cptw[0:(dimension - 1)]]

        return cpt

    def evaluate(self, **kwargs):
        """ Evaluates the curve. """
        dimension = kwargs.get('dimension')

        # Algorithm A4.1
        cptw = super(NURBSCurveEvaluator, self).evaluate(**kwargs)

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


class NURBSSurfaceEvaluator(SurfaceEvaluator):
    """ Sequential NURBS surface evaluation algorithms.

    This evaluator implements the following algorithms from The NURBS Book:

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
