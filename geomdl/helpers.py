"""
.. module:: helpers
    :platform: Unix, Windows
    :synopsis: Evaluation helper functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from copy import deepcopy
from . import linalg
from .exceptions import *


def find_span_binsearch(degree, knot_vector, num_ctrlpts, knot, **kwargs):
    """ Finds the span of the knot over the input knot vector using binary search.

    Implementation of Algorithm A2.1 from The NURBS Book by Piegl & Tiller.

    The NURBS Book states that the knot span index always starts from zero, i.e. for a knot vector [0, 0, 1, 1];
    if FindSpan returns 1, then the knot is between the interval [0, 1).

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot vector, :math:`U`
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points, :math:`n + 1`
    :type num_ctrlpts: int
    :param knot: knot or parameter, :math:`u`
    :type knot: float
    :return: knot span
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


def find_span_linear(degree, knot_vector, num_ctrlpts, knot, **kwargs):
    """ Finds the span of a single knot over the knot vector using linear search.

    Alternative implementation for the Algorithm A2.1 from The NURBS Book by Piegl & Tiller.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot vector, :math:`U`
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points, :math:`n + 1`
    :type num_ctrlpts: int
    :param knot: knot or parameter, :math:`u`
    :type knot: float
    :return: knot span
    :rtype: int
    """
    span = 0  # Knot span index starts from zero
    while span < num_ctrlpts and knot_vector[span] <= knot:
        span += 1

    return span - 1


def find_spans(degree, knot_vector, num_ctrlpts, knots, func=find_span_linear):
    """ Finds spans of a list of knots over the knot vector.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot vector, :math:`U`
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points, :math:`n + 1`
    :type num_ctrlpts: int
    :param knots: list of knots or parameters
    :type knots: list, tuple
    :param func: function for span finding, e.g. linear or binary search
    :return: list of spans
    :rtype: list
    """
    spans = []
    for knot in knots:
        spans.append(func(degree, knot_vector, num_ctrlpts, knot))
    return spans


def find_multiplicity(knot, knot_vector, **kwargs):
    """ Finds knot multiplicity over the knot vector.

    Keyword Arguments:
        * ``tol``: tolerance (delta) value for equality checking

    :param knot: knot or parameter, :math:`u`
    :type knot: float
    :param knot_vector: knot vector, :math:`U`
    :type knot_vector: list, tuple
    :return: knot multiplicity, :math:`s`
    :rtype: int
    """
    # Get tolerance value
    tol = kwargs.get('tol', 10e-8)

    mult = 0  # initial multiplicity

    for kv in knot_vector:
        if abs(knot - kv) <= tol:
            mult += 1

    return mult


