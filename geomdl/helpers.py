"""
.. module:: helpers
    :platform: Unix, Windows
    :synopsis: Provides spline evaluation helper functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import os
from copy import deepcopy
from . import linalg
from .exceptions import GeomdlException
try:
    from functools import lru_cache
except ImportError:
    from .functools_lru_cache import lru_cache


def find_span_binsearch(degree, knot_vector, num_ctrlpts, knot, **kwargs):
    """ Finds the span of the knot over the input knot vector using binary search.

    Implementation of Algorithm A2.1 from The NURBS Book by Piegl & Tiller.

    The NURBS Book states that the knot span index always starts from zero, i.e. for a knot vector [0, 0, 1, 1];
    if FindSpan returns 1, then the knot is between the half-open interval [0, 1).

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
    span = degree + 1  # Knot span index starts from zero
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
    Uses recurrence to compute the basis functions, also known as Cox - de
    Boor recursion formula.

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


def basis_functions(degree, knot_vector, spans, knots):
    """ Computes the non-vanishing basis functions for a list of parameters.

    Wrapper for :func:`.helpers.basis_function` to process multiple span
    and knot values. Uses recurrence to compute the basis functions, also
    known as Cox - de Boor recursion formula.

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
    Wrapper for :func:`.helpers.basis_function` to compute multiple basis functions.
    Uses recurrence to compute the basis functions, also known as Cox - de Boor
    recursion formula.

    For instance; if ``degree = 2``, then this function will compute the basis function
    values of degrees **0, 1** and **2** for the ``knot`` value at the input knot ``span``
    of the ``knot_vector``.

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


def basis_functions_ders(degree, knot_vector, spans, knots, order):
    """ Computes derivatives of the basis functions for a list of parameters.

    Wrapper for :func:`.helpers.basis_function_ders` to process multiple span
    and knot values.

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


def knot_insertion(degree, knotvector, ctrlpts, u, **kwargs):
    """ Computes the control points of the rational/non-rational spline after knot insertion.

    Part of Algorithm A5.1 of The NURBS Book by Piegl & Tiller, 2nd Edition.

    Keyword Arguments:
        * ``num``: number of knot insertions. *Default: 1*
        * ``s``: multiplicity of the knot. *Default: computed via :func:`.find_multiplicity`*
        * ``span``: knot span. *Default: computed via :func:`.find_span_linear`*

    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param ctrlpts: control points
    :type ctrlpts: list
    :param u: knot to be inserted
    :type u: float
    :return: updated control points
    :rtype: list
    """
    # Get keyword arguments
    num = kwargs.get('num', 1)  # number of knot insertions
    s = kwargs.get('s', find_multiplicity(u, knotvector))  # multiplicity
    k = kwargs.get('span', find_span_linear(degree, knotvector, len(ctrlpts), u))  # knot span

    # Initialize variables
    np = len(ctrlpts)
    nq = np + num

    # Initialize new control points array (control points may be weighted or not)
    ctrlpts_new = [[] for _ in range(nq)]

    # Initialize a local array of length p + 1
    temp = [[] for _ in range(degree + 1)]

    # Save unaltered control points
    for i in range(0, k - degree + 1):
        ctrlpts_new[i] = ctrlpts[i]
    for i in range(k - s, np):
        ctrlpts_new[i + num] = ctrlpts[i]

    # Start filling the temporary local array which will be used to update control points during knot insertion
    for i in range(0, degree - s + 1):
        temp[i] = deepcopy(ctrlpts[k - degree + i])

    # Insert knot "num" times
    for j in range(1, num + 1):
        L = k - degree + j
        for i in range(0, degree - j - s + 1):
            alpha = knot_insertion_alpha(u, tuple(knotvector), k, i, L)
            if isinstance(temp[i][0], float):
                temp[i][:] = [alpha * elem2 + (1.0 - alpha) * elem1 for elem1, elem2 in zip(temp[i], temp[i + 1])]
            else:
                for idx in range(len(temp[i])):
                    temp[i][idx][:] = [alpha * elem2 + (1.0 - alpha) * elem1 for elem1, elem2 in
                                       zip(temp[i][idx], temp[i + 1][idx])]
        ctrlpts_new[L] = deepcopy(temp[0])
        ctrlpts_new[k + num - j - s] = deepcopy(temp[degree - j - s])

    # Load remaining control points
    L = k - degree + num
    for i in range(L + 1, k - s):
        ctrlpts_new[i] = deepcopy(temp[i - L])

    # Return control points after knot insertion
    return ctrlpts_new


