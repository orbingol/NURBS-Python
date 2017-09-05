"""
.. module:: Surface
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation class for B-spline and NURBS surfaces

.. moduleauthor:: Onur Rauf Bingol

"""

import sys
import itertools
import nurbs.utilities as utils


class Surface(object):
    """ A data storage and evaluation class for B-Spline and NURBS surfaces.

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
    * ctrlptsw
    * ctrlpts2D
    * weights
    * surfpts

    The functions :func:`.read_ctrlpts()` and :func:`.read_ctrlptsw()` provide an easy way to read control points from a text file.
    Additional details for the text format can be found in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

    **Evaluation**

    The evaluation methods in the :class:`.Surface` class are:

    * :func:`.evaluate()`
    * :func:`.evaluate_rational()`
    * :func:`.derivatives()`
    * :func:`.tangent()`
    * :func:`.normal()`

    **Examples**

    Please see the examples in the repository named as ``ex_surfaceXX.py``, where ``XX`` is the example number, for details on using the :class:`.Surface` class

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
        self._mWeights = []
        self._mDelta = 0.01
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
        # Automatically generate a weights vector of 1.0s in the size of ctrlpts array
        self._mWeights = [1.0] * self._mCtrlPts_sizeU * self._mCtrlPts_sizeV

    @property
    def ctrlpts2d(self):
        """ Control points

        2D control points in [u][v] format.

        :getter: Gets the control points
        :type: list
        """
        return self._mCtrlPts2D

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
        if len(value) != self._mCtrlPts_sizeU * self._mCtrlPts_sizeV:
            raise ValueError("Size of the weight vector should be equal to size of control points.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set weights vector
        value_float = [float(w) for w in value]
        self._mWeights = value_float

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
    def ctrlptsw(self):
        """ Weighted control points

        This property is a tuple containing (x*w, y*w, z*w, w) values.
        The setter method automatically separates the weights vector from the input and computes the unweighted control points.

        :getter: Gets the weighted control points
        :setter: Sets the weights vector and the control points
        :type: list
        """
        ret_list = []
        for c, w in itertools.product(self._mCtrlPts, self._mWeights):
            temp = (float(c[0]) * float(w), float(c[1]) * float(w), float(c[2]) * float(w), float(w))
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
                temp_list = [float(c[0]) / float(c[3]), float(c[1]) / float(c[3]), float(c[2]) / float(c[3])]
                ctrlpts_u.append(temp_list)
                weights_u.append(float(c[3]))
            ctrlpts_uv.append(ctrlpts_u)
            weights_uv.append(weights_u)
        # Assign unzipped values to the class fields
        self._mCtrlPts = ctrlpts_uv
        self._mWeights = weights_uv

    @property
    def surfpts(self):
        """ Evaluated surface points

        .. note:: :func:`.evaluate` or :func:`.evaluate_rational` should be called first.

        :getter: (x, y, z) coordinates of the evaluated surface points
        :type: list
        """
        return self._mSurfPts

    # Cleans up the control points and the weights (private)
    def _reset_ctrlpts(self):
        if self._mCtrlPts:
            # Delete control points
            del self._mCtrlPts[:]
            del self._mCtrlPts2D[:]
            # Delete weight vector
            del self._mWeights[:]
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
        # Check degree values
        if self._mDegreeU == 0 or self._mDegreeV == 0:
            works = False

        if not self._mCtrlPts:
            works = False

        if not self._mKnotVectorU or not self._mKnotVectorV:
            works = False

        if not works:
            raise ValueError("Some required parameters for surface evaluation are not set.")

    # Reads control points from a text file and generates a weight vector composed of 1.0s
    def read_ctrlpts(self, filename=''):
        """ Reads control points from a text file and generates a weight vector composed of 1.0s.

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
            # Generate a 1D list of weights
            self._mWeights = [1.0] * self._mCtrlPts_sizeU * self._mCtrlPts_sizeV
        except IOError:
            print('ERROR: Cannot open file ' + filename)
            sys.exit(1)

    # Reads weighted control points from a text file
    def read_ctrlptsw(self, filename=''):
        """ Reads weighted control points from a text file.

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
                        pt = [float(cpt[0]) / float(cpt[3]), float(cpt[1]) / float(cpt[3]),
                              float(cpt[2]) / float(cpt[3])]
                        self._mWeights.append(float(cpt[3]))
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
        weights_new = []
        for v in range(0, ctrlpts_new_sizeV):
            for u in range(0, ctrlpts_new_sizeU):
                ctrlpts_new.append(ctrlpts2D_new[u][v])
                weights_new.append(self._mWeights[v + (u * ctrlpts_new_sizeV)])

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
        self._mWeights = weights_new

    # Evaluates the B-Spline surface
    def evaluate(self):
        """ Evaluates the B-Spline surface.

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

    # Evaluates the NURBS surface
    def evaluate_rational(self):
        """ Evaluates the NURBS surface.

        .. note:: The evaluated surface points are stored in :py:attr:`~surfpts`.

        :return: None
        """
        # Check all parameters are set before the surface evaluation
        self._check_variables()
        # Clean up the surface points lists, if necessary
        self._reset_surface()

        # Prepare a 2D weighted control points array
        ctrlptsw = []
        c_u = 0
        while c_u < self._mCtrlPts_sizeU:
            ctrlptsw_v = []
            c_v = 0
            while c_v < self._mCtrlPts_sizeV:
                temp = [self._mCtrlPts2D[c_u][c_v][0] * self._mWeights[c_u + (c_v * self._mCtrlPts_sizeU)],
                        self._mCtrlPts2D[c_u][c_v][1] * self._mWeights[c_u + (c_v * self._mCtrlPts_sizeU)],
                        self._mCtrlPts2D[c_u][c_v][2] * self._mWeights[c_u + (c_v * self._mCtrlPts_sizeU)],
                        self._mWeights[c_u + (c_v * self._mCtrlPts_sizeU)]]
                ctrlptsw_v.append(temp)
                c_v += 1
            ctrlptsw.append(ctrlptsw_v)
            c_u += 1

        # Algorithm A4.3
        for v in utils.frange(0, 1, self._mDelta):
            span_v = utils.find_span(self._mDegreeV, tuple(self._mKnotVectorV), self._mCtrlPts_sizeV, v)
            basis_v = utils.basis_functions(self._mDegreeV, tuple(self._mKnotVectorV), span_v, v)
            for u in utils.frange(0, 1, self._mDelta):
                span_u = utils.find_span(self._mDegreeU, tuple(self._mKnotVectorU), self._mCtrlPts_sizeU, u)
                basis_u = utils.basis_functions(self._mDegreeU, tuple(self._mKnotVectorU), span_u, u)
                idx_u = span_u - self._mDegreeU
                surfptw = [0.0, 0.0, 0.0, 0.0]
                for l in range(0, self._mDegreeV + 1):
                    temp = [0.0, 0.0, 0.0, 0.0]
                    idx_v = span_v - self._mDegreeV + l
                    for k in range(0, self._mDegreeU + 1):
                        temp[0] += (basis_u[k] * ctrlptsw[idx_u + k][idx_v][0])
                        temp[1] += (basis_u[k] * ctrlptsw[idx_u + k][idx_v][1])
                        temp[2] += (basis_u[k] * ctrlptsw[idx_u + k][idx_v][2])
                        temp[3] += (basis_u[k] * ctrlptsw[idx_u + k][idx_v][3])
                    surfptw[0] += (basis_v[l] * temp[0])
                    surfptw[1] += (basis_v[l] * temp[1])
                    surfptw[2] += (basis_v[l] * temp[2])
                    surfptw[3] += (basis_v[l] * temp[3])
                # Divide by weight to obtain 3D surface points
                surfpt = [surfptw[0] / surfptw[3], surfptw[1] / surfptw[3], surfptw[2] / surfptw[3]]
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
