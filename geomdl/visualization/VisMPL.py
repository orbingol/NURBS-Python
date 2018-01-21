"""
.. module:: VisMPL
    :platform: Unix, Windows
    :synopsis: Matplotlib visualization component for NURBS-Python (experimental)

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from .VisBase import VisAbstract

import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class VisCurve2D(VisAbstract):
    """ Visualization module for 2D Curves """
    def __init__(self):
        super(VisCurve2D, self).__init__()

    def render(self):
        """ Plots the 2D curve and the control points polygon """
        if not self._points:
            return False

        cpts = np.array(self._points[0])
        crvpts = np.array(self._points[1])

        # Draw control points polygon and the curve
        plt.figure(figsize=(10.67, 8), dpi=96)
        cppolygon, = plt.plot(cpts[:, 0], cpts[:, 1], color=self._colors[0], linestyle='-.', marker='o')
        curveplt, = plt.plot(crvpts[:, 0], crvpts[:, 1], color=self._colors[1], linestyle='-')
        plt.legend([cppolygon, curveplt], [self._names[0], self._names[1]])
        plt.show()


class VisCurve3D(VisAbstract):
    """ Visualization module for 3D Curves """
    def __init__(self):
        super(VisCurve3D, self).__init__()

    def render(self):
        """ Plots the 3D curve and the control points polygon """
        if not self._points:
            return False

        cpts = np.array(self._points[0])
        crvpts = np.array(self._points[1])

        # Draw control points polygon and the 3D curve
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = fig.gca(projection='3d')

        # Plot 3D lines
        ax.plot(cpts[:, 0], cpts[:, 1], cpts[:, 2], color=self._colors[0], linestyle='-.', marker='o')
        ax.plot(crvpts[:, 0], crvpts[:, 1], crvpts[:, 2], color=self._colors[1], linestyle='-')

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='^')
        ax.legend([plot1_proxy, plot2_proxy], [self._names[0], self._names[1]], numpoints=1)

        # Display the 3D plot
        plt.show()


class VisSurfWireframe(VisAbstract):
    """ Visualization module for Surfaces

    Scatter plot for the control points and wireframe for the surface points
    """
    def __init__(self):
        super(VisSurfWireframe, self).__init__()

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._points:
            return False

        cpgrid = np.array(self._points[0])
        surf = np.array(self._points[1])

        # Reshape surface points array for plotting, @ref: https://stackoverflow.com/a/21352257
        cols = surf[:, 0].shape[0]
        Xs = surf[:, 0].reshape(-1, cols)
        Ys = surf[:, 1].reshape(-1, cols)
        Zs = surf[:, 2].reshape(-1, cols)

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = fig.gca(projection='3d')

        # Plot control points
        ax.scatter(cpgrid[:, 0], cpgrid[:, 1], cpgrid[:, 2], color=self._colors[0], s=25, depthshade=True)

        # Plot surface wireframe plot
        ax.plot_wireframe(Xs, Ys, Zs, color=self._colors[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='^')
        ax.legend([plot1_proxy, plot2_proxy], [self._names[0], self._names[1]], numpoints=1)

        # Display the 3D plot
        plt.show()


class VisSurfTriangle(VisAbstract):
    """ Visualization module for Surfaces

    Wireframe plot for the control points and triangulated plot for the surface points
    """
    def __init__(self):
        super(VisSurfTriangle, self).__init__()

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._points:
            return False

        cpgrid = np.array(self._points[0])
        surf = np.array(self._points[1])

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = fig.gca(projection='3d')

        # Draw control points grid
        ax.plot(cpgrid[:, 0], cpgrid[:, 1], cpgrid[:, 2], color=self._colors[0], linestyle='-.', marker='o')

        # Draw surface plot
        ax.plot_trisurf(surf[:, 0], surf[:, 1], surf[:, 2], color=self._colors[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='^')
        ax.legend([plot1_proxy, plot2_proxy], [self._names[0], self._names[1]], numpoints=1)

        # Display the 3D plot
        plt.show()


class VisSurfScatter(VisAbstract):
    """ Visualization module for Surfaces

    Wireframe plot for the control points and scatter plot for the surface points
    """
    def __init__(self):
        super(VisSurfScatter, self).__init__()

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._points:
            return False

        cpgrid = np.array(self._points[0])
        surf = np.array(self._points[1])

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = fig.gca(projection='3d')

        # Draw control points grid
        ax.plot(cpgrid[:, 0], cpgrid[:, 1], cpgrid[:, 2], color=self._colors[0], linestyle='-.', marker='o')

        # Draw surface points scatter plot
        ax.scatter(surf[:, 0], surf[:, 1], surf[:, 2], color=self._colors[1], s=50, depthshade=True)

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        plot1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='-.', color=self._colors[0], marker='o')
        plot2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='o')
        ax.legend([plot1_proxy, plot2_proxy], [self._names[0], self._names[1]], numpoints=1)

        # Display the 3D plot
        plt.show()
