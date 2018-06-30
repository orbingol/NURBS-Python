"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation module for NURBS curves and surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import copy
from . import BSpline
from . import utilities
from . import compatibility
from . import evaluators


class Curve(BSpline.Curve):
    """ Data storage and evaluation class for NURBS curves.

    The following properties are present in this class:

    * dimension
    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * weights
    * evalpts

    """

    def __init__(self):
        super(Curve, self).__init__()
        self._name = "NURBS Curve"
        self._rational = True
        self._evaluator = evaluators.NURBSCurveEvaluator()
        # Variables for caching
        self._cache['ctrlpts'] = []
        self._cache['weights'] = []

    def __str__(self):
        return self.name

    __repr__ = __str__

    @property
    def ctrlptsw(self):
        """ Weighted control points (Pw).

        Weighted control points are in (x*w, y*w, z*w, w) format; where x,y,z are the coordinates and w is the weight.

        :getter: Gets the weighted control points
        :setter: Sets the weighted control points
        """
        return self._control_points

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        self.set_ctrlpts(value)

    @property
    def ctrlpts(self):
        """ Unweighted control points (P).

        :getter: Gets unweighted control points. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets unweighted control points
        :type: list
        """
        # Populate the cache, if necessary
        if not self._cache['ctrlpts']:
            c, w = compatibility.separate_ctrlpts_weights(self._control_points)
            self._cache['ctrlpts'] = [tuple(crd) for crd in c]
            self._cache['weights'] = w
        return tuple(self._cache['ctrlpts'])

    @ctrlpts.setter
    def ctrlpts(self, value):
        # Check if we can retrieve the existing weights. If not, generate a weights vector of 1.0s.
        if not self.weights:
            weights = [1.0 for _ in range(len(value))]
        else:
            weights = self.weights

        # Generate weighted control points using the new control points
        ctrlptsw = compatibility.combine_ctrlpts_weights(value, weights)

        # Set new weighted control points
        self.set_ctrlpts(ctrlptsw)

    @property
    def weights(self):
        """ Weights vector.

        :getter: Gets the weights vector
        :setter: Sets the weights vector
        :type: list
        """
        # Populate the cache, if necessary
        if not self._cache['weights']:
            c, w = compatibility.separate_ctrlpts_weights(self._control_points)
            self._cache['ctrlpts'] = [tuple(crd) for crd in c]
            self._cache['weights'] = w
        return tuple(self._cache['weights'])

    @weights.setter
    def weights(self, value):
        if not self.ctrlpts:
            raise ValueError("Set control points first")

        # Generate weighted control points using the new weights
        ctrlptsw = compatibility.combine_ctrlpts_weights(self.ctrlpts, value)

        # Set new weighted control points
        self.set_ctrlpts(ctrlptsw)

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:

            * ``evalpts``: if True, then resets evaluated points
            * ``ctrlpts`` if True, then resets control points

        """
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        reset_evalpts = kwargs.get('evalpts', False)

        # Call parent function
        super(Curve, self).reset(ctrlpts=reset_ctrlpts, evalpts=reset_evalpts)

        if reset_ctrlpts:
            # Delete the caches
            del self._cache['ctrlpts'][:]
            del self._cache['weights'][:]

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
        CK = [[None for _ in range(self._dimension - 1)] for _ in range(order + 1)]
        for k in range(0, order + 1):
            v = [val for val in CKw[k][0:(self._dimension - 1)]]
            for i in range(1, k + 1):
                v[:] = [tmp - (utilities.binomial_coefficient(k, i) * CKw[i][-1] * drv) for tmp, drv in zip(v, CK[k - i])]
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
        """ Translates the curve by the input vector.

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
        for point, w in zip(self.ctrlpts, self.weights):
            temp = [(v + vec[i]) * w for i, v in enumerate(point[0:self._dimension - 1])]
            temp.append(w)
            new_ctrlpts.append(temp)

        self.ctrlpts = new_ctrlpts


