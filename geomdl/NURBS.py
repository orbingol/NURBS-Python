"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: Provides data storage and evaluation functionality for NURBS curves and surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline
from . import compatibility
from . import evaluators


class Curve(BSpline.Curve):
    """ Data storage and evaluation class for n-variate NURBS (rational) curves.

    The rational shapes have some minor differences between the non-rational ones. This class is designed to operate
    with weighted control points (Pw) as described in *The NURBS Book* by Piegl and Tiller. Therefore, it provides
    a different set of properties (i.e. getters and setters):

        * ``ctrlptsw``: 1-dimensional array of weighted control points
        * ``ctrlpts``: 1-dimensional array of control points
        * ``weights``: 1-dimensional array of weights

    You may also use ``set_ctrlpts()`` function which is designed to work with all types of control points.

    This class provides the following properties:

    * :py:attr:`order`
    * :py:attr:`degree`
    * :py:attr:`knotvector`
    * :py:attr:`ctrlptsw`
    * :py:attr:`ctrlpts`
    * :py:attr:`weights`
    * :py:attr:`delta`
    * :py:attr:`sample_size`
    * :py:attr:`bbox`
    * :py:attr:`vis`
    * :py:attr:`name`
    * :py:attr:`dimension`
    * :py:attr:`evaluator`
    * :py:attr:`rational`

    Notes:
        * Please see the :py:class:`.abstract.Surface()` documentation for details.
        * This class sets the *FindSpan* implementation to Linear Search by default.

    Please refer to ``ex_curve04.py`` in the :doc:`Examples repository <examples_repo>` for a NURBS curve example.
    """

    def __init__(self, **kwargs):
        super(Curve, self).__init__(**kwargs)
        self._rational = True
        self._evaluator = evaluators.NURBSCurveEvaluator(find_span_func=self._span_func)
        # Variables for caching
        self.init_cache()

    def __deepcopy__(self, memo):
        # Call parent method
        result = super(Curve, self).__deepcopy__(memo)
        result.init_cache()
        return result

    def init_cache(self):
        self._cache['ctrlpts'] = self._init_var(self._array_type)
        self._cache['weights'] = self._init_var(self._array_type)

    @property
    def ctrlptsw(self):
        """ Weighted control points (Pw).

        Weighted control points are in (x*w, y*w, z*w, w) format; where x,y,z are the coordinates and w is the weight.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the weighted control points
        :setter: Sets the weighted control points
        """
        return self._control_points

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        self.set_ctrlpts(value)

    @property
    def ctrlpts(self):
        """ Control points (P).

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

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

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

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
            self._cache['ctrlpts'] = self._init_var(self._array_type)
            self._cache['weights'][:] = self._init_var(self._array_type)


class Surface(BSpline.Surface):
    """ Data storage and evaluation class for NURBS (rational) surfaces.

    The rational shapes have some minor differences between the non-rational ones. This class is designed to operate
    with weighted control points (Pw) as described in *The NURBS Book* by Piegl and Tiller. Therefore, it provides
    a different set of properties (i.e. getters and setters):

        * ``ctrlptsw``: 1-dimensional array of weighted control points
        * ``ctrlpts2d``: 2-dimensional array of weighted control points
        * ``ctrlpts``: 1-dimensional array of control points
        * ``weights``: 1-dimensional array of weights

    You may also use ``set_ctrlpts()`` function which is designed to work with all types of control points.

    This class provides the following properties:

    * :py:attr:`order_u`
    * :py:attr:`order_v`
    * :py:attr:`degree_u`
    * :py:attr:`degree_v`
    * :py:attr:`knotvector_u`
    * :py:attr:`knotvector_v`
    * :py:attr:`ctrlptsw`
    * :py:attr:`ctrlpts`
    * :py:attr:`weights`
    * :py:attr:`ctrlpts_size_u`
    * :py:attr:`ctrlpts_size_v`
    * :py:attr:`ctrlpts2d`
    * :py:attr:`delta`
    * :py:attr:`delta_u`
    * :py:attr:`delta_v`
    * :py:attr:`sample_size`
    * :py:attr:`sample_size_u`
    * :py:attr:`sample_size_v`
    * :py:attr:`bbox`
    * :py:attr:`name`
    * :py:attr:`dimension`
    * :py:attr:`vis`
    * :py:attr:`evaluator`
    * :py:attr:`tessellator`
    * :py:attr:`rational`
    * :py:attr:`trims`

    Notes:
        * Please see the :py:class:`.abstract.Surface()` documentation for details.
        * This class sets the *FindSpan* implementation to Linear Search by default.

    Please refer to ``ex_surface03.py`` in the :doc:`Examples repository <examples_repo>` for a NURBS surface example.
    """

    def __init__(self, **kwargs):
        super(Surface, self).__init__(**kwargs)
        self._rational = True
        self._evaluator = evaluators.NURBSSurfaceEvaluator(find_span_func=self._span_func)
        # Variables for caching
        self.init_cache()

    def __deepcopy__(self, memo):
        # Call parent method
        result = super(Surface, self).__deepcopy__(memo)
        result.init_cache()
        return result

    def init_cache(self):
        self._cache['ctrlpts'] = self._init_array(self._array_type)
        self._cache['weights'] = self._init_array(self._array_type)

    @property
    def ctrlptsw(self):
        """ 1-dimensional array of weighted control points (Pw).

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
        if self.ctrlpts_size_u <= 0 or self.ctrlpts_size_v <= 0:
            raise ValueError("Please set the number of control points on the u- and v-directions")
        self.set_ctrlpts(value, self.ctrlpts_size_u, self.ctrlpts_size_v)

    @property
    def ctrlpts(self):
        """ 1-dimensional array of control points (P).

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
        if self.ctrlpts_size_u <= 0 or self.ctrlpts_size_v <= 0:
            raise ValueError("Please set the number of control points on the u- and v-directions")

        # Check if we can retrieve the existing weights. If not, generate a weights vector of 1.0s.
        if not self.weights:
            weights = [1.0 for _ in range(len(value))]
        else:
            weights = self.weights

        # Generate weighted control points using the new control points
        ctrlptsw = compatibility.combine_ctrlpts_weights(value, weights)

        # Set weighted control points
        self.set_ctrlpts(ctrlptsw, self.ctrlpts_size_u, self.ctrlpts_size_v)

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
        self.set_ctrlpts(ctrlptsw, self.ctrlpts_size_u, self.ctrlpts_size_v)

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
            # Re-initialize the caches
            self.init_cache()


class Volume(BSpline.Volume):
    """ Data storage and evaluation class for NURBS (rational) volumes.

    The rational shapes have some minor differences between the non-rational ones. This class is designed to operate
    with weighted control points (Pw) as described in *The NURBS Book* by Piegl and Tiller. Therefore, it provides
    a different set of properties (i.e. getters and setters):

        * ``ctrlptsw``: 1-dimensional array of weighted control points
        * ``ctrlpts``: 1-dimensional array of control points
        * ``weights``: 1-dimensional array of weights

    This class provides the following properties:

    * :py:attr:`order_u`
    * :py:attr:`order_v`
    * :py:attr:`order_w`
    * :py:attr:`degree_u`
    * :py:attr:`degree_v`
    * :py:attr:`degree_w`
    * :py:attr:`knotvector_u`
    * :py:attr:`knotvector_v`
    * :py:attr:`knotvector_w`
    * :py:attr:`ctrlptsw`
    * :py:attr:`ctrlpts`
    * :py:attr:`weights`
    * :py:attr:`ctrlpts_size_u`
    * :py:attr:`ctrlpts_size_v`
    * :py:attr:`ctrlpts_size_w`
    * :py:attr:`delta`
    * :py:attr:`delta_u`
    * :py:attr:`delta_v`
    * :py:attr:`delta_w`
    * :py:attr:`sample_size`
    * :py:attr:`sample_size_u`
    * :py:attr:`sample_size_v`
    * :py:attr:`sample_size_w`
    * :py:attr:`bbox`
    * :py:attr:`name`
    * :py:attr:`dimension`
    * :py:attr:`vis`
    * :py:attr:`evaluator`
    * :py:attr:`rational`

    Notes:
        * Please see the :py:class:`.abstract.Volume()` documentation for details.
        * This class sets the *FindSpan* implementation to Linear Search by default.
    """

    def __init__(self, **kwargs):
        super(Volume, self).__init__(**kwargs)
        self._rational = True
        self._evaluator = evaluators.NURBSVolumeEvaluator(find_span_func=self._span_func)
        # Variables for caching
        self.init_cache()

    def __deepcopy__(self, memo):
        # Call parent method
        result = super(Volume, self).__deepcopy__(memo)
        result.init_cache()
        return result

    def init_cache(self):
        self._cache['ctrlpts'] = self._init_array(self._array_type)
        self._cache['weights'] = self._init_array(self._array_type)

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:

            * ``evalpts``: if True, then resets the evaluated points
            * ``ctrlpts`` if True, then resets the control points

        """
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        reset_evalpts = kwargs.get('evalpts', False)

        # Call parent function
        super(Volume, self).reset(ctrlpts=reset_ctrlpts, evalpts=reset_evalpts)

        if reset_ctrlpts:
            # Re-initialize the caches
            self.init_cache()

    @property
    def ctrlptsw(self):
        """ 1-dimensional array of weighted control points (Pw).

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
        if self.ctrlpts_size_u <= 0 or self.ctrlpts_size_v <= 0 or self.ctrlpts_size_w <= 0:
            raise ValueError("Please set the number of control points for all u-, v- and w-directions")
        self.set_ctrlpts(value, self.ctrlpts_size_u, self.ctrlpts_size_v, self.ctrlpts_size_w)

    @property
    def ctrlpts(self):
        """ 1-dimensional array of control points (P).

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
        if self.ctrlpts_size_u <= 0 or self.ctrlpts_size_v <= 0 or self.ctrlpts_size_w <= 0:
            raise ValueError("Please set the number of control points for all u-, v- and w-directions")

        # Check if we can retrieve the existing weights. If not, generate a weights vector of 1.0s.
        if not self.weights:
            weights = [1.0 for _ in range(len(value))]
        else:
            weights = self.weights

        # Generate weighted control points using the new control points
        ctrlptsw = compatibility.combine_ctrlpts_weights(value, weights)

        # Set weighted control points
        self.set_ctrlpts(ctrlptsw, self.ctrlpts_size_u, self.ctrlpts_size_v, self.ctrlpts_size_w)

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
        self.set_ctrlpts(ctrlptsw, self.ctrlpts_size_u, self.ctrlpts_size_v, self.ctrlpts_size_w)
