"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation module for NURBS curves and surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline
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
            raise ValueError("Please set size of the control points on the u- and v-directions")

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
            raise ValueError("Please set size of the control points on the u- and v-directions")

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
