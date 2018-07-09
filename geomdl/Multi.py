"""
.. module:: Multi
    :platform: Unix, Windows
    :synopsis: Container module for storage and visualization of curves and surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import warnings
from . import Abstract
from . import utilities


class MultiCurve(Abstract.Multi):
    """ Container class for storing multiple curves.

    Rendering depends on the visualization instance, e.g. if you are using ``VisMPL`` module,
    you can visualize a 3D curve using a ``VisCurve2D`` instance
    but you cannot visualize a 2D curve with a ``VisCurve3D`` instance.
    """

    def __init__(self):
        super(MultiCurve, self).__init__()
        self._instance = Abstract.Curve
        self._sample_size = 0  # sample size

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

    def render(self, **kwargs):
        """ Renders the curve the using the visualization component.

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
            warnings.warn("No visualization component has set")
            return

        # Get the color values from keyword arguments
        cpcolor = kwargs.get('cpcolor')
        evalcolor = kwargs.get('evalcolor')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)

        # Run the visualization component
        self._vis_component.clear()
        for idx, elem in enumerate(self._elements):
            if self._sample_size != 0:
                elem.sample_size = self._sample_size
            elem.evaluate()
            color = utilities.color_generator()
            self._vis_component.add(ptsarr=elem.ctrlpts,
                                    name="Control Points " + str(idx + 1),
                                    color=cpcolor if cpcolor is not None else color[0],
                                    plot_type='ctrlpts')
            self._vis_component.add(ptsarr=elem.curvepts,
                                    name="Curve " + str(idx + 1),
                                    color=evalcolor if evalcolor is not None else color[1],
                                    plot_type='evalpts')
        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible)


class MultiSurface(Abstract.Multi):
    """ Container class for storing multiple surfaces. """

    def __init__(self):
        super(MultiSurface, self).__init__()
        self._instance = Abstract.Surface
        self._sample_size_u = 0
        self._sample_size_v = 0

    @property
    def sample_size_u(self):
        """ Sample size for the u-direction.

        Sample size defines the number of evaluated points to generate on the defined direction.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        return self._sample_size_v

    @sample_size_u.setter
    def sample_size_u(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        self._sample_size_u = value

    @property
    def sample_size_v(self):
        """ Sample size for the v-direction.

        Sample size defines the number of evaluated points to generate on the defined direction.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        return self._sample_size_v

    @sample_size_v.setter
    def sample_size_v(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        self._sample_size_v = value

    @property
    def sample_size(self):
        """ Sample size.

        Sample size defines the number of evaluated points to generate on u- and v-direction.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        return self.sample_size_u, self.sample_size_v

    @sample_size.setter
    def sample_size(self, value):
        self.sample_size_u = value
        self.sample_size_v = value

    def render(self, **kwargs):
        """ Renders the surface the using the visualization component.

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
            warnings.warn("No visualization component has set")
            return

        # Get the color values from keyword arguments
        cpcolor = kwargs.get('cpcolor')
        evalcolor = kwargs.get('evalcolor')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)

        # Run the visualization component
        self._vis_component.clear()
        for idx, elem in enumerate(self._elements):
            if self._sample_size_u != 0:
                elem.sample_size_u = self.sample_size_u
            if self._sample_size_v != 0:
                elem.sample_size_v = self.sample_size_v
            elem.evaluate()
            color = utilities.color_generator()
            self._vis_component.add(ptsarr=elem.ctrlpts,
                                    size=[elem.ctrlpts_size_u, elem.ctrlpts_size_v],
                                    name="Control Points " + str(idx + 1),
                                    color=cpcolor if cpcolor is not None else color[0],
                                    plot_type='ctrlpts')
            self._vis_component.add(ptsarr=elem.surfpts,
                                    size=[elem.sample_size_u, elem.sample_size_v],
                                    name="Surface " + str(idx + 1),
                                    color=evalcolor if evalcolor is not None else color[1],
                                    plot_type='evalpts')
        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible)