@lru_cache(maxsize=os.environ['GEOMDL_CACHE_SIZE'] if "GEOMDL_CACHE_SIZE" in os.environ else 128)
def knot_insertion_alpha(u, knotvector, span, idx, leg):
    """ Computes :math:`\\alpha` coefficient for knot insertion algorithm.

    :param u: knot
    :type u: float
    :param knotvector: knot vector
    :type knotvector: tuple
    :param span: knot span
    :type span: int
    :param idx: index value (degree-dependent)
    :type idx: int
    :param leg: i-th leg of the control points polygon
    :type leg: int
    :return: coefficient value
    :rtype: float
    """
    return (u - knotvector[leg + idx]) / (knotvector[idx + span + 1] - knotvector[leg + idx])


def knot_insertion_kv(knotvector, u, span, r):
    """ Computes the knot vector of the rational/non-rational spline after knot insertion.

    Part of Algorithm A5.1 of The NURBS Book by Piegl & Tiller, 2nd Edition.

    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param u: knot
    :type u: float
    :param span: knot span
    :type span: int
    :param r: number of knot insertions
    :type r: int
    :return: updated knot vector
    :rtype: list
    """
    # Initialize variables
    kv_size = len(knotvector)
    kv_updated = [0.0 for _ in range(kv_size + r)]

    # Compute new knot vector
    for i in range(0, span + 1):
        kv_updated[i] = knotvector[i]
    for i in range(1, r + 1):
        kv_updated[span + i] = u
    for i in range(span + 1, kv_size):
        kv_updated[i + r] = knotvector[i]

    # Return the new knot vector
    return kv_updated


def knot_removal(degree, knotvector, ctrlpts, u, **kwargs):
    """ Computes the control points of the rational/non-rational spline after knot removal.

    Implementation based on Algorithm A5.8 and Equation 5.28 of The NURBS Book by Piegl & Tiller

    Keyword Arguments:
        * ``num``: number of knot removals

    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param ctrlpts: control points
    :type ctrlpts: list
    :param u: knot to be removed
    :type u: float
    :return: updated control points
    :rtype: list
    """
    tol = kwargs.get('tol', 10e-4)  # Refer to Eq 5.30 for the meaning
    num = kwargs.get('num', 1)  # number of same knot removals
    s = kwargs.get('s', find_multiplicity(u, knotvector))  # multiplicity
    r = kwargs.get('span', find_span_linear(degree, knotvector, len(ctrlpts), u))  # knot span

    # Edge case
    if num < 1:
        return ctrlpts

    # Initialize variables
    first = r - degree
    last = r - s

    # Don't change input variables, prepare new ones for updating
    ctrlpts_new = deepcopy(ctrlpts)

    is_volume = True
    if isinstance(ctrlpts_new[0][0], float):
        is_volume = False

    # Initialize temp array for storing new control points
    if is_volume:
        temp = [[[] for _ in range(len(ctrlpts_new[0]))] for _ in range((2 * degree) + 1)]
    else:
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
        while j - i >= t:
            alpha_i = knot_removal_alpha_i(u, degree, tuple(knotvector), t, i)
            alpha_j = knot_removal_alpha_j(u, degree, tuple(knotvector), t, j)
            if is_volume:
                for idx in range(len(ctrlpts[0])):
                    temp[ii][idx] = [(cpt - (1.0 - alpha_i) * ti) / alpha_i for cpt, ti
                                     in zip(ctrlpts[i][idx], temp[ii - 1][idx])]
                    temp[jj][idx] = [(cpt - alpha_j * tj) / (1.0 - alpha_j) for cpt, tj
                                     in zip(ctrlpts[j][idx], temp[jj + 1][idx])]
            else:
                temp[ii] = [(cpt - (1.0 - alpha_i) * ti) / alpha_i for cpt, ti in zip(ctrlpts[i], temp[ii - 1])]
                temp[jj] = [(cpt - alpha_j * tj) / (1.0 - alpha_j) for cpt, tj in zip(ctrlpts[j], temp[jj + 1])]
            i += 1
            j -= 1
            ii += 1
            jj -= 1

        # Check if the knot is removable
        if j - i < t:
            if is_volume:
                if linalg.point_distance(temp[ii - 1][0], temp[jj + 1][0]) <= tol:
                    remflag = True
            else:
                if linalg.point_distance(temp[ii - 1], temp[jj + 1]) <= tol:
                    remflag = True
        else:
            alpha_i = knot_removal_alpha_i(u, degree, tuple(knotvector), t, i)
            if is_volume:
                ptn = [(alpha_i * t1) + ((1.0 - alpha_i) * t2) for t1, t2 in zip(temp[ii + t + 1][0], temp[ii - 1][0])]
            else:
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

    # Shift control points (refer to p.183 of The NURBS Book, 2nd Edition)
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

    # Slice to get the new control points
    ctrlpts_new = ctrlpts_new[0:-t]

    return ctrlpts_new


