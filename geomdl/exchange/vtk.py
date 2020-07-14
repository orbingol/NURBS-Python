"""
.. module:: exchange.vtk
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for VTK file formats

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from ..tessellate import triangular, quadrilateral
from ..base import export, GeomdlError, GeomdlWarning
from . import exc_helpers


@export
def export_polydata_str(obj, **kwargs):
    """ Saves control points or evaluated points in VTK Polydata format (string).

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    Keyword Arguments:
        * ``point_type``: **ctrlpts** for control points or **evalpts** for evaluated points
        * ``tessellate``: tessellates the points (works only for surfaces)

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :return: contents of the VTK file
    :rtype: str
    """
    # Get keyword arguments
    point_type = kwargs.get('point_type', "evalpts")
    file_title = kwargs.get('title', "geomdl " + repr(obj))  # file title
    do_tessellate = kwargs.get('tessellate', False)

    # Input validation
    possible_types = ['ctrlpts', 'evalpts']
    if point_type not in possible_types:
        raise GeomdlError("Please choose a valid point type option. " +
                          "Possible types:", ", ".join([str(t) for t in possible_types]))

    # Check for VTK standards for the file title
    if len(file_title) >= 256:
        file_title = file_title[0:255]  # slice the array into 255 characters, we will add new line character later
        GeomdlWarning("VTK standard restricts the file title with 256 characters. New file title is:", file_title)

    # Find number of edges in a single tessellated structure
    tsl_dim = 4 if point_type == "ctrlpts" else 3

    # Initialize lists
    str_p = ""
    str_v = ""
    str_f = ""

    # Count number of vertices and faces
    v_offset = 0
    f_offset = 0

    # Loop through all geometry objects
    for o in obj:
        # Prepare data array
        if point_type == "ctrlpts":
            if do_tessellate and o.pdimension == 2:
                vertices, faces = quadrilateral.make_quad_mesh(o.ctrlpts.points, o.ctrlpts_size[0], o.ctrlpts_size[1])
                data_array = ([v.data for v in vertices], [q.data for q in faces])
            else:
                data_array = (o.ctrlpts, [])
        elif point_type == "evalpts":
            if do_tessellate and o.pdimension == 2:
                vertices, faces = triangular.make_triangle_mesh(o.evalpts, o.sample_size[0], o.sample_size[1])
                data_array = ([v.data for v in vertices], [t.data for t in faces])
            else:
                data_array = (o.evalpts, [])
        else:
            data_array = ([], [])

        # Prepare point and vertex data
        for ipt, pt in enumerate(data_array[0]):
            str_p += " ".join(str(c) for c in pt) + "\n"
            str_v += "1 " + str(ipt + v_offset) + "\n"

        # Prepare polygon data
        if data_array[1]:
            for pt in data_array[1]:
                str_f += str(tsl_dim) + " " + " ".join(str(c + v_offset) for c in pt) + "\n"
            # Update face offset
            f_offset += len(data_array[1])

        # Update vertex offset
        v_offset += len(data_array[0])

    # Start generating the file content
    line = "# vtk DataFile Version 3.0\n"
    line += file_title + "\n"
    line += "ASCII\n"

    # Define geometry/topology
    line += "DATASET POLYDATA\n"

    # Add point data to the file
    line += "POINTS " + str(v_offset) + " FLOAT\n"
    line += str_p

    # Add vertex data to the file
    line += "VERTICES " + str(v_offset) + " " + str(2 * v_offset) + "\n"
    line += str_v

    # Add polygon data to the file
    if do_tessellate:
        line += "POLYGONS " + str(f_offset) + " " + str((tsl_dim + 1) * f_offset) + "\n"
        line += str_f

    # Add dataset attributes to the file
    line += "POINT_DATA " + str(v_offset) + "\n"
    if f_offset > 0:
        line += "CELL_DATA " + str(f_offset) + "\n"

    # Return generated file content
    return line


@export
def export_polydata(obj, file_name, **kwargs):
    """ Exports control points or evaluated points in VTK Polydata format.

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    Keyword Arguments:
        * ``point_type``: **ctrlpts** for control points or **evalpts** for evaluated points
        * ``tessellate``: tessellates the points (works only for surfaces)

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :param file_name: output file name
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    return exc_helpers.write_file(file_name, export_polydata_str(obj, **kwargs))
