"""
.. module:: BSpline
    :platform: Unix, Windows
    :synopsis: Provides data storage and evaluation functionality for non-rational B-spline geometries

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from numbers import Number
from .base import export, GeomdlError, GeomdlWarning, GeomdlDict, GeomdlFloat, GeomdlTypeSequence
from .abstract import SplineGeometry
from . import evaluators, tessellate, utilities


@export
class Curve(SplineGeometry):
    """ Data storage and evaluation class for n-variate B-spline (non-rational) curves.

    This class provides the following properties:

    * :py:attr:`id`
    * :py:attr:`name`
    * :py:attr:`type`
    * :py:attr:`opt`
    * :py:attr:`evalpts`
    * :py:attr:`rational`
    * :py:attr:`dimension`
    * :py:attr:`pdimension`
    * :py:attr:`order`
    * :py:attr:`degree`
    * :py:attr:`knotvector`
    * :py:attr:`ctrlpts`
    * :py:attr:`ctrlpts_size`
    * :py:attr:`sample_size`
    * :py:attr:`delta`
    * :py:attr:`domain`
    * :py:attr:`range`
    * :py:attr:`bbox`
    * :py:attr:`evaluator`
    * :py:attr:`vis`
    * :py:attr:`data`

    This class provides the following methods:

    * :py:meth:`get_opt`
    * :py:meth:`reset`
    * :py:meth:`set_ctrlpts`
    * :py:meth:`evaluate`
    * :py:meth:`evaluate_single`
    * :py:meth:`evaluate_list`
    * :py:meth:`derivatives`

    This class provides the following keyword arguments:

    * ``id``: object ID (as an integer). *Default: 0*
    * ``name``: object name. *Default: name of the class*
    * ``normalize_kv``: if True, knot vector(s) will be normalized to [0,1] domain. *Default: True*
    """

    def __init__(self, *args, **kwargs):
        kwargs.update(dict(pdimension=1, dinit=0.01, attribs=('u',)))
        super(Curve, self).__init__(*args, **kwargs)
        self._evaluator = evaluators.CurveEvaluator()  # initialize evaluator

    def evaluate(self, **kwargs):
        """ Evaluates the curve.

        The evaluated points are stored in :py:attr:`evalpts` property.

        Keyword arguments:
            * ``start``: start parameter
            * ``stop``: stop parameter

        The following examples illustrate the usage of the keyword arguments, assuming that the knot vector
        is defined within [0.0, 1.0] range by default. ``None`` input finds the default parameter automatically.

        .. code-block:: python
            :linenos:

            # Start evaluating the (u) range from (0.3) to (0.7)
            curve.evaluate(start=(0.1,), stop=(0.7,))

            # The following results the same as the above
            curve.evaluate(start=0.1, stop=0.7)

            # Start evaluating the (u) range from (0.0) to (0.2)
            curve.evaluate(start=(None,), stop=(0.2,))

            # Get the evaluated points
            curve_points = curve.evalpts

        """
        # Call parent method
        super(Curve, self).evaluate(**kwargs)

        # Prepare for the evaluation
        start, stop = prepare_evaluation(
            kwargs.get('start', None),
            kwargs.get('stop', None),
            self.domain,
            self._cfg['bool_normalize_kv'],
        )

        # Reset cached variables
        self.reset()

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

        # Evaluator input is a always a sequence
        if isinstance(param, Number):
            param = [param]

        # Evaluate the point
        pt = self._evaluator.evaluate(self.data, start=param, stop=param)
        return pt[0]


    def derivatives(self, param, order=0, **kwargs):
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
            ders[2]  # 2nd derivative at u = 0.35

        :param u: parameter (u)
        :type u: list, tuple
        :param order: derivative order
        :type order: int
        :return: a list containing up to {order}-th derivative of the curve
        :rtype: list
        """
        # Call parent method
        super(Curve, self).derivatives(param=param, order=order, **kwargs)

        # Evaluator input is a always a sequence
        if isinstance(param, Number):
            param = [param]

        # Evaluate and return the derivative at knot u
        return self._evaluator.derivatives(self.data, parpos=param, deriv_order=order)


