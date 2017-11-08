"""
.. module:: utilities
    :platform: Unix, Windows
    :synopsis: Contains common utility functions and some helper functions for data conversion, integration, etc.

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import decimal
import math
import warnings


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
        raise ValueError("File " + str(file_in) + " cannot be opened for reading.")

    # Flip control points array
    new_ctrlpts = [[None for y in range(size_u)] for x in range(size_v)]
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
        raise ValueError("File " + str(file_in) + " cannot be opened for reading.")

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
        raise ValueError("File " + str(file_out) + " cannot be opened for writing.")


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
        raise ValueError("File " + str(file_in) + " cannot be opened for reading.")

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
        raise ValueError("File " + str(file_out) + " cannot be opened for writing.")


# A float range function, implementation of http://stackoverflow.com/a/7267280
def frange(x, y, step):
    """ An implementation of a ``range()`` function which works with decimals.

    Reference to this implementation: http://stackoverflow.com/a/7267280

    :param x: start value
    :type x: integer or float
    :param y: end value
    :type y: integer or float
    :param step: increment
    :type step: integer or float
    :return: float
    :rtype: generator
    """
    step_str = str(step)
    while x <= y:
        yield float(x)
        x += decimal.Decimal(step_str)


# Normalizes knot vector (internal functionality)
def normalize_knot_vector(knot_vector=()):
    """ Normalizes the input knot vector between 0 and 1.

    :param knot_vector: input knot vector
    :type knot_vector: tuple
    :return: normalized knot vector
    :rtype: list
    """
    if len(knot_vector) == 0:
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
    while i < degree+1:
        knot_vector.append(knot_min)
        i += 1

    # Calculate a uniform interval for middle knots
    num_segments = (m - (degree+1)*2)+1  # number of segments in the middle
    spacing = (knot_max - knot_min) / num_segments  # spacing between the knots (uniform)
    mid_knot = knot_min + spacing  # first middle knot
    # Middle knots
    while i < m-(degree+1):
        knot_vector.append(mid_knot)
        mid_knot += spacing
        i += 1

    # Last degree+1 knots are "knot_max"
    while i < m:
        knot_vector.append(knot_max)
        i += 1

    # Return auto-generated knot vector
    return knot_vector


# Algorithm A2.1 (internal functionality)
def find_span(degree=0, knot_vector=(), control_points_size=0, knot=0, tol=0.001):
    """ Algorithm A2.1 of The NURBS Book by Piegl & Tiller."""
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
    left = [None for x in range(degree+1)]
    right = [None for x in range(degree+1)]
    N = [None for x in range(degree + 1)]

    # N[0] = 1.0 by definition
    N[0] = 1.0

    for j in range(1, degree+1):
        left[j] = knot - knot_vector[span + 1 - j]
        right[j] = knot_vector[span + j] - knot
        saved = 0.0
        for r in range(0, j):
            temp = N[r] / (right[r+1] + left[j-r])
            N[r] = saved + right[r+1] * temp
            saved = left[j-r] * temp
        N[j] = saved

    return N


# Algorithm A2.2 - modified (internal functionality)
def basis_functions_all(degree=0, knot_vector=(), span=0, knot=0):
    """ A modified version of Algorithm A2.2 of The NURBS Book by Piegl & Tiller."""
    N = [[None for x in range(degree+1)] for y in range(degree+1)]
    for i in range(0, degree+1):
        bfuns = basis_functions(i, knot_vector, span, knot)
        for j in range(0, i+1):
            N[j][i] = bfuns[j]
    return N


# Algorithm A2.3 (internal functionality)
def basis_functions_ders(degree=0, knot_vector=(), span=0, knot=0, order=0):
    """ Algorithm A2.3 of The NURBS Book by Piegl & Tiller."""
    # Initialize variables for easy access
    left = [None for x in range(degree+1)]
    right = [None for x in range(degree+1)]
    ndu = [[None for x in range(degree+1)] for y in range(degree+1)]

    # N[0][0] = 1.0 by definition
    ndu[0][0] = 1.0

    for j in range(1, degree+1):
        left[j] = knot - knot_vector[span + 1 - j]
        right[j] = knot_vector[span + j] - knot
        saved = 0.0
        r = 0
        for r in range(r, j):
            # Lower triangle
            ndu[j][r] = right[r+1] + left[j-r]
            temp = ndu[r][j-1] / ndu[j][r]
            # Upper triangle
            ndu[r][j] = saved + (right[r+1] * temp)
            saved = left[j-r] * temp
        ndu[j][j] = saved

    # Load the basis functions
    ders = [[None for x in range(degree+1)] for y in range((min(degree, order)+1))]
    for j in range(0, degree+1):
        ders[0][j] = ndu[j][degree]

    # Start calculating derivatives
    a = [[None for x in range(degree+1)] for y in range(2)]
    # Loop over function index
    for r in range(0, degree+1):
        # Alternate rows in array a
        s1 = 0
        s2 = 1
        a[0][0] = 1.0
        # Loop to compute k-th derivative
        for k in range(1, order+1):
            d = 0.0
            rk = r - k
            pk = degree - k
            if r >= k:
                a[s2][0] = a[s1][0] / ndu[pk+1][rk]
                d = a[s2][0] * ndu[rk][pk]
            if rk >= -1:
                j1 = 1
            else:
                j1 = -rk
            if (r - 1) <= pk:
                j2 = k - 1
            else:
                j2 = degree - r
            for j in range(j1, j2+1):
                a[s2][j] = (a[s1][j] - a[s1][j-1]) / ndu[pk+1][rk+j]
                d += (a[s2][j] * ndu[rk+j][pk])
            if r <= pk:
                a[s2][k] = -a[s1][k-1] / ndu[pk+1][r]
                d += (a[s2][k] * ndu[r][pk])
            ders[k][r] = d

            # Switch rows
            j = s1
            s1 = s2
            s2 = j

    # Multiply through by the the correct factors
    r = float(degree)
    for k in range(1, order+1):
        for j in range(0, degree+1):
            ders[k][j] *= r
        r *= (degree - k)

    # Return the basis function derivatives list
    return ders


# Checks if the input (u, v) values are valid (internal functionality)
def check_uv(u=-1, v=None, test_normal=False, delta=0.1):
    """ Checks if the input knot values (i.e. parameters) are defined between 0 and 1."""
    # Check u value
    if u < 0.0 or u > 1.0:
        raise ValueError('"u" value should be between 0 and 1.')
    # Check v value, if necessary
    if v is not None:
        if v < 0.0 or v > 1.0:
            raise ValueError('"v" value should be between 0 and 1.')

        # Only test normal if v is defined
        if test_normal:
            # Check if we are on any edge of the surface
            if u + delta > 1.0 or u + delta < 0.0 or v + delta > 1.0 or v + delta < 0.0:
                raise ValueError("Cannot evaluate normal on an edge.")

    # Show a warning message if v = None and test_normal = True
    if v is None and test_normal:
        warnings.warn("Cannot test normal when v is not set.")


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


# Computes the binomial coefficient
def binomial_coefficient(k, i):
    """ Computes the binomial coefficient (k choose i).

    :param k: a set of k elements
    :type k: int
    :param i: subset of elements with the size i
    :type i: int
    :return:
    """
    k_fact = math.factorial(k)
    i_fact = math.factorial(i)
    k_i_fact = math.factorial(k-i)
    return k_fact / (k_i_fact * i_fact)
