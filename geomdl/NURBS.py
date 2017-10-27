"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation class for NURBS curves and surfaces

.. moduleauthor:: Onur Rauf Bingol

"""

import sys
import itertools
import nurbs.utilities as utils


class Curve(object):
    """ A data storage and evaluation class for 3D NURBS curves.

    **Data Storage**

    :class:`.Curve` class implements Python properties using the ``@property`` decorator. The following properties are present in this class:

    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * weights
    * curvepts

    The function :func:`.read_ctrlpts()` provides an easy way to read weighted control points from a text file.
    Additional details for the text format can be found in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

    **Evaluation**

    The evaluation methods in the :class:`.Curve` class are:

    * :func:`.evaluate()`
    * :func:`.derivatives()`
    * :func:`.tangent()`

    Please check the function reference for the details.

    .. note::

        If you update any of the data storage elements after the curve evaluation, the surface points stored in :py:attr:`~curvepts` property will be deleted automatically.
    """
    def __init__(self):
        self._mDegree = 0
        self._mKnotVector = []
        self._mCtrlPtsW = []
        self._mDelta = 0.01
        self._mCurvePts = []
        self._mDimension = 4  # 3D points + weights

    @property
    def order(self):
        """ Curve order

        Defined as order = degree + 1

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

        Control points of a :class:`.Curve` is stored as a list of (x*w, y*w, w) coordinates

        :getter: Gets the control points in (x, y, z) format. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets the control points in (x*w, y*w, z*w, w) format
        :type: list
        """
        ret_list = []
        for pt in self._mCtrlPtsW:
            temp = (pt[0] / pt[3], pt[1] / pt[3], pt[2] / pt[3])
            ret_list.append(temp)
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        if len(value) < self._mDegree + 1:
            raise ValueError("ERROR: Number of control points in u-direction should be at least degree + 1")

        # Clean up the curve and control points lists, if necessary
        self._reset_curve()
        self._reset_ctrlpts()

        for coord in value:
            if len(coord) < 0 or len(coord) > 4:
                raise ValueError("ERROR: Please input weighted 3D coordinates")
            # Convert to list of floats
            coord_float = [float(c) for c in coord]
            self._mCtrlPtsW.append(coord_float)

    @property
    def weights(self):
        """ Weights vector

        :getter: Extracts the weights vector from weighted control points array
        :type: list
        """
        weights = []
        for pt in self._mCtrlPtsW:
            weights.append(pt[3])
        return tuple(weights)

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

        .. note:: The delta value is 0.1 by default.

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

        .. note:: :func:`.evaluate` should be called first.

        :getter: (x, y, z) coordinates of the evaluated curve points
        :type: list
        """
        return self._mCurvePts

    # Cleans up the control points and the weights (private)
    def _reset_ctrlpts(self):
        if self._mCtrlPtsW:
            # Delete control points
            del self._mCtrlPtsW[:]

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
        if not self._mCtrlPtsW:
            works = False
        if not self._mKnotVector:
            works = False
        if not works:
            raise ValueError("Some required parameters for curve evaluation are not set.")

    # Reads weighted control points from a text file
    def read_ctrlpts(self, filename=''):
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
                    pt = [float(coords[0].strip()), float(coords[1].strip()), float(coords[2].strip()), float(coords[3].strip())]
                    self._mCtrlPtsW.append(pt)
        except IOError:
            print('Cannot open file ' + filename)
            sys.exit(1)

    # Evaluates the NURBS curve
    def evaluate(self):
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
            span = utils.find_span(self._mDegree, tuple(self._mKnotVector), len(self.ctrlpts), u)
            basis = utils.basis_functions(self._mDegree, tuple(self._mKnotVector), span, u)
            cptw = [0.0 for x in range(self._mDimension)]
            for i in range(0, self._mDegree + 1):
                cptw[0] += (basis[i] * self._mCtrlPtsW[span - self._mDegree + i][0])
                cptw[1] += (basis[i] * self._mCtrlPtsW[span - self._mDegree + i][1])
                cptw[2] += (basis[i] * self._mCtrlPtsW[span - self._mDegree + i][2])
                cptw[3] += (basis[i] * self._mCtrlPtsW[span - self._mDegree + i][3])
            # Divide by weight
            curvept = [float(cptw[0] / cptw[3]), float(cptw[1] / cptw[3]), float(cptw[2] / cptw[3])]
            self._mCurvePts.append(curvept)
