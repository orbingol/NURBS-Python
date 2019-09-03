"""
.. module:: _evaluators
    :platform: Unix, Windows
    :synopsis: Helper functions for evaluators module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""


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
