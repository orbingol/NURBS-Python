"""
.. module:: abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract base classes for representing the geometries

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import abc
from .six import add_metaclass
from .base import GeomdlBase, GeomdlEvaluator, GeomdlList, GeomdlDict, GeomdlError, GeomdlWarning, GeomdlTypeSequence
from .control_points import CPManager
from . import vis, knotvector, utilities


@add_metaclass(abc.ABCMeta)
class Geometry(GeomdlBase):
    """ Abstract base class for defining geometry objects.

    This class provides the following properties:

    * :py:attr:`id`
    * :py:attr:`name`
    * :py:attr:`type`
    * :py:attr:`dimension`
    * :py:attr:`opt`
    * :py:attr:`evalpts`

    This class provides the following methods:

    * :py:meth:`get_opt`
    * :py:meth:`reset`

    This class provides the following abstract methods:

    * :py:meth:`evaluate`

    This class provides the following keyword arguments:

    * ``id``: object ID (as an integer). *Default: 0*
    * ``name``: object name. *Default: name of the class*
    """
    __slots__ = ('_eval_points')

    def __init__(self, *args, **kwargs):
        super(Geometry, self).__init__(*args, **kwargs)
        self._geom_type = "default"  # geometry type
        self._eval_points = list()  # evaluated points

    @property
    def evalpts(self):
        """ Evaluated points

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the coordinates of the evaluated points
        """
        if not self._eval_points:
            self.evaluate()
        return self._eval_points

    @property
    def data(self):
        """ Returns a dict which contains the geometry information

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the geometry information
        """
        return GeomdlDict(
            type=self.type,
            dimension=self.dimension
        )

    def reset(self, **kwargs):
        """ Clears computed/generated data, such as caches and evaluated points """
        super(Geometry, self).reset(**kwargs)
        self._eval_points = list()

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Abstract method for the implementation of evaluation algorithm

        .. note::

            This is an abstract method and it must be implemented in the subclass.
        """


