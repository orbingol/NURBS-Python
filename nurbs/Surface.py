"""
    NURBS Python Package
    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2017
"""

import sys
import itertools
import numpy
import nurbs.utilities as utils


class Surface(object):

    def __init__(self):
        self._mDegreeU = 0
        self._mDegreeV = 0
        self._mKnotVectorU = []
        self._mKnotVectorV = []
        self._mCtrlPts = []
        self._mCtrlPts2D = []  # for now, in [v][u] format
        self._mCtrlPts_sizeU = 0  # columns
        self._mCtrlPts_sizeV = 0  # rows
        self._mWeights = []
        self._mDelta = 0.01
        self._mSurfPts = []
        self._mSurfPts2D = []  # for now, in [v][u] format

    @property
    def degree_u(self):
        return self._mDegreeU

    @degree_u.setter
    def degree_u(self, value):
        if value < 0:
            raise ValueError("Degree cannot be less than zero")
        self._mDegreeU = value

    @property
    def degree_v(self):
        return self._mDegreeV

    @degree_v.setter
    def degree_v(self, value):
        if value < 0:
            raise ValueError("Degree cannot be less than zero")
        self._mDegreeV = value

    @property
    def ctrlpts(self):
        ret_list = []
        for pt in self._mCtrlPts:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        # Control points array is a list of list of lists
        # First check v-direction
        if len(value) > self._mDegreeV + 1:
            raise ValueError("Number of control points in v-direction should be at least degree + 1")
        # Then, check u direction
        u_cnt = 0
        for u_coords in value:
            if len(u_coords) < self._mDegreeU + 1:
                raise ValueError("Number of control points in u-direction should be at least degree + 1")
            u_cnt += 1
            ctrlpts_u = []
            for coord in u_coords:
                # Save the control points as a list of 3D coordinates
                if len(coord) < 0 or len(coord) > 3:
                    raise ValueError("Please input 3D coordinates")
                # Convert to list of floats
                coord_float = [float(c) for c in coord]
                self._mCtrlPts.append(coord_float)
                # For storing 2D control points
                ctrlpts_u.append(coord_float)
            self._mCtrlPts2D.append([ctrlpts_u])

        # Set u and v sizes
        self._mCtrlPts_sizeU = u_cnt
        self._mCtrlPts_sizeV = len(value)
        # Automatically generate a weights vector of 1.0s in the size of ctrlpts array
        self._mWeights = [1.0] * self._mCtrlPts_sizeU * self._mCtrlPts_sizeV

    @property
    def ctrlpts2d(self):
        return self._mCtrlPts2D

    @property
    def weights(self):
        return tuple(self._mWeights)

    @weights.setter
    def weights(self, value):
        if len(value) != self._mCtrlPts_sizeU * self._mCtrlPts_sizeV:
            raise ValueError("Size of the weight vector should be equal to size of control points")
        value_float = [float(w) for w in value]
        self._mWeights = value_float

    @property
    def knotvector_u(self):
        return tuple(self._mKnotVectorU)

    @knotvector_u.setter
    def knotvector_u(self, value):
        value_float = [float(kv) for kv in value]
        self._mKnotVectorU = utils.normalize_knotvector(value_float)

    @property
    def knotvector_v(self):
        return tuple(self._mKnotVectorU)

    @knotvector_v.setter
    def knotvector_v(self, value):
        value_float = [float(kv) for kv in value]
        self._mKnotVectorV = utils.normalize_knotvector(value_float)

    @property
    def delta(self):
        return self._mDelta

    @delta.setter
    def delta(self, value):
        # Delta value for surface calculations should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface calculation delta should be between 0.0 and 1.0")
        self._mDelta = float(value)

    @property
    def ctrlptsw(self):
        ret_list = []
        for c, w in itertools.product(self._mCtrlPts, self._mWeights):
            temp = (float(c[0]*w), float(c[1]*w), float(c[2]*w), w)
            ret_list.append(temp)
        return tuple(ret_list)

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        # Start with clean lists
        ctrlpts_uv = []
        weights_uv = []
        # Split the weights vector from the input list for v-direction
        for udir in value:
            ctrlpts_u = []
            weights_u = []
            for i, c in enumerate(udir):
                temp_list = [float(c[0]/c[3]), float(c[1]/c[3]), float(c[2]/c[3])]
                ctrlpts_u.append(temp_list)
                weights_u.append(float(c[3]))
            ctrlpts_uv.append(ctrlpts_u)
            weights_uv.append(weights_u)
        # Assign unzipped values to the class fields
        self._mCtrlPts = ctrlpts_uv
        self._mWeights = weights_uv

    @property
    def surfpts(self):
        return self._mSurfPts

    @property
    def surfpts2d(self):
        return self._mSurfPts2D

    def read_ctrlpts(self, filename=''):
        try:
            # Open the file
            with open(filename, 'r') as fp:
                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    control_point_row = line.split(';')
                    self._mCtrlPts_sizeV = 0
                    ctrlpts_u = []
                    for cpr in control_point_row:
                        control_point = cpr.split(',')
                        # Create a temporary dictionary for appending coordinates into ctrlpts list
                        pt = [float(control_point[0]), float(control_point[1]), float(control_point[2])]
                        # Add control points to the global control point list
                        self._mCtrlPts.append(pt)
                        self._mCtrlPts_sizeV += 1
                        ctrlpts_u.append(pt)
                    self._mCtrlPts_sizeU += 1
                    self._mCtrlPts2D.append(ctrlpts_u)
            self._mWeights = [1.0] * self._mCtrlPts_sizeU * self._mCtrlPts_sizeV
        except IOError:
            print('Cannot open file ' + filename)
            sys.exit(1)

    def calculate(self):
        for v in numpy.arange(0.0, 1.0+self._mDelta, self._mDelta):
            span_v = utils.find_span(self._mDegreeV, tuple(self._mKnotVectorV), self._mCtrlPts_sizeV, v)
            basis_v = utils.basis_functions(self._mDegreeV, tuple(self._mKnotVectorV), span_v, v)
            surfpts_u = []
            for u in numpy.arange(0.0, 1.0+self._mDelta, self._mDelta):
                span_u = utils.find_span(self._mDegreeU, tuple(self._mKnotVectorU), self._mCtrlPts_sizeU, u)
                basis_u = utils.basis_functions(self._mDegreeU, tuple(self._mKnotVectorU), span_u, u)
                idx_u = span_u - self._mDegreeU
                surfpt = [0.0, 0.0, 0.0]
                for l in xrange(0, self._mDegreeV+1):
                    temp = [0.0, 0.0, 0.0]
                    idx_v = span_v - self._mDegreeV + l
                    for k in xrange(0, self._mDegreeU+1):
                        temp[0] += (basis_u[k] * self._mCtrlPts2D[idx_v][idx_u + k][0])
                        temp[1] += (basis_u[k] * self._mCtrlPts2D[idx_v][idx_u + k][1])
                        temp[2] += (basis_u[k] * self._mCtrlPts2D[idx_v][idx_u + k][2])
                    surfpt[0] += (basis_v[l] * temp[0])
                    surfpt[1] += (basis_v[l] * temp[1])
                    surfpt[2] += (basis_v[l] * temp[2])
                self._mSurfPts.append(surfpt)
                surfpts_u.append(surfpt)
            self._mSurfPts2D.append(surfpts_u)
