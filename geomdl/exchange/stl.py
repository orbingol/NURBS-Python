"""
.. module:: exchange.stl
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for STL file format

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import struct
from .. import linalg
from ..tessellate import triangular
from ..base import export, GeomdlError
from . import exc_helpers


@export
def export_stl_str(surface, **kwargs):
    """ Exports surface(s) as a .stl file in plain text or binary format (string).

    Keyword Arguments:
        * ``binary``: flag to generate a binary STL file. *Default: False*

    :param surface: input surface(s)
    :type surface: BSpline.Surface
    :return: contents of the .stl file generated
    :rtype: str
    """
    binary = kwargs.get('binary', False)

    # Input validity checking
    if surface.pdimension != 2:
        raise GeomdlError("Can only export surfaces")

    triangles_list = []
    for srf in surface:
        # Tessellate surface
        vertices, faces = triangular.make_triangle_mesh(srf.evalpts, srf.sample_size[0], srf.sample_size[1])
        triangles_list += faces

    # Write triangle list to ASCII or  binary STL file
    if binary:
        line = b'\0' * 80  # header
        line += struct.pack('<i', len(triangles_list))  # number of triangles
        for t in triangles_list:
            line += struct.pack('<3f', *linalg.triangle_normal(t))  # normal
            for v in t.vertices:
                line += struct.pack('<3f', *v.data)  # vertices
            line += b'\0\0'  # attribute byte count
    else:
        line = "solid Surface\n"
        for t in triangles_list:
            nvec = linalg.triangle_normal(t)
            line += "\tfacet normal " + str(nvec[0]) + " " + str(nvec[1]) + " " + str(nvec[2]) + "\n"
            line += "\t\touter loop\n"
            for v in t.vertices:
                line += "\t\t\tvertex " + str(v.x) + " " + str(v.y) + " " + str(v.z) + "\n"
            line += "\t\tendloop\n"
            line += "\tendfacet\n"
        line += "endsolid Surface\n"

    return line


def export_stl(surface, file_name, **kwargs):
    """ Exports surface(s) as a .stl file in plain text or binary format.

    Keyword Arguments:
        * ``binary``: flag to generate a binary STL file. *Default: True*
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 1*

    :param surface: input surface(s)
    :type surface: BSpline.Surface
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    binary = kwargs.get('binary', True)
    if 'binary' in kwargs:
        kwargs.pop('binary')
    content = export_stl_str(surface, binary=binary, **kwargs)
    return exc_helpers.write_file(file_name, content, binary=binary)
