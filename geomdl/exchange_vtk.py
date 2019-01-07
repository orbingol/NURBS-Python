"""
.. module:: exchange_vtk
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for VTK file formats

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import warnings
from geomdl import abstract
from . import _exchange as exch
from ._utilities import export


def export_polydata_str(obj, point_type='evalpts', **kwargs):
    """ Exports control points or evaluated points in VTK Polydata format (string).

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    :param obj: a B-Spline or NURBS shape
    :type obj: abstract.Curve, abstract.Surface
    :param point_type: ``ctrlpts`` for control points or ``evalpts`` for evaluated points
    :type point_type: str
    :return: contents of the VTK Polydata file
    :rtype: str
    :raises ValueError: input object is not an instance of abstract shapes
    :raises ValueError: point type is not supported
    :raises UserWarning: file title is bigger than 256 characters
    """
    if not isinstance(obj, (abstract.Curve, abstract.Surface)):
        raise ValueError("Input object should be a curve or a surface")

    # Define possible point types
    pt_types = dict(
        ctrlpts=obj.ctrlpts,
        evalpts=obj.evalpts
    )
    # Pick correct points from the object
    if point_type in pt_types:
        points = pt_types[point_type]
    else:
        raise ValueError("Please choose a valid point type option. Possible types:", ", ".join(pt_types.keys()))

    # Get file title
    file_title = kwargs.get('title', repr(obj))
    # Check for VTK standards for the file title
    if len(file_title) >= 256:
        file_title = file_title[0:255]  # slice the array into 255 characters, we will add new line character later
        warnings.warn("VTK standard restricts the file title with 256 characters. New file title is:", file_title)

    # Prepare file header
    line = "# vtk DataFile Version 3.0\n"
    line += file_title + "\n"
    line += "ASCII\n"

    # Define geometry/topology
    line += "DATASET POLYDATA\n"

    # Prepare points data
    line += "POINTS " + str(len(points)) + " FLOAT\n"
    for pt in points:
        line += " ".join(str(c) for c in pt) + "\n"

    # Return generated file content
    return line


@export
def export_polydata(obj, file_name, point_type='evalpts', **kwargs):
    """ Exports control points or evaluated points in VTK Polydata format.

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    :param obj: a curve or a surface object
    :type obj: abstract.Curve, abstract.Surface
    :param file_name: output file name
    :type file_name: str
    :param point_type: ``ctrlpts`` for control points or ``evalpts`` for evaluated points
    :type point_type: str
    :raises IOError: an error occurred writing the file
    """
    content = export_polydata_str(obj, point_type, **kwargs)
    return exch.write_file(file_name, content)