@lru_cache(maxsize=os.environ['GEOMDL_CACHE_SIZE'] if "GEOMDL_CACHE_SIZE" in os.environ else 128)
def knot_removal_alpha_i(u, degree, knotvector, num, idx):
    """ Computes :math:`\\alpha_{i}` coefficient for knot removal algorithm.

    Please refer to Eq. 5.29 of The NURBS Book by Piegl & Tiller, 2nd Edition, p.184 for details.

    :param u: knot
    :type u: float
    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: tuple
    :param num: knot removal index
    :type num: int
    :param idx: iterator index
    :type idx: int
    :return: coefficient value
    :rtype: float
    """
    return (u - knotvector[idx]) / (knotvector[idx + degree + 1 + num] - knotvector[idx])


@lru_cache(maxsize=os.environ['GEOMDL_CACHE_SIZE'] if "GEOMDL_CACHE_SIZE" in os.environ else 128)
def knot_removal_alpha_j(u, degree, knotvector, num, idx):
    """ Computes :math:`\\alpha_{j}` coefficient for knot removal algorithm.

    Please refer to Eq. 5.29 of The NURBS Book by Piegl & Tiller, 2nd Edition, p.184 for details.

    :param u: knot
    :type u: float
    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: tuple
    :param num: knot removal index
    :type num: int
    :param idx: iterator index
    :type idx: int
    :return: coefficient value
    :rtype: float
    """
    return (u - knotvector[idx - num]) / (knotvector[idx + degree + 1] - knotvector[idx - num])


def knot_removal_kv(knotvector, span, r):
    """ Computes the knot vector of the rational/non-rational spline after knot removal.

    Part of Algorithm A5.8 of The NURBS Book by Piegl & Tiller, 2nd Edition.

    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param span: knot span
    :type span: int
    :param r: number of knot removals
    :type r: int
    :return: updated knot vector
    :rtype: list
    """
    # Edge case
    if r < 1:
        return knotvector

    # Create a deep copy of the input knot  vector
    kv_updated = deepcopy(knotvector)

    # Shift knots
    for k in range(span + 1, len(knotvector)):
        kv_updated[k - r] = knotvector[k]

    # Slice to get the new knot vector
    kv_updated = kv_updated[0:-r]

    # Return the new knot vector
    return kv_updated