@export
class Surface(SplineGeometry):
    """ Data storage and evaluation class for B-spline (non-rational) surfaces.

    This class provides the following properties:

    * :py:attr:`id`
    * :py:attr:`name`
    * :py:attr:`type`
    * :py:attr:`opt`
    * :py:attr:`evalpts`
    * :py:attr:`rational`
    * :py:attr:`dimension`
    * :py:attr:`pdimension`
    * :py:attr:`order`
    * :py:attr:`degree`
    * :py:attr:`knotvector`
    * :py:attr:`ctrlpts`
    * :py:attr:`ctrlpts_size`
    * :py:attr:`sample_size`
    * :py:attr:`delta`
    * :py:attr:`domain`
    * :py:attr:`range`
    * :py:attr:`bbox`
    * :py:attr:`evaluator`
    * :py:attr:`vis`
    * :py:attr:`data`

    This class provides the following methods:

    * :py:meth:`get_opt`
    * :py:meth:`reset`
    * :py:meth:`set_ctrlpts`
    * :py:meth:`evaluate`
    * :py:meth:`evaluate_single`
    * :py:meth:`evaluate_list`
    * :py:meth:`derivatives`

    This class provides the following keyword arguments:

    * ``id``: object ID (as an integer). *Default: 0*
    * ``name``: object name. *Default: name of the class*
    * ``normalize_kv``: if True, knot vector(s) will be normalized to [0,1] domain. *Default: True*
    """

    def __init__(self, *args, **kwargs):
        kwargs.update(dict(pdimension=2, dinit=0.01, attribs=('u', 'v')))
        super(Surface, self).__init__(*args, **kwargs)
        self._evaluator = evaluators.SurfaceEvaluator()
        self._trims = list()  # trimming curves
        self._tsl_component = tessellate.TriangularTessellate()  # tessellation component

    def reset(self, **kwargs):
        """ Clears computed/generated data, such as caches and evaluated points """
        # Call parent function
        super(Surface, self).reset(**kwargs)

        # Reset vertices and triangles
        self._tsl_component.reset()

    def evaluate(self, **kwargs):
        """ Evaluates the surface.

        The evaluated points are stored in :py:attr:`evalpts` property.

        Keyword arguments:
            * ``start``: start parameter
            * ``stop``: stop parameter

        The following examples illustrate the usage of the keyword arguments, assuming that the knot vectors
        are defined within [0.0, 1.0] range by default. ``None`` input finds the default parameter automatically.

        .. code-block:: python
            :linenos:

            # Start evaluating the (u, v) range from (0.0, 0.1) to (0.7, 1.0)
            surf.evaluate(start=(None, 0.1), stop=(0.7, None))

            # Start evaluating the (u, v) range from (0.2, 0.0) to (1.0, 0.3)
            surf.evaluate(start=(0.2, None), stop=(None, 0.3))

            # Start evaluating the (u, v) range from (0.5, 0.5) to (0.9, 0.9)
            surf.evaluate(start=(0.5, 0.5), stop=(0.9, 0.9))

            # The following results the same as the above
            surf.evaluate(start=0.5, stop=0.9)

            # Get the evaluated points
            surface_points = surf.evalpts

        """
        # Call parent method
        super(Surface, self).evaluate(**kwargs)

        # Prepare for the evaluation
        start, stop = prepare_evaluation(
            kwargs.get('start', None),
            kwargs.get('stop', None),
            self.domain,
            self._cfg['bool_normalize_kv'],
        )

        # Reset cached variables
        self.reset()

        # Evaluate and re-cache
        self._eval_points = self._evaluator.evaluate(self.data, start=start, stop=stop)

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

    # Evaluates n-th order surface derivatives at the given (u,v) parameter
    def derivatives(self, param, order=0, **kwargs):
        """ Evaluates n-th order surface derivatives at the given (u, v) parameter pair.

        * SKL[0][0] will be the surface point itself
        * SKL[0][1] will be the 1st derivative w.r.t. v
        * SKL[2][1] will be the 2nd derivative w.r.t. u and 1st derivative w.r.t. v

        :param param: parameter (u, v)
        :type param: list, tuple
        :param order: derivative order
        :type order: integer
        :return: A list SKL, where SKL[k][l] is the derivative of the surface S(u,v) w.r.t. u k times and v l times
        :rtype: list
        """
        # Call parent method
        super(Surface, self).derivatives(param=param, order=order, **kwargs)

        # Evaluate and return the derivatives
        return self._evaluator.derivatives(self.data, parpos=param, deriv_order=order)

    @property
    def data(self):
        """ Returns a dict which contains the geometry information

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the geometry information
        """
        data = super(Surface, self).data
        data.update(GeomdlDict(trims=tuple([t.data for t in self._trims])))
        return data

    @property
    def tessellator(self):
        """ Tessellation component.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the tessellation component
        :setter: Sets the tessellation component
        """
        return self._tsl_component

    @tessellator.setter
    def tessellator(self, value):
        if not isinstance(value, tessellate.AbstractTessellate):
            GeomdlWarning("Tessellation component must be an instance of AbstractTessellate class")
            return
        self._tsl_component = value

    @property
    def vertices(self):
        """ Vertices generated by the tessellation operation.

        If the tessellation component is set to None, the result will be an empty list.

        :getter: Gets the vertices
        """
        if self.tessellator is None:
            return tuple()
        if not self.tessellator.is_tessellated():
            self.tessellate()
        return self.tessellator.vertices

    @property
    def faces(self):
        """ Faces (triangles, quads, etc.) generated by the tessellation operation.

        If the tessellation component is set to None, the result will be an empty list.

        :getter: Gets the faces
        """
        if self.tessellator is None:
            return tuple()
        if not self.tessellator.is_tessellated():
            self.tessellate()
        return self.tessellator.faces

    @property
    def trims(self):
        """ Trim curves

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the array of trim curves
        :setter: Sets the array of trim curves
        """
        return tuple(self._trims)

    @trims.setter
    def trims(self, value):
        # Input type validation
        if not isinstance(value, GeomdlTypeSequence):
            raise GeomdlError("'trims' setter only accepts a list or a tuple containing the trimming curves")
        # Trim curve validation
        for i, v in enumerate(value):
            try:
                self.add_trim(v)
            except GeomdlError:
                raise GeomdlError("Invalid geometry at index " + str(i))

    def add_trim(self, trim):
        """ Adds a trim to the surface.

        A trim is a 2-dimensional curve defined on the parametric domain of the surface. Therefore, x-coordinate
        of the trimming curve corresponds to u parametric direction of the surfaceand y-coordinate of the trimming
        curve corresponds to v parametric direction of the surface.

        :attr:`trims` uses this method to add trims to the surface.

        :param trim: surface trimming curve
        :type trim: abstract.Geometry
        """
        if trim.dimension != 2:
            raise GeomdlError("Input geometry should be 2-dimensional")
        self._trims.append(trim)

    def tessellate(self, **kwargs):
        """ Tessellates the surface.

        Keyword arguments are directly passed to the tessellation component.
        """
        # Call tessellation component for vertex and triangle generation
        self._tsl_component.tessellate(
            self.evalpts,
            size_u=self.sample_size_u,
            size_v=self.sample_size_v,
            trims=self.trims,
            **kwargs
        )

        # Re-evaluate vertex coordinates
        for idx in range(len(self._tsl_component.vertices)):
            uv = self._tsl_component.vertices[idx].uv
            if self._cfg['bool_normalize_kv'] and not utilities.check_params(uv):
                continue
            self._tsl_component.vertices[idx].data = self.evaluate_single(uv)


