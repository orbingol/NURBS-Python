"""
.. module:: interpolate
    :platform: Unix, Windows
    :synopsis: Provides global interpolation functions for parametric shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from typing import List, Tuple
import math
from . import BSpline
from . import utilities
from . import helpers


def interpolate_curve(points, degree, **kwargs):
    # type: (List[List[float]], int, **bool) -> BSpline.Curve
    """ Curve interpolation through the data points.

    Please see Algorithm A9.1 on The NURBS Book (2nd Edition), pp.369-370 for details.

    Keyword Arguments:
        * ``centripetal``: activates centripetal parametrization method. *Default: False*

    :param points: data points
    :type points: list, tuple
    :param degree: degree of the output parametric curve
    :type degree: int
    :return: interpolated B-Spline curve
    :rtype: BSpline.Curve
    """
    # Keyword arguments
    use_centripetal = kwargs.get('centripetal', False)

    # Number of control points
    num_points = len(points)

    # Get uk
    uk = compute_params_curve(points, use_centripetal)

    # Compute knot vector
    kv = compute_knot_vector(degree, num_points, uk)

    # Do global interpolation
    matrix_a = _build_coeff_matrix(degree, kv, uk, points)
    ctrlpts = ginterp(matrix_a, points)

    # Generate B-spline curve
    curve = BSpline.Curve()
    curve.degree = degree
    curve.ctrlpts = ctrlpts
    curve.knotvector = kv

    return curve


def interpolate_surface(points, size_u, size_v, degree_u, degree_v, **kwargs):
    # type: (List[List[float]], int, int, int, int, **bool) -> BSpline.Surface
    """ Surface interpolation through the data points.

    Please refer to the Algorithm A9.4 on The NURBS Book (2nd Edition), pp.380 for details.

    Keyword Arguments:
        * ``centripetal``: activates centripetal parametrization method. *Default: False*

    :param points: data points
    :type points: list, tuple
    :param size_u: number of data points on the u-direction
    :type size_u: int
    :param size_v: number of data points on the v-direction
    :type size_v: int
    :param degree_u: degree of the output surface for the u-direction
    :type degree_u: int
    :param degree_v: degree of the output surface for the v-direction
    :type degree_v: int
    :return: interpolated B-Spline surface
    :rtype: BSpline.Surface
    """
    # Keyword arguments
    use_centripetal = kwargs.get('centripetal', False)

    # Get uk and vl
    uk, vl = compute_params_surface(points, size_u, size_v, use_centripetal)

    # Compute knot vectors
    kv_u = compute_knot_vector(degree_u, size_u, uk)
    kv_v = compute_knot_vector(degree_v, size_v, vl)

    # Do global interpolation on the u-direction
    ctrlpts_r = []
    for v in range(size_v):
        pts = [points[v + (size_v * u)] for u in range(size_u)]
        matrix_a = _build_coeff_matrix(degree_u, kv_u, uk, pts)
        ctrlpts_r += ginterp(matrix_a, pts)

    # Do global interpolation on the v-direction
    ctrlpts = []
    for u in range(size_u):
        pts = [ctrlpts_r[u + (size_u * v)] for v in range(size_v)]
        matrix_a = _build_coeff_matrix(degree_v, kv_v, vl, pts)
        ctrlpts += ginterp(matrix_a, pts)

    # Generate B-spline surface
    surf = BSpline.Surface()
    surf.degree_u = degree_u
    surf.degree_v = degree_v
    surf.ctrlpts_size_u = size_u
    surf.ctrlpts_size_v = size_v
    surf.ctrlpts = ctrlpts
    surf.knotvector_u = kv_u
    surf.knotvector_v = kv_v

    return surf


def approximate_surface(points, size_u, size_v, degree_u, degree_v, **kwargs):
    # type: (List[List[float]], int, int, int, int, **bool) -> BSpline.Surface
    """ Surface approximation using least squares method with fixed number of control points.

    This algorithm interpolates the corner control points and approximates the inner control points. Please refer to
    The NURBS Book (2nd Edition), pp.422-423 for details.

    :param points: data points
    :type points: list, tuple
    :param size_u: number of data points on the u-direction, :math:`r`
    :type size_u: int
    :param size_v: number of data points on the v-direction, :math:`s`
    :type size_v: int
    :param degree_u: degree of the output surface for the u-direction
    :type degree_u: int
    :param degree_v: degree of the output surface for the v-direction
    :type degree_v: int
    :return: approximated B-Spline surface
    :rtype: BSpline.Surface
    """
    # Keyword arguments
    use_centripetal = kwargs.get('centripetal', False)
    cpts_size_u = kwargs.get('ctrlpts_size_u', size_u - 1)  # number of datapts > number of ctrlpts, n + 1
    cpts_size_v = kwargs.get('ctrlpts_size_v', size_v - 1)  # number of datapts > number of ctrlpts, m + 1

    # Dimension
    dim = len(points[0])

    # Get uk and vl
    uk, vl = compute_params_surface(points, size_u, size_v, use_centripetal)

    # Compute knot vectors
    kv_u = compute_knot_vector2(degree_u, size_u, cpts_size_u, uk)
    kv_v = compute_knot_vector2(degree_v, size_v, cpts_size_v, vl)

    # Construct matrix Nu
    matrix_nu = []
    for i in range(1, size_u - 1):
        m_temp = []
        for j in range(1, cpts_size_u - 1):
            m_temp.append(helpers.basis_function_one(degree_u, kv_u, j, uk[i]))
        matrix_nu.append(m_temp)
    # Compute Nu transpose
    matrix_ntu = utilities.matrix_transpose(matrix_nu)
    # Compute NTNu matrix
    matrix_ntnu = utilities.matrix_multiply(matrix_ntu, matrix_nu)
    # Compute LU-decomposition of NTNu matrix
    matrix_ntnul, matrix_ntnuu = utilities.lu_decomposition(matrix_ntnu)

    # Fit u-direction
    ctrlpts_tmp = [[0.0 for _ in range(dim)] for _ in range(cpts_size_u * size_v)]
    for j in range(size_v):
        ctrlpts_tmp[j + (size_v * 0)] = list(points[j + (size_v * 0)])
        ctrlpts_tmp[j + (size_v * (cpts_size_u - 1))] = list(points[j + (size_v * (size_u - 1))])
        # Compute Rku - Eqn. 9.63
        pt0 = points[j + (size_v * 0)]  # Qzero
        ptm = points[j + (size_v * (size_u - 1))]  # Qm
        rku = []
        for i in range(1, size_u - 1):
            ptk = points[j + (size_v * i)]
            n0p = helpers.basis_function_one(degree_u, kv_u, 0, uk[i])
            nnp = helpers.basis_function_one(degree_u, kv_u, cpts_size_u - 1, uk[i])
            elem2 = [c * n0p for c in pt0]
            elem3 = [c * nnp for c in ptm]
            rku.append([a - b - c for a, b, c in zip(ptk, elem2, elem3)])
        # Compute Ru - Eqn. 9.67
        ru = [[0.0 for _ in range(dim)] for _ in range(cpts_size_u - 2)]
        for i in range(1, cpts_size_u - 1):
            ru_tmp = []
            for idx, pt in enumerate(rku):
                ru_tmp.append([p * helpers.basis_function_one(degree_u, kv_u, i, uk[idx + 1]) for p in pt])
            for d in range(dim):
                for idx in range(len(ru_tmp)):
                    ru[i - 1][d] += ru_tmp[idx][d]
        # Get intermediate control points
        for d in range(dim):
            b = [pt[d] for pt in ru]
            y = utilities.forward_substitution(matrix_ntnul, b)
            x = utilities.backward_substitution(matrix_ntnuu, y)
            for i in range(1, cpts_size_u - 1):
                ctrlpts_tmp[j + (size_v * i)][d] = x[i - 1]

    # Construct matrix Nv
    matrix_nv = []
    for i in range(1, size_v - 1):
        m_temp = []
        for j in range(1, cpts_size_v - 1):
            m_temp.append(helpers.basis_function_one(degree_v, kv_v, j, vl[i]))
        matrix_nv.append(m_temp)
    # Compute Nv transpose
    matrix_ntv = utilities.matrix_transpose(matrix_nv)
    # Compute NTNv matrix
    matrix_ntnv = utilities.matrix_multiply(matrix_ntv, matrix_nv)
    # Compute LU-decomposition of NTNv matrix
    matrix_ntnvl, matrix_ntnvu = utilities.lu_decomposition(matrix_ntnv)

    # Fit v-direction
    ctrlpts = [[0.0 for _ in range(dim)] for _ in range(cpts_size_u * cpts_size_v)]
    for i in range(cpts_size_u):
        ctrlpts[0 + (cpts_size_v * i)] = list(ctrlpts_tmp[0 + (size_v * i)])
        ctrlpts[cpts_size_v - 1 + (cpts_size_v * i)] = list(ctrlpts_tmp[size_v - 1 + (size_v * i)])
        # Compute Rkv - Eqs. 9.63
        pt0 = ctrlpts_tmp[0 + (size_v * i)]  # Qzero
        ptm = ctrlpts_tmp[size_v - 1 + (size_v * i)]  # Qm
        rkv = []
        for j in range(1, size_v - 1):
            ptk = ctrlpts_tmp[j + (size_v * i)]
            n0p = helpers.basis_function_one(degree_v, kv_v, 0, vl[j])
            nnp = helpers.basis_function_one(degree_v, kv_v, cpts_size_v - 1, vl[j])
            elem2 = [c * n0p for c in pt0]
            elem3 = [c * nnp for c in ptm]
            rkv.append([a - b - c for a, b, c in zip(ptk, elem2, elem3)])
        # Compute Rv - Eqn. 9.67
        rv = [[0.0 for _ in range(dim)] for _ in range(cpts_size_v - 2)]
        for j in range(1, cpts_size_v - 1):
            rv_tmp = []
            for idx, pt in enumerate(rkv):
                rv_tmp.append([p * helpers.basis_function_one(degree_v, kv_v, j, vl[idx + 1]) for p in pt])
            for d in range(dim):
                for idx in range(len(rv_tmp)):
                    rv[j - 1][d] += rv_tmp[idx][d]
        # Get intermediate control points
        for d in range(dim):
            b = [pt[d] for pt in rv]
            y = utilities.forward_substitution(matrix_ntnvl, b)
            x = utilities.backward_substitution(matrix_ntnvu, y)
            for j in range(1, cpts_size_v - 1):
                ctrlpts[j + (cpts_size_v * i)][d] = x[j - 1]

    # Generate B-spline surface
    surf = BSpline.Surface()
    surf.degree_u = degree_u
    surf.degree_v = degree_v
    surf.ctrlpts_size_u = cpts_size_u
    surf.ctrlpts_size_v = cpts_size_v
    surf.ctrlpts = ctrlpts
    surf.knotvector_u = kv_u
    surf.knotvector_v = kv_v

    return surf


def compute_knot_vector(degree, num_points, params):
    # type: (int, int, List[float]) -> List[float]
    """ Computes a knot vector from the parameter list using averaging method.

    Please refer to the Equation 9.8 on The NURBS Book (2nd Edition), pp.365 for details.

    :param degree: degree
    :type degree: int
    :param num_points: number of data points
    :type num_points: int
    :param params: list of parameters, :math:`\\overline{u}_{k}`
    :type params: list, tuple
    :return: knot vector
    :rtype: list
    """
    # Start knot vector
    kv = [0.0 for _ in range(degree + 1)]

    # Use averaging method (Eqn 9.8) to compute internal knots in the knot vector
    for i in range(num_points - degree - 1):
        temp_kv = (1.0 / degree) * sum([params[j] for j in range(i + 1, i + degree + 1)])
        kv.append(temp_kv)

    # End knot vector
    kv += [1.0 for _ in range(degree + 1)]

    return kv


def compute_knot_vector2(degree, num_dpts, num_cpts, params):
    # type: (int, int, int, List[float]) -> List[float]
    """ Computes a knot vector ensuring that every knot span has at least one :math:`\\overline{u}_{k}`.

    Please refer to the Equations 9.68 and 9.69 on The NURBS Book (2nd Edition), p.412 for details.

    :param degree: degree
    :type degree: int
    :param num_dpts: number of data points
    :type num_dpts: int
    :param num_cpts: number of control points
    :type num_cpts: int
    :param params: list of parameters, :math:`\\overline{u}_{k}`
    :type params: list, tuple
    :return: knot vector
    :rtype: list
    """
    # Start knot vector
    kv = [0.0 for _ in range(degree + 1)]

    # Compute "d" value - Eqn 9.68
    d = float(num_dpts) / float(num_cpts - degree)
    # Find internal knots
    for j in range(1, num_cpts - degree):
        i = int(j * d)
        alpha = (j * d) - i
        temp_kv = ((1.0 - alpha) * params[i - 1]) + (alpha * params[i])
        kv.append(temp_kv)

    # End knot vector
    kv += [1.0 for _ in range(degree + 1)]

    return kv


def compute_params_curve(points, centripetal):
    # type: (List[List[float]], bool) -> List[float]
    """ Computes :math:`\\overline{u}_{k}` for curves.

    Please refer to the Equations 9.4 and 9.5 for chord length parametrization, and Equation 9.6 for centripetal method
    on The NURBS Book (2nd Edition), pp.364-365.

    :param points: data points
    :type points: list, tuple
    :param centripetal: activates centripetal parametrization method
    :type centripetal: bool
    :return: parameter array, :math:`\\overline{u}_{k}`
    :rtype: list
    """
    # Length of the points array
    num_points = len(points)

    # Calculate chord lengths
    cds = [0.0 for _ in range(num_points + 1)]
    cds[-1] = 1.0
    for i in range(1, num_points):
        distance = utilities.point_distance(points[i], points[i - 1])
        cds[i] = math.sqrt(distance) if centripetal else distance

    # Find the total chord length
    d = sum(cds[1:-1])

    # Divide individual chord lengths by the total chord length
    uk = [0.0 for _ in range(num_points)]
    for i in range(num_points):
        uk[i] = sum(cds[0:i + 1]) / d

    return uk


def compute_params_surface(points, size_u, size_v, centripetal):
    # type: (List[List[float]], int, int, bool) -> Tuple[List[float], List[float]]
    """ Computes :math:`\\overline{u}_{k}` and :math:`\\overline{u}_{l}` for surfaces.

    The data points array has a row size of ``size_v`` and column size of ``size_u`` and it is 1-dimensional. Please
    refer to The NURBS Book (2nd Edition), pp.366-367 for details on how to compute :math:`\\overline{u}_{k}` and
    :math:`\\overline{u}_{l}` arrays for global surface interpolation.

    Please note that this function is not a direct implementation of Algorithm A9.3 which can be found on The NURBS Book
    (2nd Edition), pp.377-378. However, the output is the same.

    :param points: data points
    :type points: list, tuple
    :param size_u: number of points on the u-direction
    :type size_u: int
    :param size_v: number of points on the v-direction
    :type size_v: int
    :param centripetal: activates centripetal parametrization method
    :type centripetal: bool
    :return: :math:`\\overline{u}_{k}` and :math:`\\overline{u}_{l}` parameter arrays as a tuple
    :rtype: tuple
    """
    # Compute uk
    uk = [0.0 for _ in range(size_u)]

    # Compute for each curve on the v-direction
    uk_temp = []
    for v in range(size_v):
        pts_u = [points[v + (size_v * u)] for u in range(size_u)]
        uk_temp += compute_params_curve(pts_u, centripetal)

    # Do averaging on the u-direction
    for u in range(size_u):
        knots_v = [uk_temp[u + (size_u * v)] for v in range(size_v)]
        uk[u] = sum(knots_v) / size_v

    # Compute vl
    vl = [0.0 for _ in range(size_v)]

    # Compute for each curve on the u-direction
    vl_temp = []
    for u in range(size_u):
        pts_v = [points[v + (size_v * u)] for v in range(size_v)]
        vl_temp += compute_params_curve(pts_v, centripetal)

    # Do averaging on the v-direction
    for v in range(size_v):
        knots_u = [vl_temp[v + (size_v * u)] for u in range(size_u)]
        vl[v] = sum(knots_u) / size_u

    return uk, vl


def ginterp(coeff_matrix, points):
    # type: (List[List[float]], List[List[float]]) -> List[List[float]]
    """ Applies global interpolation to the set of data points to find control points.

    :param coeff_matrix: coefficient matrix
    :type coeff_matrix: list, tuple
    :param points: data points
    :type points: list, tuple
    :return: control points
    :rtype: list
    """
    # Dimension
    dim = len(points[0])

    # Number of data points
    num_points = len(points)

    # Solve system of linear equations
    matrix_l, matrix_u = utilities.lu_decomposition(coeff_matrix)
    ctrlpts = [[0.0 for _ in range(dim)] for _ in range(num_points)]
    for i in range(dim):
        b = [pt[i] for pt in points]
        y = utilities.forward_substitution(matrix_l, b)
        x = utilities.backward_substitution(matrix_u, y)
        for j in range(num_points):
            ctrlpts[j][i] = x[j]

    # Return control points
    return ctrlpts


def _build_coeff_matrix(degree, knotvector, params, points):
    # type: (int, List[float], List[float], List[List[float]]) -> List[List[float]]
    """ Builds the coefficient matrix for global interpolation.

    This function only uses data points to build the coefficient matrix. Please refer to The NURBS Book (2nd Edition),
    pp364-370 for details.

    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param params: list of parameters
    :type params: list, tuple
    :param points: data points
    :type points: list, tuple
    :return: coefficient matrix
    :rtype: list
    """
    # Number of data points
    num_points = len(points)

    # Set up coefficient matrix
    matrix_a = [[0.0 for _ in range(num_points)] for _ in range(num_points)]
    for i in range(num_points):
        span = helpers.find_span_linear(degree, knotvector, num_points, params[i])
        matrix_a[i][span-degree:span+1] = helpers.basis_function(degree, knotvector, span, params[i])

    # Return coefficient matrix
    return matrix_a


def _build_coeff_matrix_ders(degree, knotvector, params, points):
    # type: (int, List[float], List[float], List[List[float]]) -> List[List[float]]
    """ Builds the coefficient matrix for global interpolation.

    This function uses data points and first derivatives to build the coefficient matrix. Please refer to The NURBS Book
    (2nd Edition), pp373-376 for details.

    :param degree: degree
    :type degree: int
    :param knotvector: knot vector
    :type knotvector: list, tuple
    :param params: list of parameters
    :type params: list, tuple
    :param points: data points and first derivatives
    :type points: list, tuple
    :return: coefficient matrix
    :rtype: list
    """
    # TODO: Implement global interpolation with first derivatives specified
    # Points array = [P0, D0, P1, D1, P2, D2, ....]
    pass