def knot_refinement(degree, knotvector, ctrlpts, **kwargs):
    """ Computes the knot vector and the control points of the rational/non-rational spline after knot refinement.

    Implementation of Algorithm A5.4 of The NURBS Book by Piegl & Tiller, 2nd Edition.

    The algorithm automatically find the knots to be refined, i.e. the middle knots in the knot vector, and their
    multiplicities, i.e. number of same knots in the knot vector. This is the basis of knot refinement algorithm.
    This operation can be overridden by providing a list of knots via ``knot_list`` argument. In addition, users can
    provide a list of additional knots to be inserted in the knot vector via ``add_knot_list`` argument.

    Moreover, a numerical ``density`` argument can be used to automate extra knot insertions. If ``density`` is bigger
    than 1, then the algorithm finds the middle knots in each internal knot span to increase the number of knots to be
    refined.

    **Example**: Let the degree is 2 and the knot vector to be refined is ``[0, 2, 4]`` with the superfluous knots
    from the start and end are removed. Knot vectors with the changing ``density (d)`` value will be:

    * ``d = 1``, knot vector ``[0, 1, 1, 2, 2, 3, 3, 4]``
    * ``d = 2``, knot vector ``[0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2, 2, 2.5, 2.5, 3, 3, 3.5, 3.5, 4]``

    Keyword Arguments:
        * ``knot_list``: knot list to be refined. *Default: list of internal knots*
        * ``add_knot_list``: additional list of knots to be refined. *Default: []*
        * ``density``: Density of the knots. *Default: 1*

    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param ctrlpts: control points
    :return: updated control points and knot vector
    :rtype: tuple
    """
    # Get keyword arguments
    tol = kwargs.get('tol', 10e-8)  # tolerance value for zero equality checking
    check_num = kwargs.get('check_num', True)  # enables/disables input validity checking
    knot_list = kwargs.get('knot_list', knotvector[degree:-degree])
    add_knot_list = kwargs.get('add_knot_list', list())
    density = kwargs.get('density', 1)

    # Input validity checking
    if check_num:
        if not isinstance(density, int):
            raise GeomdlException("Density value must be an integer", data=dict(density=density))

        if density < 1:
            raise GeomdlException("Density value cannot be less than 1", data=dict(density=density))

    # Add additional knots to be refined
    if add_knot_list:
        knot_list += list(add_knot_list)

    # Sort the list and convert to a set to make sure that the values are unique
    knot_list = sorted(set(knot_list))

    # Increase knot density
    for d in range(0, density):
        rknots = []
        for i in range(len(knot_list) - 1):
            knot_tmp = knot_list[i] + ((knot_list[i + 1] - knot_list[i]) / 2.0)
            rknots.append(knot_list[i])
            rknots.append(knot_tmp)
        rknots.append(knot_list[i + 1])
        knot_list = rknots

    # Find how many knot insertions are necessary
    X = []
    for mk in knot_list:
        s = find_multiplicity(mk, knotvector)
        r = degree - s
        X += [mk for _ in range(r)]

    # Check if the knot refinement is possible
    if not X:
        raise GeomdlException("Cannot refine knot vector on this parametric dimension")

    # Initialize common variables
    r = len(X) - 1
    n = len(ctrlpts) - 1
    m = n + degree + 1
    a = find_span_linear(degree, knotvector, n, X[0])
    b = find_span_linear(degree, knotvector, n, X[r]) + 1

    # Initialize new control points array
    if isinstance(ctrlpts[0][0], float):
        new_ctrlpts = [[] for _ in range(n + r + 2)]
    else:
        new_ctrlpts = [[[] for _ in range(len(ctrlpts[0]))] for _ in range(n + r + 2)]

    # Fill unchanged control points
    for j in range(0, a - degree + 1):
        new_ctrlpts[j] = ctrlpts[j]
    for j in range(b - 1, n + 1):
        new_ctrlpts[j + r + 1] = ctrlpts[j]

    # Initialize new knot vector array
    new_kv = [0.0 for _ in range(m + r + 2)]

    # Fill unchanged knots
    for j in range(0, a + 1):
        new_kv[j] = knotvector[j]
    for j in range(b + degree, m + 1):
        new_kv[j + r + 1] = knotvector[j]

    # Initialize variables for knot refinement
    i = b + degree - 1
    k = b + degree + r
    j = r

    # Apply knot refinement
    while j >= 0:
        while X[j] <= knotvector[i] and i > a:
            new_ctrlpts[k - degree - 1] = ctrlpts[i - degree - 1]
            new_kv[k] = knotvector[i]
            k -= 1
            i -= 1
        new_ctrlpts[k - degree - 1] = deepcopy(new_ctrlpts[k - degree])
        for l in range(1, degree + 1):
            idx = k - degree + l
            alpha = new_kv[k + l] - X[j]
            if abs(alpha) < tol:
                new_ctrlpts[idx - 1] = deepcopy(new_ctrlpts[idx])
            else:
                alpha = alpha / (new_kv[k + l] - knotvector[i - degree + l])
                if isinstance(ctrlpts[0][0], float):
                    new_ctrlpts[idx - 1] = [alpha * p1 + (1.0 - alpha) * p2 for p1, p2 in
                                            zip(new_ctrlpts[idx - 1], new_ctrlpts[idx])]
                else:
                    for idx2 in range(len(ctrlpts[0])):
                        new_ctrlpts[idx - 1][idx2] = [alpha * p1 + (1.0 - alpha) * p2 for p1, p2 in
                                                      zip(new_ctrlpts[idx - 1][idx2], new_ctrlpts[idx][idx2])]
        new_kv[k] = X[j]
        k = k - 1
        j -= 1

    # Return control points and knot vector after refinement
    return new_ctrlpts, new_kv