class Surface(BSpline.Surface):
    """ Data storage and evaluation class for NURBS surfaces.

    The following properties are present in this class:

    * dimension
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
    * evalpts

    """

    def __init__(self):
        super(Surface, self).__init__()
        self._name = "NURBS Surface"
        self._rational = True
        self._evaluator = evaluators.NURBSSurfaceEvaluator()
        # Variables for caching
        self._cache['ctrlpts'] = []
        self._cache['weights'] = []

    def __str__(self):
        return self.name

    __repr__ = __str__

    @property
    def ctrlptsw(self):
        """ Weighted control points (Pw).

        Weighted control points are in (x*w, y*w, z*w, w) format; where x,y,z are the coordinates and w is the weight.

        This property sets and gets the control points in 1-D.

        :getter: Gets weighted control points
        :setter: Sets weighted control points
        """
        ret_list = []
        for pt in self._control_points:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        if self._control_points_size_u <= 0 and self._control_points_size_v <= 0:
            raise ValueError("Please set size of the control points in u and v directions")

        self.set_ctrlpts(value, self._control_points_size_u, self._control_points_size_v)

    @property
    def ctrlpts(self):
        """ Control points (P).

        This property sets and gets the control points in 1-D.

        :getter: Gets unweighted control points. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets unweighted control points.
        :type: list
        """
        if not self._cache['ctrlpts']:
            c, w = compatibility.separate_ctrlpts_weights(self._control_points)
            self._cache['ctrlpts'] = [tuple(crd) for crd in c]
            self._cache['weights'] = w
        return tuple(self._cache['ctrlpts'])

    @ctrlpts.setter
    def ctrlpts(self, value):
        if self._control_points_size_u <= 0 and self._control_points_size_v <= 0:
            raise ValueError("Please set size of the control points in u and v directions")

        # Check if we can retrieve the existing weights. If not, generate a weights vector of 1.0s.
        if not self.weights:
            weights = [1.0 for _ in range(len(value))]
        else:
            weights = self.weights

        # Generate weighted control points using the new control points
        ctrlptsw = compatibility.combine_ctrlpts_weights(value, weights)

        # Set weighted control points
        self.set_ctrlpts(ctrlptsw, self._control_points_size_u, self._control_points_size_v)

    @property
    def weights(self):
        """ Weights vector.

        :getter: Gets the weights vector
        :setter: Sets the weights vector
        :type: list
        """
        if not self._cache['weights']:
            c, w = compatibility.separate_ctrlpts_weights(self._control_points)
            self._cache['ctrlpts'] = [tuple(crd) for crd in c]
            self._cache['weights'] = w
        return tuple(self._cache['weights'])

    @weights.setter
    def weights(self, value):
        if not self.ctrlpts:
            raise ValueError("Set control points first")

        # Generate weighted control points using the new weights
        ctrlptsw = compatibility.combine_ctrlpts_weights(self.ctrlpts, value)

        # Set weighted control points
        self.set_ctrlpts(ctrlptsw, self._control_points_size_u, self._control_points_size_v)

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:

            * ``evalpts``: if True, then resets evaluated points
            * ``ctrlpts`` if True, then resets control points

        """
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        reset_evalpts = kwargs.get('evalpts', False)

        # Call parent function
        super(Surface, self).reset(ctrlpts=reset_ctrlpts, evalpts=reset_evalpts)

        if reset_ctrlpts:
            # Delete the caches
            del self._cache['ctrlpts'][:]
            del self._cache['weights'][:]

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
        SKL = [[[None for _ in range(self._dimension)] for _ in range(dv + 1)] for _ in range(du + 1)]

        for k in range(0, order + 1):
            for l in range(0, order - k + 1):
                # Deep copying might seem a little overkill but we also want to avoid same pointer issues too
                v = copy.deepcopy(SKLw[k][l])

                for j in range(1, l + 1):
                    v[:] = [tmp - (utilities.binomial_coefficient(l, j) * SKLw[0][j][-1] * drv) for tmp, drv in
                            zip(v, SKL[k][l - j])]
                for i in range(1, k + 1):
                    v[:] = [tmp - (utilities.binomial_coefficient(k, i) * SKLw[i][0][-1] * drv) for tmp, drv in
                            zip(v, SKL[k - i][l])]
                    v2 = [0.0 for _ in range(self._dimension - 1)]
                    for j in range(1, l + 1):
                        v2[:] = [tmp + (utilities.binomial_coefficient(l, j) * SKLw[i][j][-1] * drv) for tmp, drv in
                                 zip(v2, SKL[k - i][l - j])]
                    v[:] = [tmp - (utilities.binomial_coefficient(k, i) * tmp2) for tmp, tmp2 in zip(v, v2)]

                SKL[k][l][:] = [tmp / SKLw[0][0][-1] for tmp in v[0:(self._dimension - 1)]]

        # Return S(u,v) derivatives
        return SKL

    def translate(self, vec=()):
        """ Translates the surface by the input vector.

        :param vec: translation vector in 3D
        :type vec: list, tuple
        """
        if not vec or not isinstance(vec, (tuple, list)):
            raise ValueError("The input must be a list or a tuple")

        if len(vec) != self._dimension - 1:
            raise ValueError("The input must have " + str(self._dimension - 1) + " elements")

        new_ctrlpts = []
        for point, w in zip(self.ctrlpts, self.weights):
            temp = [(v + vec[i]) * w for i, v in enumerate(point[0:self._dimension - 1])]
            temp.append(w)
            new_ctrlpts.append(temp)

        self.ctrlpts = new_ctrlpts
