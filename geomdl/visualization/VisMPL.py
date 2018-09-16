"""
.. module:: VisMPL
    :platform: Unix, Windows
    :synopsis: Matplotlib visualization component for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import Abstract
from . import utilities

from . import numpy as np
import matplotlib as mpl
import matplotlib.tri as mpltri
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class VisConfig(Abstract.VisConfigAbstract):
    """ Configuration class for Matplotlib visualization module.

    This class is only required when you prefer to change the default plotting behavior, such as hiding control points
    plot or legend. By default, the following variables and their default values are used in all ``VisMPL``
    visualization classes.

    * ``ctrlpts`` (True or False, *default: True*): Enables/Disables control points polygon/grid plot in the figure
    * ``legend`` (True or False): Enables/Disables legend in the figure
    * ``axes`` (True or False): Enables/Disables axes and grid in the figure
    * ``figure_size`` (list, *default: [10.67, 8]*): Size of the figure in (x, y)
    * ``figure_dpi`` (int, *default: 96*): Resolution of the figure in DPI

    The following example illustrates the usage of the configuration class.

    .. code-block:: python

        # Create a curve (or a surface) instance
        curve = NURBS.Curve()

        # Skipping degree, knot vector and control points assignments

        # Create a visualization configuration instance with no legend, no axes and set the resolution to 120 dpi
        vis_config = VisMPL.VisConfig(legend=False, axes=False, figure_dpi=120)

        # Create a visualization method instance using the configuration above
        vis_obj = VisMPL.VisCurve2D(vis_config)

        # Set the visualization method of the curve object
        curve.vis = vis_obj

        # Plot the curve
        curve.render()

    The following keyword arguments can be used to control tessellation in modules which use the tessellation function
    :py:func:`.make_triangular_mesh()`:

    * ``tessellate_vertex_func``: Sets the function called after generating the vertex list
    * ``tessellate_vertex_args``: Sets the arguments passed to the vertex post-processing function
    * ``tessellate_triangle_func``: Sets the function called after generating the triangle list
    * ``tessellate_triangle_args``: Sets the arguments passed to the triangle post-processing function

    Please refer to the **Examples Repository** for more details.
    """

    def __init__(self, **kwargs):
        super(VisConfig, self).__init__(**kwargs)
        self.display_ctrlpts = kwargs.get('ctrlpts', True)
        self.display_legend = kwargs.get('legend', True)
        self.display_axes = kwargs.get('axes', True)
        self.figure_size = kwargs.get('figure_size', [10.67, 8])
        self.figure_dpi = kwargs.get('figure_dpi', 96)
        self.figure_image_filename = "temp-figure.png"
        # Tessellation post-processing configuration
        self.tslpp_vertex_func = kwargs.get('tessellate_vertex_func', None)
        self.tslpp_vertex_args = kwargs.get('tessellate_vertex_args', None)
        self.tslpp_triangle_func = kwargs.get('tessellate_triangle_func', None)
        self.tslpp_triangle_args = kwargs.get('tessellate_triangle_args', None)

    @staticmethod
    def set_axes_equal(ax):
        """ Sets equal aspect ratio across the three axes of a 3D plot.

        Contributed by Xuefeng Zhao.

        :param ax: a Matplotlib axis, e.g., as output from plt.gca().
        """
        bounds = [ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()]
        ranges = [abs(bound[1] - bound[0]) for bound in bounds]
        centers = [np.mean(bound) for bound in bounds]
        radius = 0.5 * max(ranges)
        lower_limits = centers - radius
        upper_limits = centers + radius
        ax.set_xlim3d([lower_limits[0], upper_limits[0]])
        ax.set_ylim3d([lower_limits[1], upper_limits[1]])
        ax.set_zlim3d([lower_limits[2], upper_limits[2]])

    @staticmethod
    def save_figure_as(fig, filename):
        """ Saves the figure as a file.

        :param fig: a Matplotlib figure instance
        :param filename: file name to save
        """
        if filename is not None:
            fig.savefig(str(filename), bbox_inches='tight')


class VisCurve2D(Abstract.VisAbstract):
    """ Matplotlib visualization module for 2D curves """
    def __init__(self, config=VisConfig()):
        super(VisCurve2D, self).__init__(config=config)

    def render(self, **kwargs):
        """ Plots the 2D curve and the control points polygon. """
        # Calling parent function
        super(VisCurve2D, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Draw control points polygon and the curve
        fig = plt.figure(figsize=self._config.figure_size, dpi=self._config.figure_dpi)
        ax = fig.gca()

        # Start plotting
        for plot in self._plots:
            pts = np.array(plot['ptsarr'])
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                cpplot, = plt.plot(pts[:, 0], pts[:, 1], color=plot['color'], linestyle='-.', marker='o')
                legend_proxy.append(cpplot)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                curveplt, = plt.plot(pts[:, 0], pts[:, 1], color=plot['color'], linestyle='-')
                legend_proxy.append(curveplt)
                legend_names.append(plot['name'])

        # Add legend
        if self._config.display_legend:
            plt.legend(legend_proxy, legend_names)

        # Remove axes
        if not self._config.display_axes:
            plt.axis('off')

        # Set aspect ratio
        ax.set_aspect('equal')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if fig_display:
            plt.show()
        else:
            fig_filename = self._config.figure_image_filename if fig_filename is None else fig_filename

        # Save the figure
        self._config.save_figure_as(fig, fig_filename)


class VisCurve3D(Abstract.VisAbstract):
    """ Matplotlib visualization module for 3D curves. """
    def __init__(self, config=VisConfig()):
        super(VisCurve3D, self).__init__(config=config)

    def render(self, **kwargs):
        """ Plots the 3D curve and the control points polygon. """
        # Calling parent function
        super(VisCurve3D, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Draw control points polygon and the 3D curve
        fig = plt.figure(figsize=self._config.figure_size, dpi=self._config.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            pts = np.array(plot['ptsarr'])

            # Try not to fail if the input is 2D
            if pts.shape[1] == 2:
                pts = np.c_[pts, np.zeros(pts.shape[0])]

            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='-.', marker='o')
                plot1_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot1_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='-')
                plot2_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'])
                legend_proxy.append(plot2_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self._config.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self._config.display_axes:
            plt.axis('off')

        # Set axes equal
        self._config.set_axes_equal(ax)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if fig_display:
            plt.show()
        else:
            fig_filename = self._config.figure_image_filename if fig_filename is None else fig_filename

        # Save the figure
        self._config.save_figure_as(fig, fig_filename)


class VisSurface(Abstract.VisAbstractSurf):
    """ Matplotlib visualization module for surfaces.

    Triangular mesh plot for the surface and wireframe plot for the control points grid.
    """
    def __init__(self, config=VisConfig()):
        super(VisSurface, self).__init__(config=config)

    def render(self, **kwargs):
        """ Plots the surface and the control points grid. """
        # Calling parent function
        super(VisSurface, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self._config.figure_size, dpi=self._config.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                pts = np.array(utilities.make_quad_mesh(plot['ptsarr'], plot['size'][0], plot['size'][1]))
                cp_z = pts[:, 2] + self._ctrlpts_offset
                ax.plot(pts[:, 0], pts[:, 1], cp_z, color=plot['color'], linestyle='-.', marker='o')
                plot1_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot1_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                verts, tris = utilities.make_triangle_mesh(plot['ptsarr'], plot['size'][0], plot['size'][1],
                                                           vertex_postprocess_func=self._config.tslpp_vertex_func,
                                                           vertex_postprocess_args=self._config.tslpp_vertex_args,
                                                           triangle_postprocess_func=self._config.tslpp_triangle_func,
                                                           triangle_postprocess_args=self._config.tslpp_triangle_args)
                for tri in tris:
                    pts = np.array(tri.vertices_raw)
                    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'])
                plot2_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'])
                legend_proxy.append(plot2_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self._config.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self._config.display_axes:
            plt.axis('off')

        # Set axes equal
        self._config.set_axes_equal(ax)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if fig_display:
            plt.show()
        else:
            fig_filename = self._config.figure_image_filename if fig_filename is None else fig_filename

        # Save the figure
        self._config.save_figure_as(fig, fig_filename)


class VisSurfWireframe(Abstract.VisAbstractSurf):
    """ Matplotlib visualization module for surfaces.

    Scatter plot for the control points and wireframe plot for the surface points.
    """
    def __init__(self, config=VisConfig()):
        super(VisSurfWireframe, self).__init__(config=config)

    def render(self, **kwargs):
        """ Plots the surface and the control points grid. """
        # Calling parent function
        super(VisSurfWireframe, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self._config.figure_size, dpi=self._config.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                pts = np.array(plot['ptsarr'])
                cp_z = pts[:, 2] + self._ctrlpts_offset
                ax.scatter(pts[:, 0], pts[:, 1], cp_z, color=plot['color'], s=25, depthshade=True)
                plot1_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot1_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                pts = np.array(utilities.make_quad_mesh(plot['ptsarr'], plot['size'][0], plot['size'][1]))
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'])
                plot2_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'])
                legend_proxy.append(plot2_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self._config.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self._config.display_axes:
            plt.axis('off')

        # Set axes equal
        self._config.set_axes_equal(ax)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if fig_display:
            plt.show()
        else:
            fig_filename = self._config.figure_image_filename if fig_filename is None else fig_filename

        # Save the figure
        self._config.save_figure_as(fig, fig_filename)


class VisSurfTriangle(Abstract.VisAbstractSurf):
    """ Matplotlib visualization module for surfaces.

    Wireframe plot for the control points and triangulated plot (using ``plot_trisurf``) for the surface points.
    The surface is triangulated externally using :py:func:`.utilities.make_triangle_mesh()` function.
    """
    def __init__(self, config=VisConfig()):
        super(VisSurfTriangle, self).__init__(config=config)

    def render(self, **kwargs):
        """ Plots the surface and the control points grid.

        Keyword arguments:
            * ``colormap``: applies colormap to the surface

        Colormaps are a visualization feature of Matplotlib. They can be used for several types of surface plots via
        the following import statement: ``from matplotlib import cm``

        The following link displays the list of Matplolib colormaps and some examples on colormaps:
        https://matplotlib.org/tutorials/colors/colormaps.html
        """
        # Calling parent function
        super(VisSurfTriangle, self).render(**kwargs)

        # Colormaps
        surf_cmaps = kwargs.get('colormap', None)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self._config.figure_size, dpi=self._config.figure_dpi)
        ax = Axes3D(fig)

        surf_count = 0
        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                pts = np.array(utilities.make_quad_mesh(plot['ptsarr'], plot['size'][0], plot['size'][1]))
                cp_z = pts[:, 2] + self._ctrlpts_offset
                ax.plot(pts[:, 0], pts[:, 1], cp_z, color=plot['color'], linestyle='-.', marker='o')
                plot1_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot1_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                # Use internal triangulation algorithm instead of Qhull (MPL default)
                verts, tris = utilities.make_triangle_mesh(plot['ptsarr'], plot['size'][0], plot['size'][1],
                                                           vertex_postprocess_func=self._config.tslpp_vertex_func,
                                                           vertex_postprocess_args=self._config.tslpp_vertex_args,
                                                           triangle_postprocess_func=self._config.tslpp_triangle_func,
                                                           triangle_postprocess_args=self._config.tslpp_triangle_args)
                # Extract zero-indexed vertex number list
                tri_idxs = [tri.vertex_ids_zero for tri in tris]
                # Extract vertex coordinates
                vert_coords = [vert.data for vert in verts]
                pts = np.array(vert_coords)
                # Create MPL Triangulation object
                triangulation = mpltri.Triangulation(pts[:, 0], pts[:, 1], triangles=tri_idxs)

                # Determine the color or the colormap of the triangulated plot
                trisurf_params = {}
                if surf_cmaps:
                    try:
                        trisurf_params['cmap'] = surf_cmaps[surf_count]
                        surf_count += 1
                    except IndexError:
                        trisurf_params['color'] = plot['color']
                else:
                    trisurf_params['color'] = plot['color']

                # Use custom Triangulation object and the choice of color/colormap to plot the surface
                ax.plot_trisurf(triangulation, pts[:, 2], **trisurf_params)
                plot2_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='^')
                legend_proxy.append(plot2_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self._config.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self._config.display_axes:
            plt.axis('off')

        # Set axes equal
        self._config.set_axes_equal(ax)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if fig_display:
            plt.show()
        else:
            fig_filename = self._config.figure_image_filename if fig_filename is None else fig_filename

        # Save the figure
        self._config.save_figure_as(fig, fig_filename)


class VisSurfScatter(Abstract.VisAbstractSurf):
    """ Matplotlib visualization module for surfaces.

    Wireframe plot for the control points and scatter plot for the surface points.
    """
    def __init__(self, config=VisConfig()):
        super(VisSurfScatter, self).__init__(config=config)

    def render(self, **kwargs):
        """ Plots the surface and the control points grid. """
        # Calling parent function
        super(VisSurfScatter, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self._config.figure_size, dpi=self._config.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                pts = np.array(utilities.make_quad_mesh(plot['ptsarr'], plot['size'][0], plot['size'][1]))
                cp_z = pts[:, 2] + self._ctrlpts_offset
                ax.plot(pts[:, 0], pts[:, 1], cp_z, color=plot['color'], linestyle='-.', marker='o')
                plot1_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot1_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                pts = np.array(plot['ptsarr'])
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], s=50, depthshade=True)
                plot2_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='o')
                legend_proxy.append(plot2_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self._config.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self._config.display_axes:
            plt.axis('off')

        # Set axes equal
        self._config.set_axes_equal(ax)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if fig_display:
            plt.show()
        else:
            fig_filename = self._config.figure_image_filename if fig_filename is None else fig_filename

        # Save the figure
        self._config.save_figure_as(fig, fig_filename)
