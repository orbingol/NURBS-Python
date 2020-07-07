"""
.. module:: VisMPL
    :platform: Unix, Windows
    :synopsis: Matplotlib visualization component for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from geomdl import vis
import numpy as np
import matplotlib as mpl
import matplotlib.tri as mpltri
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation


class VisConfig(vis.VisConfigAbstract):
    """ Configuration class for Matplotlib visualization module.

    This class is only required when you would like to change the visual defaults of the plots and the figure,
    such as hiding control points plot or legend.

    The ``VisMPL`` module has the following configuration variables:

    * ``ctrlpts`` (bool): Control points polygon/grid visibility. *Default: True*
    * ``evalpts`` (bool): Curve/surface points visibility. *Default: True*
    * ``bbox`` (bool): Bounding box visibility. *Default: False*
    * ``legend`` (bool): Figure legend visibility. *Default: True*
    * ``axes`` (bool): Axes and figure grid visibility. *Default: True*
    * ``labels`` (bool): Axis labels visibility. *Default: True*
    * ``trims`` (bool): Trim curves visibility. *Default: True*
    * ``axes_equal`` (bool): Enables or disables equal aspect ratio for the axes. *Default: True*
    * ``figure_size`` (list): Size of the figure in (x, y). *Default: [10, 8]*
    * ``figure_dpi`` (int): Resolution of the figure in DPI. *Default: 96*
    * ``trim_size`` (int): Size of the trim curves. *Default: 20*
    * ``alpha`` (float): Opacity of the evaluated points. *Default: 1.0*

    There is also a ``debug`` configuration variable which currently adds quiver plots to 2-dimensional curves to show
    their directions.

    The following example illustrates the usage of the configuration class.

    .. code-block:: python
        :linenos:

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

    Please refer to the **Examples Repository** for more details.
    """

    def __init__(self, **kwargs):
        super(VisConfig, self).__init__(**kwargs)
        self.dtype = np.float
        self.display_ctrlpts = kwargs.get('ctrlpts', True)
        self.display_evalpts = kwargs.get('evalpts', True)
        self.display_bbox = kwargs.get('bbox', False)
        self.display_legend = kwargs.get('legend', True)
        self.display_axes = kwargs.get('axes', True)
        self.display_labels = kwargs.get('labels', True)
        self.display_trims = kwargs.get('trims', True)
        self.axes_equal = kwargs.get('axes_equal', True)
        self.figure_size = kwargs.get('figure_size', [10, 8])
        self.figure_dpi = kwargs.get('figure_dpi', 96)
        self.trim_size = kwargs.get('trim_size', 20)
        self.alpha = kwargs.get('alpha', 1.0)
        self.figure_image_filename = "temp-figure.png"
        self.debug_mode = kwargs.get('debug', False)  # debugging mode for determining the trim directions

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

    def is_notebook(self):
        """ Detects if Jupyter notebook GUI toolkit is active

        return: True if the module is running inside a Jupyter notebook
        rtype: bool
        """
        return True if "nbAgg" == mpl.get_backend() else False


class VisCurve2D(vis.VisAbstract):
    """ Matplotlib visualization module for 2D curves """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisCurve2D, self).__init__(config, **kwargs)

    def render(self, **kwargs):
        """ Plots the 2D curve and the control points polygon. """
        # Calling parent function
        super(VisCurve2D, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Draw control points polygon and the curve
        fig = plt.figure(figsize=self.vconf.figure_size, dpi=self.vconf.figure_dpi)
        ax = fig.gca()

        # Start plotting
        for plot in self._plots:
            pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                cpplot, = plt.plot(pts[:, 0], pts[:, 1], color=plot['color'], linestyle='-.', marker='o')
                legend_proxy.append(cpplot)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                curveplt, = plt.plot(pts[:, 0], pts[:, 1], color=plot['color'], linestyle='-', alpha=self.vconf.alpha)
                legend_proxy.append(curveplt)
                legend_names.append(plot['name'])
                # Debugging for curve directions
                if self.vconf.debug_mode:
                    plt.quiver(pts[0, 0], pts[0, 1], pts[-1, 0] - pts[0, 0], pts[-1, 1] - pts[0, 1],
                               color='k', angles='xy', scale_units='xy', scale=1, width=0.003)

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                bboxplt, = plt.plot(pts[:, 0], pts[:, 1], color=plot['color'], linestyle='--')
                legend_proxy.append(bboxplt)
                legend_names.append(plot['name'])

            # Plot extras
            if plot['type'] == 'extras':
                extrasplt, = plt.plot(pts[:, 0], pts[:, 1],
                                      color=plot['color'][0], linestyle='-', linewidth=plot['color'][1])
                legend_proxy.append(extrasplt)
                legend_names.append(plot['name'])

        # Add legend
        if self.vconf.display_legend:
            plt.legend(legend_proxy, legend_names)

        # Remove axes
        if not self.vconf.display_axes:
            plt.axis('off')

        # Set aspect ratio
        if self.vconf.axes_equal:
            ax.set_aspect('equal')

        # Axis labels
        if self.vconf.display_labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Check if running inside a Jupyter notebook
        if not self.vconf.is_notebook():
            # Display the plot or save the figure
            if fig_display:
                plt.show()
            else:
                fig_filename = self.vconf.figure_image_filename if fig_filename is None else fig_filename
                self.vconf.save_figure_as(fig, fig_filename)


class VisCurve3D(vis.VisAbstract):
    """ Matplotlib visualization module for 3D curves. """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisCurve3D, self).__init__(config, **kwargs)

    def render(self, **kwargs):
        """ Plots the 3D curve and the control points polygon. """
        # Calling parent function
        super(VisCurve3D, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Draw control points polygon and the 3D curve
        fig = plt.figure(figsize=self.vconf.figure_size, dpi=self.vconf.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)

            # Try not to fail if the input is 2D
            if pts.shape[1] == 2:
                pts = np.c_[pts, np.zeros(pts.shape[0])]

            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='-.', marker='o')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='-', alpha=self.vconf.alpha)
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='--')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='--', color=plot['color'])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot extras
            if plot['type'] == 'extras':
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                        color=plot['color'][0], linestyle='-', linewidth=plot['color'][1])
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'][0])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self.vconf.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self.vconf.display_axes:
            plt.axis('off')

        # Set axes equal
        if self.vconf.axes_equal:
            self.vconf.set_axes_equal(ax)

        # Axis labels
        if self.vconf.display_labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Check if running inside a Jupyter notebook
        if not self.vconf.is_notebook():
            # Display the plot or save the figure
            if fig_display:
                plt.show()
            else:
                fig_filename = self.vconf.figure_image_filename if fig_filename is None else fig_filename
                self.vconf.save_figure_as(fig, fig_filename)


class VisSurface(vis.VisAbstract):
    """ Matplotlib visualization module for surfaces.

    Wireframe plot for the control points and triangulated plot (using ``plot_trisurf``) for the surface points.
    The surface is triangulated externally using :py:func:`.utilities.make_triangle_mesh()` function.
    """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisSurface, self).__init__(config, **kwargs)
        self._module_config['ctrlpts'] = "quads"
        self._module_config['evalpts'] = "triangles"

    def animate(self, **kwargs):
        """ Animates the surface.

        This function only animates the triangulated surface. There will be no other elements, such as control points
        grid or bounding box.

        Keyword arguments:
            * ``colormap``: applies colormap to the surface

        Colormaps are a visualization feature of Matplotlib. They can be used for several types of surface plots via
        the following import statement: ``from matplotlib import cm``

        The following link displays the list of Matplolib colormaps and some examples on colormaps:
        https://matplotlib.org/tutorials/colors/colormaps.html
        """
        # Calling parent render function
        super(VisSurface, self).render(**kwargs)

        # Colormaps
        surf_cmaps = kwargs.get('colormap', None)

        # Initialize variables
        tri_idxs = []
        vert_coords = []
        trisurf_params = []
        frames = []
        frames_tris = []
        num_vertices = 0

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self.vconf.figure_size, dpi=self.vconf.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        surf_count = 0
        for plot in self._plots:
            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                # Use internal triangulation algorithm instead of Qhull (MPL default)
                verts = plot['ptsarr'][0]
                tris = plot['ptsarr'][1]
                # Extract zero-indexed vertex number list
                tri_idxs += [[ti + num_vertices for ti in tri.data] for tri in tris]
                # Extract vertex coordinates
                vert_coords += [vert.data for vert in verts]
                # Update number of vertices
                num_vertices = len(vert_coords)

                # Determine the color or the colormap of the triangulated plot
                params = {}
                if surf_cmaps:
                    try:
                        params['cmap'] = surf_cmaps[surf_count]
                        surf_count += 1
                    except IndexError:
                        params['color'] = plot['color']
                else:
                    params['color'] = plot['color']
                trisurf_params += [params for _ in range(len(tris))]

        # Pre-processing for the animation
        pts = np.array(vert_coords, dtype=self.vconf.dtype)

        # Create the frames (Artists)
        for tidx, pidx in zip(tri_idxs, trisurf_params):
            frames_tris.append(tidx)
            # Create MPL Triangulation object
            triangulation = mpltri.Triangulation(pts[:, 0], pts[:, 1], triangles=frames_tris)
            # Use custom Triangulation object and the choice of color/colormap to plot the surface
            p3df = ax.plot_trisurf(triangulation, pts[:, 2], alpha=self.vconf.alpha, **pidx)
            # Add to frames list
            frames.append([p3df])

        # Create MPL ArtistAnimation
        ani = animation.ArtistAnimation(fig, frames, interval=100, blit=True, repeat_delay=1000)

        # Remove axes
        if not self.vconf.display_axes:
            plt.axis('off')

        # Set axes equal
        if self.vconf.axes_equal:
            self.vconf.set_axes_equal(ax)

        # Axis labels
        if self.vconf.display_labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Check if running inside a Jupyter notebook
        if not self.vconf.is_notebook():
            # Display the plot or save the figure
            if fig_display:
                plt.show()
            else:
                fig_filename = self.vconf.figure_image_filename if fig_filename is None else fig_filename
                self.vconf.save_figure_as(fig, fig_filename)


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
        super(VisSurface, self).render(**kwargs)

        # Colormaps
        surf_cmaps = kwargs.get('colormap', None)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self.vconf.figure_size, dpi=self.vconf.figure_dpi)
        ax = Axes3D(fig)

        surf_count = 0
        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                vertices = [v.data for v in plot['ptsarr'][0]]
                faces = [q.data for q in plot['ptsarr'][1]]
                for q in faces:
                    el = np.array([vertices[i] for i in q], dtype=self.vconf.dtype)
                    el[:, 2] += self._ctrlpts_offset
                    pc3d = Poly3DCollection([el], alpha=0.0, edgecolors=plot['color'], linewidths=1.0, linestyles='-.')
                    pc3d.set_facecolor(None)
                    ax.add_collection3d(pc3d)
                pts = np.array(vertices, dtype=self.vconf.dtype)
                pts[:, 2] += self._ctrlpts_offset
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='-.', marker='o')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                # Use internal triangulation algorithm instead of Qhull (MPL default)
                verts = plot['ptsarr'][0]
                tris = plot['ptsarr'][1]
                # Extract zero-indexed vertex number list
                tri_idxs = [tri.data for tri in tris]
                # Extract vertex coordinates
                vert_coords = [vert.data for vert in verts]
                pts = np.array(vert_coords, dtype=self.vconf.dtype)

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

                # Create MPL Triangulation object
                if pts.size != 0:
                    triangulation = mpltri.Triangulation(pts[:, 0], pts[:, 1], triangles=tri_idxs)
                    # Use custom Triangulation object and the choice of color/colormap to plot the surface
                    ax.plot_trisurf(triangulation, pts[:, 2], alpha=self.vconf.alpha, **trisurf_params)
                    # Add to legend
                    plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='^')
                    legend_proxy.append(plot_proxy)
                    legend_names.append(plot['name'])

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='--')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='--', color=plot['color'])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot trim curves
            if self.vconf.display_trims:
                if plot['type'] == 'trimcurve':
                    pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], marker='o',
                               s=self.vconf.trim_size, depthshade=False)
                    plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='o')
                    legend_proxy.append(plot_proxy)
                    legend_names.append(plot['name'])

            # Plot extras
            if plot['type'] == 'extras':
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                        color=plot['color'][0], linestyle='-', linewidth=plot['color'][1])
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'][0])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self.vconf.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self.vconf.display_axes:
            plt.axis('off')

        # Set axes equal
        if self.vconf.axes_equal:
            self.vconf.set_axes_equal(ax)

        # Axis labels
        if self.vconf.display_labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Check if running inside a Jupyter notebook
        if not self.vconf.is_notebook():
            # Display the plot or save the figure
            if fig_display:
                plt.show()
            else:
                fig_filename = self.vconf.figure_image_filename if fig_filename is None else fig_filename
                self.vconf.save_figure_as(fig, fig_filename)


class VisSurfWireframe(vis.VisAbstract):
    """ Matplotlib visualization module for surfaces.

    Scatter plot for the control points and wireframe plot for the surface points.
    """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisSurfWireframe, self).__init__(config, **kwargs)
        self._module_config['ctrlpts'] = "points"
        self._module_config['evalpts'] = "quads"

    def render(self, **kwargs):
        """ Plots the surface and the control points grid. """
        # Calling parent function
        super(VisSurfWireframe, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self.vconf.figure_size, dpi=self.vconf.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                cp_z = pts[:, 2] + self._ctrlpts_offset
                ax.scatter(pts[:, 0], pts[:, 1], cp_z, color=plot['color'], s=25, depthshade=True)
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                vertices = [v.data for v in plot['ptsarr'][0]]
                faces = [q.data for q in plot['ptsarr'][1]]
                for q in faces:
                    el = np.array([vertices[i] for i in q], dtype=self.vconf.dtype)
                    el[:, 2] += self._ctrlpts_offset
                    pc3d = Poly3DCollection([el], alpha=0.0, edgecolors=plot['color'], linewidths=0.5, linestyles='-')
                    pc3d.set_facecolor(None)
                    ax.add_collection3d(pc3d)
                pts = np.array(vertices, dtype=self.vconf.dtype)
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], s=5)
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='--')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='--', color=plot['color'])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot trim curves
            if self.vconf.display_trims:
                if plot['type'] == 'trimcurve':
                    pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], marker='o',
                               s=self.vconf.trim_size, depthshade=False)
                    plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='o')
                    legend_proxy.append(plot_proxy)
                    legend_names.append(plot['name'])

            # Plot extras
            if plot['type'] == 'extras':
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                        color=plot['color'][0], linestyle='-', linewidth=plot['color'][1])
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'][0])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self.vconf.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self.vconf.display_axes:
            plt.axis('off')

        # Set axes equal
        if self.vconf.axes_equal:
            self.vconf.set_axes_equal(ax)

        # Axis labels
        if self.vconf.display_labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Check if running inside a Jupyter notebook
        if not self.vconf.is_notebook():
            # Display the plot or save the figure
            if fig_display:
                plt.show()
            else:
                fig_filename = self.vconf.figure_image_filename if fig_filename is None else fig_filename
                self.vconf.save_figure_as(fig, fig_filename)


class VisSurfScatter(vis.VisAbstract):
    """ Matplotlib visualization module for surfaces.

    Wireframe plot for the control points and scatter plot for the surface points.
    """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisSurfScatter, self).__init__(config, **kwargs)
        self._module_config['ctrlpts'] = "quads"
        self._module_config['evalpts'] = "points"

    def render(self, **kwargs):
        """ Plots the surface and the control points grid. """
        # Calling parent function
        super(VisSurfScatter, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self.vconf.figure_size, dpi=self.vconf.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                vertices = [v.data for v in plot['ptsarr'][0]]
                faces = [q.data for q in plot['ptsarr'][1]]
                for q in faces:
                    el = np.array([vertices[i] for i in q], dtype=self.vconf.dtype)
                    el[:, 2] += self._ctrlpts_offset
                    pc3d = Poly3DCollection([el], alpha=0.0, edgecolors=plot['color'], linewidths=1.0, linestyles='-.')
                    pc3d.set_facecolor(None)
                    ax.add_collection3d(pc3d)
                pts = np.array(vertices, dtype=self.vconf.dtype)
                pts[:, 2] += self._ctrlpts_offset
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='-.', marker='o')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-.', color=plot['color'], marker='o')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2],
                           color=plot['color'], s=50, depthshade=True, alpha=self.vconf.alpha)
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='o')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='--')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='--', color=plot['color'])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot trim curves
            if self.vconf.display_trims:
                if plot['type'] == 'trimcurve':
                    pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], marker='o',
                               s=self.vconf.trim_size, depthshade=False)
                    plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='o')
                    legend_proxy.append(plot_proxy)
                    legend_names.append(plot['name'])

            # Plot extras
            if plot['type'] == 'extras':
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                        color=plot['color'][0], linestyle='-', linewidth=plot['color'][1])
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'][0])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self.vconf.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self.vconf.display_axes:
            plt.axis('off')

        # Set axes equal
        if self.vconf.axes_equal:
            self.vconf.set_axes_equal(ax)

        # Axis labels
        if self.vconf.display_labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Check if running inside a Jupyter notebook
        if not self.vconf.is_notebook():
            # Display the plot or save the figure
            if fig_display:
                plt.show()
            else:
                fig_filename = self.vconf.figure_image_filename if fig_filename is None else fig_filename
                self.vconf.save_figure_as(fig, fig_filename)


class VisVolume(vis.VisAbstract):
    """ Matplotlib visualization module for volumes. """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisVolume, self).__init__(config, **kwargs)
        self._module_config['ctrlpts'] = "points"
        self._module_config['evalpts'] = "points"

    def render(self, **kwargs):
        """ Plots the volume and the control points. """
        # Calling parent function
        super(VisVolume, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self.vconf.figure_size, dpi=self.vconf.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], marker='^', s=20, depthshade=True)
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='^')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2],
                           color=plot['color'], marker='o', s=10, depthshade=True, alpha=self.vconf.alpha)
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='o')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='--')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='--', color=plot['color'])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot extras
            if plot['type'] == 'extras':
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                        color=plot['color'][0], linestyle='-', linewidth=plot['color'][1])
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'][0])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self.vconf.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self.vconf.display_axes:
            plt.axis('off')

        # Set axes equal
        if self.vconf.axes_equal:
            self.vconf.set_axes_equal(ax)

        # Axis labels
        if self.vconf.display_labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Check if running inside a Jupyter notebook
        if not self.vconf.is_notebook():
            # Display the plot or save the figure
            if fig_display:
                plt.show()
            else:
                fig_filename = self.vconf.figure_image_filename if fig_filename is None else fig_filename
                self.vconf.save_figure_as(fig, fig_filename)


class VisVoxel(vis.VisAbstract):
    """ Matplotlib visualization module for voxel representation of the volumes. """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisVoxel, self).__init__(config, **kwargs)
        self._module_config['ctrlpts'] = "points"
        self._module_config['evalpts'] = "voxels"

    def render(self, **kwargs):
        """ Displays the voxels and the control points. """
        # Calling parent function
        super(VisVoxel, self).render(**kwargs)

        # Initialize variables
        legend_proxy = []
        legend_names = []

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=self.vconf.figure_size, dpi=self.vconf.figure_dpi)
        ax = Axes3D(fig)

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], marker='^', s=20, depthshade=True)
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='^')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                faces = np.array(plot['ptsarr'][1], dtype=self.vconf.dtype)
                filled = np.array(plot['ptsarr'][2], dtype=self.vconf.dtype)
                # Find filled voxels
                faces_filled = np.concatenate(faces[filled == 1.0])
                # Create a single Poly3DCollection object
                pc3d = Poly3DCollection(faces_filled, facecolors=plot['color'], edgecolors='k')
                ax.add_collection3d(pc3d)
                # Set axis limits
                gf_min = np.amin(faces_filled, axis=(0, 1))
                gf_max = np.amax(faces_filled, axis=(0, 1))
                ax.set_xlim([gf_min[0], gf_max[0]])
                ax.set_ylim([gf_min[1], gf_max[1]])
                ax.set_zlim([gf_min[2], gf_max[2]])
                # Legend
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='none', color=plot['color'], marker='o')
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=plot['color'], linestyle='--')
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='--', color=plot['color'])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

            # Plot extras
            if plot['type'] == 'extras':
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                        color=plot['color'][0], linestyle='-', linewidth=plot['color'][1])
                plot_proxy = mpl.lines.Line2D([0], [0], linestyle='-', color=plot['color'][0])
                legend_proxy.append(plot_proxy)
                legend_names.append(plot['name'])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        if self.vconf.display_legend:
            ax.legend(legend_proxy, legend_names, numpoints=1)

        # Remove axes
        if not self.vconf.display_axes:
            plt.axis('off')

        # Set axes equal
        if self.vconf.axes_equal:
            self.vconf.set_axes_equal(ax)

        # Axis labels
        if self.vconf.display_labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Check if running inside a Jupyter notebook
        if not self.vconf.is_notebook():
            # Display the plot or save the figure
            if fig_display:
                plt.show()
            else:
                fig_filename = self.vconf.figure_image_filename if fig_filename is None else fig_filename
                self.vconf.save_figure_as(fig, fig_filename)
