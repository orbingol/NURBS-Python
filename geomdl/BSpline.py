"""
.. module:: BSpline
    :platform: Unix, Windows
    :synopsis: Provides data storage and evaluation functionality for non-rational spline geometries

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import pickle
from . import abstract, evaluators, operations, tessellate, utilities
from . import _utilities as utl
from .exceptions import GeomdlException


@utl.export
class Curve(abstract.Curve):
    """ Data storage and evaluation class for n-variate B-spline (non-rational) curves.

    This class provides the following properties:

    * :py:attr:`type` = spline
    * :py:attr:`id`
    * :py:attr:`order`
    * :py:attr:`degree`
    * :py:attr:`knotvector`
    * :py:attr:`ctrlpts`
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

        from geomdl import BSpline

        # Create a 3-dimensional B-spline Curve
        curve = BSpline.Curve()

        # Set degree
        curve.degree = 3

        # Set control points
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
    # __slots__ = ('_insert_knot_func', '_remove_knot_func')

    def __init__(self, **kwargs):
        super(Curve, self).__init__(**kwargs)
        self._evaluator = evaluators.CurveEvaluator(find_span_func=self._span_func)
        self._insert_knot_func = kwargs.get('insert_knot_func', operations.insert_knot)
        self._remove_knot_func = kwargs.get('remove_knot_func', operations.remove_knot)

    def save(self, file_name):
        """  Saves the curve as a pickled file.

        .. deprecated:: 5.2.4

            Use :func:`.exchange.export_json()` instead.

        :param file_name: name of the file to be saved
        :type file_name: str
        """
        return None

    def load(self, file_name):
        """ Loads the curve from a pickled file.

        .. deprecated:: 5.2.4

            Use :func:`.exchange.import_json()` instead.

        :param file_name: name of the file to be loaded
        :type file_name: str
        """
        return None

    def evaluate(self, **kwargs):
        """ Evaluates the curve.

        The evaluated points are stored in :py:attr:`evalpts` property.

        Keyword arguments:
            * ``start``: start parameter
            * ``stop``: stop parameter

        The ``start`` and ``stop`` parameters allow evaluation of a curve segment in the range *[start, stop]*, i.e.
        the curve will also be evaluated at the ``stop`` parameter value.

        The following examples illustrate the usage of the keyword arguments.

        .. code-block:: python

            # Start evaluating from u=0.2 to u=1.0
            curve.evaluate(start=0.2)

            # Start evaluating from u=0.0 to u=0.7
            curve.evaluate(stop=0.7)

            # Start evaluating from u=0.1 to u=0.5
            curve.evaluate(start=0.1, stop=0.5)

            # Get the evaluated points
            curve_points = curve.evalpts
        """
        # Call parent method
        super(Curve, self).evaluate(**kwargs)

        # Find evaluation start and stop parameter values
        start = kwargs.get('start', self.knotvector[self.degree])
        stop = kwargs.get('stop', self.knotvector[-(self.degree + 1)])

        # Check parameters
        if self._kv_normalize:
            if not utilities.check_params([start, stop]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Clean up the curve points
        self.reset(evalpts=True)

        # Evaluate and cache
        self._eval_points = self._evaluator.evaluate(self.data, start=start, stop=stop)

    def evaluate_single(self, param):
        """ Evaluates the curve at the input parameter.

        :param param: parameter
        :type param: float
        :return: evaluated surface point at the given parameter
        :rtype: list
        """
        # Call parent method
        super(Curve, self).evaluate_single(param)

        # Check parameters
        if self._kv_normalize:
            if not utilities.check_params([param]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Evaluate the curve point
        pt = self._evaluator.evaluate(self.data, start=param, stop=param)

        return pt[0]

    def evaluate_list(self, param_list):
        """ Evaluates the curve for an input range of parameters.

        :param param_list: list of parameters
        :type param_list: list, tuple
        :return: evaluated surface points at the input parameters
        :rtype: list
        """
        # Call parent method
        super(Curve, self).evaluate_list(param_list)

        # Evaluate parameter list
        res = []
        for prm in param_list:
            if self._kv_normalize:
                if utilities.check_params([prm]):
                    res.append(self.evaluate_single(prm))
            else:
                res.append(self.evaluate_single(prm))
        return res

    def derivatives(self, u, order=0, **kwargs):
        """ Evaluates n-th order curve derivatives at the given parameter value.

        The output of this method is list of n-th order derivatives. If ``order`` is ``0``, then it will only output
        the evaluated point. Similarly, if ``order`` is ``2``, then it will output the evaluated point, 1st derivative
        and the 2nd derivative. For instance;

        .. code-block:: python

            # Assuming a curve (crv) is defined on a parametric domain [0.0, 1.0]
            # Let's take the curve derivative at the parametric position u = 0.35
            ders = crv.derivatives(u=0.35, order=2)
            ders[0]  # evaluated point, equal to crv.evaluate_single(0.35)
            ders[1]  # 1st derivative at u = 0.35
            ders[2]  @ 2nd derivative at u = 0.35

        :param u: parameter value
        :type u: float
        :param order: derivative order
        :type order: int
        :return: a list containing up to {order}-th derivative of the curve
        :rtype: list
        """
        # Call parent method
        super(Curve, self).derivatives(u=u, order=order, **kwargs)

        # Evaluate and return the derivative at knot u
        return self._evaluator.derivatives(self.data, parpos=u, deriv_order=order)

    def insert_knot(self, param, **kwargs):
        """ Inserts the knot and updates the control points array and the knot vector.

        Keyword Arguments:
            * ``num``: Number of knot insertions. *Default: 1*

        :param param: knot to be inserted
        :type param: float
        """
        # Check if all required parameters are set before the evaluation
        self._check_variables()

        # Check parameters are correct
        if self._kv_normalize:
            if not utilities.check_params([param]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Get keyword arguments
        num = kwargs.get('num', 1)  # number of knot insertions
        check_num = kwargs.get('check_r', True)  # can be set to False when the caller checks number of insertions

        # Insert knot
        try:
            self._insert_knot_func(self, [param], [num], check_num=check_num)
        except GeomdlException as e:
            print(e)
            return

        # Evaluate curve again if it has already been evaluated before knot insertion
        if check_num and self._eval_points:
            self.evaluate()

    def remove_knot(self, param, **kwargs):
        """ Removes the knot and updates the control points array and the knot vector.

        Keyword Arguments:
            * ``num``: Number of knot removals. *Default: 1*

        :param param: knot to be removed
        :type param: float
        """
        # Check if all required parameters are set before the evaluation
        self._check_variables()

        # Check param parameters are correct
        if self._kv_normalize:
            if not utilities.check_params([param]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Get keyword arguments
        num = kwargs.get('num', 1)  # number of knot removals
        check_num = kwargs.get('check_r', True)  # can be set to False when the caller checks number of removals

        # Remove knot
        try:
            self._remove_knot_func(self, [param], [num], check_num=check_num)
        except GeomdlException as e:
            print(e)
            return

        # Evaluate curve again if it has already been evaluated before knot removal
        if check_num and self._eval_points:
            self.evaluate()

    def tangent(self, parpos, **kwargs):
        """ Evaluates the tangent vector of the curve at the given parametric position(s).

        .. deprecated: 5.3.0

            Please use :func:`operations.tangent` instead.

        :param parpos: parametric position(s) where the evaluation will be executed
        :type parpos: float, list or tuple
        :return: tangent vector as a tuple of the origin point and the vector components
        :rtype: tuple
        """
        return tuple()

    def normal(self, parpos, **kwargs):
        """ Evaluates the normal to the tangent vector of the curve at the given parametric position(s).

        .. deprecated: 5.3.0

        :param parpos: parametric position(s) where the evaluation will be executed
        :type parpos: float, list or tuple
        :return: normal vector as a tuple of the origin point and the vector components
        :rtype: tuple
        """
        return tuple()

    def binormal(self, parpos, **kwargs):
        """ Evaluates the binormal vector of the curve at the given parametric position(s).

        .. deprecated: 5.3.0

        :param parpos: parametric position(s) where the evaluation will be executed
        :type parpos: float, list or tuple
        :return: binormal vector as a tuple of the origin point and the vector components
        :rtype: tuple
        """
        return tuple()


@utl.export
class Surface(abstract.Surface):
    """ Data storage and evaluation class for B-spline (non-rational) surfaces.

    This class provides the following properties:

    * :py:attr:`type` = spline
    * :py:attr:`id`
    * :py:attr:`order_u`
    * :py:attr:`order_v`
    * :py:attr:`degree_u`
    * :py:attr:`degree_v`
    * :py:attr:`knotvector_u`
    * :py:attr:`knotvector_v`
    * :py:attr:`ctrlpts`
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

        from geomdl import BSpline

        # Create a BSpline surface instance (Bezier surface)
        surf = BSpline.Surface()

        # Set degrees
        surf.degree_u = 3
        surf.degree_v = 2

        # Set control points
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
    # __slots__ = ('_insert_knot_func', '_remove_knot_func', '_control_points2D')

    def __init__(self, **kwargs):
        super(Surface, self).__init__(**kwargs)
        self._evaluator = evaluators.SurfaceEvaluator(find_span_func=self._span_func)
        self._tsl_component = tessellate.TriangularTessellate()
        self._control_points2D = self._init_array()  # control points, 2-D array [u][v]
        self._insert_knot_func = kwargs.get('insert_knot_func', operations.insert_knot)
        self._remove_knot_func = kwargs.get('remove_knot_func', operations.remove_knot)

    @property
    def ctrlpts2d(self):
        """ 2-dimensional array of control points.

        The getter returns a tuple of 2D control points (weighted control points + weights if NURBS) in *[u][v]* format.
        The rows of the returned tuple correspond to v-direction and the columns correspond to u-direction.

        The following example can be used to traverse 2D control points:

        .. code-block:: python
            :linenos:

            # Create a BSpline surface
            surf_bs = BSpline.Surface()

            # Do degree, control points and knot vector assignments here

            # Each u includes a row of v values
            for u in surf_bs.ctrlpts2d:
                # Each row contains the coordinates of the control points
                for v in u:
                    print(str(v))  # will be something like (1.0, 2.0, 3.0)

            # Create a NURBS surface
            surf_nb = NURBS.Surface()

            # Do degree, weighted control points and knot vector assignments here

            # Each u includes a row of v values
            for u in surf_nb.ctrlpts2d:
                # Each row contains the coordinates of the weighted control points
                for v in u:
                    print(str(v))  # will be something like (0.5, 1.0, 1.5, 0.5)


        When using **NURBS.Surface** class, the output of :py:attr:`~ctrlpts2d` property could be confusing since,
        :py:attr:`~ctrlpts` always returns the unweighted control points, i.e. :py:attr:`~ctrlpts` property returns 3D
        control points all divided by the weights and you can use :py:attr:`~weights` property to access the weights
        vector, but :py:attr:`~ctrlpts2d` returns the weighted ones plus weights as the last element.
        This difference is intentionally added for compatibility and interoperability purposes.

        To explain this situation in a simple way;

        * If you need the weighted control points directly, use :py:attr:`~ctrlpts2d`
        * If you need the control points and the weights separately, use :py:attr:`~ctrlpts` and :py:attr:`~weights`

        .. note::

            Please note that the setter doesn't check for inconsistencies and using the setter is not recommended.
            Instead of the setter property, please use :func:`.set_ctrlpts()` function.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points as a 2-dimensional array in [u][v] format
        :setter: Sets the control points as a 2-dimensional array in [u][v] format
        :type: list
        """
        return self._control_points2D

    @ctrlpts2d.setter
    def ctrlpts2d(self, value):
        if not isinstance(value, (list, tuple)):
            raise ValueError("The input must be a list or tuple")

        # Clean up the surface and control points
        self.reset(evalpts=True, ctrlpts=True)

        # Assume that the user has prepared the lists correctly
        size_u = len(value)
        size_v = len(value[0])

        # Estimate dimension by checking the size of the first element
        self._dimension = len(value[0][0])

        # Make sure that all numbers are float type
        ctrlpts = [[] for _ in range(size_u * size_v)]
        for u in range(size_u):
            for v in range(size_v):
                idx = v + (size_v * u)
                ctrlpts[idx] = [float(coord) for coord in value[u][v]]

        # Set control points
        self.set_ctrlpts(ctrlpts, size_u, size_v)

    def set_ctrlpts(self, ctrlpts, *args, **kwargs):
        """ Sets the control points and checks if the data is consistent.

        This method is designed to provide a consistent way to set control points whether they are weighted or not.
        It directly sets the control points member of the class, and therefore it doesn't return any values.
        The input will be an array of coordinates. If you are working in the 3-dimensional space, then your coordinates
        will be an array of 3 elements representing *(x, y, z)* coordinates.

        This method also generates 2D control points in *[u][v]* format which can be accessed via :py:attr:`~ctrlpts2d`.

        .. note::

            The v index varies first. That is, a row of v control points for the first u value is found first.
            Then, the row of v control points for the next u value.

        :param ctrlpts: input control points as a list of coordinates
        :type ctrlpts: list
        """
        # Call parent function
        super(Surface, self).set_ctrlpts(ctrlpts, *args, **kwargs)

        # Generate a 2-dimensional list of control points
        array_init2d = kwargs.get('array_init2d', [[[] for _ in range(args[1])] for _ in range(args[0])])
        ctrlpts_float2d = array_init2d
        for i in range(0, self.ctrlpts_size_u):
            for j in range(0, self.ctrlpts_size_v):
                ctrlpts_float2d[i][j] = self._control_points[j + (i * self.ctrlpts_size_v)]

        # Set the new 2-dimension control points
        self._control_points2D = ctrlpts_float2d

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:
            * ``evalpts``: if True, then resets evaluated points
            * ``ctrlpts`` if True, then resets control points

        """
        # Call parent function
        super(Surface, self).reset(**kwargs)

        # Reset ctrlpts2d
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        if reset_ctrlpts:
            self._control_points2D = self._init_array()

    def save(self, file_name):
        """ Saves the surface as a pickled file.

        .. deprecated:: 5.2.4

            Use :func:`.exchange.export_json()` instead.

        :param file_name: name of the file to be saved
        :type file_name: str
        """
        return None

    def load(self, file_name):
        """ Loads the surface from a pickled file.

        .. deprecated:: 5.2.4

            Use :func:`.exchange.import_json()` instead.

        :param file_name: name of the file to be loaded
        :type file_name: str
        """
        return None

    def transpose(self):
        """ Transposes the surface by swapping u and v parametric directions. """
        operations.transpose(self, inplace=True)
        self.reset(evalpts=True)

    def evaluate(self, **kwargs):
        """ Evaluates the surface.

        The evaluated points are stored in :py:attr:`evalpts` property.

        Keyword arguments:
            * ``start_u``: start parameter on the u-direction
            * ``stop_u``: stop parameter on the u-direction
            * ``start_v``: start parameter on the v-direction
            * ``stop_v``: stop parameter on the v-direction

        The ``start_u``, ``start_v`` and ``stop_u`` and ``stop_v`` parameters allow evaluation of a surface segment
        in the range  *[start_u, stop_u][start_v, stop_v]* i.e. the surface will also be evaluated at the ``stop_u``
        and ``stop_v`` parameter values.

        The following examples illustrate the usage of the keyword arguments.

        .. code-block:: python
            :linenos:

            # Start evaluating in range u=[0, 0.7] and v=[0.1, 1]
            surf.evaluate(stop_u=0.7, start_v=0.1)

            # Start evaluating in range u=[0, 1] and v=[0.1, 0.3]
            surf.evaluate(start_v=0.1, stop_v=0.3)

            # Get the evaluated points
            surface_points = surf.evalpts

        """
        # Call parent method
        super(Surface, self).evaluate(**kwargs)

        # Find evaluation start and stop parameter values
        start_u = kwargs.get('start_u', self.knotvector_u[self.degree_u])
        stop_u = kwargs.get('stop_u', self.knotvector_u[-(self.degree_u + 1)])
        start_v = kwargs.get('start_v', self.knotvector_v[self.degree_v])
        stop_v = kwargs.get('stop_v', self.knotvector_v[-(self.degree_v + 1)])

        # Check parameters
        if self._kv_normalize:
            if not utilities.check_params([start_u, stop_u, start_v, stop_v]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Evaluate and cache
        self._eval_points = self._evaluator.evaluate(self.data,
                                                     start=(start_u, start_v),
                                                     stop=(stop_u, stop_v))

    def evaluate_single(self, param):
        """ Evaluates the surface at the input (u, v) parameter pair.

        :param param: parameter pair (u, v)
        :type param: list, tuple
        :return: evaluated surface point at the given parameter pair
        :rtype: list
        """
        # Call parent method
        super(Surface, self).evaluate_single(param)

        # Evaluate the surface point
        pt = self._evaluator.evaluate(self.data, start=param, stop=param)

        return pt[0]

    def evaluate_list(self, param_list):
        """ Evaluates the surface for a given list of (u, v) parameters.

        :param param_list: list of parameter pairs (u, v)
        :type param_list: list, tuple
        :return: evaluated surface point at the input parameter pairs
        :rtype: tuple
        """
        # Call parent method
        super(Surface, self).evaluate_list(param_list)

        # Evaluate (u,v) list
        res = []
        for prm in param_list:
            if self._kv_normalize:
                if utilities.check_params(prm):
                    res.append(self.evaluate_single(prm))
            else:
                res.append(self.evaluate_single(prm))
        return res

    # Evaluates n-th order surface derivatives at the given (u,v) parameter
    def derivatives(self, u, v, order=0, **kwargs):
        """ Evaluates n-th order surface derivatives at the given (u, v) parameter pair.

        * SKL[0][0] will be the surface point itself
        * SKL[0][1] will be the 1st derivative w.r.t. v
        * SKL[2][1] will be the 2nd derivative w.r.t. u and 1st derivative w.r.t. v

        :param u: parameter on the u-direction
        :type u: float
        :param v: parameter on the v-direction
        :type v: float
        :param order: derivative order
        :type order: integer
        :return: A list SKL, where SKL[k][l] is the derivative of the surface S(u,v) w.r.t. u k times and v l times
        :rtype: list
        """
        # Call parent method
        super(Surface, self).derivatives(u=u, v=v, order=order, **kwargs)

        # Evaluate and return the derivatives
        return self._evaluator.derivatives(self.data, parpos=(u, v), deriv_order=order)

    def insert_knot(self, u=None, v=None, **kwargs):
        """ Inserts knot(s) on the u- or v-directions

        Keyword Arguments:
            * ``num_u``: Number of knot insertions on the u-direction. *Default: 1*
            * ``num_v``: Number of knot insertions on the v-direction. *Default: 1*

        :param u: knot to be inserted on the u-direction
        :type u: float
        :param v: knot to be inserted on the v-direction
        :type v: float
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Check if the parameter values are correctly defined
        if self._kv_normalize:
            if not utilities.check_params([u, v]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Get keyword arguments
        num_u = kwargs.get('num_u', 1)  # number of knot insertions on the u-direction
        num_v = kwargs.get('num_v', 1)  # number of knot insertions on the v-direction
        check_num = kwargs.get('check_r', True)  # Enables/disables number of knot insertions checking

        # Insert knots
        try:
            self._insert_knot_func(self, [u, v], [num_u, num_v], check_num=check_num)
        except GeomdlException as e:
            print(e)
            return

        # Evaluate surface again if it has already been evaluated before knot insertion
        if check_num and self._eval_points:
            self.evaluate()

    def remove_knot(self, u=None, v=None, **kwargs):
        """ Inserts knot(s) on the u- or v-directions

        Keyword Arguments:
            * ``num_u``: Number of knot removals on the u-direction. *Default: 1*
            * ``num_v``: Number of knot removals on the v-direction. *Default: 1*

        :param u: knot to be removed on the u-direction
        :type u: float
        :param v: knot to be removed on the v-direction
        :type v: float
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Check if the parameter values are correctly defined
        if self._kv_normalize:
            if not utilities.check_params([u, v]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Get keyword arguments
        num_u = kwargs.get('num_u', 1)  # number of knot removals on the u-direction
        num_v = kwargs.get('num_v', 1)  # number of knot removals on the v-direction
        check_num = kwargs.get('check_r', True)  # can be set to False when the caller checks number of removals

        # Remove knots
        try:
            self._remove_knot_func(self, [u, v], [num_u, num_v], check_num=check_num)
        except GeomdlException as e:
            print(e)
            return

        # Evaluate curve again if it has already been evaluated before knot removal
        if check_num and self._eval_points:
            self.evaluate()

    def tangent(self, parpos, **kwargs):
        """ Evaluates the tangent vectors of the surface at the given parametric position(s).

        .. deprecated: 5.3.0

            Please use :func:`operations.tangent` instead.

        :param parpos: parametric position(s) where the evaluation will be executed
        :type parpos: list or tuple
        :return: an array containing "point" and "vector"s on u- and v-directions, respectively
        :rtype: tuple
        """
        return tuple()

    def normal(self, parpos, **kwargs):
        """ Evaluates the normal vector of the surface at the given parametric position(s).

        .. deprecated: 5.3.0

            Please use :func:`operations.normal` instead.

        :param parpos: parametric position(s) where the evaluation will be executed
        :type parpos: list or tuple
        :return: an array containing "point" and "vector" pairs
        :rtype: tuple
        """
        return tuple()


@utl.export
class Volume(abstract.Volume):
    """ Data storage and evaluation class for B-spline (non-rational) volumes.

    This class provides the following properties:

    * :py:attr:`type` = spline
    * :py:attr:`id`
    * :py:attr:`order_u`
    * :py:attr:`order_v`
    * :py:attr:`order_w`
    * :py:attr:`degree_u`
    * :py:attr:`degree_v`
    * :py:attr:`degree_w`
    * :py:attr:`knotvector_u`
    * :py:attr:`knotvector_v`
    * :py:attr:`knotvector_w`
    * :py:attr:`ctrlpts`
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
    # __slots__ = ('_insert_knot_func', '_remove_knot_func')

    def __init__(self, **kwargs):
        super(Volume, self).__init__(**kwargs)
        self._evaluator = evaluators.VolumeEvaluator(find_span_func=self._span_func)
        self._insert_knot_func = kwargs.get('insert_knot_func', operations.insert_knot)
        self._remove_knot_func = kwargs.get('remove_knot_func', operations.remove_knot)

    def save(self, file_name):
        """ Saves the volume as a pickled file.

        .. deprecated:: 5.2.4

            Use :func:`.exchange.export_json()` instead.

        :param file_name: name of the file to be saved
        :type file_name: str
        """
        return None

    def load(self, file_name):
        """ Loads the volume from a pickled file.

        .. deprecated:: 5.2.4

            Use :func:`.exchange.import_json()` instead.

        :param file_name: name of the file to be loaded
        :type file_name: str
        """
        return None

    def evaluate(self, **kwargs):
        """ Evaluates the volume.

        The evaluated points are stored in :py:attr:`evalpts` property.

        Keyword arguments:
            * ``start_u``: start parameter on the u-direction
            * ``stop_u``: stop parameter on the u-direction
            * ``start_v``: start parameter on the v-direction
            * ``stop_v``: stop parameter on the v-direction
            * ``start_w``: start parameter on the w-direction
            * ``stop_w``: stop parameter on the w-direction

        """
        # Call parent method
        super(Volume, self).evaluate(**kwargs)

        # Find evaluation start and stop parameter values
        start_u = kwargs.get('start_u', self.knotvector_u[self.degree_u])
        stop_u = kwargs.get('stop_u', self.knotvector_u[-(self.degree_u + 1)])
        start_v = kwargs.get('start_v', self.knotvector_v[self.degree_v])
        stop_v = kwargs.get('stop_v', self.knotvector_v[-(self.degree_v + 1)])
        start_w = kwargs.get('start_w', self.knotvector_w[self.degree_w])
        stop_w = kwargs.get('stop_w', self.knotvector_w[-(self.degree_w + 1)])

        # Check if all the input parameters are in the range
        if self._kv_normalize:
            if not utilities.check_params([start_u, stop_u, start_v, stop_v, start_w, stop_w]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Clean up the evaluated points
        self.reset(evalpts=True)

        # Evaluate and cache
        self._eval_points = self._evaluator.evaluate(self.data,
                                                     start=(start_u, start_v, start_w),
                                                     stop=(stop_u, stop_v, stop_w))

    def evaluate_single(self, param):
        """ Evaluates the volume at the input (u, v, w) parameter.

        :param param: parameter (u, v, w)
        :type param: list, tuple
        :return: evaluated surface point at the given parameter pair
        :rtype: list
        """
        # Call parent method
        super(Volume, self).evaluate_single(param)

        # Check if all parameters are in the range
        if self._kv_normalize:
            if not utilities.check_params(param):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Evaluate the volume point
        pt = self._evaluator.evaluate(self.data, start=param, stop=param)
        return pt[0]

    def evaluate_list(self, param_list):
        """ Evaluates the volume for a given list of (u, v, w) parameters.

        :param param_list: list of parameters in format (u, v, w)
        :type param_list: list, tuple
        :return: evaluated surface point at the input parameter pairs
        :rtype: tuple
        """
        # Call parent method
        super(Volume, self).evaluate_list(param_list)

        # Evaluate (u, v, w) list
        res = []
        for prm in param_list:
            if self._kv_normalize:
                if utilities.check_params(prm):
                    res.append(self.evaluate_single(prm))
            else:
                res.append(self.evaluate_single(prm))
        return res

    def insert_knot(self, u=None, v=None, w=None, **kwargs):
        """ Inserts knot(s) on the u-, v- and w-directions

        Keyword Arguments:
            * ``num_u``: Number of knot insertions on the u-direction. *Default: 1*
            * ``num_v``: Number of knot insertions on the v-direction. *Default: 1*
            * ``num_w``: Number of knot insertions on the w-direction. *Default: 1*

        :param u: knot to be inserted on the u-direction
        :type u: float
        :param v: knot to be inserted on the v-direction
        :type v: float
        :param w: knot to be inserted on the w-direction
        :type w: float
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Check if the parameter values are correctly defined
        if self._kv_normalize:
            if not utilities.check_params([u, v, w]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Get keyword arguments
        num_u = kwargs.get('num_u', 1)  # number of knot insertions on the u-direction
        num_v = kwargs.get('num_v', 1)  # number of knot insertions on the v-direction
        num_w = kwargs.get('num_w', 1)  # number of knot insertions on the w-direction
        check_num = kwargs.get('check_r', True)  # Enables/disables number of knot insertions checking

        # Insert knots
        try:
            self._insert_knot_func(self, [u, v, w], [num_u, num_v, num_w], check_num=check_num)
        except GeomdlException as e:
            print(e)
            return

        # Evaluate surface again if it has already been evaluated before knot insertion
        if check_num and self._eval_points:
            self.evaluate()

    def remove_knot(self, u=None, v=None, w=None, **kwargs):
        """ Inserts knot(s) on the u-, v- and w-directions

        Keyword Arguments:
            * ``num_u``: Number of knot removals on the u-direction. *Default: 1*
            * ``num_v``: Number of knot removals on the v-direction. *Default: 1*
            * ``num_w``: Number of knot removals on the w-direction. *Default: 1*

        :param u: knot to be removed on the u-direction
        :type u: float
        :param v: knot to be removed on the v-direction
        :type v: float
        :param w: knot to be removed on the w-direction
        :type w: float
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Check if the parameter values are correctly defined
        if self._kv_normalize:
            if not utilities.check_params([u, v, w]):
                raise GeomdlException("Parameters should be between 0 and 1")

        # Get keyword arguments
        num_u = kwargs.get('num_u', 1)  # number of knot removals on the u-direction
        num_v = kwargs.get('num_v', 1)  # number of knot removals on the v-direction
        num_w = kwargs.get('num_w', 1)  # number of knot insertions on the w-direction
        check_num = kwargs.get('check_r', True)  # can be set to False when the caller checks number of removals

        # Remove knots
        try:
            self._remove_knot_func(self, [u, v, w], [num_u, num_v, num_w], check_num=check_num)
        except GeomdlException as e:
            print(e)
            return

        # Evaluate curve again if it has already been evaluated before knot removal
        if check_num and self._eval_points:
            self.evaluate()
