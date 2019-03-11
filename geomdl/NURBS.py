"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: Provides data storage and evaluation functionality for rational spline geometries

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline, compatibility, evaluators
from ._utilities import export


@export
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

    The following code segment illustrates the usage of Curve class:

    .. code-block:: python

        from geomdl import NURBS

        # Create a 3-dimensional B-spline Curve
        curve = NURBS.Curve()

        # Set degree
        curve.degree = 3

        # Set control points (weights vector will be 1 by default)
        # Use curve.ctrlptsw is if you are using homogeneous points as Pw
        curve.ctrlpts = [[10, 5, 10], [10, 20, -30], [40, 10, 25], [-10, 5, 0]]

        # Set knot vector
        curve.knotvector = [0, 0, 0, 0, 1, 1, 1, 1]

        # Set evaluation delta (controls the number of curve points)
        curve.delta = 0.05

        # Get curve points (the curve will be automatically evaluated)
        curve_points = curve.evalpts

    **Keyword Arguments:**

    * ``precision``: number of decimal places to round to. *Default: 18*
    * ``normalize_kv``: activates knot vector normalization. *Default: True*
    * ``find_span_func``: sets knot span search implementation. *Default:* :func:`.helpers.find_span_linear`
    * ``insert_knot_func``: sets knot insertion implementation. *Default:* :func:`.operations.insert_knot`
    * ``remove_knot_func``: sets knot removal implementation. *Default:* :func:`.operations.remove_knot`

    Please refer to the :py:class:`.abstract.Curve()` documentation for more details.
    """

    def __init__(self, **kwargs):
        super(Curve, self).__init__(**kwargs)
        self._rational = True
        self._evaluator = evaluators.CurveEvaluatorRational(find_span_func=self._span_func)
        # Variables for caching
        self.init_cache()

    def __deepcopy__(self, memo):
        # Call parent method
        result = super(Curve, self).__deepcopy__(memo)
        result.init_cache()
        return result

    def init_cache(self):
        self._cache['ctrlpts'] = self._init_array()
        self._cache['weights'] = self._init_array()

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
            self._cache['ctrlpts'] = [crd for crd in c]
            self._cache['weights'] = w
        return self._cache['ctrlpts']

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
            self._cache['ctrlpts'] = [crd for crd in c]
            self._cache['weights'] = w
        return self._cache['weights']

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
            self._cache['ctrlpts'] = self._init_array()
            self._cache['weights'][:] = self._init_array()


@export
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

    The following code segment illustrates the usage of Surface class:

    .. code-block:: python
        :linenos:

        from geomdl import NURBS

        # Create a NURBS surface instance
        surf = NURBS.Surface()

        # Set degrees
        surf.degree_u = 3
        surf.degree_v = 2

        # Set control points (weights vector will be 1 by default)
        # Use curve.ctrlptsw is if you are using homogeneous points as Pw
        control_points = [[0, 0, 0], [0, 4, 0], [0, 8, -3],
                          [2, 0, 6], [2, 4, 0], [2, 8, 0],
                          [4, 0, 0], [4, 4, 0], [4, 8, 3],
                          [6, 0, 0], [6, 4, -3], [6, 8, 0]]
        surf.set_ctrlpts(control_points, 4, 3)

        # Set knot vectors
        surf.knotvector_u = [0, 0, 0, 0, 1, 1, 1, 1]
        surf.knotvector_v = [0, 0, 0, 1, 1, 1]

        # Set evaluation delta (control the number of surface points)
        surf.delta = 0.05

        # Get surface points (the surface will be automatically evaluated)
        surface_points = surf.evalpts

    **Keyword Arguments:**

    * ``precision``: number of decimal places to round to. *Default: 18*
    * ``normalize_kv``: activates knot vector normalization. *Default: True*
    * ``find_span_func``: sets knot span search implementation. *Default:* :func:`.helpers.find_span_linear`
    * ``insert_knot_func``: sets knot insertion implementation. *Default:* :func:`.operations.insert_knot`
    * ``remove_knot_func``: sets knot removal implementation. *Default:* :func:`.operations.remove_knot`

    Please refer to the :py:class:`.abstract.Surface()` documentation for more details.
    """

    def __init__(self, **kwargs):
        super(Surface, self).__init__(**kwargs)
        self._rational = True
        self._evaluator = evaluators.SurfaceEvaluatorRational(find_span_func=self._span_func)
        # Variables for caching
        self.init_cache()

    def __deepcopy__(self, memo):
        # Call parent method
        result = super(Surface, self).__deepcopy__(memo)
        result.init_cache()
        return result

    def init_cache(self):
        self._cache['ctrlpts'] = self._init_array()
        self._cache['weights'] = self._init_array()

    @property
    def ctrlptsw(self):
        """ 1-dimensional array of weighted control points (Pw).

        Weighted control points are in (x*w, y*w, z*w, w) format; where x,y,z are the coordinates and w is the weight.

        This property sets and gets the control points in 1-D.

        :getter: Gets weighted control points
        :setter: Sets weighted control points
        """
        return self._control_points

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
            self._cache['ctrlpts'] = [crd for crd in c]
            self._cache['weights'] = w
        return self._cache['ctrlpts']

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
            self._cache['ctrlpts'] = [crd for crd in c]
            self._cache['weights'] = w
        return self._cache['weights']

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


@export
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

    **Keyword Arguments:**

    * ``precision``: number of decimal places to round to. *Default: 18*
    * ``normalize_kv``: activates knot vector normalization. *Default: True*
    * ``find_span_func``: sets knot span search implementation. *Default:* :func:`.helpers.find_span_linear`
    * ``insert_knot_func``: sets knot insertion implementation. *Default:* :func:`.operations.insert_knot`
    * ``remove_knot_func``: sets knot removal implementation. *Default:* :func:`.operations.remove_knot`

    Please refer to the :py:class:`.abstract.Volume()` documentation for more details.
    """

    def __init__(self, **kwargs):
        super(Volume, self).__init__(**kwargs)
        self._rational = True
        self._evaluator = evaluators.VolumeEvaluatorRational(find_span_func=self._span_func)
        # Variables for caching
        self.init_cache()

    def __deepcopy__(self, memo):
        # Call parent method
        result = super(Volume, self).__deepcopy__(memo)
        result.init_cache()
        return result

    def init_cache(self):
        self._cache['ctrlpts'] = self._init_array()
        self._cache['weights'] = self._init_array()

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
        return self._control_points

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
            self._cache['ctrlpts'] = [crd for crd in c]
            self._cache['weights'] = w
        return self._cache['ctrlpts']

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
            self._cache['ctrlpts'] = [crd for crd in c]
            self._cache['weights'] = w
        return self._cache['weights']

    @weights.setter
    def weights(self, value):
        if not self.ctrlpts:
            raise ValueError("Set control points first")

        # Generate weighted control points using the new weights
        ctrlptsw = compatibility.combine_ctrlpts_weights(self.ctrlpts, value)

        # Set weighted control points
        self.set_ctrlpts(ctrlptsw, self.ctrlpts_size_u, self.ctrlpts_size_v, self.ctrlpts_size_w)
