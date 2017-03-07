"""
    NURBS Python Package
    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2017
"""

import sys
import itertools
import nurbs.utilities as utils


class Curve(object):

    def __init__(self):
        self._mDegree = 0
        self._mKnotVector = []
        self._mCtrlPts = []
        self._mWeights = []
        self._mDelta = 0.01
        self._mCurvePts = []

    @property
    def degree(self):
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
        return tuple(self._mKnotVector)

    @knotvector.setter
    def knotvector(self, value):
        # Clean up the surface points lists, if necessary
        self._reset_curve()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        # Normalize and set the knot vector
        self._mKnotVector = utils.normalize_knotvector(value_float)

    @property
    def delta(self):
        return self._mDelta

    @delta.setter
    def delta(self, value):
        # Delta value for surface calculations should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("ERROR: Curve calculation delta should be between 0.0 and 1.0")
        # Clean up the curve points list, if necessary
        self._reset_curve()
        # Set a new delta value
        self._mDelta = float(value)

    @property
    def ctrlptsw(self):
        ret_list = []
        for c,w in itertools.product(self._mCtrlPts, self._mWeights):
            temp_list = (float(c[0]*w), float(c[1]*w), float(w))
            ret_list.append(temp_list)
        return tuple(ret_list)

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        # Start with clean lists
        ctrlpts = []
        weights = []
        # Split the weights vector from the input list
        for i, c in enumerate(value):
            temp_list = [float(c[0]/c[2]), float(c[1]/c[2])]
            ctrlpts.append(temp_list)
            weights.append(float(c[2]))
        # Assign unzipped values to the class fields
        self._mCtrlPts = ctrlpts
        self._mWeights = weights

    @property
    def curvepts(self):
        return self._mCurvePts

    def _reset_ctrlpts(self):
        if self._mCtrlPts:
            # Delete control points
            del self._mCtrlPts[:]
            # Delete weight vector
            del self._mWeights[:]

    def _reset_curve(self):
        if self._mCurvePts:
            # Delete the calculated curve points
            del self._mCurvePts[:]

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
            raise ValueError("Some required parameters for calculations are not set.")

    def read_ctrlpts(self, filename=''):
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

    def evaluate(self):
        # Check all parameters are set before calculations
        self._check_variables()
        # Clean up the curve points, if necessary
        self._reset_curve()

        # Algorithm A3.1
        for u in utils.frange(0, 1, self._mDelta):
            span = utils.find_span(self._mDegree, tuple(self._mKnotVector), len(self._mCtrlPts), u)
            basis = utils.basis_functions(self._mDegree, tuple(self._mKnotVector), span, u)
            curvept = [0.0, 0.0]
            for i in range(0, self._mDegree+1):
                curvept[0] += (basis[i] * self._mCtrlPts[span - self._mDegree + i][0])
                curvept[1] += (basis[i] * self._mCtrlPts[span - self._mDegree + i][1])
            self._mCurvePts.append(curvept)

    def evaluatew(self):
        # Check all parameters are set before calculations
        self._check_variables()
        # Clean up the curve points, if necessary
        self._reset_curve()

        # Algorithm A4.1
        for u in utils.frange(0, 1, self._mDelta):
            span = utils.find_span(self._mDegree, tuple(self._mKnotVector), u)
            basis = utils.basis_functions(self._mDegree, tuple(self._mKnotVector), span, u)
            curveptw = [0.0, 0.0, 0.0]
            for i in range(0, self._mDegree+1):
                curveptw[0] += (basis[i] * self._mCtrlPts[span - self._mDegree + i][0])
                curveptw[1] += (basis[i] * self._mCtrlPts[span - self._mDegree + i][1])
                curveptw[2] += (basis[i] * self._mWeights[span - self._mDegree + i])
            # Divide by weight
            curvept = [float(curveptw[0] / curveptw[2]), float(curveptw[1] / curveptw[2])]
            self._mCurvePts.append(curvept)

    def derivatives(self, u=-1, order=0):
        # Check all parameters are set before calculations
        self._check_variables()
        # Check u parameters are correct
        if u < 0.0 or u > 1.0:
            raise ValueError('"u" value should be between 0 and 1.')

        # Algorithm A3.2
        du = min(self._mDegree, order)

        CK = [[None for x in range(2)] for y in range(order + 1)]
        for k in range(self._mDegree+1, order+1):
            CK[k] = [0.0, 0.0]

        span = utils.find_span(self._mDegree, tuple(self._mKnotVector), len(self._mCtrlPts), u)
        bfunsders = utils.basis_functions_ders(self._mDegree, tuple(self._mKnotVector), span, u, du)
        
        for k in range(0, du+1):
            CK[k] = [0.0, 0.0]
            for j in range(0, self._mDegree+1):
                CK[k][0] += (bfunsders[k][j] * self._mCtrlPts[span - self._mDegree + j][0])
                CK[k][1] += (bfunsders[k][j] * self._mCtrlPts[span - self._mDegree + j][1])

        # Return calculated derivatives
        return CK

    def tangent(self, u=-1):
        # Tangent is the 1st derivative of the curve
        ck = self.derivatives(u, 1)
        # Return the 1st derivative
        return ck[1]