def basis_function(degree, knot_vector, span, knot):
    """ Computes the non-vanishing basis functions for a single parameter.

    Implementation of Algorithm A2.2 from The NURBS Book by Piegl & Tiller.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot vector, :math:`U`
    :type knot_vector: list, tuple
    :param span: knot span, :math:`i`
    :type span: int
    :param knot: knot or parameter, :math:`u`
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
    """ Computes the non-vanishing basis functions for a list of parameters.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot vector, :math:`U`
    :type knot_vector: list, tuple
    :param spans: list of knot spans
    :type spans:  list, tuple
    :param knots: list of knots or parameters
    :type knots: list, tuple
    :return: basis functions
    :rtype: list
    """
    basis = []
    for span, knot in zip(spans, knots):
        basis.append(basis_function(degree, knot_vector, span, knot))
    return basis


def basis_function_all(degree, knot_vector, span, knot):
    """ Computes all non-zero basis functions of all degrees from 0 up to the input degree for a single parameter.

    A slightly modified version of Algorithm A2.2 from The NURBS Book by Piegl & Tiller.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector:  knot vector, :math:`U`
    :type knot_vector: list, tuple
    :param span: knot span, :math:`i`
    :type span: int
    :param knot: knot or parameter, :math:`u`
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
    """ Computes derivatives of the basis functions for a single parameter.

    Implementation of Algorithm A2.3 from The NURBS Book by Piegl & Tiller.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot vector, :math:`U`
    :type knot_vector: list, tuple
    :param span: knot span, :math:`i`
    :type span: int
    :param knot: knot or parameter, :math:`u`
    :type knot: float
    :param order: order of the derivative
    :type order: int
    :return: derivatives of the basis functions
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


def basis_functions_ders(degree, knot_vector, spans, knots, order):
    """ Computes derivatives of the basis functions for a list of parameters.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot vector, :math:`U`
    :type knot_vector: list, tuple
    :param spans: list of knot spans
    :type spans:  list, tuple
    :param knots: list of knots or parameters
    :type knots: list, tuple
    :param order: order of the derivative
    :type order: int
    :return: derivatives of the basis functions
    :rtype: list
    """
    basis_ders = []
    for span, knot in zip(spans, knots):
        basis_ders.append(basis_function_ders(degree, knot_vector, span, knot, order))
    return basis_ders


def basis_function_one(degree, knot_vector, span, knot):
    """ Computes the value of a basis function for a single parameter.

    Implementation of Algorithm 2.4 from The NURBS Book by Piegl & Tiller.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot vector
    :type knot_vector: list, tuple
    :param span: knot span, :math:`i`
    :type span: int
    :param knot: knot or parameter, :math:`u`
    :type knot: float
    :return: basis function, :math:`N_{i,p}`
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
    """ Computes the derivative of one basis functions for a single parameter.

    Implementation of Algorithm A2.5 from The NURBS Book by Piegl & Tiller.

    :param degree: degree, :math:`p`
    :type degree: int
    :param knot_vector: knot_vector, :math:`U`
    :type knot_vector: list, tuple
    :param span: knot span, :math:`i`
    :type span: int
    :param knot: knot or parameter, :math:`u`
    :type knot: float
    :param order: order of the derivative
    :type order: int
    :return: basis function derivatives
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


def knot_removal(degree, knotvector, ctrlpts, u, **kwargs):
    """ Removes knot from the parametrically 1-dimensional rational/non-rational spline shape.

    Implementation based on Algorithm A5.8 and Equation 5.28 of The NURBS Book by Piegl & Tiller

    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param ctrlpts: control points
    :type ctrlpts: list
    :param u: knot to be removed
    :type u: float
    :return: updated knot vector and control points
    :rtype: tuple
    """
    tol = kwargs.get('tol', 10e-4)  # Refer to Eq 5.30 for the meaning
    num = kwargs.get('num', 1)  # number of same knot removals

    # It is impossible to remove knots if num > s
    s = find_multiplicity(u, knotvector)
    if num > s or num <= 0:
        # Raise a custom exception and let the caller handle exception
        raise GeomdlException("Knot " + str(u) + " cannot be removed " + str(num) + " times",
                              data=dict(knot=u, num=num, multiplicity=s))

    # Always remove the last possible knot to satisfy the inequality U(r) != U(r+1)
    r = find_span_linear(degree, knotvector, len(ctrlpts), u)

    first = r - degree
    last = r - s

    # Don't change inputs
    ctrlpts_new = deepcopy(ctrlpts)
    knotvector_new = deepcopy(knotvector)

    # Initialize temp array for storing new control points
    temp = [[] for _ in range((2 * degree) + 1)]

    # Loop for Eqs 5.28 & 5.29
    for t in range(0, num):
        temp[0] = ctrlpts[first - 1]
        temp[last - first + 2] = ctrlpts[last + 1]
        i = first
        j = last
        ii = 1
        jj = last - first + 1
        remflag = False

        # Compute control points for one removal step
        while j - i > t:
            alpha_i = (u - knotvector[i]) / (knotvector[i + degree + 1 + t] - knotvector[i])
            alpha_j = (u - knotvector[j - t]) / (knotvector[j + degree + 1] - knotvector[j - t])
            temp[ii] = [(cpt - (1.0 - alpha_i) * ti) / alpha_i for cpt, ti in zip(ctrlpts[i], temp[ii - 1])]
            temp[jj] = [(cpt - alpha_j * tj) / (1.0 - alpha_j) for cpt, tj in zip(ctrlpts[j], temp[jj + 1])]
            i += 1
            j -= 1
            ii += 1
            jj -= 1

        # Check if the knot is removable
        if j - i < t:
            if linalg.point_distance(temp[ii - 1], temp[jj + 1]) <= tol:
                remflag = True
        else:
            alpha_i = (u - knotvector[i]) / (knotvector[i + degree + 1 + t] - knotvector[i])
            ptn = [(alpha_i * t1) + ((1.0 - alpha_i) * t2) for t1, t2 in zip(temp[ii + t + 1], temp[ii - 1])]
            if linalg.point_distance(ctrlpts[i], ptn) <= tol:
                remflag = True

        # Check if we can remove the knot and update new control points array
        if remflag:
            i = first
            j = last
            while j - i > t:
                ctrlpts_new[i] = temp[i - first + 1]
                ctrlpts_new[j] = temp[j - first + 1]
                i += 1
                j -= 1

        # Update indices
        first -= 1
        last += 1

    # Fix indexing
    t += 1

    # Shift knots
    for k in range(r + 1, len(knotvector)):
        knotvector_new[k - t] = knotvector[k]

    # Shift control points (refer to p183 of The NURBS Book, 2nd Edition)
    j = int((2*r - s - degree) / 2)  # first control point out
    i = j
    for k in range(1, t):
        if k % 2 == 1:
            i += 1
        else:
            j -= 1
    for k in range(i+1, len(ctrlpts)):
        ctrlpts_new[j] = ctrlpts[k]
        j += 1

    # Slice to get new knot vector and control points
    knotvector_new = knotvector_new[0:-t]
    ctrlpts_new = ctrlpts_new[0:-t]

    return knotvector_new, ctrlpts_new


def degree_elevation(degree, ctrlpts, **kwargs):
    """ Computes the control points of the degree-elevated parametrically 1-dimensional shape

    Implementation of Eq. 5.36 of The NURBS Book by Piegl & Tiller, 2nd Edition, p.205

    Keyword Arguments:
        * ``num``: number of degree elevations

    :param degree: degree
    :type degree: int
    :param ctrlpts: control points
    :type ctrlpts: list, tuple
    :return: control points of the degree-elevated shape
    :rtype: list
    """
    num = kwargs.get('num', 1)  # number of degree elevations
    check_ctrlpts = kwargs.get('check_pts', True)  # check if the input is a Bezier-type shape

    if check_ctrlpts and degree + 1 != len(ctrlpts):
        raise GeomdlException("Degree elevation can only work with Bezier curves")

    if num <= 0:
        raise GeomdlException("Cannot degree elevate " + str(num) + " times")

    # Initialize variables
    num_pts_elev = degree + 1 + num
    pts_elev = [[0.0 for _ in range(len(ctrlpts[0]))] for _ in range(num_pts_elev)]

    # Compute control points of degree-elevated shape
    for i in range(0, num_pts_elev):
        start = max(0, (i - num))
        end = min(degree, i)
        for j in range(start, end + 1):
            coeff = linalg.binomial_coefficient(degree, j) * linalg.binomial_coefficient(num, (i - j)) / linalg.binomial_coefficient((degree + num), i)
            pts_elev[i] = [p1 + (coeff * p2) for p1, p2 in zip(pts_elev[i], ctrlpts[j])]

    # Return computed control points
    return pts_elev
