"""
.. module:: abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract base classes for representing the geometries

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import abc
from .base import GeomdlBase, GeomdlEvaluator, GeomdlError, GeomdlWarning
from .base import GeomdlFloat, GeomdlList, GeomdlDict, GeomdlTypeSequence
from .ptmanager import CPManager, separate_ctrlpts_weights, combine_ctrlpts_weights
from . import knotvector


class Geometry(GeomdlBase, metaclass=abc.ABCMeta):
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
    * ``callbacks``: a list of callback functions to be called after setting the attributes
    """
    __slots__ = ('_eval_points',)

    def __new__(cls, *args, **kwargs):
        obj = super(Geometry, cls).__new__(cls, *args, **kwargs)
        obj._cfg['evalpts_needs_reset'] = False
        return obj

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
        if not self._eval_points or self._cfg['evalpts_needs_reset']:
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


class AnalyticGeometry(Geometry, metaclass=abc.ABCMeta):
    """ Abstract base class for analytic-type geometry classes """
    def __init__(self, **kwargs):
        super(AnalyticGeometry, self).__init__(**kwargs)
        self._geometry_type = "analytic"

    @property
    def data(self):
        """ Returns a dict which contains the geometry data.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.
        """
        return dict(
            type=self.type,
            points=tuple(self.evalpts)
        )

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Evaluates/computes the points that form the geometry.

        .. note::

            This is an abstract method and it must be implemented in the subclass.
        """


class SplineGeometry(Geometry, metaclass=abc.ABCMeta):
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
    * ``callbacks``: a list of callback functions to be called after setting the attributes
    * ``normalize_kv``: if True, knot vector(s) will be normalized to [0,1] domain. *Default: True*
    """
    __slots__ = (
         '_pdim', '_attribs', '_rational', '_degree', '_knot_vector', '_control_points',
         '_ssinit', '_sample_size', '_bounding_box', '_evaluator'
    )

    def __new__(cls, *args, **kwargs):
        obj = super(SplineGeometry, cls).__new__(cls, *args, **kwargs)
        obj._cfg['normalize_kv'] = kwargs.pop('normalize_kv', True)  # flag to control knot vector normalization
        return obj

    def __init__(self, *args, **kwargs):
        cache_vars = kwargs.get('cache_vars', dict())
        cache_vars.update(
            dict(order=list(),
            sample_size=list(),
            domain=list(),
            range=list(),
            ctrlpts=CPManager(cb=[self._evalpts_reset]),
            weights=list())
        )
        kwargs.update(dict(cache_vars=cache_vars))
        super(SplineGeometry, self).__init__(*args, **kwargs)

        # Initialize variables
        self._pdim = kwargs.get('pdimension', 0) # number of parametric dimensions
        self._ssinit = int(kwargs.get('dinit', 50))  # sample size init value
        self._attribs = kwargs.get('attribs', tuple())  # dynamic attributes
        self._geom_type = "spline"  # geometry type
        self._rational = False  # defines whether the B-spline object is rational or not
        self._control_points = CPManager(cb=[self._evalpts_reset])  # control points
        self._bounding_box = list()  # bounding box
        self._evaluator = None  # evaluator instance
        self._degree = GeomdlList(  # degree
            *[0 for _ in range(self._pdim)], attribs=self._attribs,
            cb=[self.reset], cbd=[validate_degree_value]
        )
        self._knot_vector = GeomdlList(  # knot vector
            *[list() for _ in range(self._pdim)], attribs=self._attribs,
            cb=[self.reset], cbd=[validate_knotvector_value]
        )
        self._sample_size = GeomdlList(  # sample size for evaluation
            *[self._ssinit for _ in range(self._pdim)], attribs=self._attribs,
            cb=[self.reset], cbd=[validate_sample_size_value]
        )

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
            for s, o in zip(self._control_points.size, other._control_points.size):
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
                    tmp = True if abs(s - o) < 10e-7 else False
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
                    tmp = True if abs(s - o) < 10e-7 else False
                    chk.append(tmp)
                chk_ctrlpts.append(all(chk))
            if not all(chk_kv):
                return False
        except Exception:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def _evalpts_reset(self):
        self._cfg['evalpts_needs_reset'] = True

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
            temp = [p + 1 for p in self._degree]
            self._cache['order'] = GeomdlList(*temp, attribs=self.degree.attribs)
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
        self._degree.data = value.data if isinstance(value, GeomdlList) else value if isinstance(value, GeomdlTypeSequence) else [value for _ in range(self._pdim)]

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
        val = value.data if isinstance(value, GeomdlList) else value if isinstance(value[0], GeomdlTypeSequence) else [value for _ in range(self._pdim)]
        self._knot_vector.data = [knotvector.normalize(v) if self._cfg['normalize_kv'] else v for v in val]

    @property
    def ctrlpts(self):
        """ Control points

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points
        :setter: Sets the control points
        :type: list
        """
        if not self._cache['ctrlpts'] and self.rational:
            self._cache['ctrlpts'].size = self._control_points.size
            self._cache['ctrlpts'].points, self._cache['weights'] = separate_ctrlpts_weights(self._control_points.points)
        return self._cache['ctrlpts'] if self.rational else self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")

        if self.rational:
            # Check if we can retrieve the existing weights. If not, generate a weights vector of 1.0s.
            if not self.weights:
                weights = [1.0 for _ in range(len(value))]
            else:
                weights = self.weights

            # Generate weighted control points using the new control points
            value.points  = combine_ctrlpts_weights(value.points, weights)

        # Set new control points
        self._control_points = value
        self._control_points.set_callbacks([self._evalpts_reset])

        # Clear caches
        self.reset()

    @property
    def weights(self):
        """ Weights vector

        The weights vector is a part of control points definition. It is usually denoted by :math:`w`.
        For non-rational B-spline implementations, this property will return an empty list

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the weights vector
        :setter: Sets the weights vector
        :type: list
        """
        # Populate the cache, if necessary
        if not self._cache['weights'] and self.rational:
            _, self._cache['weights']  = separate_ctrlpts_weights(self._control_points.points)
        return self._cache['weights']

    @weights.setter
    def weights(self, value):
        if self.rational:
            # Generate weighted control points using the new weights
            ctrlptsw = combine_ctrlpts_weights(self.ctrlpts, value)
            # Set new weighted control points
            self._control_points.points = ctrlptsw
            # Clear caches
            self.reset()

    @property
    def ctrlptsw(self):
        """ Weighted control points (Pw)

        Weighted control points are in (x*w, y*w, z*w, w) format; where x,y,z are the coordinates and w is the weight.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the weighted control points
        :setter: Sets the weighted control points
        """
        return self._control_points

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        if not isinstance(value, CPManager):
            raise GeomdlError("Control points must be an instance of CPManager")
        self._control_points = value
        self._control_points.set_callbacks([self._evalpts_reset])
        # Clear caches
        self.reset()

    @property
    def ctrlpts_size(self):
        """ Total number of control points

        :getter: Gets the total number of control points
        :type: int
        """
        return self._control_points.size

    @property
    def sample_size(self):
        """ Sample size

        Sample size defines the number of evaluated points to generate.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        return self._sample_size

    @sample_size.setter
    def sample_size(self, value):
        self._sample_size.data = value.data if isinstance(value, GeomdlList) else value if isinstance(value, GeomdlTypeSequence) else [value for _ in range(self._pdim)]

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
            self._bounding_box = evaluate_bounding_box(self.ctrlpts)
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
            sample_size=tuple(self._sample_size),
            degree=tuple(self.degree),
            knotvector=tuple(self.knotvector),
            size=tuple(self.ctrlpts_size),
            control_points=self.ctrlptsw  # CPManager instance
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
        self._control_points = CPManager(*args, cb=[self._evalpts_reset])
        self._control_points.points = ctrlpts

        # Clear caches
        self.reset()

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
            # Make sure that the knot vector is normalized when normalize_kv = True
            if self._cfg['normalize_kv']:
                self._knot_vector[i] = knotvector.normalize(self._knot_vector[i])
            # Check sample size values
            validate_sample_size_value(self._attribs[i], self._sample_size[i])

    def reset(self, **kwargs):
        """ Clears computed/generated data, such as caches and evaluated points """
        super(SplineGeometry, self).reset(**kwargs)
        # Reset bounding box
        self._bounding_box = list()

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
            param = [GeomdlFloat(param) for _ in range(self.pdimension)]

        # Check parameters
        if self._cfg['normalize_kv']:
            if not validate_params(param):
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
            if self._cfg['normalize_kv']:
                if validate_params([prm]):
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
            param = [GeomdlFloat(param) for _ in range(self.pdimension)]

        # Check parameters
        if self._cfg['normalize_kv']:
            if not validate_params(param):
                raise GeomdlError("Parameters should be between 0 and 1")


def validate_degree_value(key, value):
    if value <= 0:
        raise GeomdlError("Degree " + str(key) + " should be bigger than zero")
    if not isinstance(value, int):
        raise GeomdlError("Degree " + str(key) + " must be an integer value")


def validate_knotvector_value(key, value):
    if not value:
        raise GeomdlError("Knot vector " + str(key) + " is empty")


def validate_sample_size_value(key, value):
    if not isinstance(value, int):
        raise GeomdlError("Sample size must be a int value for the dimension " + str(key))
    if value <= 1:
        raise GeomdlError("Sample size must be bigger than 1 for the dimension " + str(key))


def validate_params(params):
    """ Checks if the parameters are defined in the domain [0, 1].

    :param params: parameters (u, v, w)
    :type params: list, tuple
    :return: True if defined in the domain [0, 1]. False, otherwise.
    :rtype: bool
    """
    # Check parameters
    for prm in params:
        if prm is not None:
            if not 0.0 <= prm <= 1.0:
                return False
    return True


def evaluate_bounding_box(ctrlpts):
    """ Computes the minimum bounding box of the point set.

    The (minimum) bounding box is the smallest enclosure in which all the input points lie.

    :param ctrlpts: points
    :type ctrlpts: list, tuple
    :return: bounding box in the format [min, max]
    :rtype: tuple
    """
    # Estimate dimension from the first element of the control points
    dimension = len(ctrlpts[0])

    # Evaluate bounding box
    bbmin = [GeomdlFloat('inf') for _ in range(0, dimension)]
    bbmax = [GeomdlFloat('-inf') for _ in range(0, dimension)]
    for cpt in ctrlpts:
        for i, arr in enumerate(zip(cpt, bbmin)):
            if arr[0] < arr[1]:
                bbmin[i] = arr[0]
        for i, arr in enumerate(zip(cpt, bbmax)):
            if arr[0] > arr[1]:
                bbmax[i] = arr[0]

    return tuple(bbmin), tuple(bbmax)
