"""
.. module:: Curve
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation class for B-spline and NURBS curves

.. moduleauthor:: Onur Rauf Bingol

"""

import sys
import itertools
import nurbs.utilities as utils


class Curve(object):
    """ A data storage and evaluation class for B-Spline and NURBS curves.

    **Data Storage**

    :class:`.Curve` class implements Python properties using the ``@property`` decorator. The following properties are present in this class:

    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * ctrlptsw
    * weights
    * curvepts

    The functions :func:`.read_ctrlpts()` and :func:`.read_ctrlptsw()` provide an easy way to read control points from a text file.
    Additional details for the text format can be found in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

    **Evaluation**

    The evaluation methods in the :class:`.Curve` class are:

    * :func:`.evaluate()`
    * :func:`.evaluate_rational()`
    * :func:`.derivatives()`
    * :func:`.tangent()`

    **Examples**

    Please see the examples in the repository named as ``ex_curveXX.py``, where ``XX`` is the example number, for details on using the :class:`.Curve` class

    .. note::

        If you update any of the data storage elements after the curve evaluation, the surface points stored in :py:attr:`~curvepts` property will be deleted automatically.
    """
    def __init__(self):
        self._mDegree = 0
        self._mKnotVector = []
        self._mCtrlPts = []
        self._mWeights = []
        self._mDelta = 0.01
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

        # Automatically generate a weights vector of 1.0s in the size of ctrlpts array
        self._mWeights = [1.0] * len(value)

    @property
    def weights(self):
        """ Weights vector

        .. note:: :py:attr:`~ctrlpts` property and :func:`.read_ctrlpts()` will automatically generate a weights vector of 1.0s in the size of control points array.

        :getter: Gets the weights vector
        :setter: Sets the weights vector
        :type: list
        """
        return tuple(self._mWeights)

    @weights.setter
    def weights(self, value):
        if len(value) != len(self._mCtrlPts):
            raise ValueError("ERROR: Size of the weight vector should be equal to size of control points")
        # Clean up the curve points list, if necessary
        self._reset_curve()
        # Set weights vector
        value_float = [float(w) for w in value]
        self._mWeights = value_float

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
    def ctrlptsw(self):
        """ Weighted control points

        Returns and accepts a tuple containing (x*w, y*w, w) values. The setter method automatically separates
        the weights vector and compute the unweighted control points.

        :getter: Gets the weighted control points
        :setter: Sets the weights vector and the control points
        :type: list
        """
        ret_list = []
        for c, w in itertools.product(self._mCtrlPts, self._mWeights):
            temp_list = (float(c[0] * float(w)), float(c[1] * float(w)), float(w))
            ret_list.append(temp_list)
        return tuple(ret_list)

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        # Start with clean lists
        ctrlpts = []
        weights = []
        # Split the weights vector from the input list
        for i, c in enumerate(value):
            temp_list = [float(c[0]) / float(c[2]), float(c[1]) / float(c[2])]
            ctrlpts.append(temp_list)
            weights.append(float(c[2]))
        # Assign unzipped values to the class fields
        self._mCtrlPts = ctrlpts
        self._mWeights = weights

    @property
    def curvepts(self):
        """ Evaluated curve points

        .. note:: :func:`.evaluate` or :func:`.evaluate_rational` should be called first.

        :getter: (x, y) coordinates of the evaluated surface points
        :type: list
        """
        return self._mCurvePts

    # Cleans up the control points and the weights (private)
    def _reset_ctrlpts(self):
        if self._mCtrlPts:
            # Delete control points
            del self._mCtrlPts[:]
            # Delete weight vector
            del self._mWeights[:]

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

    # Reads control points from a text file and generates a weights vector composed of 1.0s
    def read_ctrlpts(self, filename=''):
        """ Reads control points from a text file and generates a weight vector composed of 1.0s.

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
            self._mWeights = [1.0] * len(self._mCtrlPts)
        except IOError:
            print('Cannot open file ' + filename)
            sys.exit(1)

    # Reads weighted control points from a text file
    def read_ctrlptsw(self, filename=''):
        """ Reads weighted control points from a text file.

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
                    pt = [float(coords[0].strip()) / float(coords[2].strip()),
                          float(coords[1].strip()) / float(coords[2].strip())]
                    # Add the control point to the global control point list
                    self._mCtrlPts.append(pt)
                    # Add the weight to the global weights list
                    self._mWeights.append(float(coords[2].strip()))
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

    # Evaluates the NURBS curve
    def evaluate_rational(self):
        """ Evaluates the NURBS curve.

        .. note:: The evaluated surface points are stored in :py:attr:`~curvepts`.

        :return: None
        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()
        # Clean up the curve points, if necessary
        self._reset_curve()

        # Algorithm A4.1
        for u in utils.frange(0, 1, self._mDelta):
            span = utils.find_span(self._mDegree, tuple(self._mKnotVector), len(self._mCtrlPts), u)
            basis = utils.basis_functions(self._mDegree, tuple(self._mKnotVector), span, u)
            curveptw = [0.0, 0.0, 0.0]
            for i in range(0, self._mDegree + 1):
                curveptw[0] += (basis[i] * (self._mCtrlPts[span - self._mDegree + i][0] * self._mWeights[span - self._mDegree + i]))
                curveptw[1] += (basis[i] * (self._mCtrlPts[span - self._mDegree + i][1] * self._mWeights[span - self._mDegree + i]))
                curveptw[2] += (basis[i] * self._mWeights[span - self._mDegree + i])
            # Divide by weight
            curvept = [float(curveptw[0] / curveptw[2]), float(curveptw[1] / curveptw[2])]
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
