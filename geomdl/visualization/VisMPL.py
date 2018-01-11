"""
.. module:: VisMPL
    :platform: Unix, Windows
    :synopsis: Matplotlib visualization component for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from .VisBase import VisAbstract

import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class VisCurve2D(VisAbstract):

    def __init__(self):
        super(VisCurve2D, self).__init__()

    def render(self):
        if not self._points:
            return False

        cpts = np.array(self._points[0])
        crvpts = np.array(self._points[1])

        # Draw control points polygon and the curve
        plt.figure(figsize=(10.67, 8), dpi=96)
        cppolygon, = plt.plot(cpts[:, 0], cpts[:, 1], color=self._colors[0], linestyle='-.')
        curveplt, = plt.plot(crvpts[:, 0], crvpts[:, 1], color=self._colors[1], linestyle='-')
        plt.legend([cppolygon, curveplt], [self._names[0], self._names[1]])
        plt.show()


class VisCurve3D(VisAbstract):

    def __init__(self):
        super(VisCurve3D, self).__init__()

    def render(self):
        if not self._points:
            return False

        cpts = np.array(self._points[0])
        crvpts = np.array(self._points[1])

        # Draw control points polygon and the 3D curve
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = fig.gca(projection='3d')

        # Plot 3D lines
        ax.plot(cpts[:, 0], cpts[:, 1], cpts[:, 2], self._colors[0])
        ax.plot(crvpts[:, 0], crvpts[:, 1], crvpts[:, 2], self._colors[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        scatter1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[0], marker='o')
        scatter2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='o')
        ax.legend([scatter1_proxy, scatter2_proxy], [self._names[0], self._names[1]], numpoints=1)

        # Display the 3D plot
        plt.show()


class VisSurfWireframe(VisAbstract):

    def __init__(self):
        super(VisSurfWireframe, self).__init__()

    def render(self):
        if not self._points:
            return False

        cpgrid = np.array(self._points[0])
        surf = np.array(self._points[1])

        # Reshape surface points array for plotting, @ref: https://stackoverflow.com/a/21352257
        cols = surf[:, 0].shape[0]
        X = surf[:, 0].reshape(-1, cols)
        Y = surf[:, 1].reshape(-1, cols)
        Z = surf[:, 2].reshape(-1, cols)

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = fig.gca(projection='3d')

        # Control points as a scatter plot (use mode='linear' while saving CSV file)
        ax.scatter(cpgrid[:, 0], cpgrid[:, 1], cpgrid[:, 2], color=self._colors[0], s=50, depthshade=True)

        # Surface points as a wireframe plot (use mode='wireframe' while saving CSV file)
        ax.plot_wireframe(X, Y, Z, color=self._colors[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        scatter1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[0], marker='o')
        scatter2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='o')
        ax.legend([scatter1_proxy, scatter2_proxy], [self._names[0], self._names[1]], numpoints=1)

        # Display the 3D plot
        plt.show()


class VisTriSurf(VisAbstract):

    def __init__(self):
        super(VisTriSurf, self).__init__()

    def render(self):
        if not self._points:
            return False

        cpgrid = np.array(self._points[0])
        surf = np.array(self._points[1])

        # Arrange control points grid for plotting, @ref: https://stackoverflow.com/a/21352257
        cols = cpgrid[:, 0].shape[0]
        Xc = cpgrid[:, 0].reshape(-1, cols)
        Yc = cpgrid[:, 1].reshape(-1, cols)
        Zc = cpgrid[:, 2].reshape(-1, cols)

        # Arrange surface points array for plotting
        X = surf[:, 0]
        Y = surf[:, 1]
        Z = surf[:, 2]

        # Start plotting of the surface and the control points grid
        fig = plt.figure(figsize=(10.67, 8), dpi=96)
        ax = fig.gca(projection='3d')

        # Control points as a scatter plot (use mode='wireframe' while saving CSV file)
        ax.plot_wireframe(Xc, Yc, Zc, color=self._colors[0])

        # Surface points as a triangulated surface plot (use mode='linear' while saving CSV file)
        ax.plot_trisurf(X, Y, Z, color=self._colors[1])

        # Add legend to 3D plot, @ref: https://stackoverflow.com/a/20505720
        scatter1_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[0], marker='o')
        scatter2_proxy = matplotlib.lines.Line2D([0], [0], linestyle='none', color=self._colors[1], marker='o')
        ax.legend([scatter1_proxy, scatter2_proxy], [self._names[0], self._names[1]], numpoints=1)

        # Display the 3D plot
        plt.show()
