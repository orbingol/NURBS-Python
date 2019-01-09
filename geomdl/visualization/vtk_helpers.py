"""
.. module:: vtk_helpers
    :platform: Unix, Windows
    :synopsis: Helper functions for VTK visualization component for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import vtk


def create_render_window(actors, callbacks, **kwargs):
    """ Creates VTK render window with an interactor.

    :param actors: list of VTK actors
    :type actors: list, tuple
    :param callbacks: callback functions for registering custom events
    :type callbacks: dict
    """
    # Get keyword arguments
    figure_size = kwargs.get('figure_size', (800, 600))
    camera_position = kwargs.get('camera_position', (0, 0, 100))
    camera_focal_point = kwargs.get('camera_focal_point', (0, 0, 0))

    # Create camera
    camera = vtk.vtkCamera()
    camera.SetPosition(*camera_position)
    camera.SetFocalPoint(*camera_focal_point)

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

    # Add event observers
    for cb in callbacks:
        window_interactor.AddObserver(cb, callbacks[cb][0], callbacks[cb][1])  # cb name, cb function ref, cb priority

    # Render actors
    render_window.Render()

    # Set window name after render() is called
    render_window.SetWindowName("NURBS-Python")

    # Start interactor
    window_interactor.Start()


def create_color(color):
    """ Creates VTK-compatible RGB color from a color string.

    :param color: color
    :type color: str
    :return: RGB color values
    :rtype: list
    """
    if color[0] == "#":
        # Convert hex string to RGB
        return [int(color[i:i + 2], 16) / 255 for i in range(1, 7, 2)]
    else:
        # Create a named colors instance
        nc = vtk.vtkNamedColors()
        return nc.GetColor3d(color)


def create_actor_pts(pts, color, **kwargs):
    """ Creates a VTK actor for rendering scatter plots.

    :param pts: points
    :type pts: vtkFloatArray
    :param color: actor color
    :type color: list
    :return: a VTK actor
    :rtype: vtkActor
    """
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
    actor.GetProperty().SetColor(*color)
    actor.GetProperty().SetPointSize(point_size)
    actor.GetProperty().SetRenderPointsAsSpheres(point_sphere)

    # Return the actor
    return actor


def create_actor_polygon(pts, color, **kwargs):
    """ Creates a VTK actor for rendering polygons.

    :param pts: points
    :type pts: vtkFloatArray
    :param color: actor color
    :type color: list
    :return: a VTK actor
    :rtype: vtkActor
    """
    line_width = kwargs.get('size', 1.0)

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
    actor.GetProperty().SetColor(*color)
    actor.GetProperty().SetLineWidth(line_width)

    # Return the actor
    return actor


def create_actor_mesh(pts, lines, color, **kwargs):
    """ Creates a VTK actor for rendering quadrilateral plots.

    :param pts: points
    :type pts: vtkFloatArray
    :param lines: point connectivity information
    :type lines: vtkIntArray
    :param color: actor color
    :type color: list
    :return: a VTK actor
    :rtype: vtkActor
    """
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
    actor.GetProperty().SetColor(*color)
    actor.GetProperty().SetLineWidth(line_width)

    # Return the actor
    return actor


def create_actor_tri(pts, color, **kwargs):
    """ Creates a VTK actor for rendering triangulated plots.

    :param pts: points
    :type pts: vtkFloatArray
    :param color: actor color
    :type color: list
    :return: a VTK actor
    :rtype: vtkActor
    """
    # Get keyword arguments
    use_delaunay3d = kwargs.get("d3d", False)

    # Create points
    points = vtk.vtkPoints()
    points.SetData(pts)

    # Convert points to poly data
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # Apply Delaunay triangulation on the poly data object
    triangulation = vtk.vtkDelaunay3D() if use_delaunay3d else vtk.vtkDelaunay2D()
    triangulation.SetInputData(polydata)

    # Map triangulated surface to the graphics primitives
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputConnection(triangulation.GetOutputPort())

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*color)

    # Return the actor
    return actor
