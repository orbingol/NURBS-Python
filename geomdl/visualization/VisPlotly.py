"""
.. module:: VisPlotly
    :platform: Unix, Windows
    :synopsis: Plotly visualization component for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import sys
from . import vis
import numpy as np
from plotly import graph_objs


class VisConfig(vis.VisConfigAbstract):
    """ Configuration class for Plotly visualization module.

    This class is only required when you would like to change the visual defaults of the plots and the figure,
    such as hiding control points plot or legend.

    The ``VisPlotly`` module has the following configuration variables:

    * ``ctrlpts`` (bool): Control points polygon/grid visibility. *Default: True*
    * ``evalpts`` (bool): Curve/surface points visibility. *Default: True*
    * ``bbox`` (bool): Bounding box visibility. *Default: False*
    * ``legend`` (bool): Figure legend visibility. *Default: True*
    * ``axes`` (bool): Axes and figure grid visibility. *Default: True*
    * ``trims`` (bool): Trim curves visibility. *Default: True*
    * ``axes_equal`` (bool): Enables or disables equal aspect ratio for the axes. *Default: True*
    * ``line_width`` (int): Thickness of the lines on the figure. *Default: 2*
    * ``figure_size`` (list): Size of the figure in (x, y). *Default: [800, 600]*
    * ``trim_size`` (int): Size of the trim curves. *Default: 20*

    The following example illustrates the usage of the configuration class.

    .. code-block:: python
        :linenos:

        # Create a surface (or a curve) instance
        surf = NURBS.Surface()

        # Skipping degree, knot vector and control points assignments

        # Create a visualization configuration instance with no legend, no axes and no control points grid
        vis_config = VisPlotly.VisConfig(legend=False, axes=False, ctrlpts=False)

        # Create a visualization method instance using the configuration above
        vis_obj = VisPlotly.VisSurface(vis_config)

        # Set the visualization method of the surface object
        surf.vis = vis_obj

        # Plot the surface
        surf.render()

    Please refer to the **Examples Repository** for more details.
    """
    def __init__(self, **kwargs):
        super(VisConfig, self).__init__(**kwargs)
        self.dtype = np.float
        # Set Plotly custom variables
        self.figure_image_filename = "temp-plot.html"
        self.use_renderer = kwargs.get("use_renderer", False)

        # Get keyword arguments
        self.display_ctrlpts = kwargs.get('ctrlpts', True)
        self.display_evalpts = kwargs.get('evalpts', True)
        self.display_bbox = kwargs.get('bbox', False)
        self.display_trims = kwargs.get('trims', True)
        self.display_legend = kwargs.get('legend', True)
        self.display_axes = kwargs.get('axes', True)
        self.axes_equal = kwargs.get('axes_equal', True)
        self.figure_size = kwargs.get('figure_size', [1024, 768])
        self.trim_size = kwargs.get('trim_size', 1)
        self.line_width = kwargs.get('line_width', 2)

    # https://stackoverflow.com/a/37661854/3345747
    def in_notebook(self):
        return 'ipykernel' in sys.modules


class VisCurve2D(vis.VisAbstract):
    """ Plotly visualization module for 2D curves. """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisCurve2D, self).__init__(config, **kwargs)

    def render(self, **kwargs):
        """ Plots the curve and the control points polygon. """
        # Calling parent function
        super(VisCurve2D, self).render(**kwargs)

        # Initialize variables
        plot_data = []

        for plot in self._plots:
            pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)

            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                figure = graph_objs.Scatter(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    name=plot['name'],
                    mode='lines+markers',
                    line=dict(
                        color=plot['color'],
                        width=self.vconf.line_width,
                        dash='dash'
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                figure = graph_objs.Scatter(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self.vconf.line_width
                    )
                )
                plot_data.append(figure)

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                figure = graph_objs.Scatter(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    name=plot['name'],
                    line=dict(
                        color=plot['color'],
                        width=self.vconf.line_width,
                        dash='dashdot',
                    )
                )
                plot_data.append(figure)

            # Plot extras
            if plot['type'] == 'extras':
                figure = graph_objs.Scatter(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    name=plot['name'],
                    mode='markers',
                    marker=dict(
                        color=plot['color'][0],
                        size=plot['color'][1],
                        line=dict(
                            width=self.vconf.line_width
                        )
                    )
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self.vconf.figure_size[0],
            height=self.vconf.figure_size[1],
            autosize=False,
            showlegend=self.vconf.display_legend,
            yaxis=dict(
                scaleanchor="x",
                showgrid=self.vconf.display_axes,
                showline=self.vconf.display_axes,
                zeroline=self.vconf.display_axes,
                showticklabels=self.vconf.display_axes,
            ),
            xaxis=dict(
                showgrid=self.vconf.display_axes,
                showline=self.vconf.display_axes,
                zeroline=self.vconf.display_axes,
                showticklabels=self.vconf.display_axes,
            )
        )

        # Generate the figure
        fig = graph_objs.Figure(data=plot_data, layout=plot_layout)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if self.vconf.in_notebook() or self.vconf.use_renderer:
            fig.show()
        elif fig_display:
            fig.write_html(file=self.vconf.figure_image_filename if fig_filename is None else fig_filename)
        else:
            fig.write_image(file=self.vconf.figure_image_filename if fig_filename is None else fig_filename)


class VisCurve3D(vis.VisAbstract):
    """ Plotly visualization module for 3D curves. """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisCurve3D, self).__init__(config, **kwargs)

    def render(self, **kwargs):
        """ Plots the curve and the control points polygon. """
        # Calling parent function
        super(VisCurve3D, self).render(**kwargs)

        # Initialize variables
        plot_data = []

        for plot in self._plots:
            pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)

            # Try not to fail if the input is 2D
            if pts.shape[1] == 2:
                pts = np.c_[pts, np.zeros(pts.shape[0])]

            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines+markers',
                    line=dict(
                        color=plot['color'],
                        width=self.vconf.line_width,
                        dash='dash'
                    ),
                    marker=dict(
                        color=plot['color'],
                        size=self.vconf.line_width * 2,
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self.vconf.line_width
                    ),
                )
                plot_data.append(figure)

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self.vconf.line_width,
                        dash='dashdot',
                    ),
                )
                plot_data.append(figure)

            # Plot extras
            if plot['type'] == 'extras':
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='markers',
                    marker=dict(
                        color=plot['color'][0],
                        size=plot['color'][1],
                        line=dict(
                            width=self.vconf.line_width
                        )
                    )
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self.vconf.figure_size[0],
            height=self.vconf.figure_size[1],
            autosize=False,
            showlegend=self.vconf.display_legend,
            scene=dict(
                xaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
                yaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
                zaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
            ),
        )

        # Set aspect ratio
        if self.vconf.axes_equal:
            plot_layout['scene']['aspectmode'] = 'data'

        # Generate the figure
        fig = graph_objs.Figure(data=plot_data, layout=plot_layout)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if self.vconf.in_notebook() or self.vconf.use_renderer:
            fig.show()
        elif fig_display:
            fig.write_html(file=self.vconf.figure_image_filename if fig_filename is None else fig_filename)
        else:
            fig.write_image(file=self.vconf.figure_image_filename if fig_filename is None else fig_filename)


class VisSurface(vis.VisAbstract):
    """ Plotly visualization module for surfaces.

    Triangular mesh plot for the surface and wireframe plot for the control points grid.
    """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisSurface, self).__init__(config, **kwargs)
        self._module_config['ctrlpts'] = "points"
        self._module_config['evalpts'] = "triangles"

    def render(self, **kwargs):
        """ Plots the surface and the control points grid. """
        # Calling parent function
        super(VisSurface, self).render(**kwargs)

        # Initialize variables
        plot_data = []

        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                pts[:, 2] += self._ctrlpts_offset
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='markers',
                    marker=dict(
                        color=plot['color'],
                        size=self.vconf.line_width * 2,
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                vertices = plot['ptsarr'][0]
                triangles = plot['ptsarr'][1]
                pts = [v.data for v in vertices]
                tri = [t.data for t in triangles]
                pts = np.array(pts, dtype=self.vconf.dtype)
                tri = np.array(tri, dtype=self.vconf.dtype)
                figure = graph_objs.Mesh3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    i=tri[:, 0],
                    j=tri[:, 1],
                    k=tri[:, 2],
                    color=plot['color'],
                    opacity=0.75,
                )
                plot_data.append(figure)

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self.vconf.line_width,
                        dash='dashdot',
                    ),
                )
                plot_data.append(figure)

            # Plot trim curves
            if self.vconf.display_trims:
                if plot['type'] == 'trimcurve':
                    pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                    figure = graph_objs.Scatter3d(
                        x=pts[:, 0],
                        y=pts[:, 1],
                        z=pts[:, 2],
                        name=plot['name'],
                        mode='markers',
                        marker=dict(
                            color=plot['color'],
                            size=self.vconf.trim_size * 2,
                        ),
                    )
                    plot_data.append(figure)

            # Plot extras
            if plot['type'] == 'extras':
                pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='markers',
                    marker=dict(
                        color=plot['color'][0],
                        size=plot['color'][1],
                        line=dict(
                            width=self.vconf.line_width
                        )
                    )
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self.vconf.figure_size[0],
            height=self.vconf.figure_size[1],
            autosize=False,
            showlegend=self.vconf.display_legend,
            scene=dict(
                xaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
                yaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
                zaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
            ),
        )

        # Set aspect ratio
        if self.vconf.axes_equal:
            plot_layout['scene']['aspectmode'] = 'data'

        # Generate the figure
        fig = graph_objs.Figure(data=plot_data, layout=plot_layout)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if self.vconf.in_notebook() or self.vconf.use_renderer:
            fig.show()
        elif fig_display:
            fig.write_html(file=self.vconf.figure_image_filename if fig_filename is None else fig_filename)
        else:
            fig.write_image(file=self.vconf.figure_image_filename if fig_filename is None else fig_filename)


class VisVolume(vis.VisAbstract):
    """ Plotly visualization module for volumes. """
    def __init__(self, config=VisConfig(), **kwargs):
        super(VisVolume, self).__init__(config, **kwargs)
        self._module_config['ctrlpts'] = "points"
        self._module_config['evalpts'] = "points"

    def render(self, **kwargs):
        """ Plots the evaluated and the control points. """
        # Calling parent function
        super(VisVolume, self).render(**kwargs)

        # Initialize variables
        plot_data = []

        for plot in self._plots:
            pts = np.array(plot['ptsarr'], dtype=self.vconf.dtype)
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='markers',
                    marker=dict(
                        color=plot['color'],
                        size=self.vconf.line_width,
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='markers',
                    marker=dict(
                        color=plot['color'],
                        size=self.vconf.line_width * 2,
                    )
                )
                plot_data.append(figure)

            # Plot bounding box
            if plot['type'] == 'bbox' and self.vconf.display_bbox:
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self.vconf.line_width,
                        dash='dashdot',
                    ),
                )
                plot_data.append(figure)

            # Plot extras
            if plot['type'] == 'extras':
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='markers',
                    marker=dict(
                        color=plot['color'][0],
                        size=plot['color'][1],
                        line= dict(
                            width=self.vconf.line_width
                        )
                    )
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self.vconf.figure_size[0],
            height=self.vconf.figure_size[1],
            autosize=False,
            showlegend=self.vconf.display_legend,
            scene=dict(
                xaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
                yaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
                zaxis=dict(
                    showgrid=self.vconf.display_axes,
                    showline=self.vconf.display_axes,
                    zeroline=self.vconf.display_axes,
                    showticklabels=self.vconf.display_axes,
                    title='',
                ),
            ),
        )

        # Set aspect ratio
        if self.vconf.axes_equal:
            plot_layout['scene']['aspectmode'] = 'data'

        # Generate the figure
        fig = graph_objs.Figure(data=plot_data, layout=plot_layout)

        # Process keyword arguments
        fig_filename = kwargs.get('fig_save_as', None)
        fig_display = kwargs.get('display_plot', True)

        # Display the plot
        if self.vconf.in_notebook() or self.vconf.use_renderer:
            fig.show()
        elif fig_display:
            fig.write_html(file=self.vconf.figure_image_filename if fig_filename is None else fig_filename)
        else:
            fig.write_image(file=self.vconf.figure_image_filename if fig_filename is None else fig_filename)
