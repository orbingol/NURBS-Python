"""
.. module:: VisVTK
    :platform: Unix, Windows
    :synopsis: VTK visualization component for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from geomdl import vis
from . import np
try:
    import vtk
    from vtk.util.numpy_support import numpy_to_vtk
except ImportError:
    print("Please install VTK with its Python wrappers before using VisVTK visualization module")
    exit(0)


class VisConfig(vis.VisConfigAbstract):
    """ Configuration class for VTK visualization module.

    This class is only required when you would like to change the visual defaults of the plots and the figure.

    The ``VisVTK`` module has the following configuration variables:

    * ``ctrlpts`` (bool): Control points polygon/grid visibility. *Default: True*
    * ``evalpts`` (bool): Curve/surface points visibility. *Default: True*
    * ``figure_size`` (list): Size of the figure in (x, y). *Default: (800, 600)*
    """
    def __init__(self, **kwargs):
        super(VisConfig, self).__init__(**kwargs)
        self._vtk_bg = ((0.5, 0.5, 0.5), (0.25, 0.5, 0.75), (0.5, 0.25, 0.75), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0))
        self._vtk_bg_id = 0  # used for keeping track of the background numbering
        self.display_ctrlpts = kwargs.get('ctrlpts', True)
        self.display_evalpts = kwargs.get('evalpts', True)
        self.figure_size = kwargs.get('figure_size', (800, 600))  # size of the render window

    def vtk_keypress_callback(self, obj, ev):
        """ VTK callback for keypress events """
        key = obj.GetKeySym()
        # Change background
        if key == 'b':
            if self._vtk_bg_id >= len(self._vtk_bg):
                self._vtk_bg_id = 0
            obj.GetRenderWindow().GetRenderers().GetFirstRenderer().SetBackground(*self._vtk_bg[self._vtk_bg_id])
            self._vtk_bg_id += 1
            obj.GetRenderWindow().Render()


class VisCurve2D(vis.VisAbstract):
    def __init__(self, config=VisConfig()):
        super(VisCurve2D, self).__init__(config=config)

    def render(self, **kwargs):
        """ Plots the curve and the control points polygon. """
        # Calling parent function
        super(VisCurve2D, self).render(**kwargs)

        # Initialize a list to store VTK actors
        vtk_actors = []

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                # Points as spheres
                pts = np.array(plot['ptsarr'], dtype=np.float)
                # Handle 2-dimensional data
                if pts.shape[1] == 2:
                    pts = np.c_[pts, np.zeros(pts.shape[0], dtype=np.float)]
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=vtk.VTK_FLOAT)
                temp_actor_pts = create_actor_pts(vtkpts)
                vtk_actors.append(temp_actor_pts)
                # Lines
                temp_actor_lines = create_actor_polygon(vtkpts)
                vtk_actors.append(temp_actor_lines)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self._config.display_evalpts:
                pts = np.array(plot['ptsarr'], dtype=np.float)
                # Handle 2-dimensional data
                if pts.shape[1] == 2:
                    pts = np.c_[pts, np.zeros(pts.shape[0], dtype=np.float)]
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=vtk.VTK_FLOAT)
                temp_actor = create_actor_polygon(vtkpts)
                vtk_actors.append(temp_actor)

        # Render actors
        create_render_window(vtk_actors, self._config.figure_size, dict(keypress=self._config.vtk_keypress_callback))


# VisCurve3D is an alias for VisCurve2D
VisCurve3D = VisCurve2D


class VisSurface(vis.VisAbstractSurf):
    """ VTK visualization module for surfaces. """
    def __init__(self, config=VisConfig()):
        super(VisSurface, self).__init__(config=config)
        self._plot_types = {'ctrlpts': 'quadmesh', 'evalpts': 'points'}

    def render(self, **kwargs):
        """ Plots the surface and the control points grid. """
        # Calling parent function
        super(VisSurface, self).render(**kwargs)

        # Initialize a list to store VTK actors
        vtk_actors = []

        # Start plotting
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                vertices = [v.data for v in plot['ptsarr'][0]]
                quads = [q.data for q in plot['ptsarr'][1]]
                # Points as spheres
                pts = np.array(vertices, dtype=np.float)
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=vtk.VTK_FLOAT)
                temp_actor_pts = create_actor_pts(vtkpts)
                vtk_actors.append(temp_actor_pts)
                # Quad mesh
                lines = np.array(quads, dtype=np.int)
                temp_actor_lines = create_actor_mesh(vtkpts, lines)
                vtk_actors.append(temp_actor_lines)

            # Plot evaluated points
            if plot['type'] == 'evalpts' and self._config.display_evalpts:
                pts = np.array(plot['ptsarr'], dtype=np.float)
                vtkpts = numpy_to_vtk(pts, deep=False, array_type=vtk.VTK_FLOAT)
                temp_actor = create_actor_tri2d(vtkpts)
                vtk_actors.append(temp_actor)

        # Render actors
        create_render_window(vtk_actors, self._config.figure_size, dict(keypress=self._config.vtk_keypress_callback))


########################
# VTK Helper Functions #
########################
def create_render_window(actors, figure_size, callbacks):
    """ Creates VTK render window with an interactor.

    :param actors: list of VTK actors
    :type actors: list, tuple
    :param figure_size: size of the VTK render window
    :type figure_size: list, tuple
    :param callbacks: callback functions for registering custom events
    :type callbacks: dict
    """
    # Create camera
    camera = vtk.vtkCamera()
    camera.SetPosition(0, 0, 100)
    camera.SetFocalPoint(0, 0, 0)

    # Create renderer
    renderer = vtk.vtkRenderer()
    renderer.SetActiveCamera(camera)
    renderer.SetBackground(1.0, 1.0, 1.0)

    # Add actors to the scene
    for actor in actors:
        renderer.AddActor(actor)

    # Render window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(*figure_size)

    # Render window interactor
    window_interactor = vtk.vtkRenderWindowInteractor()
    window_interactor.SetRenderWindow(render_window)
    window_interactor.AddObserver("KeyPressEvent", callbacks['keypress'], 1.0)

    # Render actors
    render_window.Render()

    # Set window name after render() is called
    render_window.SetWindowName("NURBS-Python")

    # Start interactor
    window_interactor.Start()


def create_actor_pts(pts, **kwargs):
    """ Creates a VTK actor for rendering scatter plots.

    :param pts: points
    :type pts: vtkFloatArray
    :return: a VTK actor
    :rtype: vtkActor
    """
    point_color = kwargs.get('color', (0.0, 0.0, 128/255))
    point_size = kwargs.get('size', 5)
    point_sphere = kwargs.get('point_as_sphere', True)

    # Create points
    points = vtk.vtkPoints()
    points.SetData(pts)

    # Create poly data objects
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # Run vertex glyph filter on the points array
    vertex_filter = vtk.vtkVertexGlyphFilter()
    vertex_filter.SetInputData(polydata)

    # Map ploy data to the graphics primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(vertex_filter.GetOutputPort())

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*point_color)
    actor.GetProperty().SetPointSize(point_size)
    actor.GetProperty().SetRenderPointsAsSpheres(point_sphere)

    # Return the actor
    return actor


def create_actor_polygon(pts, **kwargs):
    """ Creates a VTK actor for rendering polygons.

    :param pts: points
    :type pts: vtkFloatArray
    :return: a VTK actor
    :rtype: vtkActor
    """
    line_color = kwargs.get('color', (0.0, 0.0, 1.0))
    line_width = kwargs.get('size', 0.5)

    # Create points
    points = vtk.vtkPoints()
    points.SetData(pts)

    # Number of points
    num_points = points.GetNumberOfPoints()

    # Create lines
    cells = vtk.vtkCellArray()
    for i in range(num_points - 1):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, i)
        line.GetPointIds().SetId(1, i + 1)
        cells.InsertNextCell(line)

    # Create poly data objects
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(cells)

    # Map poly data to the graphics primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputDataObject(polydata)

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*line_color)
    actor.GetProperty().SetLineWidth(line_width)

    # Return the actor
    return actor


def create_actor_mesh(pts, lines, **kwargs):
    """ Creates a VTK actor for rendering quadrilateral plots.

    :param pts: points
    :type pts: vtkFloatArray
    :param lines: point connectivity information
    :type lines: vtkIntArray
    :return: a VTK actor
    :rtype: vtkActor
    """
    line_color = kwargs.get('color', (0.0, 0.0, 1.0))
    line_width = kwargs.get('size', 0.5)

    # Create points
    points = vtk.vtkPoints()
    points.SetData(pts)

    # Create lines
    cells = vtk.vtkCellArray()
    for line in lines:
        pline = vtk.vtkPolyLine()
        pline.GetPointIds().SetNumberOfIds(5)
        for i in range(len(line)):
            pline.GetPointIds().SetId(i, line[i])
        pline.GetPointIds().SetId(4, line[0])
        cells.InsertNextCell(pline)

    # Create poly data objects
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(cells)

    # Map poly data to the graphics primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputDataObject(polydata)

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*line_color)
    actor.GetProperty().SetLineWidth(line_width)

    # Return the actor
    return actor


def create_actor_tri2d(pts, **kwargs):
    """ Creates a VTK actor for rendering triangulated plots.

    :param pts: points
    :type pts: vtkFloatArray
    :return: a VTK actor
    :rtype: vtkActor
    """
    point_color = kwargs.get('color', (0.0, 1.0, 0.25))

    # Create points
    points = vtk.vtkPoints()
    points.SetData(pts)

    # Convert points to poly data
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # Apply 2-dimensional Delaunay triangulation on the poly data object
    triangulation = vtk.vtkDelaunay2D()
    triangulation.SetInputData(polydata)

    # Map triangulated surface to the graphics primitives
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputConnection(triangulation.GetOutputPort())

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*point_color)

    # Return the actor
    return actor
