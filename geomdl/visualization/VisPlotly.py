"""
.. module:: VisPlotly
    :platform: Unix, Windows
    :synopsis: Plotly visualization component for NURBS-Python (experimental)

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import Abstract
from . import utilities

from . import numpy as np
import plotly
from plotly import graph_objs


class VisConfig(Abstract.VisConfigAbstract):
    def __init__(self, **kwargs):
        super(VisConfig, self).__init__(**kwargs)
        self.display_ctrlpts = kwargs.get('ctrlpts', True)
        self.figure_size = kwargs.get('figure_size', [800, 800])
        self.display_legend = kwargs.get('legend', True)
        self.line_width = kwargs.get('linewidth', 2)


class VisCurve2D(Abstract.VisAbstract):
    """ Plotly visualization module for 2D Curves """
    def __init__(self, config=VisConfig()):
        super(VisCurve2D, self).__init__(config=config)

    def render(self):
        if not self._plots:
            return

        plot_data = []
        for plot in self._plots:
            pts = np.array(plot['ptsarr'])

            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                figure = graph_objs.Scatter(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    name=plot['name'],
                    mode='lines+markers',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width,
                        dash='dashdot'
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                figure = graph_objs.Scatter(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width
                    )
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self._config.figure_size[0],
            height=self._config.figure_size[1],
            autosize=False,
            showlegend=self._config.display_legend,
            yaxis=dict(
                scaleanchor="x",
            )
        )

        plotly.offline.plot({
            "data": plot_data,
            "layout": plot_layout
        }, show_link=False)


class VisCurve3D(Abstract.VisAbstract):
    """ Plotly visualization module for 3D Curves """
    def __init__(self, config=VisConfig()):
        super(VisCurve3D, self).__init__(config=config)

    def render(self):
        if not self._plots:
            return

        plot_data = []
        for plot in self._plots:
            pts = np.array(plot['ptsarr'])

            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines+markers',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width,
                        dash='dashdot'
                    ),
                    marker=dict(
                        color=plot['color'],
                        size=self._config.line_width
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width
                    ),
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self._config.figure_size[0],
            height=self._config.figure_size[1],
            autosize=False,
            showlegend=self._config.display_legend
        )

        plotly.offline.plot({
            "data": plot_data,
            "layout": plot_layout
        }, show_link=False)


class VisSurface(Abstract.VisAbstractSurf):
    """ Plotly visualization module for Surfaces """
    def __init__(self, config=VisConfig()):
        super(VisSurface, self).__init__(config=config)

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._plots:
            return

        plot_data = []
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                pts = np.array(utilities.make_quad(plot['ptsarr'], plot['size'][1], plot['size'][0]))
                cp_z = pts[:, 2] + self._ctrlpts_offset
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=cp_z,
                    name=plot['name'],
                    mode='lines+markers',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width,
                        dash='solid'
                    ),
                    marker=dict(
                        color=plot['color'],
                        size=self._config.line_width
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                pts = np.array(utilities.make_triangle(plot['ptsarr'], plot['size'][1], plot['size'][0]))
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width
                    ),
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self._config.figure_size[0],
            height=self._config.figure_size[1],
            autosize=False,
            showlegend=self._config.display_legend
        )

        plotly.offline.plot({
            "data": plot_data,
            "layout": plot_layout
        }, show_link=False)
