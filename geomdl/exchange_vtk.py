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
    """ Exports control points or evaluated points in VTK Polydata format (string).

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    Keyword Arguments:
        * ``point_type``: **ctrlpts** for control points or **evalpts** for evaluated points
        * ``tessellate``: tessellates the points (works only for surfaces)

    :param obj: a spline geometry
    :type obj: abstract.SplineGeometry
    :return: contents of the VTK file
    :rtype: str
    :raises GeomdlException: input object is not an instance of abstract shapes
    :raises GeomdlException: point type is not supported
    :raises UserWarning: file title is bigger than 256 characters
    """
    if not isinstance(obj, abstract.SplineGeometry):
        raise exch.GeomdlException("Input object should be a spline geometry")

    # Get keyword arguments
    point_type = kwargs.get('point_type', 'evalpts')
    tessellate = kwargs.get('tessellate', False)

    possible_types = ['ctrlpts', 'evalpts']
    # Pick correct points from the object
    if point_type not in possible_types:
        raise exch.GeomdlException("Please choose a valid point type option. " +
                                   "Possible types:", ", ".join([str(t) for t in possible_types]))

    # Get file title
    file_title = kwargs.get('title', repr(obj))
    # Check for VTK standards for the file title
    if len(file_title) >= 256:
        file_title = file_title[0:255]  # slice the array into 255 characters, we will add new line character later
        warnings.warn("VTK standard restricts the file title with 256 characters. New file title is:", file_title)

    # Prepare data array
    tsl_dim = 0
    if point_type == "ctrlpts":
        if tessellate and obj.pdimension == 2:
            tsl = abstract.tessellate.QuadTessellate()
            tsl.tessellate(obj.ctrlpts, size_u=obj.ctrlpts_size_u, size_v=obj.ctrlpts_size_v)
            data_array = ([v.data for v in tsl.vertices], [q.data for q in tsl.faces])
            tsl_dim = 4
        else:
            data_array = (obj.ctrlpts, [])
    elif point_type == "evalpts":
        if tessellate and obj.pdimension == 2:
            obj.tessellate()
            data_array = ([v.data for v in obj.tessellator.vertices], [t.vertex_ids_zero for t in obj.tessellator.faces])
            tsl_dim = 3
        else:
            data_array = (obj.evalpts, [])
    else:
        data_array = ([], [])

    # Prepare file header
    line = "# vtk DataFile Version 3.0\n"
    line += file_title + "\n"
    line += "ASCII\n"

    # Define geometry/topology
    line += "DATASET POLYDATA\n"

    # Prepare points data
    line += "POINTS " + str(len(data_array[0])) + " FLOAT\n"
    vert_line = ""
    for ipt, pt in enumerate(data_array[0]):
        line += " ".join(str(c) for c in pt) + "\n"
        vert_line += "1 " + str(ipt) + "\n"

    # Add vertices
    line += "VERTICES " + str(len(data_array[0])) + " " + str(2 * len(data_array[0])) + "\n"
    line += vert_line

    # Add polygons
    if data_array[1]:
        line += "POLYGONS " + str(len(data_array[1])) + " " + str((tsl_dim + 1) * len(data_array[1])) + "\n"
        for pt in data_array[1]:
            line += str(tsl_dim) + " " + " ".join(str(c) for c in pt) + "\n"

    # Add dataset attributes
    line += "POINT_DATA " + str(len(data_array[0])) + "\n"
    line += "CELL_DATA " + str(len(data_array[1])) + "\n"

    # Return generated file content
    return line


@export
def export_polydata(obj, file_name, **kwargs):
    """ Exports control points or evaluated points in VTK Polydata format.

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    Keyword Arguments:
        * ``point_type``: **ctrlpts** for control points or **evalpts** for evaluated points
        * ``tessellate``: tessellates the points (works only for surfaces)

    :param obj: a spline geometry
    :type obj: abstract.SplineGeometry
    :param file_name: output file name
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    content = export_polydata_str(obj, **kwargs)
    return exch.write_file(file_name, content)
