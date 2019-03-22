"""
.. module:: exchange_vtk
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for VTK file formats

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import warnings
from . import abstract
from . import _exchange as exch
from ._utilities import export


def export_polydata_str(obj, **kwargs):
    """ Saves control points or evaluated points in VTK Polydata format (string).

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    Keyword Arguments:
        * ``point_type``: **ctrlpts** for control points or **evalpts** for evaluated points
        * ``tessellate``: tessellates the points (works only for surfaces)

    :param obj: geometry object
    :type obj: abstract.SplineGeometry, multi.AbstractContainer
    :return: contents of the VTK file
    :rtype: str
    :raises GeomdlException: point type is not supported
    :raises UserWarning: file title is bigger than 256 characters
    """
    # Get keyword arguments
    point_type = kwargs.get('point_type', "evalpts")
    file_title = kwargs.get('title', "geomdl " + repr(obj))  # file title
    tessellate = kwargs.get('tessellate', False)

    # Input validation
    possible_types = ['ctrlpts', 'evalpts']
    if point_type not in possible_types:
        raise exch.GeomdlException("Please choose a valid point type option. " +
                                   "Possible types:", ", ".join([str(t) for t in possible_types]))

    # Check for VTK standards for the file title
    if len(file_title) >= 256:
        file_title = file_title[0:255]  # slice the array into 255 characters, we will add new line character later
        warnings.warn("VTK standard restricts the file title with 256 characters. New file title is:", file_title)

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
            if tessellate and o.pdimension == 2:
                tsl = abstract.tessellate.QuadTessellate()
                tsl.tessellate(o.ctrlpts, size_u=o.ctrlpts_size_u, size_v=o.ctrlpts_size_v)
                data_array = ([v.data for v in tsl.vertices], [q.data for q in tsl.faces])
            else:
                data_array = (o.ctrlpts, [])
        elif point_type == "evalpts":
            if tessellate and o.pdimension == 2:
                o.tessellate()
                data_array = ([v.data for v in o.vertices], [t.data for t in o.faces])
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
    if tessellate:
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

    :param obj: geometry object
    :type obj: abstract.SplineGeometry, multi.AbstractContainer
    :param file_name: output file name
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    content = export_polydata_str(obj, **kwargs)
    return exch.write_file(file_name, content)
