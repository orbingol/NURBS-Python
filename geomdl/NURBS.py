"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation module for NURBS curves and surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import copy

from . import BSpline
from . import utilities as utils


class Curve(BSpline.Curve):
    """ Data storage and evaluation class for 3D NURBS curves.

    **Data Storage**

    The following properties are present in this class:

    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * weights
    * curvepts

    The function :func:`.read_ctrlpts_from_txt()` provides an easy way to read weighted control points from a text file.
    Additional details on the file formats can be found in the documentation.

    .. note:: Control points are stored as a list of (x*w, y*w, z*w, w) coordinates

    **Evaluation**

    The evaluation methods are:

    * :py:meth:`.evaluate()`
    * :py:meth:`.derivatives()`
    * :py:meth:`.tangent()`
    * :py:meth:`.normal()`
    * :py:meth:`.binormal()`
    * :py:meth:`.insert_knot()`

    .. note::

        If you update any of the data storage elements after the curve evaluation, the surface points stored in
        :py:attr:`~curvepts` property will be deleted automatically.
    """

    def __init__(self):
        super(Curve, self).__init__()
        # Override dimension variable
        self._dimension = 4  # 3D coordinates + weights
        self._rational = True

    def __str__(self):
        return "3D NURBS Curve"

    __repr__ = __str__

    @property
    def ctrlpts(self):
        """ Control points.

        :getter: Gets un-weighted control points. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets weighted control points
        :type: list
        """
        ret_list = []
        for pt in self._control_points:
            temp = []
            for idx in range(self._dimension - 1):
                temp.append(float(pt[idx] / pt[-1]))
            ret_list.append(tuple(temp))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        self.set_ctrlpts(value)

    @property
    def weights(self):
        """ Weights vector.

        :getter: Extracts the weights vector from weighted control points array
        :type: list
        """
        weights = []
        for pt in self._control_points:
            weights.append(pt[-1])
        return tuple(weights)

    # Prepares control points for exporting as a CSV file
    def _get_ctrlpts_for_exporting(self):
        """ Prepares control points for exporting as a CSV file.

        :return: list of control points
        :rtype: list
        """
        ctrlpts_noweight = []
        for pt in self._control_points:
            temp = []
            for idx in range(self._dimension - 1):
                temp.append(float(pt[idx] / pt[-1]))
            ctrlpts_noweight.append(temp)
        return ctrlpts_noweight

    # Prepares and returns the CSV file header
    def _get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, coord z, scalar\n"

    # Evaluates the rational curve at the given parameter
    def curvept(self, u=-1, check_vars=True, get_ctrlpts=False):
        """ Evaluates the curve at the input parameter value.

        :param u: parameter
        :type u: float
        :param check_vars: flag to disable variable checking (only for internal eval functions)
        :type check_vars: bool
        :param get_ctrlpts: flag to add a list of control points associated with the curve evaluation to return value
        :param get_ctrlpts: bool
        :return: evaluated curve point at the given knot value
        :rtype: list
        """
        if check_vars:
            # Check all parameters are set before the curve evaluation
            self._check_variables()
            # Check if u parameter is in the range
            utils.check_uv(u)

        # Initialize an empty list which will contain the list of associated control points
        ctrlpts = []

        # Algorithm A4.1
        span = utils.find_span(self._degree, tuple(self._knot_vector), len(self._control_points), u)
        basis = utils.basis_functions(self._degree, tuple(self._knot_vector), span, u)
        cptw = [0.0 for _ in range(self._dimension)]
        for i in range(0, self._degree + 1):
            cptw[:] = [elem1 + (basis[i] * elem2) for elem1, elem2 in
                       zip(cptw, self._control_points[span - self._degree + i])]
            if get_ctrlpts:
                ctrlpts.append(self._control_points[span - self._degree + i])

        # Divide by weight
        cpt = []
        for idx in range(self._dimension - 1):
            cpt.append(float(cptw[idx] / cptw[-1]))

        if get_ctrlpts:
            return cpt, ctrlpts
        return cpt

    # Evaluates the rational curve derivative
    def derivatives(self, u=-1, order=0):
        """ Evaluates n-th order curve derivatives at the given parameter value.

        :param u: knot value
        :type u: float
        :param order: derivative order
        :type order: integer
        :return: A list containing up to {order}-th derivative of the curve
        :rtype: list
        """
        # Call the parent function to evaluate A(u) and w(u) derivatives
        CKw = super(Curve, self).derivatives(u, order)

        # Algorithm A4.2
        # CK = [[None for x in range(self._dimension - 1)] for y in range(order + 1)]
        CK = [[None for _ in range(self._dimension - 1)] for _ in range(order + 1)]
        for k in range(0, order + 1):
            v = []
            for idx in range(self._dimension - 1):
                v.append(CKw[idx])

            for i in range(1, order + 1):
                v[:] = [tmp - (utils.binomial_coefficient(k, i) * CKw[i][-1] * drv) for tmp, drv in zip(v, CK[k - i])]
            CK[k][:] = [tmp / CKw[0][-1] for tmp in v]

        # Return C(u) derivatives
        return CK

    # Evaluates the rational curve derivative
    def derivatives2(self, u=-1, order=0):
        """ Evaluates n-th order curve derivatives at the given parameter value.

        :param u: knot value
        :type u: float
        :param order: derivative order
        :type order: integer
        :return: A list containing up to {order}-th derivative of the curve
        :rtype: list
        """
        return self.derivatives(u, order)

    def translate(self, vec=()):
        """ Translates the curve using the input vector.

        The input vector list/tuple must have

        * 2 elements for 2D curves
        * 3 elements for 3D curves

        :param vec: translation vector
        :type vec: list, tuple
        """
        if not vec or not isinstance(vec, (tuple, list)):
            raise ValueError("The input must be a list or a tuple")

        if len(vec) != self._dimension - 1:
            raise ValueError("The input must have " + str(self._dimension - 1) + " elements")

        new_ctrlpts = []
        for point in self._control_points:
            temp = [v + vec[i] for i, v in enumerate(point[0:self._dimension - 1])]
            new_ctrlpts.append(temp)

        self._control_points = new_ctrlpts


