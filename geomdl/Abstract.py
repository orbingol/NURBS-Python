"""
.. module:: Abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract classes for all BSpline / NURBS curves and surfaces using Python's ABC module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import abc
from . import six
from . import warnings
from . import utilities


class Curve(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract class for all curves. """

    def __init__(self):
        self._name = "Curve"  # descriptor field
        self._rational = False  # defines whether the curve is rational or not
        self._degree = 0  # degree
        self._knot_vector = None  # knot vector
        self._control_points = None  # control points
        self._delta = 0.1  # evaluation delta
        self._curve_points = None  # evaluated points
        self._dimension = 0  # dimension of the curve
        self._vis_component = None  # visualization component
        self._bounding_box = None  # bounding box
        self._evaluator = None  # evaluator instance
        self._precision = 6  # number of decimal places to round to
        self._cache = {}  # cache dictionary

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

            \\left[ {{u_{start}},{u_{start}} + \\delta ,({u_{start}} + \\delta ) + \\delta , \\ldots ,{u_{end}}} \\right]

        .. note:: The delta value is 0.1 by default.

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

    # Runs visualization component to render the surface
    def render(self, **kwargs):
        """ Renders the curve using the loaded visualization component

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Possible keyword arguments are

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
        curvecolor = kwargs.get('evalcolor', 'black')
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
        self._vis_component.add(ptsarr=self.evalpts, name="Curve", color=curvecolor, plot_type='evalpts')
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
        pass


class Surface(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract class for all surfaces. """

    def __init__(self):
        # Define u-direction variables
        self._degree_u = 0  # degree
        self._knot_vector_u = None  # knot vector
        self._control_points_size_u = 0  # control points array length
        self._delta_u = 0.1  # evaluation delta
        # Define v-direction variables
        self._degree_v = 0  # degree
        self._knot_vector_v = None  # knot vector
        self._control_points_size_v = 0  # control points array length
        self._delta_v = 0.1  # evaluation delta
        # Define common variables
        self._name = "Surface"  # descriptor field
        self._rational = False  # defines whether the surface is rational or not
        self._control_points = None  # control points, 1-D array (v-order)
        self._control_points2D = None  # control points, 2-D array [u][v]
        self._surface_points = None  # evaluated points
        self._dimension = 0  # dimension of the surface
        self._vis_component = None  # visualization component
        self._bounding_box = None  # bounding box
        self._evaluator = None  # evaluator instance
        self._precision = 6  # number of decimal places to round to
        self._cache = {}  # cache dictionary

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

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

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

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

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

        :getter: Gets sample size as a tuple of values corresponding to u- and v-directions
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

        Evaluation delta corresponds to the *step size* while ``evaluate`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        .. note:: The delta value is 0.1 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
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

        Evaluation delta corresponds to the *step size* while ``evaluate`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        .. note:: The delta value is 0.1 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
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

        Evaluation delta corresponds to the *step size* while ``evaluate`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        The following figure illustrates the working principles of the delta property:

        .. math::

            \\left[ {{u_{start}},{u_{start}} + \\delta ,({u_{start}} + \\delta ) + \\delta , \\ldots ,{u_{end}}} \\right]

        .. note:: The delta value is 0.1 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
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
    def bbox(self):
        """ Bounding box.

        Evaluates the bounding box of the surface and returns the minimum and maximum coordinates.

        :getter: Gets bounding box
        :type: tuple
        """
        if self._bounding_box is None or len(self._bounding_box) == 0:
            self._bounding_box = utilities.evaluate_bounding_box(self.ctrlpts)

        return tuple(self._bounding_box)

    # Runs visualization component to render the surface
    def render(self, **kwargs):
        """ Renders the surface using the loaded visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Keyword Arguments:

        * ``cpcolor``: sets the color of the control points grid
        * ``evalcolor``: sets the color of the surface
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
        surfcolor = kwargs.get('evalcolor', 'green')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)

        # Check all parameters are set
        self._check_variables()

        # Check if the surface has been evaluated
        if self._surface_points is None or len(self._surface_points) == 0:
            self.evaluate()

        # Run the visualization component
        self._vis_component.clear()
        self._vis_component.add(ptsarr=self.ctrlpts,
                                size=[self._control_points_size_u, self._control_points_size_v],
                                name="Control Points", color=cpcolor, plot_type='ctrlpts')
        self._vis_component.add(ptsarr=self.evalpts,
                                size=[self.sample_size_u, self.sample_size_v],
                                name="Surface", color=surfcolor, plot_type='evalpts')
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
        pass


class Multi(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract class for curve and surface containers. """

    def __init__(self):
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
            raise TypeError("Cannot add non-matching types of Multi containers")
        ret = self.__class__()
        new_elems = self._elements + other._elements
        ret.add_list(new_elems)
        return ret

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
        """ Abstract method for adding surface or curve objects to the container.

        :param element: the curve or surface object to be added
        :type element:
        """
        if not isinstance(element, self._instance):
            warnings.warn("Cannot add, incompatible type.")
            return
        self._elements.append(element)

    def add_list(self, elements):
        """ Adds curve objects to the container.

        :param elements: curve objects to be added
        :type elements: list, tuple
        """
        if not isinstance(elements, (list, tuple)):
            warnings.warn("Input must be a list or a tuple")
            return

        for element in elements:
            self.add(element)

    def translate(self, vec=()):
        """ Translates the elements in the container by the input vector.

        :param vec: translation vector
        :type vec: list, tuple
        """
        for elem in self._elements:
            elem.translate(vec)

    # Runs visualization component to render the surface
    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots using the visualization component. """
        pass


class Evaluator(six.with_metaclass(abc.ABCMeta, object)):
    """ Evaluator abstract base class.

    The methods ``evaluate`` and ``derivative`` is intended to be used for computation over a range of values.
    The suggested usage of ``evaluate_single`` and ``derivative_single`` methods are computation of a single value.
    """

    def __init__(self, **kwargs):
        self._name = kwargs.get('name', self.__class__.__name__)

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
        pass

    @abc.abstractmethod
    def insert_knot(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm. """
        pass


class SurfaceEvaluator(six.with_metaclass(abc.ABCMeta, object)):
    """ Surface customizations for the Evaluator abstract base class. """

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def insert_knot_u(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm on the u-direction. """
        pass

    @abc.abstractmethod
    def insert_knot_v(self, **kwargs):
        """ Abstract method for implementation of knot insertion algorithm on the v-direction. """
        pass


class SurfaceTessellator(six.with_metaclass(abc.ABCMeta, object)):
    """ Tessellator abstract base for the surface evaluator classes. """

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def tessellate(self, **kwargs):
        """ Abstract method for implementation of the surface tessellation algorithm. """
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

    Implements ``VisABstract`` class and also uses Python's *Abstract Base Class* implementation to define a base
    for **surface** visualization options in NURBS-Python package.
    """

    def __init__(self, config=None):
        super(VisAbstractSurf, self).__init__(config=config)
        self._ctrlpts_offset = 0.0

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
