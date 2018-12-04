"""
.. module:: interpolate
    :platform: Unix, Windows
    :synopsis: Provides global interpolation functions for parametric shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import utilities


def interpolate_curve(points, degree, **kwargs):
    # Keyword arguments
    clamped = kwargs.get('clamped', True)

    # Number of control points
    num_cpts = len(points)

    # Number of knots
    m = num_cpts + degree + 1

    # Number of middle knots
    n = degree + 1 if clamped else 1
    m_compute = m - (n * 2)

    # Start knot vector
    kv = [0.0 for _ in range(n)]

    # Compute middle knots if required
    if m_compute > 0:
        # Chord length parametrization
        uk = [0.0 for _ in range(num_cpts + 1)]
        uk[-1] = 1.0
        for i in range(1, num_cpts):
            uk[i] = utilities.point_distance(points[i], points[i - 1])
        # Find total chord length
        d = sum(uk[1:-1])
        # Divide individual chord lengths by the total chord length
        u_bar = [0.0 for _ in range(num_cpts)]
        for i in range(num_cpts):
            u_bar[i] = sum(uk[0:i+1]) / d
        # Use averaging to compute middle knots in the knot vector
        for i in range(m_compute):
            temp_kv = (1.0 / degree) * sum([u_bar[j] for j in range(i + 1, i + degree + 1)])
            kv.append(temp_kv)

    # End knot vector
    kv += [1.0 for _ in range(n)]

    # Set up coefficient matrix
    pass