@add_metaclass(abc.ABCMeta)
class SplineGeometry(Geometry):
    """ Abstract base class for defining spline geometry objects.

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
    * :py:attr:`weights` (for completeness)
    * :py:attr:`ctrlpts_size`
    * :py:attr:`sample_size`
    * :py:attr:`delta`
    * :py:attr:`domain`
    * :py:attr:`range`
    * :py:attr:`bbox`
    * :py:attr:`trims` (for completeness)
    * :py:attr:`evaluator`
    * :py:attr:`vis`
    * :py:attr:`data`

    This class provides the following methods:

    * :py:meth:`get_opt`
    * :py:meth:`reset`
    * :py:meth:`set_ctrlpts`
    * :py:meth:`evaluate_list`

    This class provides the following abstract methods:

    * :py:meth:`evaluate`
    * :py:meth:`evaluate_single`
    * :py:meth:`derivatives`

    This class provides the following keyword arguments:

    * ``id``: object ID (as an integer). *Default: 0*
    * ``name``: object name. *Default: name of the class*
    * ``normalize_kv``: if True, knot vector(s) will be normalized to [0,1] domain. *Default: True*
    """
    __slots__ = (
         '_pdim', '_dinit', '_attribs', '_rational', '_degree', '_knot_vector', '_control_points', '_control_points_size',
         '_delta', '_bounding_box', '_evaluator', '_vis_component'
    )

    def __init__(self, *args, **kwargs):
        super(SplineGeometry, self).__init__(*args, **kwargs)
        # Update the following if defined in the child class
        self._pdim = 0 if not hasattr(self, '_pdim') else self._pdim  # parametric dimension
        self._dinit = 0.1 if not hasattr(self, '_dinit') else self._dinit  # evaluation delta init value
        self._attribs = tuple() if not hasattr(self, '_attribs') else self._attribs  # dynamic attributes

        # Initialize variables
        self._geom_type = "spline"  # geometry type
        self._rational = False  # defines whether the B-spline object is rational or not
        self._control_points = CPManager()  # control points
        self._bounding_box = list()  # bounding box
        self._evaluator = None  # evaluator instance
        self._vis_component = None  # visualization component
        self._degree = GeomdlList(  # degree
            [0 for _ in range(self._pdim)], attribs=self._attribs,
            cb=[self.reset], cbd=[validate_degree_value]
        )
        self._knot_vector = GeomdlList(  # knot vector
            [list() for _ in range(self._pdim)], attribs=self._attribs,
            cb=[self.reset], cbd=[validate_knotvector_value]
        )
        self._delta = GeomdlList(  # evaluation delta
            [self._dinit for _ in range(self._pdim)], attribs=self._attribs,
            cb=[self.reset], cbd=[validate_delta_value]
        )

        # Get keyword arguments
        self._cfg['config_normalize_kv'] = kwargs.pop('normalize_kv', True)  # flag to control knot vector normalization

    def __eq__(self, other):
        if not hasattr(other, '_pdim'):
            return False
        if not hasattr(other, '_degree') or not hasattr(other, '_knot_vector') or not hasattr(other, '_control_points'):
            return False
        if self.pdimension != other.pdimension:
            return False
        if self.rational != other.rational:
            return False
        try:
            for s, o in zip(self._control_points_size, other._control_points_size):
                if s != o:
                    return False
            chk_degree = []
            for s, o in zip(self._degree, other._degree):
                tmp = True if s == o else False
                chk_degree.append(tmp)
            if not all(chk_degree):
                return False
            chk_kv = []
            for sk, ok in zip(self._knot_vector, other._knot_vector):
                if len(sk) != len(ok):
                    return False
                chk = []
                for s, o in zip(sk, ok):
                    tmp = True if abs(s - o) < self._precision else False
                    chk.append(tmp)
                chk_kv.append(all(chk))
            if not all(chk_kv):
                return False
            chk_ctrlpts = []
            for sk, ok in zip(self._control_points, other._control_points):
                if len(sk) != len(ok):
                    return False
                chk = []
                for s, o in zip(sk, ok):
                    tmp = True if abs(s - o) < self._precision else False
                    chk.append(tmp)
                chk_ctrlpts.append(all(chk))
            if not all(chk_kv):
                return False
        except Exception:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def rational(self):
        """ Defines the rational and non-rational B-spline shapes.

        Rational shapes use homogeneous coordinates which includes a weight alongside with the Cartesian coordinates.
        Rational B-splines are also named as NURBS (Non-uniform rational basis spline) and non-rational B-splines are
        sometimes named as NUBS (Non-uniform basis spline) or directly as B-splines.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Returns True is the B-spline object is rational (NURBS)
        :type: bool
        """
        return self._rational

    @property
    def dimension(self):
        """ Spatial dimension.

        Spatial dimension will be automatically estimated from the first element of the control points array.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the spatial dimension, e.g. 2D, 3D, etc.
        :type: int
        """
        if self._rational:
            return self._control_points.dimension - 1
        return self._control_points.dimension

    @property
    def pdimension(self):
        """ Parametric dimension.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the parametric dimension
        :type: int
        """
        return self._pdim

    @property
    def order(self):
        """ Order

        Defined as ``order = degree + 1``

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the order
        :type: list
        """
        # Check cache for order
        if not self._cache['order']:
            self._cache['order'] = GeomdlList([p + 1 for p in self._degree], attribs=self.degree.attribs)
        return self._cache['order']

    @property
    def degree(self):
        """ Degree

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the degree
        :setter: Sets the degree
        :type: list
        """
        return self._degree

    @degree.setter
    def degree(self, value):
        self._degree.data = value.data if isinstance(value, GeomdlList) else value if isinstance(value, GeomdlTypeSequence) else [value]

    @property
    def knotvector(self):
        """ Knot vector

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the knot vector
        :setter: Sets the knot vector
        :type: list
        """
        return self._knot_vector

    @knotvector.setter
    def knotvector(self, value):
        val = value.data if isinstance(value, GeomdlList) else value if isinstance(value[0], GeomdlTypeSequence) else [value]
        self._knot_vector.data = [knotvector.normalize(v) if self._cfg['config_normalize_kv'] else v for v in val]

    @property
    def ctrlpts(self):
        """ Control points

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points
        :setter: Sets the control points
        :type: list
        """
        return self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")
        self._control_points = value
        # Reset bounding box
        self._bounding_box = list()

    @property
    def weights(self):
        """ Weights vector

        The weights vector is a part of control points definition. It is usually denoted by :math:`w`.
        For non-rational B-spline implementations, this property will return an empty tuple

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the weights
        :setter: Sets the weights
        """
        return tuple()

    @weights.setter
    def weights(self, value):
        pass

    @property
    def ctrlpts_size(self):
        """ Total number of control points

        :getter: Gets the total number of control points
        :type: int
        """
        return tuple(self._control_points.size)

    @property
    def sample_size(self):
        """ Sample size

        Sample size defines the number of evaluated points to generate. It also sets the ``delta`` property.

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        if not self._cache['sample_size']:
            self._cache['sample_size'] = [utilities.compute_sample_size_from_delta(d) for d in self._delta]
        return tuple(self._cache['sample_size'])

    @sample_size.setter
    def sample_size(self, value):
        for i in range(self.pdimension):
            if not isinstance(value[i], int):
                raise GeomdlError("Sample size must be an integer value")
            if not self._knot_vector[i] or self._degree[i] == 0:
                GeomdlWarning("Cannot determine the delta value. Please set knot vector and degree before sample size.")
                return

        # Set delta value(s)
        val = value.data if isinstance(value, GeomdlList) else value if isinstance(value, GeomdlTypeSequence) else [value]
        self._delta.data = [utilities.compute_delta_from_sample_size(val[i], self.domain[i], self.range[i]) for i in range(self.pdimension)]

    @property
    def delta(self):
        """ Evaluation delta

        Evaluation delta corresponds to the *step size* while ``evaluate`` function iterates on the knot vector to
        generate curve points. Decreasing step size results in generation of more curve points.
        Therefore; smaller the delta value, smoother the curve.

        The following figure illustrates the working principles of the delta property:

        .. math::

            \\left[{{u_{start}},{u_{start}} + \\delta ,({u_{start}} + \\delta ) + \\delta , \\ldots ,{u_{end}}} \\right]

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: list
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        self._delta.data = value.data if isinstance(value, GeomdlList) else value if isinstance(value, GeomdlTypeSequence) else [value]

    @property
    def domain(self):
        """ Domain

        Domain is determined using the knot vector(s).

        :getter: Gets the domain
        :type: list
        """
        if not self._cache['domain']:
            self._cache['domain'] = [(kv[self._degree[i]], kv[-(self._degree[i] + 1)]) for i, kv in enumerate(self._knot_vector)]
        return tuple(self._cache['domain'])

    @property
    def range(self):
        """ Domain range

        :getter: Gets the range
        :type: list
        """
        if not self._cache['range']:
            self._cache['range'] = [kv[-(self._degree[i]) + 1] - kv[self._degree[i]] for i, kv in enumerate(self._knot_vector)]
        return tuple(self._cache['range'])

    @property
    def bbox(self):
        """ Bounding box

        Evaluates the bounding box and returns the minimum and maximum coordinates.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the bounding box
        :type: tuple
        """
        if self._bounding_box is None or len(self._bounding_box) == 0:
            self._bounding_box = utilities.evaluate_bounding_box(self.ctrlpts)
        return self._bounding_box

    @property
    def trims(self):
        """ Trims

        This property should be reimplemented where necessary. Otherwise, it will return an empty tuple.

        :getter: Gets the trims
        """
        return tuple()

    @property
    def evaluator(self):
        """ Evaluator

        Evaluators allow users to use different algorithms for B-Spline and NURBS evaluations. Please see the
        documentation on ``Evaluator`` classes.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the current Evaluator instance
        :setter: Sets the Evaluator instance
        :type: evaluators.AbstractEvaluator
        """
        return self._evaluator

    @evaluator.setter
    def evaluator(self, value):
        if not isinstance(value, GeomdlEvaluator):
            raise GeomdlError("The evaluator must be an instance of AbstractEvaluator")
        self._evaluator = value

    @property
    def vis(self):
        """ Visualization component

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        :type: vis.VisAbstract
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, vis.VisAbstract):
            GeomdlWarning("Visualization component must be an instance of VisAbstract")
            return
        self._vis_component = value

    @property
    def data(self):
        """ Returns a dict which contains the geometry information

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the geometry information
        """
        data = super(SplineGeometry, self).data
        spl_data = GeomdlDict(
            rational=self.rational,
            pdimension=self.pdimension,
            delta=tuple(self._delta),
            sample_size=tuple(self.sample_size),
            degree=tuple(self.degree),
            knotvector=tuple(self.knotvector),
            size=tuple(self.ctrlpts_size),
            control_points=self.ctrlpts  # CPManager instance
        )
        data.update(spl_data)
        return data

    def set_ctrlpts(self, ctrlpts, *args, **kwargs):
        """ Sets control points and checks if the data is consistent

        This method is designed to provide a consistent way to set control points whether they are weighted or not.
        It directly sets the control points member of the class, and therefore it doesn't return any values.
        The input will be an array of coordinates. If you are working in the 3-dimensional space, then your coordinates
        will be an array of 3 elements representing *(x, y, z)* coordinates.

        :param ctrlpts: input control points as a list of coordinates
        :type ctrlpts: list
        :param args: number of control points corresponding to each parametric dimension
        :type args: tuple
        """
        # Argument validation
        if len(args) == 0:
            args = [len(ctrlpts)]
        if len(args) != self._pdim:
            raise GeomdlError("Number of arguments after ctrlpts must be " + str(self._pdim))

        # Set control points and sizes
        self._control_points = CPManager([int(arg) for arg in args])
        self._control_points.points = ctrlpts
        # Reset bounding box
        self._bounding_box = list()

    def check_variables(self):
        """ Checks if the evaluation is possible by validating the variables """
        for i in range(self.pdimension):
            # Check degree assignments
            validate_degree_value(self._attribs[i], self._degree[i])
            # Check knot vector assignments
            validate_knotvector_value(self._attribs[i], self._knot_vector[i])
            # Check knot vector validity
            if not knotvector.check(self._degree[i], self._knot_vector[i], self._control_points.size[i]):
                raise GeomdlError("Input is not a valid knot vector for the parametric dimension " + self._attribs[i])
            # Check delta values
            validate_delta_value(self._attribs[i], self._delta[i])

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Evaluates the geometry

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        """
        super(SplineGeometry, self).evaluate(**kwargs)
        # Check all parameters are set before the evaluation
        self.check_variables()

    @abc.abstractmethod
    def evaluate_single(self, param):
        """ Evaluates the geometry at the given parameter

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param param: parameter
        """
        # Check all required variables are set before the evaluation
        self.check_variables()

        if isinstance(param, (int, float)):
            param = [float(param) for _ in range(self.pdimension)]

        # Check parameters
        if self._cfg['config_normalize_kv']:
            if not utilities.check_params(param):
                raise GeomdlError("Parameters should be between 0 and 1")

    def evaluate_list(self, params):
        """ Evaluates the geometry for an input range of parameters

        :param params: parameters
        :type params: list, tuple
        """
        # Check all required variables are set before the evaluation
        self.check_variables()

        # Evaluate parameter list
        res = []
        for prm in params:
            if self._cfg['config_normalize_kv']:
                if utilities.check_params([prm]):
                    res.append(self.evaluate_single(prm))
            else:
                res.append(self.evaluate_single(prm))
        return res

    @abc.abstractmethod
    def derivatives(self, param, order, **kwargs):
        """ Evaluates the derivatives of the geometry at the given parameter

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param param: parameter
        :type param: list, tuple
        :param order: derivative order
        :type order: int
        """
        # Check all required variables are set before the evaluation
        self.check_variables()

        # Convert parameter input to the correct format
        if isinstance(param, (int, float)):
            param = [float(param) for _ in range(self.pdimension)]

        # Check parameters
        if self._cfg['config_normalize_kv']:
            if not utilities.check_params(param):
                raise GeomdlError("Parameters should be between 0 and 1")


def validate_degree_value(key, value):
    if value <= 0:
        raise GeomdlError("Degree " + str(key) + " should be bigger than zero")
    if not isinstance(value, int):
        raise GeomdlError("Degree " + str(key) + " must be an integer value")


def validate_knotvector_value(key, value):
    if not value:
        raise GeomdlError("Knot vector " + str(key) + " is empty")


def validate_delta_value(key, value):
    if not isinstance(value, float):
        raise GeomdlError("Delta value must be a float value for the dimension " + str(key))
    if value <= 0 or value >= 1:
        raise GeomdlError("Delta should be between 0.0 and 1.0 for the dimension " + str(key))