class Curve2D(Curve):
    """ Data storage and evaluation class for 2D NURBS curves.

    **Data Storage**

    The following properties are present in this class:

    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * weights
    * curvepts

    The function :func:`.read_ctrlpts_from_txt()` provides an easy way to read weighted control points from a text file.
    Additional details on the file formats can be found in the documentation.

    .. note:: Control points are stored as a list of (x*w, y*w, w) coordinates

    **Evaluation**

    The evaluation methods are:

    * :py:meth:`.evaluate()`
    * :py:meth:`.derivatives()`
    * :py:meth:`.tangent()`
    * :py:meth:`.normal()`
    * :py:meth:`.binormal()`
    * :py:meth:`.insert_knot()`

    .. note::

        If you update any of the data storage elements after the curve evaluation, the surface points stored in
        :py:attr:`~curvepts` property will be deleted automatically.
    """

    def __init__(self):
        super(Curve2D, self).__init__()
        # Override dimension variable
        self._dimension = 3  # 2D coordinates + weights
        self._rational = True

    def __str__(self):
        return "2D NURBS Curve"

    __repr__ = __str__

    # Prepares and returns the CSV file header
    def _get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, scalar\n"


class Surface(BSpline.Surface):
    """ Data storage and evaluation class for NURBS surfaces.

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
    * ctrlpts2d
    * weights
    * surfpts

    **Details on Control Points**

    Control points are stored as a list of (x*w, y*w, z*w, w) coordinates, where *w* corresponds to the weight.
    The function :func:`.read_ctrlpts_from_txt()` provides an easy way to read control points from a text file.
    Additional details on the file formats can be found on the documentation.

    **Evaluation**

    The evaluation methods are:

    * :py:meth:`.evaluate()`
    * :py:meth:`.derivatives()`
    * :py:meth:`.tangent()`
    * :py:meth:`.normal()`
    * :py:meth:`.binormal()`
    * :py:meth:`.insert_knot()`

    .. note::

        If you update any of the data storage elements after the surface evaluation, the surface points stored in
        :py:attr:`~surfpts` property will be deleted automatically.
    """

    def __init__(self):
        super(Surface, self).__init__()
        # Override dimension variable
        self._dimension = 4  # 3D coordinates + weights
        self._rational = True

    def __str__(self):
        return "NURBS Surface"

    __repr__ = __str__

    @property
    def ctrlpts(self):
        """ 1D Control points.

        :getter: Gets un-weighted control points. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets weighted control points.
        :type: list
        """
        ret_list = []
        for pt in self._control_points:
            temp = []
            for idx in range(self._dimension - 1):
                temp.append(float(pt[idx] / pt[-1]))
            ret_list.append(tuple(temp))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        if self._control_points_size_u <= 0 and self._control_points_size_v <= 0:
            raise ValueError("Please set size of the control points in u and v directions")

        # Use set_ctrlpts directly
        self.set_ctrlpts(value, self._control_points_size_u, self._control_points_size_v)

    @property
    def weights(self):
        """ Weights vector.

        :getter: Extracts the weights vector from weighted control points array
        :type: list
        """
        weights = []
        for pt in self._control_points:
            weights.append(pt[-1])
        return tuple(weights)

    # Prepares control points for exporting as a CSV file
    def _get_ctrlpts_for_exporting(self):
        """ Prepares control points for exporting as a CSV file.

        :return: list of control points
        :rtype: list
        """
        ctrlpts_noweight = []
        for pt in self._control_points:
            temp = []
            for idx in range(self._dimension - 1):
                temp.append(float(pt[idx] / pt[-1]))
            ctrlpts_noweight.append(temp)
        return ctrlpts_noweight

    # Prepares and returns the CSV file header
    def _get_csv_header(self):
        """ Prepares and returns the CSV file header.

        :return: header of the CSV file
        :rtype: str
        """
        return "coord x, coord y, coord z, scalar\n"

    # Evaluates rational surface at the given (u, v) parameters
    def surfpt(self, u=-1, v=-1, check_vars=True, get_ctrlpts=False):
        """ Evaluates the surface at the given (u, v) parameter pair.

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :param check_vars: flag to disable variable checking (only for internal eval functions)
        :type check_vars: bool
        :param get_ctrlpts: flag to add a list of control points associated with the surface evaluation to return value
        :param get_ctrlpts: bool
        :return: evaluated surface point at the given knot values
        :rtype: list
        """
        if check_vars:
            # Check all parameters are set before the surface evaluation
            self._check_variables()
            # Check if u and v parameters are correct
            utils.check_uv(u, v)

        # Initialize an empty list which will contain the list of associated control points
        ctrlpts = []

        # Algorithm A4.3
        span_v = utils.find_span(self._degree_v, tuple(self._knot_vector_v), self._control_points_size_v, v)
        basis_v = utils.basis_functions(self._degree_v, tuple(self._knot_vector_v), span_v, v)
        span_u = utils.find_span(self._degree_u, tuple(self._knot_vector_u), self._control_points_size_u, u)
        basis_u = utils.basis_functions(self._degree_u, tuple(self._knot_vector_u), span_u, u)
        idx_u = span_u - self._degree_u
        sptw = [0.0 for _ in range(self._dimension)]

        for l in range(0, self._degree_v + 1):
            temp = [0.0 for _ in range(self._dimension)]
            idx_v = span_v - self._degree_v + l
            for k in range(0, self._degree_u + 1):
                temp[:] = [tmp + (basis_u[k] * cp) for tmp, cp in zip(temp, self._control_points2D[idx_u + k][idx_v])]
                if get_ctrlpts:
                    ctrlpts.append(self._control_points2D[idx_u + k][idx_v])
            sptw[:] = [ptw + (basis_v[l] * tmp) for ptw, tmp in zip(sptw, temp)]

        # Divide by weight
        spt = []
        for idx in range(self._dimension - 1):
            spt.append(float(sptw[idx] / sptw[-1]))

        if get_ctrlpts:
            return spt, ctrlpts
        return spt

    # Evaluates n-th order rational surface derivatives at the given (u, v) parameter
    def derivatives(self, u=-1, v=-1, order=0):
        """ Evaluates n-th order surface derivatives at the given (u, v) parameter pair from the rational surface.

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
        # Call the parent function to evaluate A(u) and w(u) derivatives
        SKLw = super(Surface, self).derivatives(u, v, order)

        # Algorithm A4.4
        du = min(self._degree_u, order)
        dv = min(self._degree_v, order)

        # Generate an empty list of derivatives
        # SKL = [[[None for x in range(self._dimension)] for y in range(dv + 1)] for z in range(du + 1)]
        SKL = [[[None for _ in range(self._dimension)] for _ in range(dv + 1)] for _ in range(du + 1)]

        for k in range(0, order + 1):
            for l in range(0, order - k + 1):
                # Deep copying might seem a little overkill but we also want to avoid same pointer issues too
                v = copy.deepcopy(SKLw[k][l])

                for j in range(1, l + 1):
                    v[:] = [tmp - (utils.binomial_coefficient(l, j) * SKLw[0][j][-1] * drv) for tmp, drv in
                            zip(v, SKL[k][l - j])]
                for i in range(1, k + 1):
                    v[:] = [tmp - (utils.binomial_coefficient(k, i) * SKLw[i][0][-1] * drv) for tmp, drv in
                            zip(v, SKL[k - i][l])]
                    v2 = [0.0 for _ in range(self._dimension - 1)]
                    for j in range(1, l + 1):
                        v2[:] = [tmp + (utils.binomial_coefficient(l, j) * SKLw[i][j][-1] * drv) for tmp, drv in
                                 zip(v2, SKL[k - i][l - j])]
                    v[:] = [tmp - (utils.binomial_coefficient(k, i) * tmp2) for tmp, tmp2 in zip(v, v2)]

                SKL[k][l][:] = [tmp / SKLw[0][0][-1] for tmp in v[0:3]]

        # Return S(u,v) derivatives
        return SKL
