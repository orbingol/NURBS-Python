"""
.. module:: VisPlotly
    :platform: Unix, Windows
    :synopsis: Plotly visualization component for NURBS-Python (experimental)

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import Abstract

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
            showlegend= self._config.display_legend,
            yaxis=dict(
                scaleanchor="x",
            )
        )

        plotly.offline.plot({
            "data": plot_data,
            "layout": plot_layout
        }, show_link=False)

