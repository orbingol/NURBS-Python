"""
.. module:: VisVTK
    :platform: Unix, Windows
    :synopsis: VTK visualization component for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import vis
from . import vtk_helpers as vtkh
import numpy as np
from vtk.util.numpy_support import numpy_to_vtk
from vtk import VTK_FLOAT


class VisConfig(vis.VisConfigAbstract):
    """ Configuration class for VTK visualization module.

    This class is only required when you would like to change the visual defaults of the plots and the figure.

    The ``VisVTK`` module has the following configuration variables:

    * ``ctrlpts`` (bool): Control points polygon/grid visibility. *Default: True*
    * ``evalpts`` (bool): Curve/surface points visibility. *Default: True*
    * ``figure_size`` (list): Size of the figure in (x, y). *Default: (800, 600)*
    * ``line_width`` (int): Thickness of the lines on the figure. *Default: 0.5*
    """
    def __init__(self, **kwargs):
        super(VisConfig, self).__init__(**kwargs)
        self._bg = (  # background colors
            (0.5, 0.5, 0.5), (0.2, 0.2, 0.2), (0.25, 0.5, 0.75), (1.0, 1.0, 0.0),
            (1.0, 0.5, 0.0), (0.5, 0.0, 1.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)
        )
        self._bg_id = 0  # used for keeping track of the background numbering
        self.display_ctrlpts = kwargs.get('ctrlpts', True)
        self.display_evalpts = kwargs.get('evalpts', True)
        self.figure_size = kwargs.get('figure_size', (800, 600))  # size of the render window
        self.line_width = kwargs.get('line_width', 1.0)

    def keypress_callback(self, obj, ev):
        """ VTK callback for keypress events.

        Available custom keypress events:
            * ``b``: change background color
        """
        key = obj.GetKeySym()
        # Change background
        if key == 'b':
            if self._bg_id >= len(self._bg):
                self._bg_id = 0
            obj.GetRenderWindow().GetRenderers().GetFirstRenderer().SetBackground(*self._bg[self._bg_id])
            self._bg_id += 1
            obj.GetRenderWindow().Render()


class VisCurve2D(vis.VisAbstract):
    """ VTK visualization module for curves. """
    def __init__(self, config=VisConfig()):
        super(VisCurve2D, self).__init__(config=config)
        self._module_config['others'] = "midpt"

    def render(self, **kwargs):
        """ Plots the curve and the control points polygon. """
        # Calling parent function
        super(VisCurve2D, self).render(**kwargs)
        self._module_config['other'] = "midpt"

        # Initialize a list to store VTK actors
        vtk_actors = []

        # Default focal point for VTK camera
        focal_point = [0, 0, 0]

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                # Points as spheres
                pts = np.array(plot['ptsarr'], dtype=np.float)
                # Handle 2-dimensional data
                if pts.shape[1] == 2:
                    pts = np.c_[pts, np.zeros(pts.shape[0], dtype=np.float)]
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=VTK_FLOAT)
                temp_actor_pts = vtkh.create_actor_pts(pts=vtkpts, color=vtkh.create_color(plot['color']))
                vtk_actors.append(temp_actor_pts)
                # Lines
                temp_actor_lines = vtkh.create_actor_polygon(pts=vtkpts, color=vtkh.create_color(plot['color']),
                                                             size=self.vconf.line_width)
                vtk_actors.append(temp_actor_lines)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                pts = np.array(plot['ptsarr'], dtype=np.float)
                # Handle 2-dimensional data
                if pts.shape[1] == 2:
                    pts = np.c_[pts, np.zeros(pts.shape[0], dtype=np.float)]
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=VTK_FLOAT)
                temp_actor = vtkh.create_actor_polygon(pts=vtkpts, color=vtkh.create_color(plot['color']),
                                                       size=self.vconf.line_width * 2)
                vtk_actors.append(temp_actor)

            # Update camera focal point
            if plot['type'] == 'midpt':
                focal_point = plot['ptsarr'][0]
                if len(focal_point) == 2:
                    focal_point.append(0.0)

        # Render actors
        vtkh.create_render_window(vtk_actors, dict(KeyPressEvent=(self.vconf.keypress_callback, 1.0)),
                                  figure_size=self.vconf.figure_size,
                                  camera_focal_point=focal_point)


# VisCurve3D is an alias for VisCurve2D
VisCurve3D = VisCurve2D


class VisSurface(vis.VisAbstract):
    """ VTK visualization module for surfaces. """
    def __init__(self, config=VisConfig()):
        super(VisSurface, self).__init__(config=config)
        self._module_config['ctrlpts'] = "quadmesh"
        self._module_config['evalpts'] = "points"
        self._module_config['others'] = "midpt"

    def render(self, **kwargs):
        """ Plots the surface and the control points grid. """
        # Calling parent function
        super(VisSurface, self).render(**kwargs)

        # Initialize a list to store VTK actors
        vtk_actors = []

        # Default focal point for VTK camera
        focal_point = [0, 0, 0]

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                vertices = [v.data for v in plot['ptsarr'][0]]
                quads = [q.data for q in plot['ptsarr'][1]]
                # Points as spheres
                pts = np.array(vertices, dtype=np.float)
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=VTK_FLOAT)
                temp_actor_pts = vtkh.create_actor_pts(pts=vtkpts, color=vtkh.create_color(plot['color']))
                vtk_actors.append(temp_actor_pts)
                # Quad mesh
                lines = np.array(quads, dtype=np.int)
                temp_actor_lines = vtkh.create_actor_mesh(pts=vtkpts, lines=lines,
                                                          color=vtkh.create_color(plot['color']),
                                                          size=self.vconf.line_width)
                vtk_actors.append(temp_actor_lines)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                pts = np.array(plot['ptsarr'], dtype=np.float)
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=VTK_FLOAT)
                temp_actor = vtkh.create_actor_tri(pts=vtkpts, color=vtkh.create_color(plot['color']), d3d=False)
                vtk_actors.append(temp_actor)

            # Update camera focal point
            if plot['type'] == 'midpt':
                focal_point = plot['ptsarr'][0]

        # Render actors
        vtkh.create_render_window(vtk_actors, dict(KeyPressEvent=(self.vconf.keypress_callback, 1.0)),
                                  figure_size=self.vconf.figure_size,
                                  camera_focal_point=focal_point)


class VisVolume(vis.VisAbstract):
    """ VTK visualization module for volumes. """
    def __init__(self, config=VisConfig()):
        super(VisVolume, self).__init__(config=config)
        self._module_config['ctrlpts'] = "points"
        self._module_config['evalpts'] = "points"
        self._module_config['others'] = "midpt"

    def render(self, **kwargs):
        """ Plots the volume and the control points. """
        # Calling parent function
        super(VisVolume, self).render(**kwargs)

        # Initialize a list to store VTK actors
        vtk_actors = []

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self.vconf.display_ctrlpts:
                # Points as spheres
                pts = np.array(plot['ptsarr'], dtype=np.float)
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=VTK_FLOAT)
                temp_actor_pts = vtkh.create_actor_pts(pts=vtkpts, color=vtkh.create_color(plot['color']))
                vtk_actors.append(temp_actor_pts)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self.vconf.display_evalpts:
                pts = np.array(plot['ptsarr'], dtype=np.float)
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=VTK_FLOAT)
                temp_actor = vtkh.create_actor_tri(pts=vtkpts, color=vtkh.create_color(plot['color']), d3d=True)
                vtk_actors.append(temp_actor)

        # Render actors
        vtkh.create_render_window(vtk_actors, dict(KeyPressEvent=(self.vconf.keypress_callback, 1.0)),
                                  figure_size=self.vconf.figure_size)