def degree_elevation(degree, ctrlpts, **kwargs):
    """ Computes the control points of the rational/non-rational spline after degree elevation.

    Implementation of Eq. 5.36 of The NURBS Book by Piegl & Tiller, 2nd Edition, p.205

    Keyword Arguments:
        * ``num``: number of degree elevations

    Please note that degree elevation algorithm can only operate on Bezier shapes, i.e. curves, surfaces, volumes.

    :param degree: degree
    :type degree: int
    :param ctrlpts: control points
    :type ctrlpts: list, tuple
    :return: control points of the degree-elevated shape
    :rtype: list
    """
    # Get keyword arguments
    num = kwargs.get('num', 1)  # number of degree elevations
    check_op = kwargs.get('check_num', True)  # enable/disable input validation checks

    if check_op:
        if degree + 1 != len(ctrlpts):
            raise GeomdlException("Degree elevation can only work with Bezier-type geometries")
        if num <= 0:
            raise GeomdlException("Cannot degree elevate " + str(num) + " times")

    # Initialize variables
    num_pts_elev = degree + 1 + num
    pts_elev = [[0.0 for _ in range(len(ctrlpts[0]))] for _ in range(num_pts_elev)]

    # Compute control points of degree-elevated 1-dimensional shape
    for i in range(0, num_pts_elev):
        start = max(0, (i - num))
        end = min(degree, i)
        for j in range(start, end + 1):
            coeff = linalg.binomial_coefficient(degree, j) * linalg.binomial_coefficient(num, (i - j))
            coeff /= linalg.binomial_coefficient((degree + num), i)
            pts_elev[i] = [p1 + (coeff * p2) for p1, p2 in zip(pts_elev[i], ctrlpts[j])]

    # Return computed control points after degree elevation
    return pts_elev


def degree_reduction(degree, ctrlpts, **kwargs):
    """ Computes the control points of the rational/non-rational spline after degree reduction.

    Implementation of Eqs. 5.41 and 5.42 of The NURBS Book by Piegl & Tiller, 2nd Edition, p.220

    Please note that degree reduction algorithm can only operate on Bezier shapes, i.e. curves, surfaces, volumes and
    this implementation does NOT compute the maximum error tolerance as described via Eqs. 5.45 and 5.46 of The NURBS
    Book by Piegl & Tiller, 2nd Edition, p.221 to determine whether the shape is degree reducible or not.

    :param degree: degree
    :type degree: int
    :param ctrlpts: control points
    :type ctrlpts: list, tuple
    :return: control points of the degree-reduced shape
    :rtype: list
    """
    # Get keyword arguments
    check_op = kwargs.get('check_num', True)  # enable/disable input validation checks

    if check_op:
        if degree + 1 != len(ctrlpts):
            raise GeomdlException("Degree reduction can only work with Bezier-type geometries")
        if degree < 2:
            raise GeomdlException("Input spline geometry must have degree > 1")

    # Initialize variables
    pts_red = [[0.0 for _ in range(len(ctrlpts[0]))] for _ in range(degree)]

    # Fix start and end control points
    pts_red[0] = ctrlpts[0]
    pts_red[-1] = ctrlpts[-1]

    # Find if the degree is an even or an odd number
    p_is_odd = True if degree % 2 != 0 else False

    # Compute control points of degree-reduced 1-dimensional shape
    r = int((degree - 1) / 2)
    # Handle a special case when degree = 2
    if degree == 2:
        r1 = r - 2
    else:
        # Determine r1 w.r.t. degree evenness
        r1 = r - 1 if p_is_odd else r
    for i in range(1, r1 + 1):
        alpha = float(i) / float(degree)
        pts_red[i] = [(c1 - (alpha * c2)) / (1 - alpha) for c1, c2 in zip(ctrlpts[i], pts_red[i - 1])]
    for i in range(degree - 2, r1 + 2):
        alpha = float(i + 1) / float(degree)
        pts_red[i] = [(c1 - ((1 - alpha) * c2)) / alpha for c1, c2 in zip(ctrlpts[i + 1], pts_red[i + 1])]

    if p_is_odd:
        alpha = float(r) / float(degree)
        left = [(c1 - (alpha * c2)) / (1 - alpha) for c1, c2 in zip(ctrlpts[r], pts_red[r - 1])]
        alpha = float(r + 1) / float(degree)
        right = [(c1 - ((1 - alpha) * c2)) / alpha for c1, c2 in zip(ctrlpts[r + 1], pts_red[r + 1])]
        pts_red[r] = [0.5 * (pl + pr) for pl, pr in zip(left, right)]

    # Return computed control points after degree reduction
    return pts_red


