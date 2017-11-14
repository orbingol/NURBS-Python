"""
.. module:: BSpline
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation class for B-spline curves and surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import sys
import warnings
import copy
import geomdl.utilities as utils


class Curve(object):
    """ A data storage and evaluation class for 3D B-Spline (NUBS) curves.

    **Data Storage**

    The following properties are present in this class:

    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * curvepts

    The function :func:`.read_ctrlpts()` provides an easy way to read weighted control points from a text file.
    Additional details on the file formats can be found in the documentation.

    .. note:: Control points are stored as a list of (x, y, z) coordinates

    **Evaluation**

    The evaluation methods are:

    * :func:`.evaluate()`
    * :func:`.derivatives()`
    * :func:`.tangent()`
    * :func:`.insert_knot()`

    Please check the function reference for the details.

    .. note::

        If you update any of the data storage elements after the curve evaluation, the surface points stored in :py:attr:`~curvepts` property will be deleted automatically.
    """
    def __init__(self):
        self._degree = 0
        self._knot_vector = []
        self._control_points = []
        self._delta = 0.1
        self._curve_points = []
        self._dimension = 3  # 3D coordinates
        self._rational = False

    @property
    def order(self):
        """ Curve order.

        Defined as order = degree + 1

        :getter: Gets the curve order
        :setter: Sets the curve order
        :type: integer
        """
        return self._degree + 1

    @order.setter
    def order(self, value):
        self.degree = value - 1

    @property
    def degree(self):
        """ Curve degree.

        :getter: Gets the curve degree
        :setter: Sets the curve degree
        :type: integer
        """
        return self._degree

    @degree.setter
    def degree(self, value):
        # degree = 0, dots
        # degree = 1, polylines
        # degree = 2, quadratic curves
        # degree = 3, cubic curves
        if value < 0:
            raise ValueError("ERROR: Degree cannot be less than zero")
        # Clean up the curve points list, if necessary
        self._reset_curve()
        # Set degree
        self._degree = value

    @property
    def ctrlpts(self):
        """ Control points.

        :getter: Gets the control points
        :setter: Sets the control points
        :type: list
        """
        ret_list = []
        for pt in self._control_points:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        if len(value) < self._degree + 1:
            raise ValueError("ERROR: Number of control points in u-direction should be at least degree + 1")

        # Clean up the curve and control points lists, if necessary
        self._reset_curve()
        self._reset_ctrlpts()

        for coord in value:
            if len(coord) < 0 or len(coord) > self._dimension:
                raise ValueError("ERROR: Please input 3D coordinates")
            # Convert to list of floats
            coord_float = [float(c) for c in coord]
            self._control_points.append(coord_float)

    @property
    def knotvector(self):
        """ Knot vector.

        :getter: Gets the knot vector
        :setter: Sets the knot vector
        :type: list
        """
        return tuple(self._knot_vector)

    @knotvector.setter
    def knotvector(self, value):
        # Clean up the surface points lists, if necessary
        self._reset_curve()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        # Normalize and set the knot vector
        self._knot_vector = utils.normalize_knot_vector(tuple(value_float))

    @property
    def delta(self):
        """ Curve evaluation delta.

        .. note:: The delta value is 0.1 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("ERROR: Curve evaluation delta should be between 0.0 and 1.0")
        # Clean up the curve points list, if necessary
        self._reset_curve()
        # Set a new delta value
        self._delta = float(value)

    @property
    def curvepts(self):
        """ Evaluated curve points.

        .. note:: :func:`.evaluate` or :func:`.evaluate_rational` should be called first.

        :getter: (x, y) coordinates of the evaluated surface points
        :type: list
        """
        return self._curve_points

    # Cleans up the control points
    def _reset_ctrlpts(self):
        if self._control_points:
            # Delete control points
            del self._control_points[:]

    # Cleans the evaluated curve points (private)
    def _reset_curve(self):
        if self._curve_points:
            # Delete the curve points
            del self._curve_points[:]

    # Checks whether the curve evaluation is possible or not (private)
    def _check_variables(self):
        works = True
        # Check degree values
        if self._degree == 0:
            works = False
        if not self._control_points:
            works = False
        if not self._knot_vector:
            works = False
        if not works:
            raise ValueError("Some required parameters for curve evaluation are not set.")

    # Reads control points from a text file
    def read_ctrlpts_from_txt(self, filename=''):
        """ Loads control points from a text file.

        :param filename: input file name
        :type filename: str
        :return: True if control points are loaded correctly, False otherwise
        :rtype: bool
        """
        # Clean up the curve and control points lists, if necessary
        self._reset_curve()
        self._reset_ctrlpts()

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
                    for coord in coords:
                        pt.append(float(coord.strip()))
                    self._control_points.append(pt)

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for reading.")
            ret_check = False

        return ret_check

    # Saves control points to a text file
    def save_ctrlpts_to_txt(self, filename=""):
        """ Saves control points to a text file.

        :param filename: output file name
        :type filename: str
        :return: True if control points are saved correctly, False otherwise
        :rtype: bool
        """
        # Check if we have any control points
        if not self._control_points:
            warnings.warn("There are no control points to save!")
            return

        # Initialize the return value
        ret_check = True

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:

                # Loop through the control points
                for pt in self._control_points:
                    line = ""
                    for idx, coord in enumerate(pt):
                        if idx:  # Add comma if we are not on the first element
                            line += ","
                        line += str(coord)
                    fp.write(line + "\n")

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for writing.")
            ret_check = False

        return ret_check

    # Prepares control points for exporting as a CSV file
    def _get_ctrlpts_for_exporting(self):
        """ Prepares control points for exporting as a CSV file.

        :return: list of control points
        :rtype: list
        """
        return self._control_points

    # Prepares and returns the CSV file header
    def _get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, coord z, scalar\n"

    # Saves control points to a CSV file
    def save_ctrlpts_to_csv(self, filename="", scalar=0):
        """ Saves control points to a comma separated text file.

        :param filename: output file name
        :type filename: str
        :param scalar: value of the scalar column in the output, defaults to 0
        :type scalar: int
        :return: True if control points are saved correctly, False otherwise
        :rtype: bool
        """
        # Check if we have any control points
        if not self._control_points:
            warnings.warn("There are no control points to save!")
            return

        if not isinstance(scalar, (int, float)):
            raise ValueError("Value of scalar must be integer or float.")

        # Initialize the return value
        ret_check = True

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:
                # Construct the header and write it to the file
                fp.write(self._get_csv_header())

                # Loop through control points
                ctrlpts = self._get_ctrlpts_for_exporting()
                for pt in ctrlpts:
                    # Fill coordinates
                    line = ", ".join(str(c) for c in pt)
                    # Fill scalar column
                    line += ", " + str(scalar) + "\n"
                    # Write line to file
                    fp.write(line)

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for writing.")
            ret_check = False

        return ret_check

    # Saves evaluated curve points to a CSV file
    def save_curvepts_to_csv(self, filename="", scalar=0):
        """ Saves evaluated curve points to a comma separated text file.

        :param filename: output file name
        :type filename: str
        :param scalar: value of the scalar column in the output, defaults to 0
        :type scalar: int
        :return: True if curve points are saved correctly, False otherwise
        :rtype: bool
        """
        if not isinstance(scalar, (int, float)):
            raise ValueError("Value of scalar must be integer or float.")

        # Find surface points if there is none
        if not self._curve_points:
            self.evaluate()

        # Initialize the return value
        ret_check = True

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:
                # Construct the header and write it to the file
                fp.write(self._get_csv_header())

                # Loop through control points
                for pt in self._curve_points:
                    # Fill coordinates
                    line = ", ".join(str(c) for c in pt)
                    # Fill scalar column
                    line += ", " + str(scalar) + "\n"
                    # Write line to file
                    fp.write(line)

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for writing.")
            ret_check = False

        return ret_check

    # Evaluates the B-Spline curve at the given parameter
    def curvept(self, u=-1, check_vars=True, get_ctrlpts=False):
        """ Evaluates the B-Spline curve at the given u parameter.

        :param u: parameter
        :type u: float
        :param check_vars: flag to disable variable checking (only for internal eval functions)
        :type check_vars: bool
        :param get_ctrlpts: flag to add a list of control points associated with the curve evaluation to the return value
        :param get_ctrlpts: bool
        :return: evaluated curve point at the given knot value
        :rtype: list
        """
        if check_vars:
            # Check all parameters are set before the curve evaluation
            self._check_variables()
            # Check u parameters are correct
            utils.check_uv(u)

        # Initialize an empty list which will contain the list of associated control points
        ctrlpts = []

        # Algorithm A3.1
        span = utils.find_span(self._degree, tuple(self._knot_vector), len(self._control_points), u)
        basis = utils.basis_functions(self._degree, tuple(self._knot_vector), span, u)
        cpt = [0.0 for x in range(self._dimension)]
        for i in range(0, self._degree + 1):
            cpt[:] = [curve_pt + (basis[i] * ctrl_pt) for curve_pt, ctrl_pt in zip(cpt, self._control_points[span - self._degree + i])]
            if get_ctrlpts:
                ctrlpts.append(self._control_points[span - self._degree + i])

        if get_ctrlpts:
            return cpt, ctrlpts
        return cpt

    # Evaluates the B-Spline curve
    def evaluate(self):
        """ Evaluates the B-Spline curve.

        .. note:: The evaluated surface points are stored in :py:attr:`~curvepts`.

        :return: None
        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()
        # Clean up the curve points, if necessary
        self._reset_curve()

        for u in utils.frange(0, 1, self._delta):
            cpt = self.curvept(u, False)
            self._curve_points.append(cpt)

    # Evaluates the curve derivative using "CurveDerivsAlg1" algorithm
    def derivatives2(self, u=-1, order=0):
        """ Evaluates n-th order curve derivatives at the given u using Algorithm A3.2.

        :param u: knot value
        :type u: float
        :param order: derivative order
        :type order: integer
        :return: A list containing up to {order}-th derivative of the curve
        :rtype: list
        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()
        # Check u parameters are correct
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')

        # Algorithm A3.2
        du = min(self._degree, order)

        CK = [[None for x in range(self._dimension)] for y in range(order + 1)]
        for k in range(self._degree + 1, order + 1):
            CK[k] = [0.0 for x in range(self._dimension)]

        span = utils.find_span(self._degree, tuple(self._knot_vector), len(self._control_points), u)
        bfunsders = utils.basis_functions_ders(self._degree, tuple(self._knot_vector), span, u, du)

        for k in range(0, du + 1):
            CK[k] = [0.0 for x in range(self._dimension)]
            for j in range(0, self._degree + 1):
                CK[k][:] = [drv + (bfunsders[k][j] * ctrl_pt) for drv, ctrl_pt in zip(CK[k], self._control_points[span - self._degree + j])]

        # Return the derivatives
        return CK

    # Computes the control points of all derivative curves up to and including the d-th derivative
    def derivatives_ctrlpts(self, order=0, r1=0, r2=0):
        """ Computes the control points of all derivative curves up to and including the {degree}-th derivative.

        Implements Algorithm A3.3.
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
        # Algorithm A3.3
        r = r2 - r1
        PK = [[[None for x in range(self._dimension)] for y in range(r + 1)] for z in range(order + 1)]
        for i in range(0, r + 1):
            PK[0][i][:] = [elem for elem in self._control_points[r1 + i]]

        for k in range(1, order + 1):
            tmp = self._degree - k + 1
            for i in range(0, r - k + 1):
                PK[k][i][:] = [tmp * (elem1 - elem2) / (self._knot_vector[r1 + i + self._degree + 1] - self._knot_vector[r1 + i + k]) for elem1, elem2 in zip(PK[k - 1][i + 1], PK[k - 1][i])]

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
        self._check_variables()
        # Check u parameters are correct
        utils.check_uv(u)

        # Algorithm A3.4
        du = min(self._degree, order)

        CK = [[None for x in range(self._dimension)] for y in range(order + 1)]
        for k in range(self._degree + 1, order + 1):
            CK[k] = [0.0 for x in range(self._dimension)]

        span = utils.find_span(self._degree, tuple(self._knot_vector), len(self._control_points), u)
        bfuns = utils.basis_functions_all(self._degree, tuple(self._knot_vector), span, u)
        PK = self.derivatives_ctrlpts(du, span - self._degree, span)

        for k in range(0, du + 1):
            CK[k] = [0.0 for x in range(self._dimension)]
            for j in range(0, self._degree - k + 1):
                CK[k][:] = [elem + (bfuns[j][self._degree - k] * drv_ctrlpt) for elem, drv_ctrlpt in zip(CK[k], PK[k][j])]

        # Return the derivatives
        return CK

    # Evaluates the curve tangent at the given u parameter
    def tangent(self, u=-1, normalize=False):
        """ Evaluates the surface tangent at the given (u, v) parameter.

        :param u: knot value
        :type u: float
        :param normalize: if True, the returned tangent vector is converted to a unit vector
        :type normalize: bool
        :return: A list in the order of "surface point" and "derivative"
        :rtype: list
        """
        # 1st derivative of the curve gives the tangent
        ders = self.derivatives(u, 1)

        # For readability
        point = ders[0]
        der_u = ders[1]

        # Normalize the tangent vector
        if normalize:
            der_u = utils.vector_normalize(der_u)

        # Return the list
        return point, der_u

    # Knot insertion
    def insert_knot(self, u, r=1):
        """ Inserts the given knot and updates the control points array and the knot vector.

        :param u: Knot to be inserted
        :type u: float
        :param r: number of knot insertions
        :type r: int
        :return: None
        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()
        # Check u parameters are correct
        utils.check_uv(u)
        # Check if the number of knot insertions requested is valid
        if not isinstance(r, int) or r < 0:
            raise ValueError('Number of insertions must be a positive integer value.')

        s = utils.find_multiplicity(u, self._knot_vector)

        # Check if it is possible add that many number of knots
        if r > self._degree - s:
            warnings.warn("Cannot insert " + str(r) + " number of knots")
            return

        # Algorithm A5.1
        k = utils.find_span(self._degree, self._knot_vector, len(self._control_points), u)
        mp = len(self._knot_vector)
        np = len(self._control_points)
        nq = np + r


        # Initialize new knot vector array
        UQ = [None for x in range(mp + r)]
        # Initialize new control points array (control points can be weighted or not)
        Q = [None for x in range(nq)]
        # Initialize a local array of length p + 1
        R = [None for x in range(self._degree + 1)]

        # Load new knot vector
        for i in range(0, k + 1):
            UQ[i] = self._knot_vector[i]
        for i in range(1, r+1):
            UQ[k + i] = u
        for i in range(k + 1, mp):
            UQ[i + r] = self._knot_vector[i]

        # Save unaltered control points
        for i in range(0, k - self._degree + 1):
            Q[i] = self._control_points[i]
        for i in range(k - s, np):
            Q[i + r] = self._control_points[i]

        # The algorithm uses R array to update control points
        for i in range(0, self._degree - s + 1):
            R[i] = copy.deepcopy(self._control_points[k - self._degree + i])

        # Insert the knot r times
        for j in range(1, r + 1):
            L = k - self._degree + j
            for i in range(0, self._degree - j - s + 1):
                alpha = (u - self._knot_vector[L + i]) / (self._knot_vector[i + k + 1] - self._knot_vector[L + i])
                R[i][:] = [alpha * elem2 + (1.0 - alpha) * elem1 for elem1, elem2 in zip(R[i], R[i + 1])]
            Q[L] = R[0]
            Q[k + r - j - s] = R[self._degree - j - s]

        # Load remaining control points
        L = k - self._degree + r
        for i in range(L + 1, k - s):
            Q[i] = R[i - L]

        # Update class variables
        self._knot_vector = UQ
        self._control_points = Q

        # Evaluate curve again if it has already been evaluated before knot insertion
        if self._curve_points:
            self.evaluate()