@export
class Volume(SplineGeometry):
    """ Data storage and evaluation class for B-spline (non-rational) volumes.

    This class provides the following properties:

    * :py:attr:`id`
    * :py:attr:`name`
    * :py:attr:`type`
    * :py:attr:`opt`
    * :py:attr:`evalpts`
    * :py:attr:`rational`
    * :py:attr:`dimension`
    * :py:attr:`pdimension`
    * :py:attr:`order`
    * :py:attr:`degree`
    * :py:attr:`knotvector`
    * :py:attr:`ctrlpts`
    * :py:attr:`ctrlpts_size`
    * :py:attr:`sample_size`
    * :py:attr:`delta`
    * :py:attr:`domain`
    * :py:attr:`range`
    * :py:attr:`bbox`
    * :py:attr:`evaluator`
    * :py:attr:`vis`
    * :py:attr:`data`

    This class provides the following methods:

    * :py:meth:`get_opt`
    * :py:meth:`reset`
    * :py:meth:`set_ctrlpts`
    * :py:meth:`evaluate`
    * :py:meth:`evaluate_single`
    * :py:meth:`evaluate_list`
    * :py:meth:`derivatives`

    This class provides the following keyword arguments:

    * ``id``: object ID (as an integer). *Default: 0*
    * ``name``: object name. *Default: name of the class*
    * ``normalize_kv``: if True, knot vector(s) will be normalized to [0,1] domain. *Default: True*
    """

    def __init__(self, *args, **kwargs):
        kwargs.update(dict(pdimension=3, dinit=0.05, attribs=('u', 'v', 'w')))
        super(Volume, self).__init__(*args, **kwargs)
        self._evaluator = evaluators.VolumeEvaluator()

    def evaluate(self, **kwargs):
        """ Evaluates the volume.

        The evaluated points are stored in :py:attr:`evalpts` property.
        """
        # Call parent method
        super(Volume, self).evaluate(**kwargs)

        # Prepare for the evaluation
        start, stop = prepare_evaluation(
            kwargs.get('start', None),
            kwargs.get('stop', None),
            self.domain,
            self._cfg['bool_normalize_kv'],
        )

        # Reset cached variables
        self.reset()

        # Evaluate and re-cache
        self._eval_points = self._evaluator.evaluate(self.data, start=start, stop=stop)

    def evaluate_single(self, param):
        """ Evaluates the volume at the input (u, v, w) parameter.

        :param param: parameter (u, v, w)
        :type param: list, tuple
        :return: evaluated surface point at the given parameter pair
        :rtype: list
        """
        # Call parent method
        super(Volume, self).evaluate_single(param)

        # Evaluate the volume point
        pt = self._evaluator.evaluate(self.data, start=param, stop=param)
        return pt[0]

    def derivatives(self, param, order=0, **kwargs):
        pass


def prepare_evaluation(start, stop, domain, is_kv_normalized):
    def prep_single_parameter(prm, domain, key):
        if isinstance(prm, GeomdlTypeSequence):
            if len(prm) != len(domain):
                raise GeomdlError("Parameter input should be " + str(len(domain)) + "-dimensional")
            return [d[key] if GeomdlFloat(prm[i]) is None else prm[i] for i, d in enumerate(domain)]
        return [prm for _ in domain]

    # Find evaluation start and stop parameter values
    if start is None:
        start = [d[0] for d in domain]
    else:
        start = prep_single_parameter(start, domain, 0)

    if stop is None:
        stop = [d[1] for d in domain]
    else:
        stop = prep_single_parameter(stop, domain, 1)

    # Check parameters
    if is_kv_normalized:
        for st, sp in zip(start, stop):
            if not utilities.check_params([st, sp]):
                raise GeomdlError("Parameters should be between 0 and 1")

    return start, stop