def curve_deriv_cpts(dim, degree, kv, cpts, rs, deriv_order=0):
    """ Compute control points of curve derivatives.

    Implementation of Algorithm A3.3 from The NURBS Book by Piegl & Tiller.

    :param dim: spatial dimension of the curve
    :type dim: int
    :param degree: degree of the curve
    :type degree: int
    :param kv: knot vector
    :type kv: list, tuple
    :param cpts: control points
    :type cpts: list, tuple
    :param rs: minimum (r1) and maximum (r2) knot spans that the curve derivative will be computed
    :param deriv_order: derivative order, i.e. the i-th derivative
    :type deriv_order: int
    :return: control points of the derivative curve over the input knot span range
    :rtype: list
    """
    r = rs[1] - rs[0]

    # Initialize return value (control points)
    PK = [[[None for _ in range(dim)] for _ in range(r + 1)] for _ in range(deriv_order + 1)]

    # Algorithm A3.3
    for i in range(0, r + 1):
        PK[0][i][:] = [elem for elem in cpts[rs[0] + i]]

    for k in range(1, deriv_order + 1):
        tmp = degree - k + 1
        for i in range(0, r - k + 1):
            PK[k][i][:] = [tmp * (elem1 - elem2) /
                           (kv[rs[0] + i + degree + 1] - kv[rs[0] + i + k]) for elem1, elem2
                           in zip(PK[k - 1][i + 1], PK[k - 1][i])]

    # Return control points (as a 2-dimensional list of points)
    return PK


def surface_deriv_cpts(dim, degree, kv, cpts, cpsize, rs, ss, deriv_order=0):
    """ Compute control points of surface derivatives.

    Implementation of Algorithm A3.7 from The NURBS Book by Piegl & Tiller.

    :param dim: spatial dimension of the surface
    :type dim: int
    :param degree: degrees
    :type degree: list, tuple
    :param kv: knot vectors
    :type kv: list, tuple
    :param cpts: control points
    :type cpts: list, tuple
    :param cpsize: number of control points in all parametric directions
    :type cpsize: list, tuple
    :param rs: minimum (r1) and maximum (r2) knot spans for the u-direction
    :type rs: list, tuple
    :param ss: minimum (s1) and maximum (s2) knot spans for the v-direction
    :type ss: list, tuple
    :param deriv_order: derivative order, i.e. the i-th derivative
    :type deriv_order: int
    :return: control points of the derivative surface over the input knot span ranges
    :rtype: list
    """
    # Initialize return value (control points)
    PKL = [[[[[None for _ in range(dim)]
              for _ in range(cpsize[1])] for _ in range(cpsize[0])]
            for _ in range(deriv_order + 1)] for _ in range(deriv_order + 1)]

    du = min(degree[0], deriv_order)
    dv = min(degree[1], deriv_order)

    r = rs[1] - rs[0]
    s = ss[1] - ss[0]

    # Control points of the U derivatives of every U-curve
    for j in range(ss[0], ss[1] + 1):
        PKu = curve_deriv_cpts(dim=dim,
                               degree=degree[0],
                               kv=kv[0],
                               cpts=[cpts[j + (cpsize[1] * i)] for i in range(cpsize[0])],
                               rs=rs,
                               deriv_order=du)

        # Copy into output as the U partial derivatives
        for k in range(0, du + 1):
            for i in range(0, r - k + 1):
                PKL[k][0][i][j - ss[0]] = PKu[k][i]

    # Control points of the V derivatives of every U-differentiated V-curve
    for k in range(0, du):
        for i in range(0, r - k + 1):
            dd = min(deriv_order - k, dv)

            PKuv = curve_deriv_cpts(dim=dim,
                                    degree=degree[1],
                                    kv=kv[1][ss[0]:],
                                    cpts=PKL[k][0][i],
                                    rs=(0, s),
                                    deriv_order=dd)

            # Copy into output
            for l in range(1, dd + 1):
                for j in range(0, s - l + 1):
                    PKL[k][l][i][j] = PKuv[l][j]

    # Return control points
    return PKL
