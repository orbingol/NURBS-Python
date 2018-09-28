"""
.. module:: Abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract base classes for evaluation and visualization modules

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import copy
from . import abc
from . import six
from . import warnings
from . import utilities


class Curve(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class (ABC) for all n-variate curves.

    The Curve ABC is inherited from abc.ABCMeta class which is included in Python standard library by default. Due to
    differences between Python 2 and 3 on defining a metaclass, the compatibility module ``six`` is employed. Using
    ``six`` to set metaclass allows users to use the abstract classes in a correct way.

    The abstract base classes in this module are implemented using a feature called Python Properties. This feature
    allows users to use some of the functions as if they are class fields. You can also consider properties as a
    Pythonic way to set getters and setters. You will see "getter" and "setter" descriptions on the documentation of
    these properties.

    The Curve ABC allows users to set the *FindSpan* function to be used in evaluations with ``find_span_func`` keyword
    as an input to the class constructor. NURBS-Python includes a binary and a linear search variation of the FindSpan
    function in the ``helpers`` module.
    You may also implement and use your own *FindSpan* function. Please see the ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        # Set default array type
        self._array_type = list
        # Initialize class variables
        self._name = "Curve"  # descriptor field
        self._rational = False  # defines whether the curve is rational or not
        self._degree = 0  # degree
        self._knot_vector = utilities.init_var(self._array_type)  # knot vector
        self._control_points = utilities.init_var(self._array_type)  # control points
        self._delta = 0.01  # evaluation delta
        self._curve_points = utilities.init_var(self._array_type)  # evaluated points
        self._dimension = 0  # dimension of the curve
        self._vis_component = None  # visualization component
        self._bounding_box = utilities.init_var(self._array_type)  # bounding box
        self._evaluator = None  # evaluator instance
        self._precision = 6  # number of decimal places to round to
        self._span_func = kwargs.get('find_span_func', None)  # "find_span" function
        self._cache = {}  # cache dictionary

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        # Don't copy self reference
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        # Don't copy the cache
        memo[id(self._cache)] = self._cache.__new__(dict)
        # Copy all other attributes
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __str__(self):
        return self.name

    __repr__ = __str__

    @property
    def name(self):
        """ Curve descriptor (as a string or a number).

        Descriptor field allows users to assign an identification to the curve object. The identification can be a
        string or a number.

        :getter: Gets the descriptor
        :setter: Sets the descriptor
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def evaluator(self):
        """ Curve evaluator.

        Evaluators allow users to use different algorithms for B-Spline and NURBS evaluations. Please see the
        documentation on ``Evaluator`` classes.

        :getter: Gets the current Evaluator instance
        :setter: Sets the evaluator
        """
        return self._evaluator

    @evaluator.setter
    def evaluator(self, value):
        if not isinstance(value, Evaluator):
            raise TypeError("The evaluator must be an instance of Abstract.Evaluator")
        value._span_func = self._span_func
        self._evaluator = value

    @property
    def rational(self):
        """ Returns True if the curve is rational. """
        return self._rational

    @property
    def dimension(self):
        """ Dimension of the curve.

        Dimension will be automatically estimated from the first element of the control points array.

        :getter: Gets the dimension of the curve, e.g. 2D, 3D, etc.
        :type: integer
        """
        if self._rational:
            return self._dimension - 1
        return self._dimension

    @property
    def order(self):
        """ Curve order.

        Defined as order = degree + 1

        :getter: Gets the curve order
        :setter: Sets the curve order
        :type: integer
        """
        return self._degree + 1

    @order.setter
    def order(self, value):
        self.degree = value - 1

    @property
    def degree(self):
        """ Curve degree.

        :getter: Gets the curve degree
        :setter: Sets the curve degree
        :type: integer
        """
        return self._degree

    @degree.setter
    def degree(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Degree cannot be less than zero")

        # Clean up the curve points list
        self.reset(evalpts=True)

        # Set degree
        self._degree = val

    @property
    def knotvector(self):
        """ Knot vector.

        :getter: Gets the knot vector
        :setter: Sets the knot vector
        """
        return self._knot_vector

    @knotvector.setter
    def knotvector(self, value):
        if self._degree == 0 or self._control_points is None or len(self._control_points) == 0:
            raise ValueError("Set degree and control points first")

        # Check knot vector validity
        if not utilities.check_knot_vector(self._degree, value, len(self._control_points)):
            raise ValueError("Input is not a valid knot vector")

        # Clean up the curve points lists
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector = value

    @property
    def ctrlpts(self):
        """ Control points.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        self._control_points = value

    @property
    def evalpts(self):
        """ Evaluated curve points.

        :getter: Gets the coordinates of the evaluated points
        """
        if self._curve_points is None or len(self._curve_points) == 0:
            self.evaluate()

        return self._curve_points

    @property
    def sample_size(self):
        """ Sample size.

        Sample size defines the number of curve points to generate. It also sets the ``delta`` property.

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        return int(1 / self.delta) + 1

    @sample_size.setter
    def sample_size(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if self._knot_vector is None or len(self._knot_vector) == 0 or self._degree == 0:
            warnings.warn("Cannot determine the delta value. Please set knot vector and degree before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start = self._knot_vector[self._degree]
        stop = self._knot_vector[-(self._degree+1)]

        # Set delta value
        self.delta = (stop - start) / float(value - 1)

    @property
    def delta(self):
        """ Curve evaluation delta.

        Evaluation delta corresponds to the *step size* while ``evaluate`` function iterates on the knot vector to
        generate curve points. Decreasing step size results in generation of more curve points.
        Therefore; smaller the delta value, smoother the curve.

        The following figure illustrates the working principles of the delta property:

        .. math::

            \\left[{{u_{start}},{u_{start}} + \\delta ,({u_{start}} + \\delta ) + \\delta , \\ldots ,{u_{end}}} \\right]

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Curve evaluation delta should be between 0.0 and 1.0")

        # Clean up the curve points list
        self.reset(evalpts=True)

        # Set new delta value
        self._delta = float(value)

    @property
    def vis(self):
        """ Visualization component.

        .. note::

            The visualization component is completely optional to use.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisAbstract):
            warnings.warn("Visualization component is NOT an instance of VisAbstract class")
            return
        self._vis_component = value

    @property
    def bbox(self):
        """ Bounding box.

        Evaluates the bounding box of the curve and returns the minimum and maximum coordinates.

        :getter: Gets bounding box
        :type: tuple
        """
        if self._bounding_box is None or len(self._bounding_box) == 0:
            self._bounding_box = utilities.evaluate_bounding_box(self.ctrlpts)

        return tuple(self._bounding_box)

    def set_ctrlpts(self, ctrlpts, **kwargs):
        """ Sets control points and checks if the data is consistent.

        This method is designed to provide a consistent way to set control points whether they are weighted or not.
        It directly sets the control points member of the class, and therefore it doesn't return any values.
        The input will be an array of coordinates. If you are working in the 3-dimensional space, then your coordinates
        will be an array of 3 elements representing *(x, y, z)* coordinates.

        It accepts a keyword argument ``array_init`` which defaults to a ``list`` of size ``len(ctrlpts)``
        where ``ctrlpts`` is the input list of control points. ``array_init`` keyword argument may be used to input
        other types of arrays to this method.

        The following example illustrates a way to use a NumPy array with this method.

        .. code-block:: python

            # Import numpy
            import numpy as np

            # Assuming that "ctrlpts" is a NumPy array of a shape (x,y) where x == len(ctrlpts) and y == len(ctrlpts[0])
            curve.set_ctrlpts(ctrlpts, array_init=np.zeros(ctrlpts.shape, dtype=np.float32))

        :param ctrlpts: input control points as a list of coordinates
        :type ctrlpts: list
        """
        # Degree must be set before setting the control points
        if self._degree == 0:
            raise ValueError("Set the degree first")

        if len(ctrlpts) < self._degree + 1:
            raise ValueError("Number of control points should be at least degree + 1")

        # Keyword arguments
        array_init = kwargs.get('array_init', [[] for _ in range(len(ctrlpts))])

        # Clean up the curve and control points lists
        self.reset(ctrlpts=True, evalpts=True)

        # Estimate dimension by checking the size of the first element
        self._dimension = len(ctrlpts[0])

        ctrlpts_float = array_init
        for idx, cpt in enumerate(ctrlpts):
            if not isinstance(cpt, (list, tuple)):
                raise ValueError("Element number " + str(idx) + " is not a list")
            if len(cpt) is not self._dimension:
                raise ValueError("The input must be " + str(self._dimension) + " dimensional list - " + str(cpt) +
                                 " is not a valid control point")
            # Convert to list of floats
            ctrlpts_float[idx] = [float(coord) for coord in cpt]

        self._control_points = ctrlpts_float

    # Runs visualization component to render the surface
    def render(self, **kwargs):
        """ Renders the curve using the loaded visualization component

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Keyword Arguments:
            * ``cpcolor``: sets the color of the control points polygon
            * ``evalcolor``: sets the color of the curve
            * ``filename``: saves the plot with the input name
            * ``plot``: a flag to control displaying the plot window. Default is True.

        The ``plot`` argument is useful when you would like to work on the command line without any window context.
        If ``plot`` flag is False, this method saves the plot as an image file (.png file where possible) and disables
        plot window popping out. If you don't provide a file name, the name of the image file will be pulled from the
        configuration class.
        """
        if not self._vis_component:
            warnings.warn("No visualization component has been set")
            return

        cpcolor = kwargs.get('cpcolor', 'blue')
        evalcolor = kwargs.get('evalcolor', 'black')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)

        # Check all parameters are set
        self._check_variables()

        # Check if the surface has been evaluated
        if self._curve_points is None or len(self._curve_points) == 0:
            self.evaluate()

        # Run the visualization component
        self._vis_component.clear()
        self._vis_component.add(ptsarr=self.ctrlpts, name="Control Points", color=cpcolor, plot_type='ctrlpts')
        self._vis_component.add(ptsarr=self.evalpts, name=self.name, color=evalcolor, plot_type='evalpts')
        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible)

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:
            * ``evalpts``: if True, then resets evaluated points
            * ``ctrlpts`` if True, then resets control points

        """
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        reset_evalpts = kwargs.get('evalpts', False)

        if reset_ctrlpts:
            self._control_points = None
            self._bounding_box = None

        if reset_evalpts:
            self._curve_points = None

    # Checks whether the curve evaluation is possible or not
    def _check_variables(self):
        works = True
        param_list = []
        if self._degree == 0:
            works = False
            param_list.append('degree')
        if self._control_points is None or len(self._control_points) == 0:
            works = False
            param_list.append('ctrlpts')
        if self._knot_vector is None or len(self._knot_vector) == 0:
            works = False
            param_list.append('knotvector')
        if not works:
            raise ValueError("Please set the following variables before evaluation: " + ",".join(param_list))

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Evaluates the curve. """
        # Check all parameters are set before the curve evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def derivatives(self, u, order, **kwargs):
        """ Evaluates the derivatives of the curve at parameter u.

        :param u: parameter value
        :type u: float
        :param order: derivative order
        :type order: int
        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()

        # Check u parameters are correct
        utilities.check_uv(u)

        # Should implement the derivatives functionality
        pass


class Surface(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class (ABC) for all surfaces.

    The Surface ABC is inherited from abc.ABCMeta class which is included in Python standard library by default. Due to
    differences between Python 2 and 3 on defining a metaclass, the compatibility module ``six`` is employed. Using
    ``six`` to set metaclass allows users to use the abstract classes in a correct way.

    The abstract base classes in this module are implemented using a feature called Python Properties. This feature
    allows users to use some of the functions as if they are class fields. You can also consider properties as a
    Pythonic way to set getters and setters. You will see "getter" and "setter" descriptions on the documentation of
    these properties.

    The Surface ABC allows users to set the *FindSpan* function to be used in evaluations with ``find_span_func``
    keyword as an input to the class constructor. NURBS-Python includes a binary and a linear search variation of the
    FindSpan function in the ``helpers`` module.
    You may also implement and use your own *FindSpan* function. Please see the ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        # Set default array type
        self._array_type = list
        # Define u-direction variables
        self._degree_u = 0  # degree
        self._knot_vector_u = utilities.init_var(self._array_type)  # knot vector
        self._control_points_size_u = 0  # control points array length
        self._delta_u = 0.01  # evaluation delta
        # Define v-direction variables
        self._degree_v = 0  # degree
        self._knot_vector_v = utilities.init_var(self._array_type)  # knot vector
        self._control_points_size_v = 0  # control points array length
        self._delta_v = 0.01  # evaluation delta
        # Define common variables
        self._name = "Surface"  # descriptor field
        self._rational = False  # defines whether the surface is rational or not
        self._control_points = utilities.init_var(self._array_type)  # control points, 1-D array (v-order)
        self._control_points2D = utilities.init_var(self._array_type)  # control points, 2-D array [u][v]
        self._surface_points = utilities.init_var(self._array_type)  # evaluated points
        self._dimension = 0  # dimension of the surface
        self._vis_component = None  # visualization component
        self._tsl_component = None  # tessellation component
        self._bounding_box = utilities.init_var(self._array_type)  # bounding box
        self._evaluator = None  # evaluator instance
        self._precision = 6  # number of decimal places to round to
        self._span_func = kwargs.get('find_span_func', None)  # "find_span" function
        self._cache = {}  # cache dictionary
        # Advanced functionality
        self._trims = utilities.init_var(self._array_type)  # trim curves

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        # Don't copy self reference
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        # Don't copy the cache
        memo[id(self._cache)] = self._cache.__new__(dict)
        # Copy all other attributes
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __str__(self):
        return self.name

    __repr__ = __str__

    @property
    def name(self):
        """ Surface descriptor (as a string or a number).

        Descriptor field allows users to assign an identification to the surface object. The identification can be a
        string or a number.

        :getter: Gets the descriptor
        :setter: Sets the descriptor
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def evaluator(self):
        """ Curve evaluator.

        Evaluators allow users to use different algorithms for B-Spline and NURBS evaluations. Please see the
        documentation on ``Evaluator`` classes.

        :getter: Prints the name of the evaluator and returns the current Evaluator instance
        :setter: Sets the evaluator
        """
        return self._evaluator

    @evaluator.setter
    def evaluator(self, value):
        if not isinstance(value, Evaluator):
            raise TypeError("The evaluator must be an instance of Abstract.Evaluator")
        value._span_func = self._span_func
        self._evaluator = value

    @property
    def rational(self):
        """ Returns True if the surface is rational. """
        return self._rational

    @property
    def dimension(self):
        """ Dimension of the surface.

        Dimension will be automatically estimated from the first element of the control points array.

        :getter: Gets the dimension of the surface
        :type: integer
        """
        if self._rational:
            return self._dimension - 1
        return self._dimension

    @property
    def order_u(self):
        """ Surface order for u-direction.

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for u-direction
        :setter: Sets the surface order for u-direction
        :type: integer
        """
        return self._degree_u + 1

    @order_u.setter
    def order_u(self, value):
        self.degree_u = value - 1

    @property
    def order_v(self):
        """ Surface order for v-direction.

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for v-direction
        :setter: Sets the surface order for v-direction
        :type: integer
        """
        return self._degree_v + 1

    @order_v.setter
    def order_v(self, value):
        self.degree_v = value - 1

    @property
    def degree_u(self):
        """ Surface degree for u-direction.

        :getter: Gets the surface degree for u-direction
        :setter: Sets the surface degree for u-direction
        :type: integer
        """
        return self._degree_u

    @degree_u.setter
    def degree_u(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points
        self.reset(evalpts=True)
        # Set degree u
        self._degree_u = int(value)

    @property
    def degree_v(self):
        """ Surface degree for v-direction.

        :getter: Gets the surface degree for v-direction
        :setter: Sets the surface degree for v-direction
        :type: integer
        """
        return self._degree_v

    @degree_v.setter
    def degree_v(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points
        self.reset(evalpts=True)
        # Set degree v
        self._degree_v = val

    @property
    def knotvector_u(self):
        """ Knot vector for u-direction.

        :getter: Gets the knot vector for u-direction
        :setter: Sets the knot vector for u-direction
        """
        return self._knot_vector_u

    @knotvector_u.setter
    def knotvector_u(self, value):
        if self._degree_u == 0 or self._control_points_size_u == 0:
            raise ValueError("Set degree and control points first on the u-direction")

        # Check knot vector validity
        if not utilities.check_knot_vector(self._degree_u, value, self._control_points_size_u):
            raise ValueError("Input is not a valid knot vector on the u-direction")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector_u = value

    @property
    def knotvector_v(self):
        """ Knot vector for v-direction.

        :getter: Gets the knot vector for v-direction
        :setter: Sets the knot vector for v-direction
        """
        return self._knot_vector_v

    @knotvector_v.setter
    def knotvector_v(self, value):
        if self._degree_v == 0 or self._control_points_size_v == 0:
            raise ValueError("Set degree and control points first on the v-direction")

        # Check knot vector validity
        if not utilities.check_knot_vector(self._degree_v, value, self._control_points_size_v):
            raise ValueError("Input is not a valid knot vector on the v-direction")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector_v = value

    @property
    def ctrlpts(self):
        """ 1-D control points.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        self._control_points = value

    @property
    def ctrlpts2d(self):
        """ 2-D control points.

        :getter: Gets the control points as a 2-dimensional array in [u][v] format
        :setter: Sets the control points as a 2-dimensional array in [u][v] format
        """
        return self._control_points2D

    @ctrlpts2d.setter
    def ctrlpts2d(self, value):
        self._control_points2D = value

    @property
    def ctrlpts_size_u(self):
        """ Size of the control points array on the u-direction.

        :getter: Gets number of control points on the u-direction
        :setter: Sets number of control points on the u-direction
        """
        return self._control_points_size_u

    @ctrlpts_size_u.setter
    def ctrlpts_size_u(self, value):
        if not isinstance(value, int):
            raise TypeError("Number of control points on the u-direction must be an integer number")
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size_u = value

    @property
    def ctrlpts_size_v(self):
        """ Size of the control points array on the v-direction.

        :getter: Gets number of control points on the v-direction
        :setter: Sets number of control points on the v-direction
        """
        return self._control_points_size_v

    @ctrlpts_size_v.setter
    def ctrlpts_size_v(self, value):
        if not isinstance(value, int):
            raise TypeError("Number of control points on the v-direction must be an integer number")
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size_v = value

    @property
    def evalpts(self):
        """ Evaluated surface points.

        :getter: Gets the coordinates of the evaluated points
        """
        if self._surface_points is None or len(self._surface_points) == 0:
            self.evaluate()

        return self._surface_points

    @property
    def sample_size_u(self):
        """ Sample size for the u-direction.

        Sample size defines the number of surface points to generate. It also sets the ``delta`` property.

        :getter: Gets sample size for the u-direction
        :setter: Sets sample size for the u-direction
        :type: int
        """
        return int(1 / self.delta_u) + 1

    @sample_size_u.setter
    def sample_size_u(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if (self._knot_vector_u is None or len(self._knot_vector_u) == 0) or self._degree_u == 0:
            warnings.warn("Cannot determine the delta_u value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_u = self._knot_vector_u[self._degree_u]
        stop_u = self._knot_vector_u[-(self._degree_u+1)]

        # Set delta values
        self.delta_u = (stop_u - start_u) / float(value - 1)

    @property
    def sample_size_v(self):
        """ Sample size for the v-direction.

        Sample size defines the number of surface points to generate. It also sets the ``delta`` property.

        :getter: Gets sample size for the v-direction
        :setter: Sets sample size for the v-direction
        :type: int
        """
        return int(1 / self.delta_v) + 1

    @sample_size_v.setter
    def sample_size_v(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if (self._knot_vector_v is None or len(self._knot_vector_v) == 0) or self._degree_v == 0:
            warnings.warn("Cannot determine the delta_v value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_v = self._knot_vector_v[self._degree_v]
        stop_v = self._knot_vector_v[-(self._degree_v+1)]

        # Set delta values
        self.delta_v = (stop_v - start_v) / float(value - 1)

    @property
    def sample_size(self):
        """ Sample size for both u- and v-directions.

        Sample size defines the number of surface points to generate. It also sets the ``delta`` property.

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

        :getter: Gets sample size values as a tuple of values corresponding to u- and v-directions
        :setter: Sets the same sample size value for both u- and v-directions
        :type: int
        """
        sample_size_u = int(1 / self.delta_u) + 1
        sample_size_v = int(1 / self.delta_v) + 1
        return sample_size_u, sample_size_v

    @sample_size.setter
    def sample_size(self, value):
        if (self._knot_vector_u is None or len(self._knot_vector_u) == 0) or self._degree_u == 0 or\
                (self._knot_vector_v is None or len(self._knot_vector_v) == 0 or self._degree_v == 0):
            warnings.warn("Cannot determine the delta value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_u = self._knot_vector_u[self._degree_u]
        stop_u = self._knot_vector_u[-(self._degree_u+1)]
        start_v = self._knot_vector_v[self._degree_v]
        stop_v = self._knot_vector_v[-(self._degree_v+1)]

        # Set delta values
        self.delta_u = (stop_u - start_u) / float(value - 1)
        self.delta_v = (stop_v - start_v) / float(value - 1)

    @property
    def delta_u(self):
        """ Evaluation delta for the u-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_u`` and ``sample_size_u`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_u`` will also set ``sample_size_u``.

        :getter: Gets the delta value for the u-direction
        :setter: Sets the delta value for the u-direction
        :type: float
        """
        return self._delta_u

    @delta_u.setter
    def delta_u(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta (u-direction) must be between 0.0 and 1.0")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set new delta value
        self._delta_u = float(value)

    @property
    def delta_v(self):
        """ Evaluation delta for the v-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_v`` and ``sample_size_v`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_v`` will also set ``sample_size_v``.

        :getter: Gets the delta value for the v-direction
        :setter: Sets the delta value for the v-direction
        :type: float
        """
        return self._delta_v

    @delta_v.setter
    def delta_v(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta (v-direction) should be between 0.0 and 1.0")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set new delta value
        self._delta_v = float(value)

    @property
    def delta(self):
        """ Evaluation delta for both u- and v-directions.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta`` and ``sample_size`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta`` will also set ``sample_size``.

        The following figure illustrates the working principles of the delta property:

        .. math::

            \\left[{{u_{0}},{u_{start}} + \\delta ,({u_{start}} + \\delta ) + \\delta , \\ldots ,{u_{end}}} \\right]

        :getter: Gets the delta values as a tuple of values corresponding to u- and v-directions
        :setter: Sets the same delta value for both u- and v-directions
        :type: float
        """
        return self.delta_u, self.delta_v

    @delta.setter
    def delta(self, value):
        if isinstance(value, (int, float)):
            self.delta_u = value
            self.delta_v = value
        elif isinstance(value, (list, tuple)):
            if len(value) == 2:
                self.delta_u = value[0]
                self.delta_v = value[1]
            else:
                raise ValueError("Surface requires 2 delta values")
        else:
            raise ValueError("Cannot set delta. Please input a numeric value or a list or tuple with 2 numeric values")

    @property
    def vis(self):
        """ Visualization component.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisAbstract):
            warnings.warn("Visualization component must be an instance of VisAbstract class")
            return

        self._vis_component = value

    @property
    def tessellator(self):
        """ Tessellation component.

        :getter: Gets the tessellation component
        :setter: Sets the tessellation component
        """
        return self._tsl_component

    @tessellator.setter
    def tessellator(self, value):
        if not isinstance(value, Tessellate):
            warnings.warn("Tessellation component must be an instance of Abstract.Tessellate class")
            return

        self._tsl_component = value

    @property
    def bbox(self):
        """ Bounding box.

        Evaluates the bounding box of the surface and returns the minimum and maximum coordinates.

        :getter: Gets bounding box
        """
        if self._bounding_box is None or len(self._bounding_box) == 0:
            self._bounding_box = utilities.evaluate_bounding_box(self.ctrlpts)

        return tuple(self._bounding_box)

    @property
    def trims(self):
        """ Trim curves.

        Trim curves are introduced to the surfaces on the parametric space. It should be an array (or list, tuple, etc.)
        and they are integrated to the existing visualization system.

        :getter: Gets the array of trim curves
        :setter: Sets the array of trim curves
        """
        return self._trims

    @trims.setter
    def trims(self, value):
        self._trims = value

    def set_ctrlpts(self, ctrlpts, size_u, size_v, **kwargs):
        """ Sets 1-dimensional control points and checks if the data is consistent.

        This method is designed to provide a consistent way to set control points whether they are weighted or not.
        It directly sets the control points member of the class, and therefore it doesn't return any values.
        The input will be an array of coordinates. If you are working in the 3-dimensional space, then your coordinates
        will be an array of 3 elements representing *(x, y, z)* coordinates.

        This method also generates 2D control points in *[u][v]* format which can be accessed via :py:attr:`~ctrlpts2d`.

        You may initialize the 1-dimensional and 2-dimensional arrays via ``array_init`` and ``array_init2d`` keyword
        arguments. Please see :py:meth:`.Curve.set_ctrlpts()` for details.

        .. note::

            The v index varies first. That is, a row of v control points for the first u value is found first.
            Then, the row of v control points for the next u value.

        :param ctrlpts: input control points as a list of coordinates
        :type ctrlpts: list
        :param size_u: size of the control points grid on the u-direction
        :type size_u: int
        :param size_v: size of the control points grid on the v-direction
        :type size_v: int
        :return: None
        """
        # Degrees must be set before setting the control points
        if self._degree_u == 0 or self._degree_v == 0:
            raise ValueError("Set the degrees first")

        # Check array size validity
        if size_u < self._degree_u + 1:
            raise ValueError("Number of control points on the u-direction should be at least degree + 1")
        if size_v < self._degree_v + 1:
            raise ValueError("Number of control points on the v-direction should be at least degree + 1")

        # Keyword arguments
        array_init = kwargs.get('array_init', [[] for _ in range(len(ctrlpts))])
        array_init2d = kwargs.get('array_init2d', [[[] for _ in range(size_v)] for _ in range(size_u)])

        # Clean up the surface and control points
        self.reset(evalpts=True, ctrlpts=True)

        # Estimate dimension by checking the size of the first element
        self._dimension = len(ctrlpts[0])

        # Check the dimensions of the input control points array and type cast to float
        ctrlpts_float = array_init
        for idx, cpt in enumerate(ctrlpts):
            if not isinstance(cpt, (list, tuple)):
                raise ValueError("Element number " + str(idx) + " is not a list")
            if len(cpt) is not self._dimension:
                raise ValueError("The input must be " + str(self._dimension) + " dimensional list - " + str(cpt) +
                                 " is not a valid control point")
            ctrlpts_float[idx] = [float(coord) for coord in cpt]

        # Generate a 2-dimensional list of control points
        ctrlpts_float2d = array_init2d
        for i in range(0, size_u):
            for j in range(0, size_v):
                ctrlpts_float2d[i][j] = ctrlpts_float[j + (i * size_v)]

        # Set the new control points
        self._control_points = ctrlpts_float
        self._control_points2D = ctrlpts_float2d

        # Set u and v sizes
        self._control_points_size_u = size_u
        self._control_points_size_v = size_v

    # Runs visualization component to render the surface
    def render(self, **kwargs):
        """ Renders the surface using the loaded visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Keyword Arguments:
            * ``cpcolor``: sets the color of the control points grid
            * ``evalcolor``: sets the color of the surface
            * ``trimcolor``: sets the color of the trim curves
            * ``filename``: saves the plot with the input name
            * ``plot``: a flag to control displaying the plot window. Default is True.
            * ``colormap``: sets the colormap of the surface

        The ``plot`` argument is useful when you would like to work on the command line without any window context.
        If ``plot`` flag is False, this method saves the plot as an image file (.png file where possible) and disables
        plot window popping out. If you don't provide a file name, the name of the image file will be pulled from the
        configuration class.

        Please note that ``colormap`` argument can only work with visualization classes that support colormaps. As an
        example, please see :py:class:`.VisMPL.VisSurfTriangle()` class documentation. This method expects a single
        colormap input.
        """
        if not self._vis_component:
            warnings.warn("No visualization component has been set")
            return

        cpcolor = kwargs.get('cpcolor', 'blue')
        evalcolor = kwargs.get('evalcolor', 'green')
        trimcolor = kwargs.get('trimcolor', 'black')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)

        # Get colormap and convert to a list
        surf_cmap = kwargs.get('colormap', None)
        surf_cmap = [surf_cmap] if surf_cmap else []

        # Check all parameters are set
        self._check_variables()

        # Check if the surface has been evaluated
        if self._surface_points is None or len(self._surface_points) == 0:
            self.evaluate()

        # Clear the visualization component
        self._vis_component.clear()

        # Add control points
        if self._vis_component.plot_types['ctrlpts'] == 'points':
            self._vis_component.add(ptsarr=self.ctrlpts,
                                    size=[self.ctrlpts_size_u, self.ctrlpts_size_v],
                                    name="Control Points", color=cpcolor, plot_type='ctrlpts')

        # Add control points as quads
        if self._vis_component.plot_types['ctrlpts'] == 'quads':
            ctrlpts_quads = utilities.make_quad_mesh(self.ctrlpts, self.ctrlpts_size_u, self.ctrlpts_size_v)
            self._vis_component.add(ptsarr=ctrlpts_quads,
                                    size=[self.ctrlpts_size_u, self.ctrlpts_size_v],
                                    name="Control Points", color=cpcolor, plot_type='ctrlpts')

        # Add surface points
        if self._vis_component.plot_types['evalpts'] == 'points':
            self._vis_component.add(ptsarr=self.evalpts,
                                    size=[self.sample_size_u, self.sample_size_v],
                                    name=self.name, color=evalcolor, plot_type='evalpts')

        # Add surface points as quads
        if self._vis_component.plot_types['evalpts'] == 'quads':
            evalpts_quads = utilities.make_quad_mesh(self.evalpts, self.sample_size_u, self.sample_size_v)
            self._vis_component.add(ptsarr=evalpts_quads,
                                    size=[self.sample_size_u, self.sample_size_v],
                                    name=self.name, color=evalcolor, plot_type='evalpts')

        # Add surface points as vertices and triangles
        if self._vis_component.plot_types['evalpts'] == 'triangles':
            self.tessellate()
            self._vis_component.add(ptsarr=[self.tessellator.vertices, self.tessellator.triangles],
                                    size=[self.sample_size_u, self.sample_size_v],
                                    name=self.name, color=evalcolor, plot_type='evalpts')

        # Visualize the trim curve
        for idx, trim in enumerate(self._trims):
            self._vis_component.add(ptsarr=self.evaluate_list(trim.evalpts),
                                    name="Trim Curve " + str(idx + 1), color=trimcolor, plot_type='trimcurve')

        # Plot the surface
        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible, colormap=surf_cmap)

    def tessellate(self, **kwargs):
        """ Tessellates the surface.

        Keyword arguments are directly passed to the tessellation component.
        """
        # Keyword arguments
        update_vertex_coords = kwargs.get('evaluate_vertices', True)

        # Call tessellation component
        self._tsl_component.tessellate(self.evalpts, self.sample_size_u, self.sample_size_v, trims=self.trims, **kwargs)

        # Evaluate vertex coordinates
        if update_vertex_coords:
            for idx in range(len(self._tsl_component.vertices)):
                self._tsl_component.vertices[idx].data = self.evaluate_single(self._tsl_component.vertices[idx].uv)

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:
            * ``evalpts``: if True, then resets evaluated points
            * ``ctrlpts`` if True, then resets control points

        """
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        reset_evalpts = kwargs.get('evalpts', False)

        if reset_ctrlpts:
            self._control_points = None
            self._control_points2D = None
            self._control_points_size_u = 0
            self._control_points_size_v = 0
            self._bounding_box = None

        if reset_evalpts:
            self._surface_points = None

    # Checks whether the surface evaluation is possible or not
    def _check_variables(self):
        works = True
        param_list = []
        if self._degree_u == 0:
            works = False
            param_list.append('degree_u')
        if self._degree_v == 0:
            works = False
            param_list.append('degree_v')
        if self._control_points is None or len(self._control_points) == 0:
            works = False
            param_list.append('ctrlpts')
        if self._knot_vector_u is None or len(self._knot_vector_u) == 0:
            works = False
            param_list.append('knotvector_u')
        if self._knot_vector_v is None or len(self._knot_vector_v) == 0:
            works = False
            param_list.append('knotvector_v')
        if not works:
            raise ValueError("Please set the following variables before evaluation: " + ",".join(param_list))

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Evaluates the surface. """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def evaluate_single(self, uv):
        """ Evaluates the surface at the given (u,v) parameter.

        :param uv: parameter pair (u, v)
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def evaluate_list(self, uv_list):
        """ Evaluates the surface for a given (u,v) array.

        :param uv_list: array of parameter pairs (u, v)
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def derivatives(self, u, v, order, **kwargs):
        """ Evaluates the derivatives of the surface at parameter (u,v).

        :param u: parameter on the u-direction
        :type u: float
        :param v: parameter on the v-direction
        :type v: float
        :param order: derivative order
        :type order: int
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Check u and v parameters are correct
        utilities.check_uv(u, v)

        # Should implement the derivatives functionality here
        pass


class Multi(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract class for curve and surface containers.

    This class implements Python Iterator Protocol and therefore any instance of this class can be directly used in
    a for loop.
    """

    def __init__(self, *args, **kwargs):
        self._elements = []  # elements contained
        self._vis_component = None  # visualization component
        self._iter_index = 0  # iterator index
        self._instance = None  # type of the initial element

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            result = self._elements[self._iter_index]
        except IndexError:
            raise StopIteration
        self._iter_index += 1
        return result

    def __reversed__(self):
        return reversed(self._elements)

    def __getitem__(self, index):
        return self._elements[index]

    def __len__(self):
        return len(self._elements)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Cannot add non-matching container types")
        self._elements += other._elements
        return self

    @property
    def vis(self):
        """ Visualization component.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        :type: float
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisAbstract):
            warnings.warn("Visualization component is NOT an instance of the abstract class")
            return
        self._vis_component = value

    def add(self, element):
        """ Adds shapes to the container.

        The input can be a single shape, a list of shapes or a container object.

        :param element: shape to be added
        """
        if isinstance(element, self._instance):
            self._elements.append(element)
        elif isinstance(element, self.__class__):
            self + element
        elif isinstance(element, (list, tuple)):
            for elem in element:
                self.add(elem)
        else:
            raise TypeError("Cannot add the element to the container")

    # Runs visualization component to render the surface
    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots using the visualization component. """
        pass


class Evaluator(six.with_metaclass(abc.ABCMeta, object)):
    """ Evaluator abstract base class.

    The methods ``evaluate`` and ``derivative`` is intended to be used for computation over a range of values.
    The suggested usage of ``evaluate_single`` and ``derivative_single`` methods are computation of a single value.

    Please note that this class requires the keyword argument ``find_span_func`` to be set to a valid find_span
    function implementation. Please see ``helpers`` module for details.
    """

    def __init__(self, **kwargs):
        self._name = kwargs.get('name', self.__class__.__name__)
        self._span_func = kwargs.get('find_span_func', None)

    @property
    def name(self):
        """ Evaluator name (as a string).

        :getter: Gets the name of the evaluator
        :type: str
        """
        return self._name

    @abc.abstractmethod
    def evaluate_single(self, **kwargs):
        """ Abstract method for computation of a single point at a single parameter. """
        pass

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Abstract method for computation of points over a range of parameters. """
        pass

    @abc.abstractmethod
    def derivatives_single(self, **kwargs):
        """ Abstract method for computation of derivatives at a single parameter. """
        pass

    @abc.abstractmethod
    def derivatives(self, **kwargs):
        """ Abstract method for computation of derivatives over a range of parameters. """
        pass


class CurveEvaluator(six.with_metaclass(abc.ABCMeta, object)):
    """ Curve customizations for Evaluator abstract base class. """

    def __init__(self, **kwargs):
        self._span_func = kwargs.get('find_span_func', None)

    @abc.abstractmethod
    def insert_knot(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm. """
        pass


class SurfaceEvaluator(six.with_metaclass(abc.ABCMeta, object)):
    """ Surface customizations for the Evaluator abstract base class. """

    def __init__(self, **kwargs):
        self._span_func = kwargs.get('find_span_func', None)

    @abc.abstractmethod
    def insert_knot_u(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm on the u-direction. """
        pass

    @abc.abstractmethod
    def insert_knot_v(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm on the v-direction. """
        pass


class Tessellate(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class for tessellation. """

    def __init__(self, **kwargs):
        self._vertices = None
        self._triangles = None
        self._arguments = None

    @property
    def vertices(self):
        """ Vertex objects for tessellation.

        :getter: Gets the vertices
        """
        return self._vertices

    @property
    def triangles(self):
        """ Triangle objects for tessellation.

        :getter: Gets the triangles
        """
        return self._triangles

    @property
    def arguments(self):
        """ Arguments passed to the tessellation function.

        :getter: Gets the tessellation arguments
        :setter: Sets the tessellation arguments
        """
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value

    def reset(self):
        """ Resets stored vertices and triangles. """
        self._vertices = None
        self._triangles = None

    @abc.abstractmethod
    def tessellate(self, points, size_u, size_v, **kwargs):
        """ Abstract method for implementation of the tessellation algorithm. """
        pass


class VisConfigAbstract(six.with_metaclass(abc.ABCMeta, object)):
    """ Visualization configuration abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all visualization configurations
    in NURBS-Python package.
    """

    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass


class VisAbstract(six.with_metaclass(abc.ABCMeta, object)):
    """ Visualization abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all common visualization options
    in NURBS-Python package.
    """

    def __init__(self, config=None):
        self._plots = []
        self._config = config

    def clear(self):
        """ Clears the points, colors and names lists. """
        self._plots[:] = []

    def add(self, ptsarr=(), size=0, name=None, color=None, plot_type=0):
        """ Adds points sets to the visualization instance for plotting.

        :param ptsarr: control, curve or surface points
        :type ptsarr: list, tuple
        :param size: size in all directions, e.g. in u- and v-directions
        :type size: int, tuple, list
        :param name: name of the point on the legend
        :type name: str
        :param color: color of the point on the legend
        :type color: str
        :param plot_type: type of the plot, control points (type = 1) or evaluated points (type = 0)
        :type plot_type: int
        """
        if ptsarr is None or len(ptsarr) == 0:
            return
        if not color or not name:
            return
        # Add points, size, plot color and name on the legend
        elem = {'ptsarr': ptsarr, 'size': size, 'name': name, 'color': color, 'type': plot_type}
        self._plots.append(elem)

    @abc.abstractmethod
    def render(self, **kwargs):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstract`` class.
        """
        # We need something to plot
        if self._plots is None or len(self._plots) == 0:
            raise ValueError("Nothing to plot")

        # Remaining should be implemented
        pass


class VisAbstractSurf(six.with_metaclass(abc.ABCMeta, VisAbstract)):
    """ Visualization abstract class for surfaces

    Implements ``VisAbstract`` class and also uses Python's *Abstract Base Class* implementation to define a base
    for **surface** visualization options in NURBS-Python package.
    """

    def __init__(self, config=None):
        super(VisAbstractSurf, self).__init__(config=config)
        self._ctrlpts_offset = 0.0
        self._plot_types = {'ctrlpts': 'points', 'evalpts': 'points'}

    @property
    def plot_types(self):
        """ Plot types

        :getter: Gets the plot types
        :type: tuple
        """
        return self._plot_types

    def set_ctrlpts_offset(self, offset_value):
        """ Sets an offset for the control points grid plot.

        :param offset_value: offset value
        :type offset_value: float
        """
        self._ctrlpts_offset = float(offset_value)

    @abc.abstractmethod
    def render(self, **kwargs):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstractSurf`` class.
        """
        # Calling parent function
        super(VisAbstractSurf, self).render()

        # Remaining should be implemented
        pass
