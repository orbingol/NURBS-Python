"""
.. module:: fitting.approximate_global
    :platform: Unix, Windows
    :synopsis: Global approximation functions

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import linalg, helpers, BSpline
from . import common

__all__ = []


def approximate_curve(points, degree, **kwargs):
    """ Curve approximation using least squares method with fixed number of control points.

    Please refer to The NURBS Book (2nd Edition), pp.410-413 for details.

    Keyword Arguments:
        * ``centripetal``: activates centripetal parametrization method. *Default: False*
        * ``ctrlpts_size``: number of control points. *Default: len(points) - 1*

    :param points: data points
    :type points: list, tuple
    :param degree: degree of the output parametric curve
    :type degree: int
    :return: approximated B-Spline curve
    :rtype: BSpline.Curve
    """
    # Number of data points
    num_dpts = len(points)  # corresponds to variable "r" in the algorithm

    # Get keyword arguments
    use_centripetal = kwargs.get('centripetal', False)
    num_cpts = kwargs.get('ctrlpts_size', num_dpts - 1)

    # Dimension
    dim = len(points[0])

    # Get uk
    uk = common.compute_params_curve(points, use_centripetal)

    # Compute knot vector
    kv = common.compute_knot_vector2(degree, num_dpts, num_cpts, uk)

    # Compute matrix N
    matrix_n = []
    for i in range(1, num_dpts - 1):
        m_temp = []
        for j in range(1, num_cpts - 1):
            m_temp.append(helpers.basis_function_one(degree, kv, j, uk[i]))
        matrix_n.append(m_temp)

    # Compute NT
    matrix_nt = linalg.matrix_transpose(matrix_n)

    # Compute NTN matrix
    matrix_ntn = linalg.matrix_multiply(matrix_nt, matrix_n)

    # LU-factorization
    matrix_l, matrix_u = linalg.lu_decomposition(matrix_ntn)

    # Initialize control points array
    ctrlpts = [[0.0 for _ in range(dim)] for _ in range(num_cpts)]

    # Fix start and end points
    ctrlpts[0] = list(points[0])
    ctrlpts[-1] = list(points[-1])

    # Compute Rk - Eqn 9.63
    pt0 = points[0]  # Qzero
    ptm = points[-1]  # Qm
    rk = []
    for i in range(1, num_dpts - 1):
        ptk = points[i]
        n0p = helpers.basis_function_one(degree, kv, 0, uk[i])
        nnp = helpers.basis_function_one(degree, kv, num_cpts - 1, uk[i])
        elem2 = [c * n0p for c in pt0]
        elem3 = [c * nnp for c in ptm]
        rk.append([a - b - c for a, b, c in zip(ptk, elem2, elem3)])

    # Compute R - Eqn. 9.67
    vector_r = [[0.0 for _ in range(dim)] for _ in range(num_cpts - 2)]
    for i in range(1, num_cpts - 1):
        ru_tmp = []
        for idx, pt in enumerate(rk):
            ru_tmp.append([p * helpers.basis_function_one(degree, kv, i, uk[idx + 1]) for p in pt])
        for d in range(dim):
            for idx in range(len(ru_tmp)):
                vector_r[i - 1][d] += ru_tmp[idx][d]

    # Compute control points
    for i in range(dim):
        b = [pt[i] for pt in vector_r]
        y = linalg.forward_substitution(matrix_l, b)
        x = linalg.backward_substitution(matrix_u, y)
        for j in range(1, num_cpts - 1):
            ctrlpts[j][i] = x[j - 1]

    # Generate B-spline curve
    curve = BSpline.Curve()
    curve.degree.u = degree
    curve.set_ctrlpts(ctrlpts)
    curve.knotvector.u = kv

    return curve


def approximate_surface(points, size_u, size_v, degree_u, degree_v, **kwargs):
    """ Surface approximation using least squares method with fixed number of control points.

    This algorithm interpolates the corner control points and approximates the remaining control points. Please refer to
    Algorithm A9.7 of The NURBS Book (2nd Edition), pp.422-423 for details.

    Keyword Arguments:
        * ``centripetal``: activates centripetal parametrization method. *Default: False*
        * ``ctrlpts_size_u``: number of control points on the u-direction. *Default: size_u - 1*
        * ``ctrlpts_size_v``: number of control points on the v-direction. *Default: size_v - 1*

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
    num_cpts_u = kwargs.get('ctrlpts_size_u', size_u - 1)  # number of datapts, r + 1 > number of ctrlpts, n + 1
    num_cpts_v = kwargs.get('ctrlpts_size_v', size_v - 1)  # number of datapts, s + 1 > number of ctrlpts, m + 1

    # Dimension
    dim = len(points[0])

    # Get uk and vl
    uk, vl = common.compute_params_surface(points, size_u, size_v, use_centripetal)

    # Compute knot vectors
    kv_u = common.compute_knot_vector2(degree_u, size_u, num_cpts_u, uk)
    kv_v = common.compute_knot_vector2(degree_v, size_v, num_cpts_v, vl)

    # Construct matrix Nu
    matrix_nu = []
    for i in range(1, size_u - 1):
        m_temp = []
        for j in range(1, num_cpts_u - 1):
            m_temp.append(helpers.basis_function_one(degree_u, kv_u, j, uk[i]))
        matrix_nu.append(m_temp)
    # Compute Nu transpose
    matrix_ntu = linalg.matrix_transpose(matrix_nu)
    # Compute NTNu matrix
    matrix_ntnu = linalg.matrix_multiply(matrix_ntu, matrix_nu)
    # Compute LU-decomposition of NTNu matrix
    matrix_ntnul, matrix_ntnuu = linalg.lu_decomposition(matrix_ntnu)

    # Fit u-direction
    ctrlpts_tmp = [[0.0 for _ in range(dim)] for _ in range(num_cpts_u * size_v)]
    for j in range(size_v):
        ctrlpts_tmp[0 + (num_cpts_u * j)] = list(points[0 + (size_u * j)])
        ctrlpts_tmp[(num_cpts_u - 1) + (num_cpts_u * j)] = list(points[(size_u - 1) + (size_u * j)])
        # Compute Rku - Eqn. 9.63
        pt0 = points[0 + (size_u * j)]  # Qzero
        ptm = points[(size_u - 1) + (size_u * j)]  # Qm
        rku = []
        for i in range(1, size_u - 1):
            ptk = points[i + (size_u * j)]
            n0p = helpers.basis_function_one(degree_u, kv_u, 0, uk[i])
            nnp = helpers.basis_function_one(degree_u, kv_u, num_cpts_u - 1, uk[i])
            elem2 = [c * n0p for c in pt0]
            elem3 = [c * nnp for c in ptm]
            rku.append([a - b - c for a, b, c in zip(ptk, elem2, elem3)])
        # Compute Ru - Eqn. 9.67
        ru = [[0.0 for _ in range(dim)] for _ in range(num_cpts_u - 2)]
        for i in range(1, num_cpts_u - 1):
            ru_tmp = []
            for idx, pt in enumerate(rku):
                ru_tmp.append([p * helpers.basis_function_one(degree_u, kv_u, i, uk[idx + 1]) for p in pt])
            for d in range(dim):
                for idx in range(len(ru_tmp)):
                    ru[i - 1][d] += ru_tmp[idx][d]
        # Get intermediate control points
        for d in range(dim):
            b = [pt[d] for pt in ru]
            y = linalg.forward_substitution(matrix_ntnul, b)
            x = linalg.backward_substitution(matrix_ntnuu, y)
            for i in range(1, num_cpts_u - 1):
                ctrlpts_tmp[i + (num_cpts_u * j)][d] = x[i - 1]

    # Construct matrix Nv
    matrix_nv = []
    for i in range(1, size_v - 1):
        m_temp = []
        for j in range(1, num_cpts_v - 1):
            m_temp.append(helpers.basis_function_one(degree_v, kv_v, j, vl[i]))
        matrix_nv.append(m_temp)
    # Compute Nv transpose
    matrix_ntv = linalg.matrix_transpose(matrix_nv)
    # Compute NTNv matrix
    matrix_ntnv = linalg.matrix_multiply(matrix_ntv, matrix_nv)
    # Compute LU-decomposition of NTNv matrix
    matrix_ntnvl, matrix_ntnvu = linalg.lu_decomposition(matrix_ntnv)

    # Fit v-direction
    ctrlpts = [[0.0 for _ in range(dim)] for _ in range(num_cpts_u * num_cpts_v)]
    for i in range(num_cpts_u):
        ctrlpts[i + (num_cpts_u * 0)] = list(ctrlpts_tmp[i + (num_cpts_u * 0)])
        ctrlpts[i + (num_cpts_u * (num_cpts_v - 1))] = list(ctrlpts_tmp[i + (num_cpts_u * (size_v - 1))])
        # Compute Rkv - Eqs. 9.63
        pt0 = ctrlpts_tmp[i + (num_cpts_u * 0)]  # Qzero
        ptm = ctrlpts_tmp[i + (num_cpts_u * (size_v - 1))]  # Qm
        rkv = []
        for j in range(1, size_v - 1):
            ptk = ctrlpts_tmp[i + (num_cpts_u * j)]
            n0p = helpers.basis_function_one(degree_v, kv_v, 0, vl[j])
            nnp = helpers.basis_function_one(degree_v, kv_v, num_cpts_v - 1, vl[j])
            elem2 = [c * n0p for c in pt0]
            elem3 = [c * nnp for c in ptm]
            rkv.append([a - b - c for a, b, c in zip(ptk, elem2, elem3)])
        # Compute Rv - Eqn. 9.67
        rv = [[0.0 for _ in range(dim)] for _ in range(num_cpts_v - 2)]
        for j in range(1, num_cpts_v - 1):
            rv_tmp = []
            for idx, pt in enumerate(rkv):
                rv_tmp.append([p * helpers.basis_function_one(degree_v, kv_v, j, vl[idx + 1]) for p in pt])
            for d in range(dim):
                for idx in range(len(rv_tmp)):
                    rv[j - 1][d] += rv_tmp[idx][d]
        # Get intermediate control points
        for d in range(dim):
            b = [pt[d] for pt in rv]
            y = linalg.forward_substitution(matrix_ntnvl, b)
            x = linalg.backward_substitution(matrix_ntnvu, y)
            for j in range(1, num_cpts_v - 1):
                ctrlpts[i + (num_cpts_u * j)][d] = x[j - 1]

    # Generate B-spline surface
    surf = BSpline.Surface()
    surf.degree.u = degree_u
    surf.degree.v = degree_v
    surf.set_ctrlpts(ctrlpts, num_cpts_u, num_cpts_v)
    surf.knotvector.u = kv_u
    surf.knotvector.v = kv_v

    return surf
