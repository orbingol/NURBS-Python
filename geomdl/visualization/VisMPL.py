"""
.. module:: VisMPL
    :platform: Unix, Windows
    :synopsis: Matplotlib visualization component for NURBS-Python (experimental)

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from .VisBase import VisAbstract, VisAbstractSurf
from geomdl import utilities as utils

import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class VisCurve2D(VisAbstract):
    """ Visualization module for 2D Curves """
    def __init__(self, plot_ctrlpts=True):
        super(VisCurve2D, self).__init__(plot_ctrlpts)

    def render(self):
        """ Plots the 2D curve and the control points polygon """
        if not self._points:
            return False

        cpts = np.array(self._points[0])
        crvpts = np.array(self._points[1])

        legend_proxy = []
        legend_names = []

        # Draw control points polygon and the curve
        plt.figure(figsize=(10.67, 8), dpi=96)
        if self._plot_ctrlpts:
            cppolygon, = plt.plot(cpts[:, 0], cpts[:, 1], color=self._colors[0], linestyle='-.', marker='o')
            legend_proxy.append(cppolygon)
            legend_names.append(self._names[0])

        curveplt, = plt.plot(crvpts[:, 0], crvpts[:, 1], color=self._colors[1], linestyle='-')
        legend_proxy.append(curveplt)
        legend_names.append(self._names[1])

        # Add legend
        plt.legend(legend_proxy, legend_names)

        # Display 2D plot
        plt.show()


class VisCurve3D(VisAbstract):
    """ Visualization module for 3D Curves """
    def __init__(self, plot_ctrlpts=True):
        super(VisCurve3D, self).__init__(plot_ctrlpts)

    def render(self):
        """ Plots the 3D curve and the control points polygon """
        if not self._points:
            return False

        cpts = np.array(self._points[0])
        crvpts = np.array(self._points[1])

        # Draw control points polygon and the 3D curve
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = Axes3D(fig)

        legend_proxy = []
        legend_names = []

        # Plot 3D lines
        if self._plot_ctrlpts:
            ax.plot(cpts[:, 0], cpts[:, 1], cpts[:, 2], color=self._colors[0], linestyle='-.', marker='o')
            plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
            legend_proxy.append(plot1_proxy)
            legend_names.append(self._names[0])

        ax.plot(crvpts[:, 0], crvpts[:, 1], crvpts[:, 2], color=self._colors[1], linestyle='-')
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='^')
        legend_proxy.append(plot2_proxy)
        legend_names.append(self._names[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        ax.legend(legend_proxy, legend_names, numpoints=1)

        # Display the 3D plot
        plt.show()


class VisSurface(VisAbstractSurf):
    """ Visualization module for Surfaces

    Triangular mesh plot for the surface and wireframe plot for the control points grid
    """
    def __init__(self, plot_ctrlpts=True):
        super(VisSurface, self).__init__(plot_ctrlpts)

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._points:
            return False

        cpgrid = np.array(utils.make_quad(self._points[0], self._sizes[0][1], self._sizes[0][0]))
        surf = np.array(utils.make_triangle(self._points[1], self._sizes[1][1], self._sizes[1][0]))

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = Axes3D(fig)

        legend_proxy = []
        legend_names = []

        # Draw control points grid
        if self._plot_ctrlpts:
            cp_z = cpgrid[:, 2] + self._ctrlpts_offset
            ax.plot(cpgrid[:, 0], cpgrid[:, 1], cp_z, color=self._colors[0], linestyle='-.', marker='o')
            plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
            legend_proxy.append(plot1_proxy)
            legend_names.append(self._names[0])

        # Draw surface plot
        ax.plot(surf[:, 0], surf[:, 1], surf[:, 2], color=self._colors[1])
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='^')
        legend_proxy.append(plot2_proxy)
        legend_names.append(self._names[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        ax.legend(legend_proxy, legend_names, numpoints=1)

        # Display the 3D plot
        plt.show()


class VisSurfWireframe(VisAbstractSurf):
    """ Visualization module for Surfaces

    Scatter plot for the control points and wireframe for the surface points
    """
    def __init__(self, plot_ctrlpts=True):
        super(VisSurfWireframe, self).__init__(plot_ctrlpts)

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._points:
            return False

        cpgrid = np.array(self._points[0])
        surf = np.array(utils.make_quad(self._points[1], self._sizes[1][1], self._sizes[1][0]))

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = Axes3D(fig)

        legend_proxy = []
        legend_names = []

        # Plot control points
        if self._plot_ctrlpts:
            cp_z = cpgrid[:, 2] + self._ctrlpts_offset
            ax.scatter(cpgrid[:, 0], cpgrid[:, 1], cp_z, color=self._colors[0], s=25, depthshade=True)
            plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
            legend_proxy.append(plot1_proxy)
            legend_names.append(self._names[0])

        # Plot surface wireframe plot
        ax.plot(surf[:, 0], surf[:, 1], surf[:, 2], color=self._colors[1])
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='^')
        legend_proxy.append(plot2_proxy)
        legend_names.append(self._names[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        ax.legend(legend_proxy, legend_names, numpoints=1)

        # Display the 3D plot
        plt.show()


class VisSurfTriangle(VisAbstractSurf):
    """ Visualization module for Surfaces

    Wireframe plot for the control points and triangulated plot for the surface points
    """
    def __init__(self, plot_ctrlpts=True):
        super(VisSurfTriangle, self).__init__(plot_ctrlpts)

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._points:
            return False

        cpgrid = np.array(utils.make_quad(self._points[0], self._sizes[0][1], self._sizes[0][0]))
        surf = np.array(self._points[1])

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = Axes3D(fig)

        legend_proxy = []
        legend_names = []

        # Draw control points grid
        if self._plot_ctrlpts:
            cp_z = cpgrid[:, 2] + self._ctrlpts_offset
            ax.plot(cpgrid[:, 0], cpgrid[:, 1], cp_z, color=self._colors[0], linestyle='-.', marker='o')
            plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
            legend_proxy.append(plot1_proxy)
            legend_names.append(self._names[0])

        # Draw surface plot
        ax.plot_trisurf(surf[:, 0], surf[:, 1], surf[:, 2], color=self._colors[1])
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='^')
        legend_proxy.append(plot2_proxy)
        legend_names.append(self._names[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        ax.legend(legend_proxy, legend_names, numpoints=1)

        # Display the 3D plot
        plt.show()


class VisSurfScatter(VisAbstractSurf):
    """ Visualization module for Surfaces

    Wireframe plot for the control points and scatter plot for the surface points
    """
    def __init__(self, plot_ctrlpts=True):
        super(VisSurfScatter, self).__init__(plot_ctrlpts)

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._points:
            return False

        cpgrid = np.array(utils.make_quad(self._points[0], self._sizes[0][1], self._sizes[0][0]))
        surf = np.array(self._points[1])

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = Axes3D(fig)

        legend_proxy = []
        legend_names = []

        # Draw control points grid
        if self._plot_ctrlpts:
            cp_z = cpgrid[:, 2] + self._ctrlpts_offset
            ax.plot(cpgrid[:, 0], cpgrid[:, 1], cp_z, color=self._colors[0], linestyle='-.', marker='o')
            plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
            legend_proxy.append(plot1_proxy)
            legend_names.append(self._names[0])

        # Draw surface points scatter plot
        ax.scatter(surf[:, 0], surf[:, 1], surf[:, 2], color=self._colors[1], s=50, depthshade=True)
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='o')
        legend_proxy.append(plot2_proxy)
        legend_names.append(self._names[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        ax.legend(legend_proxy, legend_names, numpoints=1)

        # Display the 3D plot
        plt.show()
