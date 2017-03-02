"""
    NURBS Python Package
    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2017
"""

def normalize_knotvector(knotvector=()):
    if len(knotvector) == 0:
        return knotvector

    first_knot = float(knotvector[0])
    last_knot = float(knotvector[-1])

    knotvector_out = []
    for kv in knotvector:
        knotvector_out.append((float(kv) - first_knot) / (last_knot - first_knot))

    return knotvector_out


# Algorithm A2.1
def find_span(degree=0, knotvector=(), knot=0):
    # Number of knots; m + 1
    # Number of basis functions, n +1
    # n = m - p - 1; where p = degree
    m = len(knotvector) - 1
    n = m - degree - 1
    if knotvector[n + 1] == knot:
        return n

    low = degree
    high = n + 1
    mid = (low + high) / 2

    while (knot < knotvector[mid]) or (knot >= knotvector[mid + 1]):
        if knot < knotvector[mid]:
            high = mid
        else:
            low = mid
        mid = (low + high) / 2

    return mid


# Algorithm A2.2
def basis_functions(degree=0, knotvector=(), span=0, knot=0):
    left = [0.0] * (degree+1)
    right = [0.0] * (degree+1)

    # N[0] = 1.0 by definition
    bfuncs_out = [1.0]

    j = 1
    while j <= degree:
        left[j] = knot - knotvector[span+1-j]
        right[j] = knotvector[span+j] - knot
        saved = 0.0
        r = 0
        while r < j:
            temp = bfuncs_out[r] / (right[r+1] + left[j-r])
            bfuncs_out[r] = saved + right[r+1] * temp
            saved = left[j-r] * temp
            r += 1
        bfuncs_out.append(saved)
        j += 1

    return bfuncs_out


def check_uv(u=-1, v=-1, delta=0.1, test_normal=False):
    pass



