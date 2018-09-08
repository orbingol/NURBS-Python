"""
.. module:: helpers
    :platform: Unix, Windows
    :synopsis: Evaluation helper functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import Abstract


def find_span_binsearch(degree, knot_vector, num_ctrlpts, knot, **kwargs):
    """ Finds the span of the knot over the input knot vector using binary search.

    Implementation of Algorithm A2.1 from The NURBS Book by Piegl & Tiller.

    The NURBS Book states that the knot span index always starts from zero, i.e. for a knot vector [0, 0, 1, 1];
    if FindSpan returns 1, then the knot is between the internal [0, 1).

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: int
    :param knot: knot
    :type knot: float
    :return: span of the knot over the knot vector
    :rtype: int
    """
    # Get tolerance value
    tol = kwargs.get('tol', 10e-6)

    # In The NURBS Book; number of knots = m + 1, number of control points = n + 1, p = degree
    # All knot vectors should follow the rule: m = p + n + 1
    n = num_ctrlpts - 1
    if abs(knot_vector[n + 1] - knot) <= tol:
        return n

    # Set max and min positions of the array to be searched
    low = degree
    high = num_ctrlpts

    # The division could return a float value which makes it impossible to use as an array index
    mid = (low + high) / 2
    # Direct int casting would cause numerical errors due to discarding the significand figures (digits after the dot)
    # The round function could return unexpected results, so we add the floating point with some small number
    # This addition would solve the issues caused by the division operation and how Python stores float numbers.
    # E.g. round(13/2) = 6 (expected to see 7)
    mid = int(round(mid + tol))

    # Search for the span
    while (knot < knot_vector[mid]) or (knot >= knot_vector[mid + 1]):
        if knot < knot_vector[mid]:
            high = mid
        else:
            low = mid
        mid = int((low + high) / 2)

    return mid


def find_span_linear(degree, knot_vector, num_ctrlpts, knot):
    """ Finds the span of a single knot over the knot vector using linear search.

    Alternative implementation for the Algorithm A2.1 from The NURBS Book by Piegl & Tiller.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: int
    :param knot: knot
    :type knot: float
    :return: span of the knot over the knot vector
    :rtype: int
    """
    span = 0  # Knot span index starts from zero
    while span < num_ctrlpts and knot_vector[span] <= knot:
        span += 1

    return span - 1


def find_spans(degree, knot_vector, num_ctrlpts, knots, func=find_span_linear):
    """ Finds spans of a list of knots over the knot vector.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: int
    :param knots: list of knots
    :type knots: list, tuple
    :param func: function to evaluate span finding operation
    :return: list of spans
    :rtype: list
    """
    spans = []
    for knot in knots:
        spans.append(func(degree, knot_vector, num_ctrlpts, knot))
    return spans


def find_multiplicity(knot, knot_vector, **kwargs):
    """ Finds knot multiplicity over the knot vector.

    :param knot: knot
    :type knot: float
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :return: multiplicity of the knot
    :rtype: int
    """
    # Get tolerance value
    tol = kwargs.get('tol', 0.001)

    mult = 0  # initial multiplicity

    for kv in knot_vector:
        if abs(knot - kv) <= tol:
            mult += 1

    return mult


def basis_function(degree, knot_vector, span, knot):
    """ Computes the non-vanishing basis functions for a single knot.

    Implementation of Algorithm A2.2 from The NURBS Book by Piegl & Tiller.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param span: span of the knot
    :type span: int
    :param knot: knot
    :type knot: float
    :return: basis functions
    :rtype: list
    """
    left = [0.0 for _ in range(degree + 1)]
    right = [0.0 for _ in range(degree + 1)]
    N = [1.0 for _ in range(degree + 1)]  # N[0] = 1.0 by definition

    for j in range(1, degree + 1):
        left[j] = knot - knot_vector[span + 1 - j]
        right[j] = knot_vector[span + j] - knot
        saved = 0.0
        for r in range(0, j):
            temp = N[r] / (right[r + 1] + left[j - r])
            N[r] = saved + right[r + 1] * temp
            saved = left[j - r] * temp
        N[j] = saved

    return N


def basis_functions(degree, knot_vector, spans, knots):
    """ Computes the non-vanishing basis functions for a list of knots.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param spans: spans
    :type spans:  list, tuple
    :param knots: knots
    :type knots: list, tuple
    :return: basis functions
    :rtype: list
    """
    basis = []

    for span, knot in zip(spans, knots):
        basis.append(basis_function(degree, knot_vector, span, knot))
    return basis


def basis_function_all(degree, knot_vector, span, knot):
    """ Finds all non-zero basis functions of all degrees from 0 up to the input degree for a single knot.

    A slightly modified version of Algorithm A2.2 from The NURBS Book by Piegl & Tiller.

    :param degree: degree
    :type degree: int
    :param knot_vector:  knot vector
    :type knot_vector: list, tuple
    :param span: span of the knot
    :type span: int
    :param knot: knot
    :type knot: float
    :return: basis functions
    :rtype: list
    """
    N = [[None for _ in range(degree + 1)] for _ in range(degree + 1)]
    for i in range(0, degree + 1):
        bfuns = basis_function(i, knot_vector, span, knot)
        for j in range(0, i + 1):
            N[j][i] = bfuns[j]
    return N


def basis_function_ders(degree, knot_vector, span, knot, order):
    """ Finds derivatives of the basis functions for a single knot.

    Implementation of Algorithm A2.3 from The NURBS Book by Piegl & Tiller.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param span: span of the knot
    :type span: int
    :param knot: knot
    :type knot: float
    :param order: order of the derivative
    :type order: int
    :return: basis function derivatives
    :rtype: list
    """
    # Initialize variables
    left = [1.0 for _ in range(degree + 1)]
    right = [1.0 for _ in range(degree + 1)]
    ndu = [[1.0 for _ in range(degree + 1)] for _ in range(degree + 1)]  # N[0][0] = 1.0 by definition

    for j in range(1, degree + 1):
        left[j] = knot - knot_vector[span + 1 - j]
        right[j] = knot_vector[span + j] - knot
        saved = 0.0
        r = 0
        for r in range(r, j):
            # Lower triangle
            ndu[j][r] = right[r + 1] + left[j - r]
            temp = ndu[r][j - 1] / ndu[j][r]
            # Upper triangle
            ndu[r][j] = saved + (right[r + 1] * temp)
            saved = left[j - r] * temp
        ndu[j][j] = saved

    # Load the basis functions
    ders = [[0.0 for _ in range(degree + 1)] for _ in range((min(degree, order) + 1))]
    for j in range(0, degree + 1):
        ders[0][j] = ndu[j][degree]

    # Start calculating derivatives
    a = [[1.0 for _ in range(degree + 1)] for _ in range(2)]
    # Loop over function index
    for r in range(0, degree + 1):
        # Alternate rows in array a
        s1 = 0
        s2 = 1
        a[0][0] = 1.0
        # Loop to compute k-th derivative
        for k in range(1, order + 1):
            d = 0.0
            rk = r - k
            pk = degree - k
            if r >= k:
                a[s2][0] = a[s1][0] / ndu[pk + 1][rk]
                d = a[s2][0] * ndu[rk][pk]
            if rk >= -1:
                j1 = 1
            else:
                j1 = -rk
            if (r - 1) <= pk:
                j2 = k - 1
            else:
                j2 = degree - r
            for j in range(j1, j2 + 1):
                a[s2][j] = (a[s1][j] - a[s1][j - 1]) / ndu[pk + 1][rk + j]
                d += (a[s2][j] * ndu[rk + j][pk])
            if r <= pk:
                a[s2][k] = -a[s1][k - 1] / ndu[pk + 1][r]
                d += (a[s2][k] * ndu[r][pk])
            ders[k][r] = d

            # Switch rows
            j = s1
            s1 = s2
            s2 = j

    # Multiply through by the the correct factors
    r = float(degree)
    for k in range(1, order + 1):
        for j in range(0, degree + 1):
            ders[k][j] *= r
        r *= (degree - k)

    # Return the basis function derivatives list
    return ders


def basis_function_one(degree, knot_vector, span, knot):
    """ Computes the value of a basis function for a knot.

    Implementation of Algorithm 2.4 from The NURBS Book by Piegl & Tiller.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, typle
    :param span: span of the knot
    :type span: int
    :param knot: knot
    :type knot: float
    :return: basis function value
    :rtype: float
    """
    # Special case at boundaries
    if (span == 0 and knot == knot_vector[0]) or \
            (span == len(knot_vector) - degree - 2) and knot == knot_vector[len(knot_vector) - 1]:
        return 1.0

    # Knot is outside of span range
    if knot < knot_vector[span] or knot >= knot_vector[span + degree + 1]:
        return 0.0

    N = [0.0 for _ in range(degree + span + 1)]

    # Initialize the zeroth degree basis functions
    for j in range(0, degree + 1):
        if knot_vector[span + j] <= knot < knot_vector[span + j + 1]:
            N[j] = 1.0

    # Computing triangular table of basis functions
    for k in range(1, degree + 1):
        # Detecting zeros saves computations
        saved = 0.0
        if N[0] != 0.0:
            saved = ((knot - knot_vector[span]) * N[0]) / (knot_vector[span + k] - knot_vector[span])

        for j in range(0, degree - k + 1):
            Uleft = knot_vector[span + j + 1]
            Uright = knot_vector[span + j + k + 1]

            # Zero detection
            if N[j + 1] == 0.0:
                N[j] = saved
                saved = 0.0
            else:
                temp = N[j + 1] / (Uright - Uleft)
                N[j] = saved + (Uright - knot) * temp
                saved = (knot - Uleft) * temp

    return N[0]


def basis_function_ders_one(degree, knot_vector, span, knot, order):
    """ Finds the derivative of one basis functions for a single knot.

    Implementation of Algorithm A2.5 from The NURBS Book by Piegl & Tiller.

    :param degree: degree
    :type degree: int
    :param knot_vector: knot_vector
    :type knot_vector: list, tuple
    :param span: span of the knot
    :type span: int
    :param knot: knot
    :type knot: float
    :param order: order of the derivative
    :type order: int
    :return: basis function derivatives values
    :rtype: list
    """
    ders = [0.0 for _ in range(0, order + 1)]

    # Knot is outside of span range
    if (knot < knot_vector[span]) or (knot >= knot_vector[span + degree + 1]):
        for k in range(0, order + 1):
            ders[k] = 0.0

        return ders

    N = [[0.0 for _ in range(0, degree + 1)] for _ in range(0, degree + 1)]

    # Initializing the zeroth degree basis functions
    for j in range(0, degree + 1):
        if knot_vector[span + j] <= knot < knot_vector[span + j + 1]:
            N[j][0] = 1.0

    # Computing all basis functions values for all degrees inside the span
    for k in range(1, degree + 1):
        saved = 0.0
        # Detecting zeros saves computations
        if N[0][k - 1] != 0.0:
            saved = ((knot - knot_vector[span]) * N[0][k - 1]) / (knot_vector[span + k] - knot_vector[span])

        for j in range(0, degree - k + 1):
            Uleft = knot_vector[span + j + 1]
            Uright = knot_vector[span + j + k + 1]

            # Zero detection
            if N[j + 1][k - 1] == 0.0:
                N[j][k] = saved
                saved = 0.0
            else:
                temp = N[j + 1][k - 1] / (Uright - Uleft)
                N[j][k] = saved + (Uright - knot) * temp
                saved = (knot - Uleft) * temp

    # The basis function value is the zeroth derivative
    ders[0] = N[0][degree]

    # Computing the basis functions derivatives
    for k in range(1, order + 1):
        # Buffer for computing the kth derivative
        ND = [0.0 for _ in range(0, k + 1)]

        # Basis functions values used for the derivative
        for j in range(0, k + 1):
            ND[j] = N[j][degree - k]

        # Computing derivatives used for the kth basis function derivative

        # Derivative order for the k-th basis function derivative
        for jj in range(1, k + 1):
            if ND[0] == 0.0:
                saved = 0.0
            else:
                saved = ND[0] / (knot_vector[span + degree - k + jj] - knot_vector[span])

            # Index of the Basis function derivatives
            for j in range(0, k - jj + 1):
                Uleft = knot_vector[span + j + 1]
                # Wrong in The NURBS Book: -k is missing.
                # The right expression is the same as for saved with the added j offset
                Uright = knot_vector[span + j + degree - k + jj + 1]

                if ND[j + 1] == 0.0:
                    ND[j] = (degree - k + jj) * saved
                    saved = 0.0
                else:
                    temp = ND[j + 1] / (Uright - Uleft)

                    ND[j] = (degree - k + jj) * (saved - temp)
                    saved = temp

        ders[k] = ND[0]

    return ders


def find_ctrlpts_curve(t, curve, **kwargs):
    """ Finds the control points involved in the evaluation of the curve point defined by the input parameter.

    This function uses a modified version of the algorithm *A3.1 CurvePoint* from The NURBS Book by Piegl & Tiller.

    :param t: parameter
    :type t: float
    :param curve: input curve object
    :type curve: Abstract.Curve
    :return: 1-dimensional control points array
    :rtype: list
    """
    if not isinstance(curve, Abstract.Curve):
        raise TypeError("Input curve must be an instance of Abstract.Curve")

    # Get keyword arguments
    span_func = kwargs.get('find_span_func', find_span_linear)

    # Find spans and the constant index
    span = span_func(curve.degree, curve.knotvector, len(curve.ctrlpts), t)
    idx = span - curve.degree

    # Find control points involved in evaluation of the curve point at the input parameter
    curve_ctrlpts = [() for _ in range(curve.degree + 1)]
    for i in range(0, curve.degree + 1):
        curve_ctrlpts[i] = curve.ctrlpts[idx + i]

    # Return control points array
    return curve_ctrlpts


def find_ctrlpts_surface(t_u, t_v, surf, **kwargs):
    """ Finds the control points involved in the evaluation of the surface point defined by the input parameter pair.

    This function uses a modified version of the algorithm *A3.5 SurfacePoint* from The NURBS Book by Piegl & Tiller.

    :param t_u: parameter on the u-direction
    :type t_u: float
    :param t_v: parameter on the v-direction
    :type t_v: float
    :param surf: input surface
    :type surf: Abstract.Surface
    :return: 2-dimensional control points array
    :rtype: list
    """
    if not isinstance(surf, Abstract.Surface):
        raise TypeError("Input curve must be an instance of Abstract.Surface")

    # Get keyword arguments
    span_func = kwargs.get('find_span_func', find_span_linear)

    # Find spans
    span_u = span_func(surf.degree_u, surf.knotvector_u, surf.ctrlpts_size_u, t_u)
    span_v = span_func(surf.degree_v, surf.knotvector_v, surf.ctrlpts_size_v, t_v)

    # Constant indices
    idx_u = span_u - surf.degree_u
    idx_v = span_v - surf.degree_v

    # Find control points involved in evaluation of the surface point at the input parameter pair (u, v)
    surf_ctrlpts = [[] for _ in range(surf.degree_u + 1)]
    for k in range(surf.degree_u + 1):
        temp = [() for _ in range(surf.degree_v + 1)]
        for l in range(surf.degree_v + 1):
            temp[l] = surf.ctrlpts2d[idx_u + k][idx_v + l]
        surf_ctrlpts[k] = temp

    # Return 2-dimensional control points array
    return surf_ctrlpts
