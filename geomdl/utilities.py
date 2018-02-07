"""
.. module:: utilities
    :platform: Unix, Windows
    :synopsis: Contains common utility functions and some helper functions for data conversion, integration, etc.

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import math


# Reads 2D control points file, flips it and saves it
def flip_ctrlpts(file_in='', file_out='ctrlpts_flip.txt'):
    """ Flips u and v directions of a 2D control points file and saves flipped coordinates to a file.

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    :return: None
    """
    # Initialize some variables
    current_ctrlpts = []
    size_u = 0
    size_v = 0

    # Read file
    try:
        with open(file_in, 'r') as fp:
            for line in fp:
                line = line.strip()
                control_point_row = line.split(';')
                size_v = 0
                ctrlpts_v = []
                for cpr in control_point_row:
                    cpt = cpr.split(',')
                    pt_temp = []
                    for pt in cpt:
                        pt_temp.append(float(pt.strip()))
                    ctrlpts_v.append(pt_temp)
                    size_v += 1
                current_ctrlpts.append(ctrlpts_v)
                size_u += 1
    except IOError:
        raise ValueError("File " + str(file_in) + " cannot be opened for reading")

    # Flip control points array
    # new_ctrlpts = [[None for y in range(size_u)] for x in range(size_v)]
    new_ctrlpts = [[None for _ in range(size_u)] for _ in range(size_v)]
    for i in range(size_v):
        for j in range(size_u):
            new_ctrlpts[i][j] = current_ctrlpts[j][i]

    # Save new control points
    try:
        with open(file_out, 'w') as fp:
            fp.truncate()
            for i in range(size_v):
                line = ""
                for j in range(size_u):
                    for idx, coord in enumerate(new_ctrlpts[i][j]):
                        if idx:  # Add comma if we are not on the first element
                            line += ","
                        line += str(coord)
                    if j != size_u - 1:
                        line += ";"
                    else:
                        line += "\n"
                fp.write(line)
    except IOError:
        raise ValueError("File " + str(file_out) + " cannot be opened for writing.")


# Generates weighted control points from unweighted ones
def generate_ctrlptsw(file_in='', file_out='ctrlptsw.txt'):
    """ Generates weighted control points from unweighted ones.

    This function takes in a 2D control points file whose coordinates are organized like (x, y, z, w),
    converts into (x*w, y*w, z*w, w), and saves it to a file.
    Therefore, it could be a direct input of the NURBS.Surface class.

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    :return: None
    """
    # Initialize some variables
    ctrlpts = []
    size_u = 0
    size_v = 0

    # Read file
    try:
        with open(file_in, 'r') as fp:
            for line in fp:
                line = line.strip()
                control_point_row = line.split(';')
                size_v = 0
                ctrlpts_v = []
                for cpr in control_point_row:
                    cpt = cpr.split(',')
                    pt_temp = []
                    for pt in cpt:
                        pt_temp.append(float(pt.strip()))
                    ctrlpts_v.append(pt_temp)
                    size_v += 1
                ctrlpts.append(ctrlpts_v)
                size_u += 1
    except IOError:
        raise ValueError("File " + str(file_in) + " cannot be opened for reading")

    # Multiply control points by weight
    new_ctrlpts = []
    for row in ctrlpts:
        ctrlptsw_v = []
        for col in row:
            temp = [float(col[0] * col[3]),
                    float(col[1] * col[3]),
                    float(col[2] * col[3]),
                    col[3]]
            ctrlptsw_v.append(temp)
        new_ctrlpts.append(ctrlptsw_v)

    # Save new control points
    try:
        with open(file_out, 'w') as fp:
            fp.truncate()
            for i in range(size_u):
                line = ""
                for j in range(size_v):
                    for idx, coord in enumerate(new_ctrlpts[i][j]):
                        if idx:  # Add comma if we are not on the first element
                            line += ","
                        line += str(coord)
                    if j != size_u - 1:
                        line += ";"
                    else:
                        line += "\n"
                fp.write(line)
    except IOError:
        raise ValueError("File " + str(file_out) + " cannot be opened for writing")


# Generates unweighted control points from weighted ones
def generate_ctrlpts_weights(file_in='', file_out='ctrlpts_weights.txt'):
    """ Generates unweighted control points from weighted ones.

    This function takes in a 2D control points file whose coordinates are organized like (x*w, y*w, z*w, w),
    converts into (x, y, z, w), and saves it to a file.

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    :return: None
    """
    # Initialize some variables
    ctrlpts = []
    size_u = 0
    size_v = 0

    # Read file
    try:
        with open(file_in, 'r') as fp:
            for line in fp:
                line = line.strip()
                control_point_row = line.split(';')
                size_v = 0
                ctrlpts_v = []
                for cpr in control_point_row:
                    cpt = cpr.split(',')
                    pt_temp = []
                    for pt in cpt:
                        pt_temp.append(float(pt.strip()))
                    ctrlpts_v.append(pt_temp)
                    size_v += 1
                ctrlpts.append(ctrlpts_v)
                size_u += 1
    except IOError:
        raise ValueError("File " + str(file_in) + " cannot be opened for reading")

    # Multiply control points by weight
    new_ctrlpts = []
    for row in ctrlpts:
        ctrlptsw_v = []
        for col in row:
            temp = [float(col[0] / col[3]),
                    float(col[1] / col[3]),
                    float(col[2] / col[3]),
                    col[3]]
            ctrlptsw_v.append(temp)
        new_ctrlpts.append(ctrlptsw_v)

    # Save new control points
    try:
        with open(file_out, 'w') as fp:
            fp.truncate()
            for i in range(size_u):
                line = ""
                for j in range(size_v):
                    for idx, coord in enumerate(new_ctrlpts[i][j]):
                        if idx:  # Add comma if we are not on the first element
                            line += ","
                        line += str(coord)
                    if j != size_u - 1:
                        line += ";"
                    else:
                        line += "\n"
                fp.write(line)
    except IOError:
        raise ValueError("File " + str(file_out) + " cannot be opened for writing")


# Changes linearly ordered list of points into a zig-zag shape
def make_zigzag(points, row_size):
    """ Changes linearly ordered list of points into a zig-zag shape.

    This function is designed to create input for the visualization software. It orders the points to draw a zig-zag
    shape which enables generating properly connected lines without any scanlines. Please see the below sketch on the
    functionality of the ``row_size`` parameter::

             row size
        <-=============->
        ------->>-------|
        |------<<-------|
        |------>>-------|
        -------<<-------|

    Please note that this function does not detect the ordering of the input points to detect the input points have
    already been processed to generate a zig-zag shape.

    :param points: list of points to be ordered
    :type points: list
    :param row_size: number of elements in a row which the zig-zag generated
    :param row_size: int
    :return: re-ordered points
    :rtype: list
    """
    new_points = []
    points_size = len(points)
    forward = True
    idx = 0
    rev_idx = -1
    while idx < points_size:
        if forward:
            new_points.append(points[idx])
        else:
            new_points.append(points[rev_idx])
            rev_idx -= 1
        idx += 1
        if idx % row_size == 0:
            forward = False if forward else True
            rev_idx = idx + row_size - 1

    return new_points


def make_quad(points, row_size, col_size):
    """ Generates a quad mesh from linearly ordered list of points.

    :param points: list of points to be ordered
    :type points: list, tuple
    :param row_size: number of elements in a row
    :param row_size: int
    :param col_size: number of elements in a column
    :param col_size: int
    :return: re-ordered points
    :rtype: list
    """
    # Start with generating a zig-zag shape in row direction and then take its reverse
    new_points = make_zigzag(points, row_size)
    new_points.reverse()

    # Start generating a zig-zag shape in col direction
    forward = True
    for row in range(0, row_size):
        temp = []
        for col in range(0, col_size):
            temp.append(points[row + (col * row_size)])
        if forward:
            forward = False
        else:
            forward = True
            temp.reverse()
        new_points += temp

    return new_points


def make_triangle(points, row_size, col_size):
    """ Generates a triangular mesh from  linearly ordered list of points.

    :param points: list of points to be ordered
    :type points: list, tuple
    :param row_size: number of elements in a row
    :param row_size: int
    :param col_size: number of elements in a column
    :param col_size: int
    :return: re-ordered points
    :rtype: list
    """
    points2d = []
    for i in range(0, col_size):
        row_list = []
        for j in range(0, row_size):
            row_list.append(points[j + (i * row_size)])
        points2d.append(row_list)

    forward = True
    triangles = []
    for col_idx in range(0, col_size - 1):
        row_idx = 0
        left_half = True
        tri_list = []
        while row_idx < row_size - 1:
            if left_half:
                tri_list.append(points2d[col_idx + 1][row_idx])
                tri_list.append(points2d[col_idx][row_idx])
                tri_list.append(points2d[col_idx][row_idx + 1])
                tri_list.append(points2d[col_idx + 1][row_idx])
                left_half = False
            else:
                tri_list.append(points2d[col_idx][row_idx + 1])
                tri_list.append(points2d[col_idx + 1][row_idx + 1])
                tri_list.append(points2d[col_idx + 1][row_idx])
                left_half = True
                row_idx += 1
        if forward:
            forward = False
        else:
            forward = True
            tri_list.reverse()
        triangles += tri_list

    return triangles


# A float range function, implementation of https://stackoverflow.com/a/47877721
def frange(start, stop, step=1.0, decimals=7):
    """ Implementation of Python's ``range()`` function which works with floats.

    Reference to this implementation: https://stackoverflow.com/a/47877721

    :param start: start value
    :type start: float
    :param stop: end value
    :type stop: float
    :param step: increment
    :type step: float
    :param decimals: rounding number
    :type decimals: int
    :return: float
    :rtype: generator
    """
    # Originally range((int(start / step), int(stop / step))) but intentionally added "+ 1" to the end to get
    # the last element when step is too small. Just to make it clear, frange function is here because we don't want
    # to use numpy or its alternatives
    for i in range(int(start / step), int(stop / step) + 1):
        yield float(("%0." + str(decimals) + "f") % (i * step))


# Normalizes knot vector (internal functionality)
def normalize_knot_vector(knot_vector=()):
    """ Normalizes the input knot vector between 0 and 1.

    :param knot_vector: input knot vector
    :type knot_vector: tuple
    :return: normalized knot vector
    :rtype: list
    """
    if not knot_vector:
        return knot_vector

    first_knot = float(knot_vector[0])
    last_knot = float(knot_vector[-1])

    knot_vector_out = []
    for kv in knot_vector:
        knot_vector_out.append((float(kv) - first_knot) / (last_knot - first_knot))

    return knot_vector_out


# Generates a uniform knot vector using the given degree and the number of control points
def generate_knot_vector(degree=0, control_points_size=0):
    """ Generates a uniformly-spaced knot vector using the degree and the number of control points.

    This function can also generate knot vectors for Bezier curves and surfaces.

    :param degree: degree of the knot vector direction
    :type degree: integer
    :param control_points_size: number of control points on that direction
    :type control_points_size: integer
    :return: knot vector
    :rtype: list
    """
    if degree == 0 or control_points_size == 0:
        raise ValueError("Input values should be different than zero.")

    # Min and max knot vector values
    knot_min = 0.0
    knot_max = 1.0

    # Equation to use: m = n + p + 1
    # p: degree, n+1: number of control points; m+1: number of knots
    m = degree + control_points_size + 1

    # Initialize return value and counter
    knot_vector = []
    i = 0

    # First degree+1 knots are "knot_min"
    while i < degree:
        knot_vector.append(knot_min)
        i += 1

    # Calculate a uniform interval for middle knots
    num_segments = (m - (degree + 1) * 2) + 1  # number of segments in the middle
    spacing = (knot_max - knot_min) / num_segments  # spacing between the knots (uniform)

    # Middle knots
    for mid_knot in frange(0, 1, spacing, decimals=4):
        knot_vector.append(mid_knot)
        i += 1

    # Last degree+1 knots are "knot_max"
    while i < m:
        knot_vector.append(knot_max)
        i += 1

    # Return auto-generated knot vector
    return knot_vector


# Checks if the input knot vector follows the mathematical rules
def check_knot_vector(degree=0, knot_vector=(), control_points_size=0, tol=0.001):
    """ Checks if the input knot vector follows the mathematical rules. """
    if not knot_vector:
        raise ValueError("Input knot vector cannot be empty")

    # Check the formula; m = p + n + 1
    if len(knot_vector) is not degree + control_points_size + 1:
        return False

    # Set up a return value
    ret_val = True

    # A proper knot vector should have a knot vector starting with degree + 1 zeros
    count = 0
    start_knot = 0.0
    for knot in knot_vector:
        if count > degree:
            break
        if not abs(start_knot - knot) < tol:
            ret_val = False
            break
        count += 1

    # A proper knot vector should have a knot vector ending with degree + 1 ones
    if ret_val:
        knot_vector.reverse()
        count = 0
        end_knot = 1.0
        for knot in knot_vector:
            if count > degree:
                break
            if not abs(end_knot - knot) < tol:
                ret_val = False
                break
            count += 1

        knot_vector.reverse()

    # Check ascending order
    if ret_val:
        prev_knot = knot_vector[0]
        for knot in knot_vector:
            if prev_knot > knot:
                ret_val = False
                break
            prev_knot = knot

    return ret_val


# FindSpan (Algorithm A2.1) implementation using linear search
def find_span(degree=0, knot_vector=(), control_points_size=0, knot=0, tol=0.001):
    """ FindSpan (Algorithm A2.1) implementation using linear search.

    .. note:: This is **NOT** direct implementation of Algorithm A2.1.
    """
    span = 0  # Knot span index starts from zero
    while span < control_points_size and knot_vector[span] <= knot:
        span += 1

    return span - 1


# FindSpan (Algorithm A2.1) implementation using binary search
def find_span2(degree=0, knot_vector=(), control_points_size=0, knot=0, tol=0.001):
    """ Algorithm A2.1 of The NURBS Book by Piegl & Tiller.

    .. note:: This algorithm uses binary search to find the knot span.

    The NURBS Book states that the knot span index always starts from zero, i.e. for a knot vector [0, 0, 1, 1];
    if FindSpan returns 1, then the knot is between the internal [0, 1).
    """
    # Number of knots; m + 1
    # Number of control points; n + 1
    # n = m - p - 1; where p = degree
    # m = len(knot_vector) - 1
    # n = m - degree - 1
    n = control_points_size - 1
    if abs(knot_vector[n + 1] - knot) <= tol:
        return n

    low = degree
    high = n + 1
    mid = int((low + high) / 2)

    while (knot < knot_vector[mid]) or (knot >= knot_vector[mid + 1]):
        if knot < knot_vector[mid]:
            high = mid
        else:
            low = mid
        mid = int((low + high) / 2)

    return mid


# Finds knot multiplicity (internal functionality)
def find_multiplicity(knot=-1, knot_vector=(), tol=0.001):
    """ Finds knot multiplicity."""
    # Find and return the multiplicity of the input knot in the given knot vector
    mult = 0  # initial multiplicity
    # Loop through the knot vector
    for kv in knot_vector:
        # Float equality should be checked w.r.t a tolerance value
        if abs(knot - kv) <= tol:
            mult += 1
    return mult


# Algorithm A2.2 (internal functionality)
def basis_functions(degree=0, knot_vector=(), span=0, knot=0):
    """ Algorithm A2.2 of The NURBS Book by Piegl & Tiller."""
    left = [None for _ in range(degree + 1)]
    right = [None for _ in range(degree + 1)]
    N = [None for _ in range(degree + 1)]

    # N[0] = 1.0 by definition
    N[0] = 1.0

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


# Algorithm A2.2 - modified (internal functionality)
def basis_functions_all(degree=0, knot_vector=(), span=0, knot=0):
    """ A modified version of Algorithm A2.2 of The NURBS Book by Piegl & Tiller."""
    # N = [[None for x in range(degree + 1)] for y in range(degree + 1)]
    N = [[None for _ in range(degree + 1)] for _ in range(degree + 1)]
    for i in range(0, degree + 1):
        bfuns = basis_functions(i, knot_vector, span, knot)
        for j in range(0, i + 1):
            N[j][i] = bfuns[j]
    return N


# Algorithm A2.3 (internal functionality)
def basis_functions_ders(degree=0, knot_vector=(), span=0, knot=0, order=0):
    """ Algorithm A2.3 of The NURBS Book by Piegl & Tiller."""
    # Initialize variables for easy access
    left = [None for _ in range(degree + 1)]
    right = [None for _ in range(degree + 1)]
    # ndu = [[None for x in range(degree + 1)] for y in range(degree + 1)]
    ndu = [[None for _ in range(degree + 1)] for _ in range(degree + 1)]

    # N[0][0] = 1.0 by definition
    ndu[0][0] = 1.0

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
    # ders = [[None for x in range(degree + 1)] for y in range((min(degree, order) + 1))]
    ders = [[None for _ in range(degree + 1)] for _ in range((min(degree, order) + 1))]
    for j in range(0, degree + 1):
        ders[0][j] = ndu[j][degree]

    # Start calculating derivatives
    # a = [[None for x in range(degree + 1)] for y in range(2)]
    a = [[None for _ in range(degree + 1)] for _ in range(2)]
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


# Checks if the input (u, v) values are valid (internal functionality)
def check_uv(u=None, v=None):
    """ Checks if the input knot values (i.e. parameters) are defined between 0 and 1."""
    # Check u value
    if u is not None:
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')
    # Check v value, if necessary
    if v is not None:
        if v < 0.0 or v > 1.0:
            raise ValueError('"v" value should be between 0 and 1.')


# Generates a vector from 2 input 3D points (as lists with length 3)
def vector_generate(start_pt=(), end_pt=(), normalize=False):
    """ Generates a vector from 2 input 3D points

    The input points must be a list with length 3.

    :param start_pt: starting point of the vector
    :type start_pt: list, tuple
    :param end_pt: ending point of the vector
    :type end_pt: list, tuple
    :param normalize: if True, the generated vector is normalized
    :type normalize: bool
    :return: a vector from start_pt to end_pt
    :rtype: list
    """
    if len(start_pt) != 3 and len(end_pt) != 3:
        raise ValueError("Input points must be in 3 dimensions")
    ret_vec = [start_pt[0] - end_pt[0], start_pt[1] - end_pt[1], start_pt[2] - end_pt[2]]
    if normalize:
        ret_vec = normalize(ret_vec)
    return ret_vec


# Computes vector cross-product
def vector_cross(vector1=(), vector2=()):
    """ Computes the cross-product of the input vectors.

    :param vector1: input vector 1
    :type vector1: tuple
    :param vector2: input vector 2
    :type vector2: tuple
    :return: result of the cross product
    :rtype: list
    """
    if not vector1 or not vector2:
        raise ValueError("Input arguments are empty.")

    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Input tuples should contain 3 elements representing (x,y,z).")

    # Compute cross-product
    vector_out = [(vector1[1] * vector2[2]) - (vector1[2] * vector2[1]),
                  (vector1[2] * vector2[0]) - (vector1[0] * vector2[2]),
                  (vector1[0] * vector2[1]) - (vector1[1] * vector2[0])]

    # Return the cross product of the input vectors
    return vector_out


# Computes vector dot-product
def vector_dot(vector1=(), vector2=()):
    """ Computes the dot-product of the input vectors.

    :param vector1: input vector 1
    :type vector1: tuple
    :param vector2: input vector 2
    :type vector2: tuple
    :return: result of the dot product
    :rtype: list
    """
    if not vector1 or not vector2:
        raise ValueError("Input arguments are empty.")

    # Compute dot-product
    value_out = (vector1[0] * vector2[0]) + (vector1[1] * vector2[1])
    if len(vector1) == 3 and len(vector2) == 3:
        value_out += (vector1[2] * vector2[2])

    # Return the dot product of the input vectors
    return value_out


# Normalizes the input vector
def vector_normalize(vector_in=()):
    """ Generates a unit vector from the input.

    :param vector_in: vector to be normalized
    :type vector_in: tuple
    :return: the normalized vector (i.e. the unit vector)
    :rtype: list
    """
    if not vector_in:
        raise ValueError("Input argument is empty.")

    sq_sum = math.pow(vector_in[0], 2) + math.pow(vector_in[1], 2)
    if len(vector_in) == 3:
        sq_sum += math.pow(vector_in[2], 2)

    # Calculate magnitude of the vector
    magnitude = math.sqrt(sq_sum)

    if magnitude != 0:
        # Normalize the vector
        if len(vector_in) == 3:
            vector_out = [vector_in[0] / magnitude,
                          vector_in[1] / magnitude,
                          vector_in[2] / magnitude]
        else:
            vector_out = [vector_in[0] / magnitude,
                          vector_in[1] / magnitude]
        # Return the normalized vector
        return vector_out
    else:
        raise ValueError("The magnitude of the vector is zero.")


# Translates the input points using the given vector
def point_translate(point_in=(), vector_in=()):
    """ Translates the input points using the given vector.

    :param point_in: input point (as a list/tuple of 3 elements)
    :type point_in: tuple
    :param vector_in: input vector (as a list/tuple of 3 elements)
    :type vector_in: tuple
    :return: translated point
    :rtype: list
    """
    if not point_in or not vector_in:
        raise ValueError("Input arguments are empty.")
    if len(point_in) != 3 or len(vector_in) != 3:
        raise ValueError("Input arguments must be a list/tuple of 3 elements.")

    # Translate the point using the input vector
    point_out = [coord + comp for coord, comp in zip(point_in, vector_in)]

    return point_out


# Computes the binomial coefficient
def binomial_coefficient(k, i):
    """ Computes the binomial coefficient (denoted by *k choose i*).

    Please see the following website for details: http://mathworld.wolfram.com/BinomialCoefficient.html

    :param k: size of the set of distinct elements
    :type k: int
    :param i: size of the subsets
    :type i: int
    :return: combination of *k* and *i*
    :rtype: float
    """
    k_fact = math.factorial(k)
    i_fact = math.factorial(i)
    k_i_fact = math.factorial(k - i)
    return float(k_fact / (k_i_fact * i_fact))
