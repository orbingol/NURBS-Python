"""
.. module:: vtk_helpers
    :platform: Unix, Windows
    :synopsis: Helper functions for VTK visualization component for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import linalg
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
    display_plot = kwargs.get('display_plot', True)
    image_filename = kwargs.get('image_filename', "screenshot.png")

    # Find camera focal point
    center_points = []
    for actor in actors:
        center_points.append(actor.GetCenter())
    camera_focal_point = linalg.vector_mean(*center_points)

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
    render_window.SetOffScreenRendering(not display_plot)

    # Render actors
    render_window.Render()

    # Set window name after render() is called
    render_window.SetWindowName("geomdl")

    if display_plot:
        # Render window interactor
        window_interactor = vtk.vtkRenderWindowInteractor()
        window_interactor.SetRenderWindow(render_window)

        # Add event observers
        for cb in callbacks:
            window_interactor.AddObserver(cb, callbacks[cb][0], callbacks[cb][1])  # cb name, cb function ref, cb priority

        # Use trackball camera
        interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        window_interactor.SetInteractorStyle(interactor_style)

        # Start interactor
        window_interactor.Start()
    else:
        # Get the screenshot
        window_image = vtk.vtkWindowToImageFilter()
        window_image.SetInput(render_window)
        window_image.Update()

        # Export screenshot to an image file
        window_image_writer = vtk.vtkPNGWriter()
        window_image_writer.SetFileName(image_filename)
        window_image_writer.SetInputConnection(window_image.GetOutputPort())
        window_image_writer.Write()


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
    # Keyword arguments
    array_name = kwargs.get('name', "")
    array_index = kwargs.get('index', 0)
    point_size = kwargs.get('size', 5)
    point_sphere = kwargs.get('point_as_sphere', True)

    # Create points
    points = vtk.vtkPoints()
    points.SetData(pts)

    # Create a PolyData object and add points
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # Run vertex glyph filter on the points array
    vertex_filter = vtk.vtkVertexGlyphFilter()
    vertex_filter.SetInputData(polydata)

    # Map ploy data to the graphics primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(vertex_filter.GetOutputPort())
    mapper.SetArrayName(array_name)
    mapper.SetArrayId(array_index)

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
    # Keyword arguments
    array_name = kwargs.get('name', "")
    array_index = kwargs.get('index', 0)
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

    # Create a PolyData object and add points & lines
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(cells)

    # Map poly data to the graphics primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputDataObject(polydata)
    mapper.SetArrayName(array_name)
    mapper.SetArrayId(array_index)

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
    # Keyword arguments
    array_name = kwargs.get('name', "")
    array_index = kwargs.get('index', 0)
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

    # Create a PolyData object and add points & lines
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(cells)

    # Map poly data to the graphics primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputDataObject(polydata)
    mapper.SetArrayName(array_name)
    mapper.SetArrayId(array_index)

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*color)
    actor.GetProperty().SetLineWidth(line_width)

    # Return the actor
    return actor


def create_actor_tri(pts, tris, color, **kwargs):
    """ Creates a VTK actor for rendering triangulated surface plots.

    :param pts: points
    :type pts: vtkFloatArray
    :param tris: list of triangle indices
    :type tris: ndarray
    :param color: actor color
    :type color: list
    :return: a VTK actor
    :rtype: vtkActor
    """
    # Keyword arguments
    array_name = kwargs.get('name', "")
    array_index = kwargs.get('index', 0)

    # Create points
    points = vtk.vtkPoints()
    points.SetData(pts)

    # Create triangles
    triangles = vtk.vtkCellArray()
    for tri in tris:
        tmp = vtk.vtkTriangle()
        for i, v in enumerate(tri):
            tmp.GetPointIds().SetId(i, v)
        triangles.InsertNextCell(tmp)

    # Create a PolyData object and add points & triangles
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(triangles)

    # Map poly data to the graphics primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputDataObject(polydata)
    mapper.SetArrayName(array_name)
    mapper.SetArrayId(array_index)

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*color)

    # Return the actor
    return actor


def create_actor_hexahedron(grid, color, **kwargs):
    """ Creates a VTK actor for rendering voxels using hexahedron elements.

    :param grid: grid
    :type grid: ndarray
    :param color: actor color
    :type color: list
    :return: a VTK actor
    :rtype: vtkActor
    """
    # Keyword arguments
    array_name = kwargs.get('name', "")
    array_index = kwargs.get('index', 0)

    # Create hexahedron elements
    points = vtk.vtkPoints()
    hexarray = vtk.vtkCellArray()
    for j, pt in enumerate(grid):
        tmp = vtk.vtkHexahedron()
        fb = pt[0]
        for i, v in enumerate(fb):
            points.InsertNextPoint(v)
            tmp.GetPointIds().SetId(i, i + (j * 8))
        ft = pt[-1]
        for i, v in enumerate(ft):
            points.InsertNextPoint(v)
            tmp.GetPointIds().SetId(i + 4, i + 4 + (j * 8))
        hexarray.InsertNextCell(tmp)

    # Create an unstructured grid object and add points & hexahedron elements
    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.SetCells(tmp.GetCellType(), hexarray)
    # ugrid.InsertNextCell(tmp.GetCellType(), tmp.GetPointIds())

    # Map unstructured grid to the graphics primitives
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputDataObject(ugrid)
    mapper.SetArrayName(array_name)
    mapper.SetArrayId(array_index)

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*color)

    # Return the actor
    return actor


def create_actor_delaunay(pts, color, **kwargs):
    """ Creates a VTK actor for rendering triangulated plots using Delaunay triangulation.

    Keyword Arguments:
        * ``d3d``: flag to choose between Delaunay2D (``False``) and Delaunay3D (``True``). *Default: False*

    :param pts: points
    :type pts: vtkFloatArray
    :param color: actor color
    :type color: list
    :return: a VTK actor
    :rtype: vtkActor
    """
    # Keyword arguments
    array_name = kwargs.get('name', "")
    array_index = kwargs.get('index', 0)
    use_delaunay3d = kwargs.get("d3d", False)

    # Create points
    points = vtk.vtkPoints()
    points.SetData(pts)

    # Create a PolyData object and add points
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # Apply Delaunay triangulation on the poly data object
    triangulation = vtk.vtkDelaunay3D() if use_delaunay3d else vtk.vtkDelaunay2D()
    triangulation.SetInputData(polydata)

    # Map triangulated surface to the graphics primitives
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputConnection(triangulation.GetOutputPort())
    mapper.SetArrayName(array_name)
    mapper.SetArrayId(array_index)

    # Create an actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*color)

    # Return the actor
    return actor
