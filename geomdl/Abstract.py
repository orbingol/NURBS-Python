"""
.. module:: Abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract classes for all BSpline / NURBS curves and surfaces using Python's ABC module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import abc
from . import warnings
from . import utilities
from . import helpers


class Curve(object):
    """ Abstract class for all curves. """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._rational = False  # defines whether the curve is rational or not
        self._degree = 0  # degree
        self._knot_vector = None  # knot vector
        self._control_points = None  # control points
        self._delta = 0.1  # evaluation delta
        self._sample_size = None  # sample size
        self._curve_points = None  # evaluated points
        self._dimension = 0  # dimension of the curve
        self._vis_component = None  # visualization component
        self._bounding_box = None  # bounding box
        self._cache = {}  # cache dictionary

    @property
    def dimension(self):
        """ Dimension of the curve.

        Dimension will be automatically estimated from the first element of the control points array.

        :getter: Gets the dimension of the curve, e.g. 2D, 3D, etc.
        :type: integer
        """
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
        self._degree = value - 1

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

        # Clean up the curve points list, if necessary
        self._reset_evalpts()

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
    def curvepts(self):
        """ Evaluated curve points.

        :getter: Gets the coordinates of the evaluated points
        """
        if not self._curve_points:
            self.evaluate()

        return self._curve_points

    @property
    def sample_size(self):
        """ Sample size.

        Sample size defines the number of curve points to generate. It sets the ``delta`` property.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        if self._sample_size is None:
            if self._knot_vector is not None and len(self._knot_vector) != 0:
                self._sample_size = int(1.0 / self.delta) + 1
            else:
                warnings.warn("Cannot determine the sample size.")
                return 0
        return self._sample_size

    @sample_size.setter
    def sample_size(self, value):
        if self._knot_vector is None or len(self._knot_vector) == 0:
            warnings.warn("Cannot determine the delta value. Please set knot vector before setting the sample size.")
            return
        # To make it operate like linspace, we have to know the starting and ending points.
        start = self._knot_vector[self._degree]
        stop = self._knot_vector[-(self._degree+1)]

        # Clean up the curve points list, if necessary
        self._reset_evalpts()

        # Set delta value
        self._delta = (stop - start) / float(value - 1)

        # Set sample size
        self._sample_size = value

    @property
    def delta(self):
        """ Curve evaluation delta.

        Evaluation delta corresponds to the *step size* while ``evaluate`` function iterates on the knot vector to
        generate curve points. Decreasing step size results in generation of more curve points.
        Therefore; smaller the delta value, smoother the curve.

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

        # Clean up the curve points list, if necessary
        self._reset_evalpts()

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
            self._eval_bbox()

        return tuple(self._bounding_box)

    def _eval_bbox(self):
        """ Evaluates bounding box of the curve. """
        # Find correct dimension of the control points
        dim = self._dimension
        if self._rational:
            dim -= 1

        # Evaluate bounding box
        bbmin = [float('inf') for _ in range(0, dim)]
        bbmax = [0.0 for _ in range(0, dim)]
        for cpt in self.ctrlpts:
            for i, arr in enumerate(zip(cpt, bbmin)):
                if arr[0] < arr[1]:
                    bbmin[i] = arr[0]
            for i, arr in enumerate(zip(cpt, bbmax)):
                if arr[0] > arr[1]:
                    bbmax[i] = arr[0]

        self._bounding_box = [tuple(bbmin), tuple(bbmax)]

    # Runs visualization component to render the surface
    def render(self, **kwargs):
        """ Renders the curve using the loaded visualization component

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Possible keyword arguments are

        * ``cpcolor``: sets the color of the control points polygon
        * ``curvecolor``: sets the color of the curve

        """
        if not self._vis_component:
            warnings.warn("No visualization component has been set")
            return

        cpcolor = kwargs.get('cpcolor', 'blue')
        curvecolor = kwargs.get('curvecolor', 'black')

        # Check all parameters are set
        self._check_variables()

        # Check if the surface has been evaluated
        if self._curve_points is None or len(self._curve_points) == 0:
            self.evaluate()

        # Run the visualization component
        self._vis_component.clear()
        self._vis_component.add(ptsarr=self.ctrlpts, name="Control Points", color=cpcolor, plot_type='ctrlpts')
        self._vis_component.add(ptsarr=self.curvepts, name="Curve", color=curvecolor, plot_type='evalpts')
        self._vis_component.render()

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

    # Resets the control points
    def _reset_ctrlpts(self):
        self._control_points = None
        self._bounding_box = None

    # Resets the evaluated points
    def _reset_evalpts(self):
        self._curve_points = None

    def curvept(self, u):
        """ Evaluates the curve at the given parameter.

        :param u: parameter
        :type u: float
        :return: evaluated curve point
        :rtype: list
        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()
        # Check u parameters are correct
        helpers.check_uv(u)

        # Algorithm A3.1 and A4.1
        span = helpers.find_span(self.knotvector, len(self._control_points), u)
        basis = helpers.basis_function(self.degree, self.knotvector, span, u)

        cpt = [0.0 for _ in range(self._dimension)]
        for i in range(0, self._degree + 1):
            cpt[:] = [crvpt + (basis[i] * ctrlpt) for crvpt, ctrlpt in
                      zip(cpt, self._control_points[span - self._degree + i])]

        # Divide by weight, if the curve is rational
        if self._rational:
            curvept = [float(pt / cpt[-1]) for pt in cpt[0:(self._dimension - 1)]]
        else:
            curvept = cpt

        return curvept

    def evaluate(self, **kwargs):
        """ Evaluates the curve.

        Keyword arguments:

        * ``start``: start parameter
        * ``stop``: stop parameter

        The ``start`` and ``stop`` parameters allow evaluation of a curve segment in the range *[start, stop]*, i.e.
        the curve will also be evaluated at the ``stop`` parameter value.

        .. note:: The evaluated surface points are stored in :py:attr:`~curvepts`.

        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()

        # Find evaluation start and stop parameter values
        start = kwargs.get('start', self.knotvector[self.degree])
        stop = kwargs.get('stop', self.knotvector[-(self.degree+1)])

        # Check if the input parameters are in the range
        helpers.check_uv(start)
        helpers.check_uv(stop)

        # Clean up the curve points, if necessary
        self._reset_evalpts()

        knots = utilities.linspace(start, stop, self.sample_size)
        spans = helpers.find_spans(self.knotvector, len(self._control_points), knots)
        basis = helpers.basis_functions(self.degree, self.knotvector, spans, knots)

        # Evaluate the curve in the input range
        for idx in range(len(knots)):
            cpt = [0.0 for _ in range(self.dimension)]
            for i in range(0, self.degree + 1):
                cpt[:] = [crvpt + (basis[idx][i] * ctrlpt) for crvpt, ctrlpt in
                          zip(cpt, self._control_points[spans[idx] - self.degree + i])]

            # Divide by weight, if the curve is rational
            if self._rational:
                curvept = [float(pt / cpt[-1]) for pt in cpt[0:(self.dimension - 1)]]
            else:
                curvept = cpt

            self._curve_points.append(curvept)


class Surface(object):
    """ Abstract class for all surfaces. """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        # U-direction
        self._degree_u = 0  # degree
        self._knot_vector_u = None  # knot vector
        self._control_points_size_u = 0  # control points array length
        self._delta_u = 0.1  # evaluation delta
        # V-direction
        self._degree_v = 0  # degree
        self._knot_vector_v = None  # knot vector
        self._control_points_size_v = 0  # control points array length
        self._delta_v = 0.1  # evaluation delta
        # Common
        self._rational = False  # defines whether the surface is rational or not
        self._sample_size = None  # defines sample size
        self._control_points = None  # control points, 1-D array (v-order)
        self._control_points2D = None  # control points, 2-D array [u][v]
        self._surface_points = None  # evaluated points
        self._dimension = 0  # dimension of the surface
        self._vis_component = None  # visualization component
        self._bounding_box = None  # bounding box
        self._cache = {}  # cache dictionary

    @property
    def dimension(self):
        """ Dimension of the surface.

        Dimension will be automatically estimated from the first element of the control points array.

        :getter: Gets the dimension of the surface
        :type: integer
        """
        return self._dimension

    @property
    def order_u(self):
        """ Surface order for U direction.

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for U direction
        :setter: Sets the surface order for U direction
        :type: integer
        """
        return self._degree_u + 1

    @order_u.setter
    def order_u(self, value):
        self._degree_u = value - 1

    @property
    def order_v(self):
        """ Surface order for V direction.

        Follows the following equality: order = degree + 1

        :getter: Gets the surface order for V direction
        :setter: Sets the surface order for V direction
        :type: integer
        """
        return self._degree_v + 1

    @order_v.setter
    def order_v(self, value):
        self._degree_v = value - 1

    @property
    def degree_u(self):
        """ Surface degree for U direction.

        :getter: Gets the surface degree for U direction
        :setter: Sets the surface degree for U direction
        :type: integer
        """
        return self._degree_u

    @degree_u.setter
    def degree_u(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points lists, if necessary
        self._reset_evalpts()
        # Set degree u
        self._degree_u = int(value)

    @property
    def degree_v(self):
        """ Surface degree for V direction.

        :getter: Gets the surface degree for V direction
        :setter: Sets the surface degree for V direction
        :type: integer
        """
        return self._degree_v

    @degree_v.setter
    def degree_v(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points lists, if necessary
        self._reset_evalpts()
        # Set degree v
        self._degree_v = val

    @property
    def knotvector_u(self):
        """ Knot vector for U direction.

        :getter: Gets the knot vector for U direction
        :setter: Sets the knot vector for U direction
        """
        return self._knot_vector_u

    @knotvector_u.setter
    def knotvector_u(self, value):
        self._knot_vector_u = value

    @property
    def knotvector_v(self):
        """ Knot vector for V direction.

        :getter: Gets the knot vector for V direction
        :setter: Sets the knot vector for V direction
        """
        return self._knot_vector_v

    @knotvector_v.setter
    def knotvector_v(self, value):
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

        :getter: Gets the control points in U and V directions
        :setter: Sets the control points in U and V directions
        """
        return self._control_points2D

    @ctrlpts2d.setter
    def ctrlpts2d(self, value):
        self._control_points2D = value

    @property
    def ctrlpts_size_u(self):
        """ Size of the control points array in U-direction.

        :getter: Gets number of control points in U-direction
        :setter: Sets number of control points in U-direction
        """
        return self._control_points_size_u

    @ctrlpts_size_u.setter
    def ctrlpts_size_u(self, value):
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size_u = value

    @property
    def ctrlpts_size_v(self):
        """ Size of the control points array in V-direction.

        :getter: Gets number of control points in V-direction
        :setter: Sets number of control points in V-direction
        """
        return self._control_points_size_v

    @ctrlpts_size_v.setter
    def ctrlpts_size_v(self, value):
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size_v = value

    @property
    def surfpts(self):
        """ Evaluated surface points.

        :getter: Gets the coordinates of the evaluated points
        """
        if not self._surface_points:
            self.evaluate()

        return self._surface_points

    @property
    def sample_size(self):
        """ Sample size.

        Sample size defines the number of surface points to generate. It sets the ``delta`` property.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        if self._sample_size is None:
            if self._knot_vector_u is not None and len(self._knot_vector_u) != 0:
                self._sample_size = int(1.0 / self.delta_u) + 1
            elif self._knot_vector_v is not None and len(self._knot_vector_v) != 0:
                self._sample_size = int(1.0 / self.delta_v) + 1
            else:
                warnings.warn("Cannot determine the sample size")
                return 0
        return self._sample_size

    @sample_size.setter
    def sample_size(self, value):
        if (self._knot_vector_u is None or len(self._knot_vector_u) == 0) or\
                (self._knot_vector_v is None or len(self._knot_vector_v) == 0):
            warnings.warn("Cannot determine the delta value. Please set knot vectors before setting the sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_u = self._knot_vector_u[self._degree_u]
        stop_u = self._knot_vector_u[-(self._degree_u+1)]
        start_v = self._knot_vector_v[self._degree_v]
        stop_v = self._knot_vector_v[-(self._degree_v+1)]

        # Clean up the surface points lists, if necessary
        self._reset_evalpts()

        # Set delta values
        self._delta_u = (stop_u - start_u) / float(value - 1)
        self._delta_v = (stop_v - start_v) / float(value - 1)

        # Set sample size
        self._sample_size = value

    @property
    def delta_u(self):
        """ Evaluation delta in U-direction.

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
            raise ValueError("Surface evaluation delta should be between 0.0 and 1.0")

        # Clean up the surface points lists, if necessary
        self._reset_evalpts()

        # Set a new delta value
        self._delta_u = float(value)

    @property
    def delta_v(self):
        """ Evaluation delta in V-direction.

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
            raise ValueError("Surface evaluation delta should be between 0.0 and 1.0")

        # Clean up the surface points lists, if necessary
        self._reset_evalpts()

        # Set a new delta value
        self._delta_v = float(value)

    @property
    def delta(self):
        """ Evaluation delta in U- and V-directions.

        Evaluation delta corresponds to the *step size* while ``evaluate`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        .. note:: The delta value is 0.1 by default.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self.delta_u, self.delta_v

    @delta.setter
    def delta(self, value):
        if isinstance(value, float):
            if float(value) <= 0 or float(value) >= 1:
                raise ValueError("Surface evaluation delta should be between 0.0 and 1.0")
            self._delta_u = value
            self._delta_v = value
        elif isinstance(value, (list, tuple)):
            if len(value) == 2:
                if float(value[0]) <= 0 or float(value[0]) >= 1 or float(value[1]) <= 0 or float(value[1]) >= 1:
                    raise ValueError("Surface evaluation delta should be between 0.0 and 1.0")
                self._delta_u = value[0]
                self._delta_v = value[1]
            else:
                raise ValueError("Surface requires 2 delta values")
        else:
            warnings.warn("Cannot set delta. Please use a float or a list with 2 elements")

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
            warnings.warn("Visualization component is NOT an instance of VisAbstract class")
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
            self._eval_bbox()

        return self._bounding_box

    def _eval_bbox(self):
        """ Evaluates bounding box of the surface. """
        # Find correct dimension of the control points
        dim = self._dimension
        if self._rational:
            dim -= 1

        # Evaluate bounding box
        bbmin = [float('inf') for _ in range(0, dim)]
        bbmax = [0.0 for _ in range(0, dim)]
        for cpt in self.ctrlpts:
            for i, arr in enumerate(zip(cpt, bbmin)):
                if arr[0] < arr[1]:
                    bbmin[i] = arr[0]
            for i, arr in enumerate(zip(cpt, bbmax)):
                if arr[0] > arr[1]:
                    bbmax[i] = arr[0]

        self._bounding_box = (tuple(bbmin), tuple(bbmax))

    # Runs visualization component to render the surface
    def render(self, **kwargs):
        """ Renders the surface using the loaded visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Possible keyword arguments are

        * ``cpcolor``: sets the color of the control points grid
        * ``surfcolor``: sets the color of the surface

        """
        if not self._vis_component:
            warnings.warn("No visualization component has been set")
            return

        cpcolor = kwargs.get('cpcolor', 'blue')
        surfcolor = kwargs.get('surfcolor', 'green')

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
        self._vis_component.add(ptsarr=self._surface_points,
                                size=[self.sample_size, self.sample_size],
                                name="Surface", color=surfcolor, plot_type='evalpts')
        self._vis_component.render()

    # Resets the control points
    def _reset_ctrlpts(self):
        self._control_points = None
        self._control_points2D = None
        self._bounding_box = None

    # Resets the evaluated points
    def _reset_evalpts(self):
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

    def surfpt(self, u, v):
        """ Evaluates the surface at the given (u,v) parameter.

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :return: evaluated surface point at the given knot values
        :rtype: list
        """
        # Check all parameters are set before the surface evaluation
        self._check_variables()
        # Check u and v parameters are correct
        helpers.check_uv(u, v)

        # Algorithm A3.5 nd A4.3
        span_u = helpers.find_span(self.knotvector_u, self.ctrlpts_size_u, u)
        basis_u = helpers.basis_function(self.degree_u, self.knotvector_u, span_u, u)
        span_v = helpers.find_span(self.knotvector_v, self.ctrlpts_size_v, v)
        basis_v = helpers.basis_function(self.degree_v, self.knotvector_v, span_v, v)

        idx_u = span_u - self.degree_u
        spt = [0.0 for _ in range(self.dimension)]

        for l in range(0, self._degree_v + 1):
            temp = [0.0 for _ in range(self.dimension)]
            idx_v = span_v - self.degree_v + l
            for k in range(0, self.degree_u + 1):
                temp[:] = [tmp + (basis_u[k] * cp) for tmp, cp in zip(temp, self._control_points2D[idx_u + k][idx_v])]
            spt[:] = [pt + (basis_v[l] * tmp) for pt, tmp in zip(spt, temp)]

        # Divide by weight, if the surface is rational
        if self._rational:
            surfpt = [float(c / spt[-1]) for c in spt[0:(self.dimension - 1)]]
        else:
            surfpt = spt

        return surfpt

    def evaluate(self, **kwargs):
        """ Evaluates the surface.

        Keyword arguments:

        * ``start_u``: start parameter in u-direction
        * ``stop_u``: stop parameter in u-direction
        * ``start_v``: start parameter in v-direction
        * ``stop_v``: stop parameter in v-direction

        The ``start_u``, ``start_v`` and ``stop_u`` and ``stop_v`` parameters allow evaluation of a surface segment
        in the range  *[start_u, stop_u][start_v, stop_v]* i.e. the surface will also be evaluated at the ``stop_u``
        and ``stop_v`` parameter values.

        .. note:: The evaluated surface points are stored in :py:attr:`~surfpts`.

        """
        # Check all parameters are set before the surface evaluation
        self._check_variables()

        # Find evaluation start and stop parameter values
        start_u = kwargs.get('start_u', self.knotvector_u[self.degree_u])
        stop_u = kwargs.get('stop_u', self.knotvector_u[-(self.degree_u+1)])
        start_v = kwargs.get('start_v', self.knotvector_v[self.degree_v])
        stop_v = kwargs.get('stop_v', self.knotvector_v[-(self.degree_v+1)])

        # Check if all the input parameters are in the range
        helpers.check_uv(start_u, stop_u)
        helpers.check_uv(start_v, stop_v)

        # Clean up the surface points lists, if necessary
        self._reset_evalpts()

        # Compute knots in the range
        knots_u = utilities.linspace(start_u, stop_u, self.sample_size)
        knots_v = utilities.linspace(start_v, stop_v, self.sample_size)

        # Find spans belonging to the knots
        spans_u = helpers.find_spans(self.knotvector_u, self.ctrlpts_size_u, knots_u)
        spans_v = helpers.find_spans(self.knotvector_v, self.ctrlpts_size_v, knots_v)

        # Find basis functions
        basis_u = helpers.basis_functions(self.degree_u, self.knotvector_u, spans_u, knots_u)
        basis_v = helpers.basis_functions(self.degree_v, self.knotvector_v, spans_v, knots_v)

        # Evaluate the surface directly
        for i in range(len(knots_u)):
            idx_u = spans_u[i] - self.degree_u
            for j in range(len(knots_v)):
                spt = [0.0 for _ in range(self.dimension)]
                for l in range(0, self.degree_v + 1):
                    temp = [0.0 for _ in range(self.dimension)]
                    idx_v = spans_v[j] - self.degree_v + l
                    for k in range(0, self.degree_u + 1):
                        temp[:] = [tmp + (basis_u[i][k] * cp) for tmp, cp in
                                   zip(temp, self._control_points2D[idx_u + k][idx_v])]
                    spt[:] = [pt + (basis_v[j][l] * tmp) for pt, tmp in zip(spt, temp)]

                # Divide by weight, if the surface is rational
                if self._rational:
                    surfpt = [float(c / spt[-1]) for c in spt[0:(self.dimension - 1)]]
                else:
                    surfpt = spt

                self._surface_points.append(surfpt)


class Multi(object):
    """ Abstract class for curve and surface containers. """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._elements = []  # elements contained
        self._sample_size = 10 # sample size
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
    def sample_size(self):
        """ Sample size.

        Sample size defines the number of evaluated points to generate. It sets the ``delta`` property.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        return self._sample_size

    @sample_size.setter
    def sample_size(self, value):
        self._sample_size = value

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


class VisConfigAbstract(object):
    """ Visualization configuration abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all visualization configurations
    in NURBS-Python package.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass


class VisAbstract(object):
    """ Visualization abstract class

    Uses Python's *Abstract Base Class* implementation to define a base for all common visualization options
    in NURBS-Python package.
    """
    __metaclass__ = abc.ABCMeta

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
        :param size: size in all directions, e.g. in U- and V-direction
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
    def render(self):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstract`` class.
        """
        pass


class VisAbstractSurf(VisAbstract):
    """ Visualization abstract class for surfaces

    Implements ``VisABstract`` class and also uses Python's *Abstract Base Class* implementation to define a base
    for **surface** visualization options in NURBS-Python package.
    """
    __metaclass__ = abc.ABCMeta

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
    def render(self):
        """ Abstract method for rendering plots of the point sets.

        This method must be implemented in all subclasses of ``VisAbstractSurf`` class.
        """
        pass
