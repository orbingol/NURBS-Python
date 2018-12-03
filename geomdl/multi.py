"""
.. module:: Multi
    :platform: Unix, Windows
    :synopsis: Container module for storage and visualization of curves and surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
import warnings
import six
from . import abstract
from . import utilities


class AbstractContainer(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract class for curve and surface containers.

    This class implements Python Iterator Protocol and therefore any instance of this class can be directly used in
    a for loop.

    This class provides the following properties:

    * dimension
    * evalpts
    * bbox
    * vis
    """

    def __init__(self, *args, **kwargs):
        self._elements = []  # elements contained
        self._delta = None  # evaluation delta
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
    def dimension(self):
        """ Shape dimension.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the dimension of the shape
        """
        if self._elements:
            return self._elements[0].dimension
        return 0

    @property
    def evalpts(self):
        """ Evaluated points.

        Since there are multiple shapes contained in the Multi objects, the evaluated points will be returned in the
        format of list of individual evaluated points which is also a list of Cartesian coordinates.

        The following code example illustrates these details:

        .. code-block:: python

            multi_obj = Multi.SurfaceContainer()  # it can be Multi.CurveContainer() too
            # Add shapes to multi_obj via multi_obj.add() method
            # Then, the following loop will print all the evaluated points of the Multi object
            for idx, mpt in enumerate(multi_obj.evalpts):
                print("Shape", idx+1, "contains", len(mpt), "points. These points are:")
                for pt in mpt:
                    line = ", ".join([str(p) for p in pt])
                    print(line)

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the evaluated points of all contained shapes
        """
        ret = []
        for elem in self._elements:
            elem.delta = self._delta
            evalpts = elem.evalpts
            ret.append(evalpts)
        return ret

    @property
    def bbox(self):
        """ Bounding box.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the bounding box of all contained shapes
        """
        all_box = []
        for elem in self._elements:
            all_box += list(elem.bbox)
        return utilities.evaluate_bounding_box(all_box)

    @property
    def vis(self):
        """ Visualization component.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        :type: float
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, abstract.VisAbstract):
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
        """ Renders plots using the visualization component.

        .. note::

            This is an abstract method and it must be implemented in the subclass.
        """
        pass


class CurveContainer(AbstractContainer):
    """ Container class for storing multiple curves.

    This class implements Python Iterator Protocol and therefore any instance of this class can be directly used in
    a for loop.

    Rendering depends on the visualization instance, e.g. if you are using ``VisMPL`` module,
    you can visualize a 3D curve using a ``VisCurve2D`` instance
    but you cannot visualize a 2D curve with a ``VisCurve3D`` instance.

    This class provides the following properties:

    * dimension
    * evalpts
    * bbox
    * vis
    * delta
    * sample_size

    The following code example illustrates the usage of the Python properties:

    .. code-block:: python

        # Create a multi-curve container instance
        mcrv = Multi.CurveContainer()

        # Add single or multi curves to the multi container using mcrv.add() command
        # Addition operator, e.g. mcrv1 + mcrv2, also works

        # Set the evaluation delta of the multi-curve
        mcrv.delta = 0.05

        # Get the evaluated points
        curve_points = mcrv.evalpts
    """

    def __init__(self, *args, **kwargs):
        super(CurveContainer, self).__init__()
        self._instance = abstract.Curve
        self._delta = 0.01  # evaluation delta
        for arg in args:
            self.add(arg)

    @property
    def delta(self):
        """ Evaluation delta.

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
        :type: float
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Curve evaluation delta should be between 0.0 and 1.0")
        self._delta = float(value)

    @property
    def sample_size(self):
        """ Sample size.

        Sample size defines the number of curve points to generate. It also sets the ``delta`` property.

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        return int(1 / self.delta) + 1

    @sample_size.setter
    def sample_size(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")
        self.delta = 1.0 / float(value - 1)

    def render(self, **kwargs):
        """ Renders the curve the using the visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Keyword Arguments:

        * ``cpcolor``: sets the color of the control points grid
        * ``evalcolor``: sets the color of the surface
        * ``filename``: saves the plot with the input name
        * ``plot``: a flag to control displaying the plot window. *Default: True*
        * ``delta``: if True, the evaluation delta of the Multi object will be used. *Default: True*

        The ``cpcolor`` and ``evalcolor`` arguments can be a string or a list of strings corresponding to the color
        values. Both arguments are processed separately, e.g. ``cpcolor`` can be a string whereas ``evalcolor`` can be
        a list or  a tuple, or vice versa. A single string value sets the color to the same value. List input allows
        customization over the color values. If none provided, a random color will be selected.

        The ``plot`` argument is useful when you would like to work on the command line without any window context.
        If ``plot`` flag is False, this method saves the plot as an image file (.png file where possible) and disables
        plot window popping out. If you don't provide a file name, the name of the image file will be pulled from the
        configuration class.
        """
        if not self._vis_component:
            warnings.warn("No visualization component has set")
            return

        # Get the color values from keyword arguments
        cpcolor = kwargs.get('cpcolor')
        evalcolor = kwargs.get('evalcolor')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)
        # Flag to control evaluation delta updates
        update_delta = kwargs.get('delta', True)

        # Check if the input list sizes are equal
        if isinstance(cpcolor, (list, tuple)):
            if len(cpcolor) < len(self._elements):
                raise ValueError("The number of color values in 'cpcolor' (" + str(len(cpcolor)) +
                                 ") cannot be less than the number of curves (" + str(len(self._elements)) + ")")

        if isinstance(evalcolor, (list, tuple)):
            if len(evalcolor) < len(self._elements):
                raise ValueError("The number of color values in 'evalcolor' (" + str(len(evalcolor)) +
                                 ") cannot be less than the number of curves (" + str(len(self._elements)) + ")")

        # Run the visualization component
        self._vis_component.clear()
        for idx, elem in enumerate(self._elements):
            if update_delta:
                elem.delta = self.delta
            elem.evaluate()

            # Color selection
            color = _select_color(cpcolor, evalcolor, idx=idx)

            self._vis_component.add(ptsarr=elem.ctrlpts,
                                    name="Control Points for " + elem.name,
                                    color=color[0],
                                    plot_type='ctrlpts')
            self._vis_component.add(ptsarr=elem.evalpts,
                                    name=elem.name,
                                    color=color[1],
                                    plot_type='evalpts')
        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible)


class SurfaceContainer(AbstractContainer):
    """ Container class for storing multiple surfaces.

    This class implements Python Iterator Protocol and therefore any instance of this class can be directly used in
    a for loop.

    This class provides the following properties:

    * dimension
    * evalpts
    * bbox
    * vis
    * delta
    * delta_u
    * delta_v
    * sample_size
    * sample_size_u
    * sample_size_v

    The following code example illustrates the usage of these Python properties:

    .. code-block:: python

        # Create a multi-surface container instance
        msurf = Multi.SurfaceContainer()

        # Add single or multi surfaces to the multi container using msurf.add() command
        # Addition operator, e.g. msurf1 + msurf2, also works

        # Set the evaluation delta of the multi-surface
        msurf.delta = 0.05

        # Get the evaluated points
        surface_points = msurf.evalpts
    """

    def __init__(self, *args, **kwargs):
        super(SurfaceContainer, self).__init__()
        self._instance = abstract.Surface
        self._delta = [0.01, 0.01]  # evaluation delta
        for arg in args:
            self.add(arg)

    @property
    def sample_size_u(self):
        """ Sample size for the u-direction.

        Sample size defines the number of surface points to generate. It also sets the ``delta`` property.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size for the u-direction
        :setter: Sets sample size for the u-direction
        :type: int
        """
        return int(1.0 / self.delta_u) + 1

    @sample_size_u.setter
    def sample_size_u(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")
        self.delta_u = 1.0 / float(value - 1)

    @property
    def sample_size_v(self):
        """ Sample size for the v-direction.

        Sample size defines the number of surface points to generate. It also sets the ``delta`` property.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size for the v-direction
        :setter: Sets sample size for the v-direction
        :type: int
        """
        return int(1.0 / self.delta_v) + 1

    @sample_size_v.setter
    def sample_size_v(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")
        self.delta_v = 1.0 / float(value - 1)

    @property
    def sample_size(self):
        """ Sample size for both u- and v-directions.

        Sample size defines the number of surface points to generate. It also sets the ``delta`` property.

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size values as a tuple of values corresponding to u- and v-directions
        :setter: Sets the same sample size value for both u- and v-directions
        :type: int
        """
        sample_size_u = int(1.0 / self.delta_u) + 1
        sample_size_v = int(1.0 / self.delta_v) + 1
        return sample_size_u, sample_size_v

    @sample_size.setter
    def sample_size(self, value):
        self.delta_u = 1.0 / float(value - 1)
        self.delta_v = 1.0 / float(value - 1)

    @property
    def delta_u(self):
        """ Evaluation delta for the u-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_u`` and ``sample_size_u`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_u`` will also set ``sample_size_u``.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the delta value for the u-direction
        :setter: Sets the delta value for the u-direction
        :type: float
        """
        return self._delta[0]

    @delta_u.setter
    def delta_u(self, value):
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta (u-direction) must be between 0.0 and 1.0")
        self._delta[0] = float(value)

    @property
    def delta_v(self):
        """ Evaluation delta for the v-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_v`` and ``sample_size_v`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_v`` will also set ``sample_size_v``.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the delta value for the v-direction
        :setter: Sets the delta value for the v-direction
        :type: float
        """
        return self._delta[1]

    @delta_v.setter
    def delta_v(self, value):
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta (v-direction) should be between 0.0 and 1.0")
        self._delta[1] = float(value)

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

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the delta values as a tuple of values corresponding to u- and v-directions
        :setter: Sets the same delta value for both u- and v-directions
        :type: float
        """
        return tuple(self._delta)

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

    def render(self, **kwargs):
        """ Renders the surface the using the visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Keyword Arguments:
            * ``cpcolor``: sets the color of the control points grids
            * ``evalcolor``: sets the color of the surface
            * ``filename``: saves the plot with the input name
            * ``plot``: a flag to control displaying the plot window. *Default: True*
            * ``colormap``: sets the colormap of the surfaces
            * ``delta``: if True, the evaluation delta of the Multi object will be used. *Default: True*

        The ``cpcolor`` and ``evalcolor`` arguments can be a string or a list of strings corresponding to the color
        values. Both arguments are processed separately, e.g. ``cpcolor`` can be a string whereas ``evalcolor`` can be
        a list or  a tuple, or vice versa. A single string value sets the color to the same value. List input allows
        customization over the color values. If none provided, a random color will be selected.

        The ``plot`` argument is useful when you would like to work on the command line without any window context.
        If ``plot`` flag is False, this method saves the plot as an image file (.png file where possible) and disables
        plot window popping out. If you don't provide a file name, the name of the image file will be pulled from the
        configuration class.

        Please note that ``colormap`` argument can only work with visualization classes that support colormaps. As an
        example, please see :py:class:`.VisMPL.VisSurfTriangle()` class documentation. This method expects multiple
        colormap inputs as a list or tuple, preferable the input list size is the same as the number of surfaces
        contained in the class. In the case of number of surfaces is bigger than number of input colormaps, this method
        will automatically assign a random color for the remaining surfaces.
        """
        if not self._vis_component:
            warnings.warn("No visualization component has set")
            return

        # Get the color values from keyword arguments
        cpcolor = kwargs.get('cpcolor')
        evalcolor = kwargs.get('evalcolor')
        trimcolor = kwargs.get('trimcolor', 'black')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)
        # Flag to control evaluation delta updates
        update_delta = kwargs.get('delta', True)

        # Check if the input list sizes are equal
        if isinstance(cpcolor, (list, tuple)):
            if len(cpcolor) != len(self._elements):
                raise ValueError("The number of colors in 'cpcolor' (" + str(len(cpcolor)) +
                                 ") cannot be less than the number of surfaces (" + str(len(self._elements)) + ")")

        if isinstance(evalcolor, (list, tuple)):
            if len(evalcolor) != len(self._elements):
                raise ValueError("The number of colors in 'evalcolor' (" + str(len(evalcolor)) +
                                 ") cannot be less than the number of surfaces (" + str(len(self._elements)) + ")")

        # Get colormaps as a list
        surf_cmaps = kwargs.get('colormap', [])
        if not isinstance(surf_cmaps, (list, tuple)):
            warnings.warn("Expecting a list of colormap values, not " + str(type(surf_cmaps)))
            surf_cmaps = []

        # Run the visualization component
        self._vis_component.clear()
        for idx, elem in enumerate(self._elements):
            if update_delta:
                elem.delta = self.delta
            elem.evaluate()

            # Color selection
            color = _select_color(cpcolor, evalcolor, idx=idx)

            # Add control points
            if self._vis_component.plot_types['ctrlpts'] == 'points':
                self._vis_component.add(ptsarr=elem.ctrlpts, name="Control Points for " + elem.name,
                                        color=color[0], plot_type='ctrlpts')

            # Add control points as quads
            if self._vis_component.plot_types['ctrlpts'] == 'quads':
                ctrlpts_quads = utilities.make_quad_mesh(elem.ctrlpts, elem.ctrlpts_size_u, elem.ctrlpts_size_v)
                self._vis_component.add(ptsarr=ctrlpts_quads, name="Control Points for " + elem.name,
                                        color=color[0], plot_type='ctrlpts')

            # Add surface points
            if self._vis_component.plot_types['evalpts'] == 'points':
                self._vis_component.add(ptsarr=elem.evalpts, name=elem.name, color=color[1], plot_type='evalpts')

            # Add surface points as quads
            if self._vis_component.plot_types['evalpts'] == 'quads':
                evalpts_quads = utilities.make_quad_mesh(elem.evalpts, elem.sample_size_u, elem.sample_size_v)
                self._vis_component.add(ptsarr=evalpts_quads, name=elem.name, color=color[1], plot_type='evalpts')

            # Add surface points as vertices and triangles
            if self._vis_component.plot_types['evalpts'] == 'triangles':
                elem.tessellate()
                self._vis_component.add(ptsarr=[elem.tessellator.vertices, elem.tessellator.triangles],
                                        name=elem.name, color=color[1], plot_type='evalpts')

            # Visualize the trim curve
            for idx, trim in enumerate(elem.trims):
                self._vis_component.add(ptsarr=elem.evaluate_list(trim.evalpts),
                                        name="Trim Curve " + str(idx + 1),
                                        color=trimcolor, plot_type='trimcurve')

        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible, colormap=surf_cmaps)


def _select_color(cpcolor, evalcolor, idx=0):
    """ Selects item color for plotting.

    :param cpcolor: color for control points grid item
    :type cpcolor: str, list, tuple
    :param evalcolor: color for evaluated points grid item
    :type evalcolor: str, list, tuple
    :param idx: index of the current shape
    :type idx: int
    :return: a list of color values
    :rtype: list
    """
    # Random colors by default
    color = utilities.color_generator()

    # Constant color for control points grid
    if isinstance(cpcolor, str):
        color[0] = cpcolor

    # User-defined color for control points grid
    if isinstance(cpcolor, (list, tuple)):
        color[0] = cpcolor[idx]

    # Constant color for evaluated points grid
    if isinstance(evalcolor, str):
        color[1] = evalcolor

    # User-defined color for evaluated points grid
    if isinstance(evalcolor, (list, tuple)):
        color[1] = evalcolor[idx]

    return color
