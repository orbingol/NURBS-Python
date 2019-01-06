"""
.. module:: _evaluators
    :platform: Unix, Windows
    :synopsis: Helper functions for B-Spline and NURBS algorithms

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from copy import deepcopy


# Initialize an empty __all__ for controlling imports
__all__ = []


def compute_knot_vector(knotvector, r, param, span):
    kv_new = [0.0 for _ in range(len(knotvector) + r)]
    for i in range(0, span + 1):
        kv_new[i] = knotvector[i]
    for i in range(1, r + 1):
        kv_new[span + i] = param
    for i in range(span + 1, len(knotvector)):
        kv_new[i + r] = knotvector[i]
    return kv_new


def insert_knot_u(span_func, **kwargs):
    param = kwargs.get('parameter')
    r = kwargs.get('r')
    s = kwargs.get('s')
    degree = kwargs.get('degree')
    knotvector = kwargs.get('knotvector')
    ctrlpts = kwargs.get('ctrlpts')
    ctrlpts_size = kwargs.get('ctrlpts_size')

    # Algorithm A5.3
    span = span_func(degree, knotvector, ctrlpts_size[0], param)

    # Compute new know vector
    UQ = compute_knot_vector(knotvector, r, param, span)

    # Initialize new control points array (control points can be weighted or not)
    Q = [[] for _ in range((ctrlpts_size[0] + r) * ctrlpts_size[1])]
    # Initialize a local array of length p + 1
    R = [[] for _ in range(degree + 1)]

    # Update control points
    for row in range(0, ctrlpts_size[1]):
        for i in range(0, span - degree + 1):
            Q[row + (ctrlpts_size[1] * i)] = ctrlpts[row + (ctrlpts_size[1] * i)]
        for i in range(span - s, ctrlpts_size[0]):
            Q[row + (ctrlpts_size[1] * (i + r))] = ctrlpts[row + (ctrlpts_size[1] * i)]
        # Load auxiliary control points
        for i in range(0, degree - s + 1):
            R[i] = deepcopy(ctrlpts[row + (ctrlpts_size[1] * (span - degree + i))])
        # Insert the knot r times
        for j in range(1, r + 1):
            L = span - degree + j
            for i in range(0, degree - j - s + 1):
                alpha = (param - knotvector[L + i]) / (knotvector[i + span + 1] - knotvector[L + i])
                R[i][:] = [alpha * elem2 + (1.0 - alpha) * elem1 for elem1, elem2 in zip(R[i], R[i + 1])]
            Q[row + (ctrlpts_size[1] * L)] = deepcopy(R[0])
            Q[row + (ctrlpts_size[1] * (span + r - j - s))] = deepcopy(R[degree - j - s])
        # Load the remaining control points
        L = span - degree + r
        for i in range(L + 1, span - s):
            Q[row + (ctrlpts_size[1] * i)] = deepcopy(R[i - L])

    return UQ, Q


def insert_knot_v(span_func, **kwargs):
    param = kwargs.get('parameter')
    r = kwargs.get('r')
    s = kwargs.get('s')
    degree = kwargs.get('degree')
    knotvector = kwargs.get('knotvector')
    ctrlpts = kwargs.get('ctrlpts')
    ctrlpts_size = kwargs.get('ctrlpts_size')

    # Algorithm A5.3
    span = span_func(degree, knotvector, ctrlpts_size[1], param)

    # Compute new know vector
    VQ = compute_knot_vector(knotvector, r, param, span)

    # Initialize new control points array (control points can be weighted or not)
    Q = [[] for _ in range(ctrlpts_size[0] * (ctrlpts_size[1] + r))]
    # Initialize a local array of length q + 1
    R = [[] for _ in range(degree + 1)]

    # Update control points
    for col in range(0, ctrlpts_size[0]):
        for i in range(0, span - degree + 1):
            Q[i + ((ctrlpts_size[1] + r) * col)] = ctrlpts[i + (ctrlpts_size[1] * col)]
        for i in range(span - s, ctrlpts_size[1]):
            Q[i + r + ((ctrlpts_size[1] + r) * col)] = ctrlpts[i + (ctrlpts_size[1] * col)]
        # Load auxiliary control points
        for i in range(0, degree - s + 1):
            R[i] = deepcopy(ctrlpts[span - degree + i + (ctrlpts_size[1] * col)])
        # Insert the knot r times
        for j in range(1, r + 1):
            L = span - degree + j
            for i in range(0, degree - j - s + 1):
                alpha = (param - knotvector[L + i]) / (knotvector[i + span + 1] - knotvector[L + i])
                R[i][:] = [alpha * elem2 + (1.0 - alpha) * elem1 for elem1, elem2 in zip(R[i], R[i + 1])]
            Q[L + ((ctrlpts_size[1] + r) * col)] = deepcopy(R[0])
            Q[span + r - j - s + ((ctrlpts_size[1] + r) * col)] = deepcopy(R[degree - j - s])
        # Load the remaining control points
        L = span - degree + r
        for i in range(L + 1, span - s):
            Q[i + ((ctrlpts_size[1] + r) * col)] = deepcopy(R[i - L])

    return VQ, Q