class Curve2D(Curve):
    """ A data storage and evaluation class for 2D B-Spline (NUBS) curves.

    **Data Storage**

    The following properties are present in this class:

    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * curvepts

    The function :func:`.read_ctrlpts()` provides an easy way to read weighted control points from a text file.
    Additional details on the file formats can be found in the documentation.

    .. note:: Control points are stored as a list of (x, y) coordinates

    **Evaluation**

    The evaluation methods are:

    * :func:`.evaluate()`
    * :func:`.derivatives()`
    * :func:`.tangent()`
    * :func:`.insert_knot()`

    Please check the function reference for the details.

    .. note::

        If you update any of the data storage elements after the curve evaluation, the surface points stored in :py:attr:`~curvepts` property will be deleted automatically.
    """
    def __init__(self):
        super(Curve2D, self).__init__()
        # Override dimension variable
        self._dimension = 2  # 2D coordinates
        self._rational = False

    # Prepares and returns the CSV file header
    def _get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, scalar\n"


class Surface(object):
    """ A data storage and evaluation class for B-Spline (NUBS) surfaces.

    **Data Storage**

    The following properties are present in this class:

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
    Additional details on the file formats can be found in the documentation.

    .. note:: Control points are stored as a list of (x, y, z) coordinates

    **Evaluation**

    The evaluation methods are:

    * :func:`.evaluate()`
    * :func:`.derivatives()`
    * :func:`.tangent()`
    * :func:`.normal()`
    * :func:`.insert_knot()`

    Please check the function reference for the details.

    .. note::

        If you update any of the data storage elements after the surface evaluation, the surface points stored in :py:attr:`~surfpts` property will be deleted automatically.
    """
    def __init__(self):
        self._degree_u = 0
        self._degree_v = 0
        self._knot_vector_u = []
        self._knot_vector_v = []
        self._control_points = []
        self._control_points2D = []  # in [u][v] format
        self._control_points_size_u = 0  # columns
        self._control_points_size_v = 0  # rows
        self._delta = 0.1
        self._surface_points = []
        self._dimension = 3  # 3D coordinates
        self._rational = False

    @property
    def order_u(self):
        """ Surface order for U direction.

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for U direction
        :setter: Sets the surface order for U direction
        :type: integer
        """
        return self._degree_u + 1

    @order_u.setter
    def order_u(self, value):
        self.degree_u = value - 1

    @property
    def order_v(self):
        """ Surface order for V direction.

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for V direction
        :setter: Sets the surface order for V direction
        :type: integer
        """
        return self._degree_v + 1

    @order_v.setter
    def order_v(self, value):
        self.degree_v = value - 1

    @property
    def degree_u(self):
        """ Surface degree for U direction.

        :getter: Gets the surface degree for U direction
        :setter: Sets the surface degree for U direction
        :type: integer
        """
        return self._degree_u

    @degree_u.setter
    def degree_u(self, value):
        if value < 0:
            raise ValueError("Degree cannot be less than zero.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set degree u
        self._degree_u = value

    @property
    def degree_v(self):
        """ Surface degree for V direction.

        :getter: Gets the surface degree V for V direction
        :setter: Sets the surface degree V for V direction
        :type: integer
        """
        return self._degree_v

    @degree_v.setter
    def degree_v(self, value):
        if value < 0:
            raise ValueError("Degree cannot be less than zero.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set degree v
        self._degree_v = value

    @property
    def ctrlpts(self):
        """ Control points.

        .. note::

            The v index varies first. That is, a row of v control points for the first u value is found first.
            Then, the row of v control points for the next u value.

        :getter: Gets the control points
        :type: list
        """
        ret_list = []
        for pt in self._control_points:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @property
    def ctrlpts2d(self):
        """ Control points.

        2D control points in *[u][v]* format.

        :getter: Gets the control points
        :type: list
        """
        return self._control_points2D

    @property
    def ctrlpts_size_u(self):
        """ Gets the size of the control points array in U-direction.

        :return: number of control points in U-direction
        :rtype: int
        """
        return self._control_points_size_u

    @property
    def ctrlpts_size_v(self):
        """ Gets the size of the control points array in V-direction.

        :return: number of control points in V-direction
        :rtype: int
        """
        return self._control_points_size_v

    def set_ctrlpts(self, ctrlpts, size_u, size_v):
        """ Sets 1D control points.

        This function expects a list coordinates which is also a list. For instance, if you are working in 3D space, then
        your coordinates will be a list of 3 elements representing *(x, y, z)* coordinates.

        This function also generates 2D control points in *[u][v]* format which can be accessed via
        :py:attr:`~ctrlpts2d` property.

        .. note::

            The v index varies first. That is, a row of v control points for the first u value is found first.
            Then, the row of v control points for the next u value.

        :param ctrlpts: input control points as a list of coordinates
        :type ctrlpts: list
        :param size_u: size of the control points grid in U-direction
        :param size_u: int
        :param size_v: size of the control points grid in V-direction
        :param size_v: int
        :return: None
        """
        # Clean up the surface and control points lists, if necessary
        self._reset_surface()
        self._reset_ctrlpts()

        if self._degree_u == 0 or self._degree_v == 0:
            raise ValueError("First, set the degrees!")
        if size_u < self._degree_u + 1:
            raise ValueError("Number of control points in u-direction should be at least degree + 1.")
        if size_v < self._degree_v + 1:
            raise ValueError("Number of control points in v-direction should be at least degree + 1.")

        # Set the new control points
        self._control_points = copy.deepcopy(ctrlpts)

        # Set u and v sizes
        self._control_points_size_u = size_u
        self._control_points_size_v = size_v

        # Generate a 2D list of control points
        for i in range(0, self._control_points_size_u):
            ctrlpts_v = []
            for j in range(0, self._control_points_size_v):
                ctrlpts_v.append(self._control_points[i + (j * self._control_points_size_u)])
            self._control_points2D.append(ctrlpts_v)

    @property
    def knotvector_u(self):
        """ Knot vector for U direction.

        :getter: Gets the knot vector for U direction
        :setter: Sets the knot vector for U direction
        :type: list
        """
        return tuple(self._knot_vector_u)

    @knotvector_u.setter
    def knotvector_u(self, value):
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        self._knot_vector_u = utils.normalize_knot_vector(tuple(value_float))

    @property
    def knotvector_v(self):
        """ Knot vector for V direction.

        :getter: Gets the knot vector for V direction
        :setter: Sets the knot vector for V direction
        :type: list
        """
        return tuple(self._knot_vector_v)

    @knotvector_v.setter
    def knotvector_v(self, value):
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        self._knot_vector_v = utils.normalize_knot_vector(tuple(value_float))

    @property
    def delta(self):
        """ Surface evaluation delta.

        .. note:: The delta value is 0.01 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta should be between 0.0 and 1.0.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set a new delta value
        self._delta = float(value)

    @property
    def surfpts(self):
        """ Evaluated surface points.

        .. note:: :func:`.evaluate` or :func:`.evaluate_rational` should be called first.

        :getter: (x, y, z) coordinates of the evaluated surface points
        :type: list
        """
        return self._surface_points

    # Cleans up the control points
    def _reset_ctrlpts(self):
        if self._control_points:
            # Delete control points
            del self._control_points[:]
            del self._control_points2D[:]
            # Set the control point sizes to zero
            self._control_points_size_u = 0
            self._control_points_size_v = 0

    # Cleans the evaluated surface points (private)
    def _reset_surface(self):
        if self._surface_points:
            # Delete the surface points
            del self._surface_points[:]

    # Checks whether the surface evaluation is possible or not (private)
    def _check_variables(self):
        works = True
        if self._degree_u == 0 or self._degree_v == 0:
            works = False
        if not self._control_points:
            works = False
        if not self._knot_vector_u or not self._knot_vector_v:
            works = False
        if not works:
            raise ValueError("Some required parameters for surface evaluation are not set.")

    # Reads control points from a text file
    def read_ctrlpts_from_txt(self, filename='', two_dimensional=True, size_u=0, size_v=0):
        """ Loads control points from a text file.

        The control points loaded from the file should follow the right-hand rule.
        In case two_dimensional = False, then the following rules apply.

        * The v index varies first. That is, a row of v control points for the first u value is found first.
        * Then, the row of v control points for the next u value.

        :param filename: input file name
        :type filename: str
        :param two_dimensional: flag to control point list. one dimensional or two dimensional
        :type two_dimensional: bool
        :param size_u: length of the control points array in U-direction
        :type size_u: int
        :param size_v: length of the control points array in V-direction
        :type size_v: int
        :return: True if control points are loaded correctly, False otherwise
        :rtype: bool
        """
        # Clean up the surface and control points lists, if necessary
        self._reset_ctrlpts()
        self._reset_surface()

        # Initialize the return value
        ret_check = True

        # Try opening the file for reading
        try:
            with open(filename, 'r') as fp:

                if two_dimensional:
                    # Start reading file
                    for line in fp:
                        # Remove whitespace
                        line = line.strip()
                        # Convert the string containing the coordinates into a list
                        control_point_row = line.split(';')
                        self._control_points_size_v = 0
                        for cpr in control_point_row:
                            cpt = cpr.split(',')
                            pt_temp = []
                            for pt in cpt:
                                pt_temp.append(float(pt.strip()))
                            # Add control points to the global control point list
                            self._control_points.append(pt_temp)
                            self._control_points_size_v += 1
                        self._control_points_size_u += 1
                else:
                    # Check inputs
                    if size_u <= 0 or size_v <= 0:
                        raise ValueError("size_u and size_v inputs must be positive integers.")
                    # Start reading file
                    for line in fp:
                        # Remove whitespace
                        line = line.strip()
                        # Convert the string containing the coordinates into a list
                        coords = line.split(',')
                        # Remove extra whitespace and convert to float
                        pt = []
                        for coord in coords:
                            pt.append(float(coord.strip()))
                        self._control_points.append(pt)
                    # These depends on the user input
                    self._control_points_size_u = size_u
                    self._control_points_size_v = size_v

            # Generate a 2D list of control points
            for i in range(0, self._control_points_size_u):
                ctrlpts_v = []
                for j in range(0, self._control_points_size_v):
                    ctrlpts_v.append(self._control_points[j + (i * self._control_points_size_v)])
                self._control_points2D.append(ctrlpts_v)

        except IOError:
            # Show a warning about not finding the file
            warnings.warn("File " + str(filename) + " cannot be opened for reading.")
            ret_check = False

        return ret_check

    # Saves control points to a text file
    def save_ctrlpts_to_txt(self, filename="", two_dimensional=True):
        """ Saves control points to a text file.

        The control points saved to the file follow the right-hand rule.
        In case two_dimensional = False, then the following rules apply.

        * The v index varies first. That is, a row of v control points for the first u value is found first.
        * Then, the row of v control points for the next u value.

        :param filename: output file name
        :type filename: str
        :param two_dimensional: flag to control point list
        :type two_dimensional: bool
        :return: True if control points are saved correctly, False otherwise
        :rtype: bool
        """
        # Check if we have any control points
        if not self._control_points:
            warnings.warn("There are no control points to save!")
            return

        # Initialize the return value
        ret_check = True

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:

                if two_dimensional:
                    for i in range(0, self._control_points_size_u):
                        line = ""
                        for j in range(0, self._control_points_size_v):
                            for idx, coord in enumerate(self._control_points2D[i][j]):
                                if idx:  # Add comma if we are not on the first element
                                    line += ","
                                line += str(coord)
                            if j != self._control_points_size_v - 1:
                                line += ";"
                            else:
                                line += "\n"
                        fp.write(line)
                else:
                    for pt in self._control_points:
                        # Fill coordinates
                        line = ", ".join(str(c) for c in pt)
                        fp.write(line)

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for writing.")
            ret_check = False

        return ret_check

    # Prepares control points for exporting as a CSV file
    def _get_ctrlpts_for_exporting(self):
        """ Prepares control points for exporting as a CSV file.

        :return: list of control points
        :rtype: list
        """
        return self._control_points

    # Prepares and returns the CSV file header
    def _get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, coord z, scalar\n"

    # Saves control points to a CSV file
    def save_ctrlpts_to_csv(self, filename="", scalar=0, mode='linear'):
        """ Saves control points to a comma separated text file.

        **Available Modes**

        The following modes are available via ``mode=`` parameter:

        * ``linear``: Default mode, saves the stored point array without any change
        * ``zigzag``: Generates a zig-zag shape
        * ``wireframe``: Generates a wireframe

        Please note that mode parameter does not modify the stored points in the object instance.

        :param filename: output file name
        :type filename: str
        :param scalar: value of the scalar column in the output, defaults to 0
        :type scalar: int
        :param mode: sets the arrangement of the points, default is linear
        :type: str
        :return: True if control points are saved correctly, False otherwise
        :rtype: bool
        """
        # Check if we have any control points
        if not self._control_points:
            warnings.warn("There are no control points to save!")
            return

        # Check possible modes
        mode_list = ['linear', 'zigzag', 'wireframe']
        if mode not in mode_list:
            warnings.warn("Input mode '" + mode + "' is not valid, defaulting to 'linear'.")

        # Check input parameters
        if not isinstance(scalar, (int, float)):
            raise ValueError("Value of scalar must be integer or float.")

        # Initialize the return value
        ret_check = True

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:
                # Construct the header and write it to the file
                fp.write(self._get_csv_header())

                # Get the control points
                ctrlpts = self._get_ctrlpts_for_exporting()

                # If the user requested a different point arrangment, apply it here
                if mode == 'zigzag':
                    ctrlpts = utils.make_zigzag(ctrlpts, self._control_points_size_v)
                if mode == 'wireframe':
                    ctrlpts = utils.make_quad(ctrlpts, self._control_points_size_v, self._control_points_size_u)

                # Loop through control points
                for pt in ctrlpts:
                    # Fill coordinates
                    line = ", ".join(str(c) for c in pt)
                    # Fill scalar column
                    line += ", " + str(scalar) + "\n"
                    # Write line to file
                    fp.write(line)

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for writing.")
            ret_check = False

        return ret_check

    # Saves evaluated surface points to a CSV file
    def save_surfpts_to_csv(self, filename="", scalar=0, mode='linear'):
        """ Saves evaluated surface points to a comma separated text file.

        **Available Modes**

        The following modes are available via ``mode=`` parameter:

        * ``linear``: Default mode, saves the stored point array without any change
        * ``zigzag``: Generates a zig-zag shape
        * ``wireframe``: Generates a wireframe
        * ``triangle``: Triangulates the points
        * ``mesh``: Generates a quad mesh

        Please note that mode parameter does not modify the stored points in the object instance.

        :param filename: output file name
        :type filename: str
        :param scalar: value of the scalar column in the output, defaults to 0
        :type scalar: int
        :param mode: sets the arrangement of the points, default is linear
        :type: str
        :return: True if surface points are saved correctly, False otherwise
        :rtype: bool
        """
        # Check possible modes
        mode_list = ['linear', 'zigzag', 'wireframe', 'triangle', 'mesh']
        if mode not in mode_list:
            warnings.warn("Input mode '" + mode + "' is not valid, defaulting to 'linear'.")

        # Check input parameters
        if not isinstance(scalar, (int, float)):
            raise ValueError("Value of scalar must be integer or float.")

        # Find surface points if there is none
        if not self._surface_points:
            self.evaluate()

        # Initialize the return value
        ret_check = True

        # Try opening the file for writing
        try:
            with open(filename, 'w') as fp:
                # Construct the header and write it to the file
                fp.write(self._get_csv_header())

                # If the user requested a different point arrangment, apply it here
                if mode == 'zigzag':
                    points = utils.make_zigzag(self._surface_points, int((1.0 / self._delta) + 1))
                elif mode == 'wireframe':
                    points = utils.make_quad(self._surface_points, int((1.0 / self._delta) + 1), int((1.0 / self._delta) + 1))
                elif mode == 'triangle':
                    warnings.warn("Triangle mode has not been implemented yet!")
                    points = self._surface_points
                elif mode == 'mesh':
                    warnings.warn("Mesh mode has not been implemented yet!")
                    points = self._surface_points
                else:
                    points = self._surface_points

                # Loop through control points
                for pt in points:
                    # Fill coordinates
                    line = ", ".join(str(c) for c in pt)
                    # Fill scalar column
                    line += ", " + str(scalar) + "\n"
                    # Write line to file
                    fp.write(line)

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + str(filename) + " cannot be opened for writing.")
            ret_check = False

        return ret_check

    # Transposes the surface by swapping U and V directions
    def transpose(self):
        """ Transposes the surface by swapping U and V directions.

        :return: None
        """
        # Transpose existing data
        degree_u_new = self._degree_v
        degree_v_new = self._degree_u
        kv_u_new = self._knot_vector_v
        kv_v_new = self._knot_vector_u
        ctrlpts2D_new = []
        for v in range(0, self._control_points_size_v):
            ctrlpts_u = []
            for u in range(0, self._control_points_size_u):
                temp = self._control_points2D[u][v]
                ctrlpts_u.append(temp)
            ctrlpts2D_new.append(ctrlpts_u)
        ctrlpts_new_sizeU = self._control_points_size_v
        ctrlpts_new_sizeV = self._control_points_size_u

        ctrlpts_new = []
        for v in range(0, ctrlpts_new_sizeV):
            for u in range(0, ctrlpts_new_sizeU):
                ctrlpts_new.append(ctrlpts2D_new[u][v])

        # Clean up the surface points lists, if necessary
        self._reset_surface()

        # Save transposed data
        self._degree_u = degree_u_new
        self._degree_v = degree_v_new
        self._knot_vector_u = kv_u_new
        self._knot_vector_v = kv_v_new
        self._control_points = ctrlpts_new
        self._control_points_size_u = ctrlpts_new_sizeU
        self._control_points_size_v = ctrlpts_new_sizeV
        self._control_points2D = ctrlpts2D_new

    def surfpt(self, u=-1, v=-1, check_vars=True, get_ctrlpts=False):
        """ Evaluates the B-Spline surface at the given (u,v) parameters.

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :param check_vars: flag to disable variable checking (only for internal eval functions)
        :type check_vars: bool
        :param get_ctrlpts: flag to add a list of control points associated with the surface evaluation to the return value
        :param get_ctrlpts: bool
        :return: evaluated surface point at the given knot values
        :rtype: list
        """
        if check_vars:
            # Check all parameters are set before the surface evaluation
            self._check_variables()
            # Check u and v parameters are correct
            utils.check_uv(u, v)

        # Initialize an empty list which will contain the list of associated control points
        ctrlpts = []

        # Algorithm A3.5
        span_v = utils.find_span(self._degree_v, tuple(self._knot_vector_v), self._control_points_size_v, v)
        basis_v = utils.basis_functions(self._degree_v, tuple(self._knot_vector_v), span_v, v)
        span_u = utils.find_span(self._degree_u, tuple(self._knot_vector_u), self._control_points_size_u, u)
        basis_u = utils.basis_functions(self._degree_u, tuple(self._knot_vector_u), span_u, u)

        idx_u = span_u - self._degree_u
        spt = [0.0 for x in range(self._dimension)]

        for l in range(0, self._degree_v + 1):
            temp = [0.0 for x in range(self._dimension)]
            idx_v = span_v - self._degree_v + l
            for k in range(0, self._degree_u + 1):
                temp[:] = [tmp + (basis_u[k] * cp) for tmp, cp in zip(temp, self._control_points2D[idx_u + k][idx_v])]
                if get_ctrlpts:
                    ctrlpts.append(self._control_points2D[idx_u + k][idx_v])
            spt[:] = [pt + (basis_v[l] * tmp) for pt, tmp in zip(spt, temp)]

        if get_ctrlpts:
            return spt, ctrlpts
        return spt

    # Evaluates the B-Spline surface
    def evaluate(self):
        """ Evaluates the surface.

        .. note:: The evaluated surface points are stored in :py:attr:`~surfpts`.

        :return: None
        """
        # Check all parameters are set before the surface evaluation
        self._check_variables()
        # Clean up the surface points lists, if necessary
        self._reset_surface()

        for u in utils.frange(0, 1, self._delta):
            for v in utils.frange(0, 1, self._delta):
                spt = self.surfpt(u, v, False)
                self._surface_points.append(spt)

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
        self._check_variables()
        # Check u and v parameters are correct
        utils.check_uv(u, v)

        # Algorithm A3.6
        du = min(self._degree_u, order)
        dv = min(self._degree_v, order)

        SKL = [[[0.0 for x in range(self._dimension)] for y in range(dv + 1)] for z in range(du + 1)]

        span_u = utils.find_span(self._degree_u, tuple(self._knot_vector_u), self._control_points_size_u, u)
        bfunsders_u = utils.basis_functions_ders(self._degree_u, self._knot_vector_u, span_u, u, du)
        span_v = utils.find_span(self._degree_v, tuple(self._knot_vector_v), self._control_points_size_v, v)
        bfunsders_v = utils.basis_functions_ders(self._degree_v, self._knot_vector_v, span_v, v, dv)

        for k in range(0, du + 1):
            temp = [[] for y in range(self._degree_v + 1)]
            for s in range(0, self._degree_v + 1):
                temp[s] = [0.0 for x in range(self._dimension)]
                for r in range(0, self._degree_u + 1):
                    cu = span_u - self._degree_u + r
                    cv = span_v - self._degree_v + s
                    temp[s][:] = [tmp + (bfunsders_u[k][r] * cp) for tmp, cp in zip(temp[s], self._control_points2D[cu][cv])]

            dd = min(order - k, dv)
            for l in range(0, dd + 1):
                for s in range(0, self._degree_v + 1):
                    SKL[k][l][:] = [elem + (bfunsders_v[l][s] * tmp) for elem, tmp in zip(SKL[k][l], temp[s])]

        # Return the derivatives
        return SKL

    # Evaluates the surface tangent at the given (u, v) parameter
    def tangent(self, u=-1, v=-1, normalize=False):
        """ Evaluates the surface tangent at the given (u, v) parameter.

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :param normalize: if True, the returned tangent vector is converted to a unit vector
        :type normalize: bool
        :return: A list in the order of "surface point", "derivative w.r.t. u" and "derivative w.r.t. v"
        :rtype: list
        """
        # Tangent is the 1st derivative of the surface
        skl = self.derivatives(u, v, 1)

        # Doing this just for readability
        point = skl[0][0]
        der_u = skl[1][0]
        der_v = skl[0][1]

        # Normalize the tangent vectors
        if normalize:
            der_u = utils.vector_normalize(der_u)
            der_v = utils.vector_normalize(der_v)

        # Return the list of tangents w.r.t. u and v
        return tuple(point), der_u, der_v

    # Evaluates the surface normal at the given (u, v) parameter
    def normal(self, u=-1, v=-1, normalize=True):
        """ Evaluates the surface normal at the given (u, v) parameter.

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :param normalize: if True, the returned normal vector is converted to a unit vector
        :type normalize: bool
        :return: normal vector
        :rtype: list
        """
        # Check u and v parameters are correct for the normal evaluation
        utils.check_uv(u, v, test_normal=True, delta=self._delta)

        # Take the 1st derivative of the surface
        skl = self.derivatives(u, v, 1)

        # For readability
        der_u = skl[1][0]
        der_v = skl[0][1]

        # Compute normal
        normal = utils.vector_cross(der_u, der_v)

        if normalize:
            # Convert normal vector to a unit vector
            normal = utils.vector_normalize(tuple(normal))

        # Return the surface normal at the input u,v location
        return normal

    def insert_knot(self, u=-1, v=-1, r=1):
        """ Inserts the given knots and updates the control points array and the knot vectors.

        :param u: Knot to be inserted in U-direction
        :type u: float
        :param v: Knot to be inserted in V-direction
        :type v: float
        :param r: Number of knot insertions
        :type r: int
        :return: None
        """

        # Check all parameters are set before the curve evaluation
        self._check_variables()

        # Check if the parameter values are correctly defined
        if not u == -1 or not v == -1:
            utils.check_uv(u, v)

        if not isinstance(r, int) or r < 0:
            raise ValueError('Number of insertions must be a positive integer value.')

        # Algorithm A5.3
        s_u = utils.find_multiplicity(u, self._knot_vector_u)
        s_v = utils.find_multiplicity(v, self._knot_vector_v)

        # Check if it is possible add that many number of knots
        if r > self._degree_u - s_u:
            warnings.warn("Cannot insert " + str(r) + " number of knots in the U direction")
            return

        if r > self._degree_u - s_v:
            warnings.warn("Cannot insert " + str(r) + " number of knots in the V direction")
            return

        # Insert knot in U
        if u != -1:
            k = utils.find_span(self._degree_u, self._knot_vector_u, len(self._control_points), u)
            mp = len(self._knot_vector_u)
            p = self._degree_u
            s = s_u

            # Initialize new knot vector array
            UQ = [None for x in range(mp + r)]
            # Initialize new control points array (control points can be weighted or not)
            Q = [[None for v in range(self._control_points_size_v)] for u in range(self._control_points_size_u)]
            # Initialize a local array of length p + 1
            R = [None for x in range(p + 1)]

            # Load new knot vector
            for i in range(0, k + 1):
                UQ[i] = self._knot_vector_u[i]
            for i in range(1, r + 1):
                UQ[k + i] = u
            for i in range(k + 1, mp + 1):
                UQ[i + r] = self._knot_vector_u[i]

            # Save the alphas
            alpha = [[None for j in range(r + 1)] for i in range(p - r - s + 1)]
            for j in range(1, r + 1):
                L = k - p + j
                for i in range(0, p - j - s + 1):
                    alpha[i][j] = (u - self._knot_vector_u[L + i]) / (self._knot_vector_u[i + k + 1] - self._knot_vector_u[L + i])

            # For each row do
            for row in range(0, mp + 1):
                for i in range(0, k - p + 1):
                    Q[i][row] = self._control_points2D[i][row]
                for i in range(k - s, self._control_points_size_u + 1):
                    Q[i + r][row] = self._control_points2D[i][row]
                # Load auxiliary control points
                for i in range(0, p - s + 1):
                    R[i] = copy.deepcopy(self._control_points2D[k - p + i][row])
                # Insert the knot r times
                for j in range(1, r + 1):
                    L = k - p + j
                    for i in range(0, p - j - s + 1):
                        R[i][:] = [alpha[i][j] * elem2 + (1.0 - alpha[i][j]) * elem1 for elem1, elem2 in zip(R[i], R[i + 1])]
                    Q[L][row] = R[0]
                    Q[k + r - j - s][row] = R[p - j - s]
                # Load the remaining control points
                for i in range(L + 1, k - s):
                    Q[i][row] = R[i - L]

            # Update class variables for knot insertion in U-direction
            self._knot_vector_u = UQ
            self._control_points2D = Q

        # Insert knot in V
        if v != -1:
            k = utils.find_span(self._degree_v, self._knot_vector_v, len(self._control_points), v)
            mp = len(self._knot_vector_v)
            p = self._degree_v
            s = s_u

            # Initialize new knot vector array
            VQ = [None for x in range(mp + r)]
            # Initialize new control points array (control points can be weighted or not)
            Q = [[None for v in range(self._control_points_size_v)] for u in range(self._control_points_size_u)]
            # Initialize a local array of length p + 1
            R = [None for x in range(p + 1)]

            # Load new knot vector
            for i in range(0, k + 1):
                VQ[i] = self._knot_vector_v[i]
            for i in range(1, r + 1):
                VQ[k + i] = v
            for i in range(k + 1, mp + 1):
                VQ[i + r] = self._knot_vector_v[i]

            # Save the alphas
            alpha = [[None for j in range(r + 1)] for i in range(p - r - s + 1)]
            for j in range(1, r + 1):
                L = k - p + j
                for i in range(0, p - j - s + 1):
                    alpha[i][j] = (v - self._knot_vector_v[L + i]) / (self._knot_vector_v[i + k + 1] - self._knot_vector_v[L + i])

            # For each row do
            for row in range(0, mp + 1):
                for i in range(0, k - p + 1):
                    Q[row][i] = self._control_points2D[row][i]
                for i in range(k - s, self._control_points_size_u + 1):
                    Q[row][i + r] = self._control_points2D[row][i]
                # Load auxiliary control points
                for i in range(0, p - s + 1):
                    R[i] = copy.deepcopy(self._control_points2D[row][k - p + i])
                # Insert the knot r times
                for j in range(1, r + 1):
                    L = k - p + j
                    for i in range(0, p - j - s + 1):
                        R[i][:] = [alpha[i][j] * elem2 + (1.0 - alpha[i][j]) * elem1 for elem1, elem2 in zip(R[i], R[i + 1])]
                    Q[row][L] = R[0]
                    Q[row][k + r - j - s] = R[p - j - s]
                # Load the remaining control points
                for i in range(L + 1, k - s):
                    Q[row][i] = R[i - L]

            # Update class variables for knot insertion in U-direction
            self._knot_vector_v = VQ
            self._control_points2D = Q

        # Evaluate surface again if it has already been evaluated before knot insertion
        if self._surface_points:
            self.evaluate()
