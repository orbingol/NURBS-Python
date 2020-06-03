"""
.. module:: exchange.off
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for OFF file format

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import exc_helpers
from ..base import export, GeomdlError


@export
def export_off(surface, file_name, **kwargs):
    """ Exports surface(s) as a .off file.

    Keyword Arguments:
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 1*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: True*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.SurfaceContainer
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    content = export_off_str(surface, **kwargs)
    return exc_helpers.write_file(file_name, content)


@export
def export_off_str(surface, **kwargs):
    """ Exports surface(s) as a .off file (string).

    Keyword Arguments:
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 1*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: True*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.SurfaceContainer
    :return: contents of the .off file generated
    :rtype: str
    """
    # Get keyword arguments
    vertex_spacing = int(kwargs.get('vertex_spacing', 1))
    update_delta = kwargs.get('update_delta', True)

    # Input validity checking
    if surface.pdimension != 2:
        raise GeomdlError("Can only export surfaces")
    if vertex_spacing < 1:
        raise GeomdlError("Vertex spacing should be bigger than zero")

    # Count the vertices to update the face numbers correctly
    vertex_offset = 0

    # Initialize lists for vertices, vertex normals and faces
    str_v = []
    str_f = []

    for srf in surface:
        # Set surface evaluation delta
        if update_delta:
            srf.sample_size_u = surface.sample_size_u
            srf.sample_size_v = surface.sample_size_v

        # Tessellate surface
        srf.tessellate(vertex_spacing=vertex_spacing)
        vertices = srf.tessellator.vertices
        triangles = srf.tessellator.faces

        # Collect vertices
        for vert in vertices:
            line = str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
            str_v.append(line)

        # Collect faces (zero-indexed)
        for t in triangles:
            vl = t.data
            line = "3 " + \
                   str(vl[0] + vertex_offset) + " " + \
                   str(vl[1] + vertex_offset) + " " + \
                   str(vl[2] + vertex_offset) + "\n"
            str_f.append(line)

        # Update vertex offset
        vertex_offset = len(str_v)

    # Write file header
    line = "OFF\n"
    line += str(len(str_v)) + " " + str(len(str_f)) + " 0\n"

    # Write all collected data to the file
    for lv in str_v:
        line += lv
    for lf in str_f:
        line += lf

    return line
