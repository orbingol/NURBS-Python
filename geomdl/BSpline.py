"""
.. module:: BSpline
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation class for B-spline curves and surfaces

.. moduleauthor:: Onur Rauf Bingol

"""

import sys
import warnings
import geomdl.utilities as utils


class Curve(object):
    """ A data storage and evaluation class for 3D B-Spline curves.

    **Data Storage**

    :class:`.Curve` class implements Python properties using the ``@property`` decorator. The following properties are present in this class:

    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * curvepts

    The function :func:`.read_ctrlpts()` provides an easy way to read control points from a text file.
    Additional details for the text format can be found in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

    **Evaluation**

    The evaluation methods in the :class:`.Curve` class are:

    * :func:`.evaluate()`
    * :func:`.derivatives()`
    * :func:`.derivatives2()`
    * :func:`.tangent()`

    Please check the function reference for the details.

    .. note::

        If you update any of the data storage elements after the curve evaluation, the surface points stored in :py:attr:`~curvepts` property will be deleted automatically.
    """
    def __init__(self):
        self.__degree = 0
        self.__knot_vector = []
        self.__control_points = []
        self.__delta = 0.1
        self.__curve_points = []
        self.__dimension = 3  # 3D coordinates

    @property
    def order(self):
        """ Curve order

        Defined as order = degree + 1

        :getter: Gets the curve order
        :setter: Sets the curve order
        :type: integer
        """
        return self.__degree + 1

    @order.setter
    def order(self, value):
        self.degree = value - 1

    @property
    def degree(self):
        """ Curve degree

        :getter: Gets the curve degree
        :setter: Sets the curve degree
        :type: integer
        """
        return self.__degree

    @degree.setter
    def degree(self, value):
        # degree = 0, dots
        # degree = 1, polylines
        # degree = 2, quadratic curves
        # degree = 3, cubic curves
        if value < 0:
            raise ValueError("ERROR: Degree cannot be less than zero")
        # Clean up the curve points list, if necessary
        self.__reset_curve()
        # Set degree
        self.__degree = value

    @property
    def ctrlpts(self):
        """ Control points

        Control points of a :class:`.Curve` is stored as a list of (x, y, z) coordinates

        :getter: Gets the control points
        :setter: Sets the control points
        :type: list
        """
        ret_list = []
        for pt in self.__control_points:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        if len(value) < self.__degree + 1:
            raise ValueError("ERROR: Number of control points in u-direction should be at least degree + 1")

        # Clean up the curve and control points lists, if necessary
        self.__reset_curve()
        self.__reset_ctrlpts()

        for coord in value:
            if len(coord) < 0 or len(coord) > self.__dimension:
                raise ValueError("ERROR: Please input 3D coordinates")
            # Convert to list of floats
            coord_float = [float(c) for c in coord]
            self.__control_points.append(coord_float)

    @property
    def knotvector(self):
        """ Knot vector

        :getter: Gets the knot vector
        :setter: Sets the knot vector
        :type: list
        """
        return tuple(self.__knot_vector)

    @knotvector.setter
    def knotvector(self, value):
        # Clean up the surface points lists, if necessary
        self.__reset_curve()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        # Normalize and set the knot vector
        self.__knot_vector = utils.normalize_knot_vector(tuple(value_float))

    @property
    def delta(self):
        """ Curve evaluation delta

        .. note:: The delta value is 0.1 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self.__delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("ERROR: Curve evaluation delta should be between 0.0 and 1.0")
        # Clean up the curve points list, if necessary
        self.__reset_curve()
        # Set a new delta value
        self.__delta = float(value)

    @property
    def curvepts(self):
        """ Evaluated curve points

        .. note:: :func:`.evaluate` or :func:`.evaluate_rational` should be called first.

        :getter: (x, y) coordinates of the evaluated surface points
        :type: list
        """
        return self.__curve_points

    # Cleans up the control points
    def __reset_ctrlpts(self):
        if self.__control_points:
            # Delete control points
            del self.__control_points[:]

    # Cleans the evaluated curve points (private)
    def __reset_curve(self):
        if self.__curve_points:
            # Delete the curve points
            del self.__curve_points[:]

    # Checks whether the curve evaluation is possible or not (private)
    def __check_variables(self):
        works = True
        # Check degree values
        if self.__degree == 0:
            works = False
        if not self.__control_points:
            works = False
        if not self.__knot_vector:
            works = False
        if not works:
            raise ValueError("Some required parameters for curve evaluation are not set.")

    # Reads control points from a text file
    def read_ctrlpts_from_txt(self, filename=''):
        """ Loads control points from a text file.

        :param filename: input file name
        :type filename: string
        :return: True if control points are loaded correctly, False otherwise
        """
        # Clean up the curve and control points lists, if necessary
        self.__reset_curve()
        self.__reset_ctrlpts()

        # Initialize the return value
        ret_check = True

        # Try opening the file for reading
        try:
            with open(filename, 'r') as fp:

                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    coords = line.split(',')
                    # Remove extra whitespace and convert to float
                    pt = []
                    idx = 0
                    while idx < self.__dimension:
                        pt.append(float(coords[idx].strip()))
                        idx += 1
                    self.__control_points.append(pt)

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for reading.")
            ret_check = False

        return ret_check

    # Saves control points to a text file
    def save_ctrlpts_to_txt(self, filename=""):
        """ Saves control points to a text file.

        :param filename: output file name
        :type filename: string
        :return: True if control points are saved correctly, False otherwise
        """

        # Initialize the return value
        ret_check = True

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:

                # Loop through control points)
                for pt in self.__control_points:
                    line = ""
                    idx = 0
                    while idx < self.__dimension:
                        line += str(pt[idx])
                        if not idx == self.__dimension - 1:
                            line += ","
                        idx += 1
                    fp.write(line + "\n")

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for saving.")
            ret_check = False

        return ret_check

    # Prepares control points for exporting to external visualization software
    def __prepare_ctrlpts_for_exporting(self):
        """ Prepares control points for exporting to external visualization software, such as Paraview.

        :return: list of control points
        :rtype: list
        """
        return self.__control_points

    # Prepares and returns the CSV file header
    def __get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, coord z, scalar\n"

    # Saves control points to a text file
    def save_ctrlpts_to_csv(self, filename=""):
        """ Saves control points to a comma separated text file.

        :param filename: output file name
        :type filename: string
        :return: True if control points are saved correctly, False otherwise
        """

        # Initialize the return value
        ret_check = True

        coord_names = ["x", "y", "z"]

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:
                # Construct the header and write it to the file
                fp.write(self.__get_csv_header())

                # Loop through control points
                ctrlpts = self.__prepare_ctrlpts_for_exporting()
                for pt in ctrlpts:
                    line = ""
                    idx = 0
                    while idx < self.__dimension:
                        line += str(pt[idx])
                        if not idx == self.__dimension - 1:
                            line += ", "
                        idx += 1
                    fp.write(line + "\n")

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for saving.")
            ret_check = False

        return ret_check

    # Evaluates the B-Spline curve at the given parameter
    def curvept(self, u=-1, check_vars=True):
        """ Evaluates the B-Spline curve at the given u parameter

        :param u: parameter
        :type u: float
        :param check_vars: flag to disable variable checking (only for internal eval functions)
        :type check_vars: bool
        :return: evaluated curve point at the given knot value
        """
        if check_vars:
            # Check all parameters are set before the curve evaluation
            self.__check_variables()
            # Check u parameters are correct
            if u < 0.0 or u > 1.0:
                raise ValueError('"u" value should be between 0 and 1.')

        # Algorithm A3.1
        span = utils.find_span(self.__degree, tuple(self.__knot_vector), len(self.__control_points), u)
        basis = utils.basis_functions(self.__degree, tuple(self.__knot_vector), span, u)
        cpt = [0.0 for x in range(self.__dimension)]
        for i in range(0, self.__degree + 1):
            idx = 0
            while idx < self.__dimension:
                cpt[idx] += (basis[i] * self.__control_points[span - self.__degree + i][idx])
                idx += 1

        return cpt

    # Evaluates the B-Spline curve
    def evaluate(self):
        """ Evaluates the B-Spline curve.

        .. note:: The evaluated surface points are stored in :py:attr:`~curvepts`.

        :return: None
        """
        # Check all parameters are set before the curve evaluation
        self.__check_variables()
        # Clean up the curve points, if necessary
        self.__reset_curve()

        for u in utils.frange(0, 1, self.__delta):
            cpt = self.curvept(u, False)
            self.__curve_points.append(cpt)

    # Evaluates the curve derivative using "CurveDerivsAlg1" algorithm
    def derivatives2(self, u=-1, order=0):
        """ Evaluates n-th order curve derivatives at the given u using Algorithm A3.2

        :param u: knot value
        :type u: float
        :param order: derivative order
        :type order: integer
        :return: A list containing up to {order}-th derivative of the curve
        :rtype: list
        """
        # Check all parameters are set before the curve evaluation
        self.__check_variables()
        # Check u parameters are correct
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')

        # Algorithm A3.2: CurveDerivsAlg1
        du = min(self.__degree, order)

        CK = [[None for x in range(self.__dimension)] for y in range(order + 1)]
        for k in range(self.__degree + 1, order + 1):
            CK[k] = [0.0 for x in range(self.__dimension)]

        span = utils.find_span(self.__degree, tuple(self.__knot_vector), len(self.__control_points), u)
        bfunsders = utils.basis_functions_ders(self.__degree, tuple(self.__knot_vector), span, u, du)

        for k in range(0, du + 1):
            CK[k] = [0.0 for x in range(self.__dimension)]
            for j in range(0, self.__degree+1):
                idx = 0
                while idx < self.__dimension:
                    CK[k][idx] = (bfunsders[k][j] * self.__control_points[span - self.__degree + j][idx])
                    idx += 1

        # Return the derivatives
        return CK

    # Computes the control points of all derivative curves up to and including the d-th derivative
    def derivatives_ctrlpts(self, order=0, r1=0, r2=0):
        """ Computes the control points of all derivative curves up to and including the {degree}-th derivative.

        Output is PK[k][i], i-th control point of the k-th derivative curve where 0 <= k <= degree and r1 <= i <= r2-k

        :param order: derivative order
        :type order: integer
        :param r1: minimum span
        :type r1: integer
        :param r2: maximum span
        :type r2: integer
        :return: PK, a 2D list of control points
        :rtype: list
        """
        r = r2 - r1
        PK = [[[None for x in range(self.__dimension)] for y in range(r + 1)] for z in range(order + 1)]
        for i in range(0, r + 1):
            idx = 0
            while idx < self.__dimension:
                PK[0][i][idx] = self.__control_points[r1 + i][idx]
                idx += 1

        for k in range(1, order + 1):
            tmp = self.__degree - k + 1
            for i in range(0, r - k + 1):
                idx = 0
                while idx < self.__dimension:
                    PK[k][i][idx] = tmp * (PK[k - 1][i + 1][idx] - PK[k - 1][i][idx]) / (self.__knot_vector[r1 + i + self.__degree + 1] - self.__knot_vector[r1 + i + k])
                    idx += 1

        return PK

    # Evaluates the curve derivative using "CurveDerivsAlg2" algorithm
    def derivatives(self, u=-1, order=0):
        """ Evaluates n-th order curve derivatives at the given u using Algorithm A3.4.

        :param u: knot value
        :type u: float
        :param order: derivative order
        :type order: integer
        :return: A list containing up to {order}-th derivative of the curve
        :rtype: list
        """
        # Check all parameters are set before the curve evaluation
        self.__check_variables()
        # Check u parameters are correct
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')

        # Algorithm A3.4: CurveDerivsAlg2
        du = min(self.__degree, order)

        CK = [[None for x in range(self.__dimension)] for y in range(order + 1)]
        for k in range(self.__degree + 1, order + 1):
            CK[k] = [0.0 for x in range(self.__dimension)]

        span = utils.find_span(self.__degree, tuple(self.__knot_vector), len(self.__control_points), u)
        bfuns = utils.basis_functions_all(self.__degree, tuple(self.__knot_vector), span, u)
        PK = self.derivatives_ctrlpts(du, span - self.__degree, span)

        for k in range(0, du + 1):
            CK[k] = [0.0 for x in range(self.__dimension)]
            for j in range(0, self.__degree - k + 1):
                idx = 0
                while idx < self.__dimension:
                    CK[k][idx] += (bfuns[j][self.__degree - k] * PK[k][j][idx])
                    idx += 1

        # Return the derivatives
        return CK

    # Evaluates the curve tangent at the given u parameter
    def tangent(self, u=-1):
        """ Evaluates the surface tangent at the given (u, v) parameter.

        :param u: knot value
        :type u: float
        :return: A list in the order of "surface point" and "derivative"
        :rtype: list
        """
        # 1st derivative of the curve gives the tangent
        ders = self.derivatives(u, 1)

        # For readability
        point = ders[0]
        der_u = ders[1]

        # Return the list
        return point, der_u

    # Knot insertion
    def insert_knot(self, u, r=1):
        """ Inserts the given knot and updates the control points array and the knot vector.

        :param u: Knot parameter to be inserted
        :type u: float
        :param r: number of knot insertions
        :type r: int
        :return: None
        """
        # Check all parameters are set before the curve evaluation
        self.__check_variables()
        # Check u parameters are correct
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')
        if not isinstance(r, int) or r < 0:
            raise ValueError('Number of insertions must be a positive integer value.')

        s = utils.find_multiplicity(u, self.__knot_vector)

        # Check if it is possible add that many number of knots
        if r > self.__degree - s:
            warnings.warn("Cannot insert " + str(r) + " number of knots")
            return

        # Algorithm A5.1
        k = utils.find_span(self.__degree, self.__knot_vector, len(self.__control_points), u)
        mp = len(self.__knot_vector)
        np = len(self.__control_points)
        nq = np + r

        # Initialize new knot vector array
        UQ = [None for x in range(mp + r)]
        # Initialize new control points array (control points can be weighted or not)
        Q = [None for x in range(nq)]
        # Initialize a local array of length p + 1
        R = [None for x in range(self.__degree + 1)]

        # Load new knot vector
        for i in range(0, k + 1):
            UQ[i] = self.__knot_vector[i]
        for i in range(1, r+1):
            UQ[k + i] = u
        for i in range(k + 1, mp + 1):
            UQ[i + r] = self.__knot_vector[i]

        # Save unaltered control points
        for i in range(0, k - self.__degree + 1):
            Q[i] = self.__control_points[i]
        for i in range(k - s, np + 1):
            Q[i + r] = self.__control_points[i]
        for i in range(0, self.__degree - s + 1):
            R[i] = self.__control_points[k - self.__degree + i]

        # Insert the knot r times
        for j in range(1, r + 1):
            L = k - self.__degree + j
            for i in range(0, self.__degree - j - s + 1):
                alpha = (u - self.__knot_vector[L + i]) / (self.__knot_vector[i + k + 1] - self.__knot_vector[L + i])
                idx = 0
                while idx < self.__dimension:
                    R[i][idx] = alpha * R[i + 1][idx] + (1.0 - alpha) * R[i][idx]
                    idx += 1
            Q[L] = R[0]
            Q[k + r - j - s] = R[self.__degree - j - s]

        # Load remaining control points
        L = k - self.__degree + r
        for i in range(L + 1, k - s):
            Q[i] = R[i - L]

        # Update class variables
        self.__knot_vector = UQ
        self.__control_points = Q


class Curve2D(Curve):
    """ A data storage and evaluation class for 2D B-Spline curves.

    This class is a subclass of :class:`.Curve` with only the dimensional change.
    """
    def __init__(self):
        super(Curve2D, self).__init__()
        # Override dimension variable
        self.__dimension = 2  # 2D coordinates

    # Prepares and returns the CSV file header
    def __get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, scalar\n"


class Surface(object):
    """ A data storage and evaluation class for B-Spline surfaces.

    **Data Storage**

    :class:`.Surface` class implements Python properties using the ``@property`` decorator. The following properties are present in this class:

    * order_u
    * order_v
    * degree_u
    * degree_v
    * knotvector_u
    * knotvector_v
    * delta
    * ctrlpts
    * ctrlpts2D
    * surfpts

    The function :func:`.read_ctrlpts()` provides an easy way to read control points from a text file.
    Additional details for the text format can be found in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

    **Evaluation**

    The evaluation methods in the :class:`.Surface` class are:

    * :func:`.evaluate()`
    * :func:`.derivatives()`
    * :func:`.tangent()`
    * :func:`.normal()`

    .. note::

        If you update any of the data storage elements after the surface evaluation, the surface points stored in :py:attr:`~surfpts` property will be deleted automatically.
    """
    def __init__(self):
        self.__degree_u = 0
        self.__degree_v = 0
        self.__knot_vector_u = []
        self.__knot_vector_v = []
        self.__control_points = []
        self.__control_points2D = []  # in [u][v] format
        self.__control_points_size_u = 0  # columns
        self.__control_points_size_v = 0  # rows
        self.__delta = 0.1
        self.__surface_points = []
        self.__dimension = 3  # 3D coordinates

    @property
    def order_u(self):
        """ Surface order for U direction

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for U direction
        :setter: Sets the surface order for U direction
        :type: integer
        """
        return self.__degree_u + 1

    @order_u.setter
    def order_u(self, value):
        self.degree_u = value - 1

    @property
    def order_v(self):
        """ Surface order for V direction

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for V direction
        :setter: Sets the surface order for V direction
        :type: integer
        """
        return self.__degree_v + 1

    @order_v.setter
    def order_v(self, value):
        self.degree_v = value - 1

    @property
    def degree_u(self):
        """ Surface degree for U direction

        :getter: Gets the surface degree for U direction
        :setter: Sets the surface degree for U direction
        :type: integer
        """
        return self.__degree_u

    @degree_u.setter
    def degree_u(self, value):
        if value < 0:
            raise ValueError("Degree cannot be less than zero.")
        # Clean up the surface points lists, if necessary
        self.__reset_surface()
        # Set degree u
        self.__degree_u = value

    @property
    def degree_v(self):
        """ Surface degree for V direction

        :getter: Gets the surface degree V for V direction
        :setter: Sets the surface degree V for V direction
        :type: integer
        """
        return self.__degree_v

    @degree_v.setter
    def degree_v(self, value):
        if value < 0:
            raise ValueError("Degree cannot be less than zero.")
        # Clean up the surface points lists, if necessary
        self.__reset_surface()
        # Set degree v
        self.__degree_v = value

    @property
    def ctrlpts(self):
        """ Control points

        Control points are stored as a list of (x, y, z) coordinates. The v index varies first.
        That is, a row of v control points for the first u value is found first.
        Then, the row of v control points for the next u value.

        :getter: Gets the control points
        :setter: Sets the control points
        :type: list
        """
        ret_list = []
        for pt in self.__control_points:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        # Clean up the surface and control points lists, if necessary
        self.__reset_surface()
        self.__reset_ctrlpts()

        # First check v-direction
        if len(value) < self.__degree_v + 1:
            raise ValueError("Number of control points in v-direction should be at least degree + 1.")
        # Then, check U direction
        u_cnt = 0
        for u_coords in value:
            if len(u_coords) < self.__degree_u + 1:
                raise ValueError("Number of control points in u-direction should be at least degree + 1.")
            u_cnt += 1
            for coord in u_coords:
                # Save the control points as a list of 3D coordinates
                if len(coord) < 0 or len(coord) > self.__dimension:
                    raise ValueError("Please input 3D coordinates")
                # Convert to list of floats
                coord_float = [float(c) for c in coord]
                self.__control_points.append(coord_float)
        # Set u and v sizes
        self.__control_points_size_u = u_cnt
        self.__control_points_size_v = len(value)
        # Generate a 2D list of control points
        for i in range(0, self.__control_points_size_u):
            ctrlpts_v = []
            for j in range(0, self.__control_points_size_v):
                ctrlpts_v.append(self.__control_points[i + (j * self.__control_points_size_u)])
            self.__control_points2D.append(ctrlpts_v)

    @property
    def ctrlpts2d(self):
        """ Control points

        2D control points in [u][v] format.

        :getter: Gets the control points
        :type: list
        """
        return self.__control_points2D

    @property
    def knotvector_u(self):
        """ Knot vector for U direction

        :getter: Gets the knot vector for U direction
        :setter: Sets the knot vector for U direction
        :type: list
        """
        return tuple(self.__knot_vector_u)

    @knotvector_u.setter
    def knotvector_u(self, value):
        # Clean up the surface points lists, if necessary
        self.__reset_surface()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        self.__knot_vector_u = utils.normalize_knot_vector(tuple(value_float))

    @property
    def knotvector_v(self):
        """ Knot vector for V direction

        :getter: Gets the knot vector for V direction
        :setter: Sets the knot vector for V direction
        :type: list
        """
        return tuple(self.__knot_vector_v)

    @knotvector_v.setter
    def knotvector_v(self, value):
        # Clean up the surface points lists, if necessary
        self.__reset_surface()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        self.__knot_vector_v = utils.normalize_knot_vector(tuple(value_float))

    @property
    def delta(self):
        """ Surface evaluation delta

        .. note:: The delta value is 0.01 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self.__delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta should be between 0.0 and 1.0.")
        # Clean up the surface points lists, if necessary
        self.__reset_surface()
        # Set a new delta value
        self.__delta = float(value)

    @property
    def surfpts(self):
        """ Evaluated surface points

        .. note:: :func:`.evaluate` or :func:`.evaluate_rational` should be called first.

        :getter: (x, y, z) coordinates of the evaluated surface points
        :type: list
        """
        return self.__surface_points

    # Cleans up the control points
    def __reset_ctrlpts(self):
        if self.__control_points:
            # Delete control points
            del self.__control_points[:]
            del self.__control_points2D[:]
            # Set the control point sizes to zero
            self.__control_points_size_u = 0
            self.__control_points_size_v = 0

    # Cleans the evaluated surface points (private)
    def __reset_surface(self):
        if self.__surface_points:
            # Delete the surface points
            del self.__surface_points[:]

    # Checks whether the surface evaluation is possible or not (private)
    def __check_variables(self):
        works = True
        if self.__degree_u == 0 or self.__degree_v == 0:
            works = False
        if not self.__control_points:
            works = False
        if not self.__knot_vector_u or not self.__knot_vector_v:
            works = False
        if not works:
            raise ValueError("Some required parameters for surface evaluation are not set.")

    # Reads control points from a text file
    def read_ctrlpts_from_txt(self, filename=''):
        """ Loads control points from a text file.

        The control points loaded from the file should follow the right-hand rule.

        :param filename: input file name
        :type filename: string
        :return: True if control points are loaded correctly, False otherwise
        """
        # Clean up the surface and control points lists, if necessary
        self.__reset_ctrlpts()
        self.__reset_surface()

        # Initialize the return value
        ret_check = True

        # Try reading the file
        try:
            # Open the file
            with open(filename, 'r') as fp:
                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    control_point_row = line.split(';')
                    self.__control_points_size_v = 0
                    for cpr in control_point_row:
                        cpt = cpr.split(',')
                        # Create a temporary dictionary for appending coordinates into ctrlpts list
                        pt = []
                        idx = 0
                        while idx < self.__dimension:
                            pt.append(float(cpt[idx].strip()))
                            idx += 1
                        # Add control points to the global control point list
                        self.__control_points.append(pt)
                        self.__control_points_size_v += 1
                    self.__control_points_size_u += 1

            # Generate a 2D list of control points
            for i in range(0, self.__control_points_size_u):
                ctrlpts_v = []
                for j in range(0, self.__control_points_size_v):
                    ctrlpts_v.append(self.__control_points[j + (i * self.__control_points_size_v)])
                self.__control_points2D.append(ctrlpts_v)

        except IOError:
            # Show a warning about not finding the file
            warnings.warn("File " + str(filename) + " cannot be opened for reading.")
            ret_check = False

        return ret_check

    # Saves control points to a text file
    def save_ctrlpts_to_txt(self, filename="", two_dimensional=True):
        """ Saves control points to a text file.

        :param filename: output file name
        :type filename: string
        :param two_dimensional: flag to control point list
        :type two_dimensional: bool
        :return: True if control points are saved correctly, False otherwise
        """

        # Initialize the return value
        ret_check = True

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:

                if two_dimensional:
                    for i in range(0, self.__control_points_size_u):
                        line = ""
                        for j in range(0, self.__control_points_size_v):
                            idx = 0
                            while idx < self.__dimension:
                                line += self.__control_points2D[i][j]
                                if not idx == self.__dimension - 1:
                                    line += ","
                            idx += 1
                            if j != self.__control_points_size_v - 1:
                                line += ";"
                            else:
                                line += "\n"
                        fp.write(line)
                else:
                    for pt in self.__control_points:
                        line = ""
                        idx = 0
                        while idx < self.__dimension:
                            line += str(pt[idx])
                            if not idx == self.__dimension - 1:
                                line += ","
                            idx += 1
                        fp.write(line + "\n")

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for saving.")
            ret_check = False

        return ret_check

    # Prepares control points for exporting to external visualization software
    def __get_ctrlpts_for_exporting(self):
        """ Prepares control points for exporting to external visualization software, such as Paraview.

        :return: list of control points
        :rtype: list
        """
        return self.__control_points

    # Prepares and returns the CSV file header
    def __get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, coord z, scalar\n"

    # Saves control points to a text file
    def save_ctrlpts_to_csv(self, filename=""):
        """ Saves control points to a comma separated text file.

        :param filename: output file name
        :type filename: string
        :return: True if control points are saved correctly, False otherwise
        """

        # Initialize the return value
        ret_check = True

        coord_names = ["x", "y", "z"]

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:
                # Construct the header and write it to the file
                fp.write(self.__get_csv_header())

                # Loop through control points
                ctrlpts = self.__get_ctrlpts_for_exporting()
                for pt in ctrlpts:
                    line = ""
                    idx = 0
                    while idx < self.__dimension:
                        line += str(pt[idx])
                        if not idx == self.__dimension - 1:
                            line += ", "
                        idx += 1
                    fp.write(line + "\n")

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for saving.")
            ret_check = False

        return ret_check

    # Transposes the surface by swapping U and V directions
    def transpose(self):
        """ Transposes the surface by swapping U and V directions.

        :return: None
        """
        # Transpose existing data
        degree_u_new = self.__degree_v
        degree_v_new = self.__degree_u
        kv_u_new = self.__knot_vector_v
        kv_v_new = self.__knot_vector_u
        ctrlpts2D_new = []
        for v in range(0, self.__control_points_size_v):
            ctrlpts_u = []
            for u in range(0, self.__control_points_size_u):
                temp = self.__control_points2D[u][v]
                ctrlpts_u.append(temp)
            ctrlpts2D_new.append(ctrlpts_u)
        ctrlpts_new_sizeU = self.__control_points_size_v
        ctrlpts_new_sizeV = self.__control_points_size_u

        ctrlpts_new = []
        for v in range(0, ctrlpts_new_sizeV):
            for u in range(0, ctrlpts_new_sizeU):
                ctrlpts_new.append(ctrlpts2D_new[u][v])

        # Clean up the surface points lists, if necessary
        self.__reset_surface()

        # Save transposed data
        self.__degree_u = degree_u_new
        self.__degree_v = degree_v_new
        self.__knot_vector_u = kv_u_new
        self.__knot_vector_v = kv_v_new
        self.__control_points = ctrlpts_new
        self.__control_points_size_u = ctrlpts_new_sizeU
        self.__control_points_size_v = ctrlpts_new_sizeV
        self.__control_points2D = ctrlpts2D_new

    def surfpt(self, u=-1, v=-1, check_vars=True):
        """ Evaluates the B-Spline surface at the given (u,v) parameters

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :param check_vars: flag to disable variable checking (only for internal eval functions)
        :type check_vars: bool
        :return: evaluated surface point at the given knot values
        """
        if check_vars:
            # Check all parameters are set before the surface evaluation
            self.__check_variables()
            # Check u and v parameters are correct
            utils.check_uv(u, v)

        # Algorithm A3.5
        span_v = utils.find_span(self.__degree_v, tuple(self.__knot_vector_v), self.__control_points_size_v, v)
        basis_v = utils.basis_functions(self.__degree_v, tuple(self.__knot_vector_v), span_v, v)
        span_u = utils.find_span(self.__degree_u, tuple(self.__knot_vector_u), self.__control_points_size_u, u)
        basis_u = utils.basis_functions(self.__degree_u, tuple(self.__knot_vector_u), span_u, u)

        idx_u = span_u - self.__degree_u
        spt = [0.0 for x in range(self.__dimension)]

        for l in range(0, self.__degree_v + 1):
            temp = [0.0 for x in range(self.__dimension)]
            idx_v = span_v - self.__degree_v + l
            for k in range(0, self.__degree_u + 1):
                idx = 0
                while idx < self.__dimension:
                    temp[idx] += (basis_u[k] * self.__control_points2D[idx_u + k][idx_v][idx])
                    idx += 1
            idx = 0
            while idx < self.__dimension:
                spt[idx] += (basis_v[l] * temp[idx])
                idx += 1

        return spt

    # Evaluates the B-Spline surface
    def evaluate(self):
        """ Evaluates the surface.

        .. note:: The evaluated surface points are stored in :py:attr:`~surfpts`.

        :return: None
        """
        # Check all parameters are set before the surface evaluation
        self.__check_variables()
        # Clean up the surface points lists, if necessary
        self.__reset_surface()

        for u in utils.frange(0, 1, self.__delta):
            for v in utils.frange(0, 1, self.__delta):
                spt = self.surfpt(u, v, False)
                self.__surface_points.append(spt)

    # Evaluates n-th order surface derivatives at the given (u,v) parameter
    def derivatives(self, u=-1, v=-1, order=0):
        """ Evaluates n-th order surface derivatives at the given (u,v) parameter.

        * SKL[0][0] will be the surface point itself
        * SKL[0][1] will be the 1st derivative w.r.t. v
        * SKL[2][1] will be the 2nd derivative w.r.t. u and 1st derivative w.r.t. v

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :param order: derivative order
        :type order: integer
        :return: A list SKL, where SKL[k][l] is the derivative of the surface S(u,v) w.r.t. u k times and v l times
        :rtype: list
        """
        # Check all parameters are set before the surface evaluation
        self.__check_variables()
        # Check u and v parameters are correct
        utils.check_uv(u, v)

        # Algorithm A3.6
        du = min(self.__degree_u, order)
        dv = min(self.__degree_v, order)

        SKL = [[[0.0 for x in range(self.__dimension)] for y in range(dv + 1)] for z in range(du + 1)]

        span_u = utils.find_span(self.__degree_u, tuple(self.__knot_vector_u), self.__control_points_size_u, u)
        bfunsders_u = utils.basis_functions_ders(self.__degree_u, self.__knot_vector_u, span_u, u, du)
        span_v = utils.find_span(self.__degree_v, tuple(self.__knot_vector_v), self.__control_points_size_v, v)
        bfunsders_v = utils.basis_functions_ders(self.__degree_v, self.__knot_vector_v, span_v, v, dv)

        for k in range(0, du + 1):
            temp = [[] for y in range(self.__degree_v + 1)]
            for s in range(0, self.__degree_v + 1):
                temp[s] = [0.0 for x in range(self.__dimension)]
                for r in range(0, self.__degree_u + 1):
                    cu = span_u - self.__degree_u + r
                    cv = span_v - self.__degree_v + s
                    idx = 0
                    while idx < self.__dimension:
                        temp[s][idx] += (bfunsders_u[k][r] * self.__control_points2D[cu][cv][idx])
                        idx += 1

            dd = min(order - k, dv)
            for l in range(0, dd + 1):
                for s in range(0, self.__degree_v + 1):
                    idx = 0
                    while idx < self.__dimension:
                        SKL[k][l][idx] += (bfunsders_v[l][s] * temp[s][idx])
                        idx += 1

        # Return the derivatives
        return SKL

    # Evaluates the surface tangent at the given (u, v) parameter
    def tangent(self, u=-1, v=-1):
        """ Evaluates the surface tangent at the given (u, v) parameter.

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :return: A list in the order of "surface point", "derivative w.r.t. u" and "derivative w.r.t. v"
        :rtype: list
        """
        # Tangent is the 1st derivative of the surface
        skl = self.derivatives(u, v, 1)

        # Doing this just for readability
        point = skl[0][0]
        der_u = skl[1][0]
        der_v = skl[0][1]

        # Return the list of tangents w.r.t. u and v
        return tuple(point), tuple(der_u), tuple(der_v)

    # Evaluates the surface normal at the given (u, v) parameter
    def normal(self, u=-1, v=-1, normalized=True):
        """ Evaluates the surface normal at the given (u, v) parameter.

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :param normalized: if True, the returned normal vector is an unit vector
        :type normalized: boolean
        :return: normal vector
        :rtype: list
        """
        # Check u and v parameters are correct for the normal evaluation
        utils.check_uv(u, v, test_normal=True, delta=self.__delta)

        # Take the 1st derivative of the surface
        skl = self.derivatives(u, v, 1)

        # For readability
        der_u = skl[1][0]
        der_v = skl[0][1]

        # Compute normal
        normal = utils.vector_cross(der_u, der_v)

        if normalized:
            # Convert normal vector to a unit vector
            normal = utils.vector_normalize(tuple(normal))

        # Return the surface normal at the input u,v location
        return tuple(normal)
