"""
.. module:: BSpline
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation class for B-spline curves and surfaces

.. moduleauthor:: Onur Rauf Bingol

"""

import sys
import geomdl.utilities as utils


class Curve(object):
    """ A data storage and evaluation class for B-Spline curves.

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
        self._mDegree = 0
        self._mKnotVector = []
        self._mCtrlPts = []
        self._mDelta = 0.1
        self._mCurvePts = []

    @property
    def order(self):
        """ Curve order

        Follows the following equality: order = degree + 1

        :getter: Gets the curve order
        :setter: Sets the curve order
        :type: integer
        """
        return self._mDegree + 1

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
        return self._mDegree

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
        self._mDegree = value

    @property
    def ctrlpts(self):
        """ Control points

        Control points of a :class:`.Curve` is stored as a list of (x, y) coordinates

        :getter: Gets the control points
        :setter: Sets the control points
        :type: list
        """
        ret_list = []
        for pt in self._mCtrlPts:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        if len(value) < self._mDegree + 1:
            raise ValueError("ERROR: Number of control points in u-direction should be at least degree + 1")

        # Clean up the curve and control points lists, if necessary
        self._reset_curve()
        self._reset_ctrlpts()

        for coord in value:
            if len(coord) < 0 or len(coord) > 2:
                raise ValueError("ERROR: Please input 2D coordinates")
            # Convert to list of floats
            coord_float = [float(c) for c in coord]
            self._mCtrlPts.append(coord_float)

    @property
    def knotvector(self):
        """ Knot vector

        :getter: Gets the knot vector
        :setter: Sets the knot vector
        :type: list
        """
        return tuple(self._mKnotVector)

    @knotvector.setter
    def knotvector(self, value):
        # Clean up the surface points lists, if necessary
        self._reset_curve()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        # Normalize and set the knot vector
        self._mKnotVector = utils.knotvector_normalize(tuple(value_float))

    @property
    def delta(self):
        """ Curve evaluation delta

        .. note:: The delta value is 0.01 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self._mDelta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("ERROR: Curve evaluation delta should be between 0.0 and 1.0")
        # Clean up the curve points list, if necessary
        self._reset_curve()
        # Set a new delta value
        self._mDelta = float(value)

    @property
    def curvepts(self):
        """ Evaluated curve points

        .. note:: :func:`.evaluate` or :func:`.evaluate_rational` should be called first.

        :getter: (x, y) coordinates of the evaluated surface points
        :type: list
        """
        return self._mCurvePts

    # Cleans up the control points
    def _reset_ctrlpts(self):
        if self._mCtrlPts:
            # Delete control points
            del self._mCtrlPts[:]

    # Cleans the evaluated curve points (private)
    def _reset_curve(self):
        if self._mCurvePts:
            # Delete the curve points
            del self._mCurvePts[:]

    # Checks whether the curve evaluation is possible or not (private)
    def _check_variables(self):
        works = True
        # Check degree values
        if self._mDegree == 0:
            works = False
        if not self._mCtrlPts:
            works = False
        if not self._mKnotVector:
            works = False
        if not works:
            raise ValueError("Some required parameters for curve evaluation are not set.")

    # Reads control points from a text file
    def read_ctrlpts(self, filename=''):
        """ Reads control points from a text file.

        .. note:: The format of the text files is described in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

        :param filename: input file name
        :type filename: string
        :return: None
        """
        # Clean up the curve and control points lists, if necessary
        self._reset_curve()
        self._reset_ctrlpts()

        # Try reading the file
        try:
            # Open the file
            with open(filename, 'r') as fp:
                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    coords = line.split(',')
                    # Remove extra whitespace and convert to float
                    pt = [float(coords[0].strip()), float(coords[1].strip())]
                    self._mCtrlPts.append(pt)
        except IOError:
            print('Cannot open file ' + filename)
            sys.exit(1)

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

        # Algorithm A3.1
        for u in utils.frange(0, 1, self._mDelta):
            span = utils.find_span(self._mDegree, tuple(self._mKnotVector), len(self._mCtrlPts), u)
            basis = utils.basis_functions(self._mDegree, tuple(self._mKnotVector), span, u)
            curvept = [0.0, 0.0]
            for i in range(0, self._mDegree + 1):
                curvept[0] += (basis[i] * self._mCtrlPts[span - self._mDegree + i][0])
                curvept[1] += (basis[i] * self._mCtrlPts[span - self._mDegree + i][1])
            self._mCurvePts.append(curvept)

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
        self._check_variables()
        # Check u parameters are correct
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')

        # Algorithm A3.2: CurveDerivsAlg1
        du = min(self._mDegree, order)

        CK = [[None for x in range(2)] for y in range(order + 1)]
        for k in range(self._mDegree+1, order+1):
            CK[k] = [0.0 for x in range(2)]

        span = utils.find_span(self._mDegree, tuple(self._mKnotVector), len(self._mCtrlPts), u)
        bfunsders = utils.basis_functions_ders(self._mDegree, tuple(self._mKnotVector), span, u, du)

        for k in range(0, du+1):
            CK[k] = [0.0 for x in range(2)]
            for j in range(0, self._mDegree+1):
                CK[k][0] += (bfunsders[k][j] * self._mCtrlPts[span - self._mDegree + j][0])
                CK[k][1] += (bfunsders[k][j] * self._mCtrlPts[span - self._mDegree + j][1])

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
        PK = [[[None for x in range(0, 2)] for y in range(r + 1)] for z in range(order + 1)]
        for i in range(0, r + 1):
            PK[0][i][0] = self._mCtrlPts[r1 + i][0]
            PK[0][i][1] = self._mCtrlPts[r1 + i][1]

        for k in range(1, order + 1):
            tmp = self._mDegree - k + 1
            for i in range(0, r - k + 1):
                PK[k][i][0] = tmp * (PK[k - 1][i + 1][0] - PK[k - 1][i][0]) /(self._mKnotVector[r1 + i + self._mDegree + 1] - self._mKnotVector[r1 + i + k])
                PK[k][i][1] = tmp * (PK[k - 1][i + 1][1] - PK[k - 1][i][1]) /(self._mKnotVector[r1 + i + self._mDegree + 1] - self._mKnotVector[r1 + i + k])

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
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')

        # Algorithm A3.4: CurveDerivsAlg2
        du = min(self._mDegree, order)

        CK = [[None for x in range(2)] for y in range(order + 1)]
        for k in range(self._mDegree + 1, order + 1):
            CK[k] = [0.0 for x in range(2)]

        span = utils.find_span(self._mDegree, tuple(self._mKnotVector), len(self._mCtrlPts), u)
        bfuns = utils.basis_functions_all(self._mDegree, tuple(self._mKnotVector), span, u)
        PK = self.derivatives_ctrlpts(du, span - self._mDegree, span)

        for k in range(0, du + 1):
            CK[k] = [0.0 for x in range(2)]
            for j in range(0, self._mDegree - k + 1):
                CK[k][0] += (bfuns[j][self._mDegree - k] * PK[k][j][0])
                CK[k][1] += (bfuns[j][self._mDegree - k] * PK[k][j][1])

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
        self._mDegreeU = 0
        self._mDegreeV = 0
        self._mKnotVectorU = []
        self._mKnotVectorV = []
        self._mCtrlPts = []
        self._mCtrlPts2D = []  # in [u][v] format
        self._mCtrlPts_sizeU = 0  # columns
        self._mCtrlPts_sizeV = 0  # rows
        self._mDelta = 0.1
        self._mSurfPts = []

    @property
    def order_u(self):
        """ Surface order for U direction

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for U direction
        :setter: Sets the surface order for U direction
        :type: integer
        """
        return self._mDegreeU + 1

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
        return self._mDegreeV + 1

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
        return self._mDegreeU

    @degree_u.setter
    def degree_u(self, value):
        if value < 0:
            raise ValueError("Degree cannot be less than zero.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set degree u
        self._mDegreeU = value

    @property
    def degree_v(self):
        """ Surface degree for V direction

        :getter: Gets the surface degree V for V direction
        :setter: Sets the surface degree V for V direction
        :type: integer
        """
        return self._mDegreeV

    @degree_v.setter
    def degree_v(self, value):
        if value < 0:
            raise ValueError("Degree cannot be less than zero.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set degree v
        self._mDegreeV = value

    @property
    def ctrlpts(self):
        """ Control points

        Control points of a :class:`.Surface` is stored as a list of (x, y, z) coordinates

        :getter: Gets the control points
        :setter: Sets the control points
        :type: list
        """
        ret_list = []
        for pt in self._mCtrlPts:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        # Clean up the surface and control points lists, if necessary
        self._reset_surface()
        self._reset_ctrlpts()

        # First check v-direction
        if len(value) < self._mDegreeV + 1:
            raise ValueError("Number of control points in v-direction should be at least degree + 1.")
        # Then, check U direction
        u_cnt = 0
        for u_coords in value:
            if len(u_coords) < self._mDegreeU + 1:
                raise ValueError("Number of control points in u-direction should be at least degree + 1.")
            u_cnt += 1
            for coord in u_coords:
                # Save the control points as a list of 3D coordinates
                if len(coord) < 0 or len(coord) > 3:
                    raise ValueError("Please input 3D coordinates")
                # Convert to list of floats
                coord_float = [float(c) for c in coord]
                self._mCtrlPts.append(coord_float)
        # Set u and v sizes
        self._mCtrlPts_sizeU = u_cnt
        self._mCtrlPts_sizeV = len(value)
        # Generate a 2D list of control points
        for i in range(0, self._mCtrlPts_sizeU):
            ctrlpts_v = []
            for j in range(0, self._mCtrlPts_sizeV):
                ctrlpts_v.append(self._mCtrlPts[i + (j * self._mCtrlPts_sizeU)])
            self._mCtrlPts2D.append(ctrlpts_v)

    @property
    def ctrlpts2d(self):
        """ Control points

        2D control points in [u][v] format.

        :getter: Gets the control points
        :type: list
        """
        return self._mCtrlPts2D

    @property
    def knotvector_u(self):
        """ Knot vector for U direction

        :getter: Gets the knot vector for U direction
        :setter: Sets the knot vector for U direction
        :type: list
        """
        return tuple(self._mKnotVectorU)

    @knotvector_u.setter
    def knotvector_u(self, value):
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        self._mKnotVectorU = utils.knotvector_normalize(tuple(value_float))

    @property
    def knotvector_v(self):
        """ Knot vector for V direction

        :getter: Gets the knot vector for V direction
        :setter: Sets the knot vector for V direction
        :type: list
        """
        return tuple(self._mKnotVectorV)

    @knotvector_v.setter
    def knotvector_v(self, value):
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        self._mKnotVectorV = utils.knotvector_normalize(tuple(value_float))

    @property
    def delta(self):
        """ Surface evaluation delta

        .. note:: The delta value is 0.01 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self._mDelta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta should be between 0.0 and 1.0.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set a new delta value
        self._mDelta = float(value)

    @property
    def surfpts(self):
        """ Evaluated surface points

        .. note:: :func:`.evaluate` or :func:`.evaluate_rational` should be called first.

        :getter: (x, y, z) coordinates of the evaluated surface points
        :type: list
        """
        return self._mSurfPts

    # Cleans up the control points
    def _reset_ctrlpts(self):
        if self._mCtrlPts:
            # Delete control points
            del self._mCtrlPts[:]
            del self._mCtrlPts2D[:]
            # Set the control point sizes to zero
            self._mCtrlPts_sizeU = 0
            self._mCtrlPts_sizeV = 0

    # Cleans the evaluated surface points (private)
    def _reset_surface(self):
        if self._mSurfPts:
            # Delete the surface points
            del self._mSurfPts[:]

    # Checks whether the surface evaluation is possible or not (private)
    def _check_variables(self):
        works = True
        if self._mDegreeU == 0 or self._mDegreeV == 0:
            works = False
        if not self._mCtrlPts:
            works = False
        if not self._mKnotVectorU or not self._mKnotVectorV:
            works = False
        if not works:
            raise ValueError("Some required parameters for surface evaluation are not set.")

    # Reads control points from a text file
    def read_ctrlpts(self, filename=''):
        """ Reads control points from a text file.

        .. note:: The format of the text files is described in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

        :param filename: input file name
        :type filename: string
        :return: None
        """
        # Clean up the surface and control points lists, if necessary
        self._reset_ctrlpts()
        self._reset_surface()

        # Try reading the file
        try:
            # Open the file
            with open(filename, 'r') as fp:
                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    control_point_row = line.split(';')
                    self._mCtrlPts_sizeU = 0
                    for cpr in control_point_row:
                        cpt = cpr.split(',')
                        # Create a temporary dictionary for appending coordinates into ctrlpts list
                        pt = [float(cpt[0]), float(cpt[1]), float(cpt[2])]
                        # Add control points to the global control point list
                        self._mCtrlPts.append(pt)
                        self._mCtrlPts_sizeU += 1
                    self._mCtrlPts_sizeV += 1
            # Generate a 2D list of control points
            for i in range(0, self._mCtrlPts_sizeU):
                ctrlpts_v = []
                for j in range(0, self._mCtrlPts_sizeV):
                    ctrlpts_v.append(self._mCtrlPts[i + (j * self._mCtrlPts_sizeU)])
                self._mCtrlPts2D.append(ctrlpts_v)
        except IOError:
            print('ERROR: Cannot open file ' + filename)
            sys.exit(1)

    # Transposes the surface by swapping U and V directions
    def transpose(self):
        """ Transposes the surface by swapping U and V directions.

        :return: None
        """
        # Transpose existing data
        degree_u_new = self._mDegreeV
        degree_v_new = self._mDegreeU
        kv_u_new = self._mKnotVectorV
        kv_v_new = self._mKnotVectorU
        ctrlpts2D_new = []
        for v in range(0, self._mCtrlPts_sizeV):
            ctrlpts_u = []
            for u in range(0, self._mCtrlPts_sizeU):
                temp = self._mCtrlPts2D[u][v]
                ctrlpts_u.append(temp)
            ctrlpts2D_new.append(ctrlpts_u)
        ctrlpts_new_sizeU = self._mCtrlPts_sizeV
        ctrlpts_new_sizeV = self._mCtrlPts_sizeU

        ctrlpts_new = []
        for v in range(0, ctrlpts_new_sizeV):
            for u in range(0, ctrlpts_new_sizeU):
                ctrlpts_new.append(ctrlpts2D_new[u][v])

        # Clean up the surface points lists, if necessary
        self._reset_surface()

        # Save transposed data
        self._mDegreeU = degree_u_new
        self._mDegreeV = degree_v_new
        self._mKnotVectorU = kv_u_new
        self._mKnotVectorV = kv_v_new
        self._mCtrlPts = ctrlpts_new
        self._mCtrlPts_sizeU = ctrlpts_new_sizeU
        self._mCtrlPts_sizeV = ctrlpts_new_sizeV
        self._mCtrlPts2D = ctrlpts2D_new

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

        # Algorithm A3.5
        for v in utils.frange(0, 1, self._mDelta):
            span_v = utils.find_span(self._mDegreeV, tuple(self._mKnotVectorV), self._mCtrlPts_sizeV, v)
            basis_v = utils.basis_functions(self._mDegreeV, tuple(self._mKnotVectorV), span_v, v)
            for u in utils.frange(0, 1, self._mDelta):
                span_u = utils.find_span(self._mDegreeU, tuple(self._mKnotVectorU), self._mCtrlPts_sizeU, u)
                basis_u = utils.basis_functions(self._mDegreeU, tuple(self._mKnotVectorU), span_u, u)
                idx_u = span_u - self._mDegreeU
                surfpt = [0.0, 0.0, 0.0]
                for l in range(0, self._mDegreeV + 1):
                    temp = [0.0, 0.0, 0.0]
                    idx_v = span_v - self._mDegreeV + l
                    for k in range(0, self._mDegreeU + 1):
                        temp[0] += (basis_u[k] * self._mCtrlPts2D[idx_u + k][idx_v][0])
                        temp[1] += (basis_u[k] * self._mCtrlPts2D[idx_u + k][idx_v][1])
                        temp[2] += (basis_u[k] * self._mCtrlPts2D[idx_u + k][idx_v][2])
                    surfpt[0] += (basis_v[l] * temp[0])
                    surfpt[1] += (basis_v[l] * temp[1])
                    surfpt[2] += (basis_v[l] * temp[2])
                self._mSurfPts.append(surfpt)

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
        du = min(self._mDegreeU, order)
        dv = min(self._mDegreeV, order)

        SKL = [[[0.0 for x in range(3)] for y in range(dv + 1)] for z in range(du + 1)]

        span_u = utils.find_span(self._mDegreeU, tuple(self._mKnotVectorU), self._mCtrlPts_sizeU, u)
        bfunsders_u = utils.basis_functions_ders(self._mDegreeU, self._mKnotVectorU, span_u, u, du)
        span_v = utils.find_span(self._mDegreeV, tuple(self._mKnotVectorV), self._mCtrlPts_sizeV, v)
        bfunsders_v = utils.basis_functions_ders(self._mDegreeV, self._mKnotVectorV, span_v, v, dv)

        for k in range(0, du + 1):
            temp = [[] for y in range(self._mDegreeV + 1)]
            for s in range(0, self._mDegreeV + 1):
                temp[s] = [0.0 for x in range(3)]
                for r in range(0, self._mDegreeU + 1):
                    cu = span_u - self._mDegreeU + r
                    cv = span_v - self._mDegreeV + s
                    temp[s][0] += (bfunsders_u[k][r] * self._mCtrlPts2D[cu][cv][0])
                    temp[s][1] += (bfunsders_u[k][r] * self._mCtrlPts2D[cu][cv][1])
                    temp[s][2] += (bfunsders_u[k][r] * self._mCtrlPts2D[cu][cv][2])
            dd = min(order - k, dv)
            for l in range(0, dd + 1):
                for s in range(0, self._mDegreeV + 1):
                    SKL[k][l][0] += (bfunsders_v[l][s] * temp[s][0])
                    SKL[k][l][1] += (bfunsders_v[l][s] * temp[s][1])
                    SKL[k][l][2] += (bfunsders_v[l][s] * temp[s][2])

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
        utils.check_uv(u, v, test_normal=True, delta=self._mDelta)

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
