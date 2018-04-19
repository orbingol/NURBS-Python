"""
.. module:: exchange_helpers
    :platform: Unix, Windows
    :synopsis: CAD exchange and interoperability module for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import warnings
import struct

from . import Abstract
from . import Multi
from .elements import Vertex, Triangle


# Saves surface(s) as a .obj file
def save_obj(surf_in=None, file_name=None, **kwargs):
    """ Exports surface(s) as a .obj file.

    :param surf_in: surface or surfaces to be saved
    :type surf_in: Abstract.Surface or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str

    Keyword Arguments:
        * *vertex_spacing* (``int``): size of the triangle edge in terms of points sampled on the surface

    """
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    if isinstance(surf_in, Multi.MultiSurface):
        save_obj_multi(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
    else:
        save_obj_single(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)


# Saves surface(s) as a .stl file
def save_stl(surf_in=None, file_name=None, **kwargs):
    """ Exports surface(s) as a .stl file in plain text or binary format.

    :param surf_in: surface or surfaces to be saved
    :type surf_in: Abstract.Surface or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str

    Keyword Arguments:
        * *binary* (``bool``): True if the saved STL file is going to be in binary format
        * *vertex_spacing* (``int``): size of the triangle edge in terms of points sampled on the surface

    """
    binary = kwargs.get('binary', True)
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    if isinstance(surf_in, Multi.MultiSurface):
        if binary:
            save_stl_binary_multi(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
        else:
            save_stl_ascii_multi(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
    else:
        if binary:
            save_stl_binary_single(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
        else:
            save_stl_ascii_single(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)


# Saves surface(s) as a .off file
def save_off(surf_in=None, file_name=None, **kwargs):
    """ Exports surface(s) as a .off file.

    :param surf_in: surface or surfaces to be saved
    :type surf_in: Abstract.Surface or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str

    Keyword Arguments:
        * *vertex_spacing* (``int``): size of the triangle edge in terms of points sampled on the surface

    """
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    if isinstance(surf_in, Multi.MultiSurface):
        save_off_multi(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
    else:
        save_off_single(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)


# Generates triangles
def _gen_triangles_vertices(points, row_size, col_size, vertex_spacing):
    points2d = []
    for i in range(0, col_size):
        row_list = []
        for j in range(0, row_size):
            row_list.append(points[j + (i * row_size)])
        points2d.append(row_list)

    u_range = 1.0 / float(col_size - 1)
    v_range = 1.0 / float(row_size - 1)
    vertices = []
    vert_id = 1
    u = 0.0
    for col_idx in range(0, col_size, vertex_spacing):
        vert_list = []
        v = 0.0
        for row_idx in range(0, row_size, vertex_spacing):
            temp = Vertex()
            temp.data = points2d[col_idx][row_idx]
            temp.id = vert_id
            temp.uv = [u, v]
            vert_list.append(temp)
            vert_id += 1
            v += v_range
        vertices.append(vert_list)
        u += u_range

    v_col_size = len(vertices)
    v_row_size = len(vert_list)

    tri_id = 1
    forward = True
    triangles = []
    for col_idx in range(0, v_col_size - 1):
        row_idx = 0
        left_half = True
        tri_list = []
        while row_idx < v_row_size - 1:
            tri = Triangle()
            if left_half:
                tri.add_vertex(vertices[col_idx + 1][row_idx])
                tri.add_vertex(vertices[col_idx][row_idx])
                tri.add_vertex(vertices[col_idx][row_idx + 1])
                left_half = False
            else:
                tri.add_vertex(vertices[col_idx][row_idx + 1])
                tri.add_vertex(vertices[col_idx + 1][row_idx + 1])
                tri.add_vertex(vertices[col_idx + 1][row_idx])
                left_half = True
                row_idx += 1
            tri.id = tri_id
            tri_list.append(tri)
            tri_id += 1
        if forward:
            forward = False
        else:
            forward = True
            tri_list.reverse()
        triangles += tri_list

    return vertices, triangles


def save_obj_single(surface=None, **kwargs):
    """ Saves a single surface as a .obj file.

    :param surface: surface to be saved
    :type surface: Abstract.Surface

    Keyword Arguments:
        * file_name (str): name of the output file
        * vertex_spacing (int): size of the triangle edge in terms of points sampled on the surface

    """
    # Get keyword arguments
    file_name = kwargs.get('file_name', 'default.obj')
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    # Input validity checking
    if not isinstance(surface, Abstract.Surface):
        raise ValueError("Input is not a surface")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    try:
        with open(file_name, 'w') as fp:
            fp.write("# Generated by NURBS-Python\n")
            vertices, triangles = _gen_triangles_vertices(surface.surfpts,
                                                          surface.sample_size, surface.sample_size,
                                                          vertex_spacing)

            # Write vertices
            for vert_row in vertices:
                for vert in vert_row:
                    line = "v " + str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
                    fp.write(line)

            # Write vertex normals
            for vert_row in vertices:
                for vert in vert_row:
                    sn = surface.normal(vert.uv[0], vert.uv[1], True)
                    line = "vn " + str(sn[1][0]) + " " + str(sn[1][1]) + " " + str(sn[1][2]) + "\n"
                    fp.write(line)

            # Write faces
            for t in triangles:
                vl = t.vertex_ids
                line = "f " + str(vl[0]) + " " + str(vl[1]) + " " + str(vl[2]) + "\n"
                fp.write(line)
    except IOError:
        print("Cannot open " + str(file_name) + " for writing")


def save_obj_multi(surface_list=(), **kwargs):
    """ Saves multiple surfaces as a single .obj file.

    :param surface_list: list of surfaces to be saved
    :type surface_list: Multi.MultiSurface

    Keyword Arguments:
        * file_name (str): name of the output file
        * vertex_spacing (int): size of the triangle edge in terms of points sampled on the surface

    """
    # Get keyword arguments
    file_name = kwargs.get('file_name', 'default.obj')
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    # Input validity checking
    if not isinstance(surface_list, Multi.MultiSurface):
        raise ValueError("Input must be a list of surfaces")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    try:
        with open(file_name, 'w') as fp:
            fp.write("# Generated by NURBS-Python\n")
            vertex_offset = 0  # count the vertices to update the face numbers correctly

            # Initialize lists for vertices, vertex normals and faces
            str_v = []
            str_vn = []
            str_f = []

            # Loop through MultiSurface object
            for surface in surface_list:
                if not isinstance(surface, Abstract.Surface):
                    warnings.warn("Encountered a non-surface object")
                    continue

                # Set surface delta
                surface.delta = surface_list.delta

                # Generate triangles
                vertices, triangles = _gen_triangles_vertices(surface.surfpts,
                                                              surface.sample_size, surface.sample_size,
                                                              vertex_spacing)

                # Collect vertices
                for vert_row in vertices:
                    for vert in vert_row:
                        line = "v " + str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
                        str_v.append(line)

                # Collect vertex normals
                for vert_row in vertices:
                    for vert in vert_row:
                        sn = surface.normal(vert.uv[0], vert.uv[1], True)
                        line = "vn " + str(sn[1][0]) + " " + str(sn[1][1]) + " " + str(sn[1][2]) + "\n"
                        str_vn.append(line)

                # Collect faces
                for t in triangles:
                    vl = t.vertex_ids
                    line = "f " + \
                           str(vl[0] + vertex_offset) + " " + \
                           str(vl[1] + vertex_offset) + " " + \
                           str(vl[2] + vertex_offset) + "\n"
                    str_f.append(line)

                # Update vertex offset
                vertex_offset = len(str_v)

            # Write all collected data to the file
            for line in str_v:
                fp.write(line)
            for line in str_vn:
                fp.write(line)
            for line in str_f:
                fp.write(line)
    except IOError:
        print("Cannot open " + str(file_name) + " for writing")


def save_stl_ascii_single(surface=None, **kwargs):
    """ Saves a single surface as an ASCII .stl file.

    :param surface: surface to be saved
    :type surface: Abstract.Surface

    Keyword Arguments:
        * file_name (str): name of the output file
        * vertex_spacing (int): size of the triangle edge in terms of points sampled on the surface

    """
    # Get keyword arguments
    file_name = kwargs.get('file_name', 'default.stl')
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    # Input validity checking
    if not isinstance(surface, Abstract.Surface):
        raise ValueError("Input is not a surface")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    try:
        with open(file_name, 'w') as fp:
            vertices, triangles = _gen_triangles_vertices(surface.surfpts,
                                                          surface.sample_size, surface.sample_size,
                                                          vertex_spacing)

            fp.write("solid Surface\n")
            for t in triangles:
                line = "\tfacet normal " + str(t.normal[0]) + " " + str(t.normal[1]) + " " + str(t.normal[2]) + "\n"
                fp.write(line)
                fp.write("\t\touter loop\n")
                for v in t.vertices:
                    line = "\t\t\tvertex " + str(v.x) + " " + str(v.y) + " " + str(v.z) + "\n"
                    fp.write(line)
                fp.write("\t\tendloop\n")
                fp.write("\tendfacet\n")
            fp.write("endsolid Surface\n")
    except IOError:
        print("Cannot open " + str(file_name) + " for writing")


def save_stl_ascii_multi(surface_list=(), **kwargs):
    """ Saves multiple surfaces as an ASCII .stl file.

    :param surface_list: list of surfaces to be saved
    :type surface_list: Multi.MultiAbstract

    Keyword Arguments:
        * file_name (str): name of the output file
        * vertex_spacing (int): size of the triangle edge in terms of points sampled on the surface

    """
    # Get keyword arguments
    file_name = kwargs.get('file_name', 'default.stl')
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    # Input validity checking
    if not isinstance(surface_list, Abstract.Multi):
        raise ValueError("Input must be a list of surfaces")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    try:
        with open(file_name, 'w') as fp:
            fp.write("solid Surface\n")

            # Loop through MultiSurface object
            for surface in surface_list:
                if not isinstance(surface, Abstract.Surface):
                    warnings.warn("Encountered a non-surface object")
                    continue

                # Set surface delta
                surface.delta = surface_list.delta

                vertices, triangles = _gen_triangles_vertices(surface.surfpts,
                                                              surface.sample_size, surface.sample_size,
                                                              vertex_spacing)

                for t in triangles:
                    line = "\tfacet normal " + str(t.normal[0]) + " " + str(t.normal[1]) + " " + str(t.normal[2]) + "\n"
                    fp.write(line)
                    fp.write("\t\touter loop\n")
                    for v in t.vertices:
                        line = "\t\t\tvertex " + str(v.x) + " " + str(v.y) + " " + str(v.z) + "\n"
                        fp.write(line)
                    fp.write("\t\tendloop\n")
                    fp.write("\tendfacet\n")

            fp.write("endsolid Surface\n")
    except IOError:
        print("Cannot open " + str(file_name) + " for writing")


def save_stl_binary_single(surface=None, **kwargs):
    """ Saves a single surface as a binary .stl file.

    Inspired from https://github.com/apparentlymart/python-stl

    :param surface: surface to be saved
    :type surface: Abstract.Surface

    Keyword Arguments:
        * file_name (str): name of the output file
        * vertex_spacing (int): size of the triangle edge in terms of points sampled on the surface

    """
    # Get keyword arguments
    file_name = kwargs.get('file_name', 'default.stl')
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    # Input validity checking
    if not isinstance(surface, Abstract.Surface):
        raise ValueError("Input is not a surface")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    try:
        with open(file_name, 'wb') as fp:
            vertices, triangles = _gen_triangles_vertices(surface.surfpts,
                                                          surface.sample_size, surface.sample_size,
                                                          vertex_spacing)

            # Write triangle list to the binary STL file
            fp.write(b'\0' * 80)  # header
            fp.write(struct.pack('<i', len(triangles)))  # number of triangles
            for t in triangles:
                fp.write(struct.pack('<3f', *t.normal))  # normal
                for v in t.vertices:
                    fp.write(struct.pack('<3f', *v.data))  # vertices
                fp.write(b'\0\0')  # attribute byte count
    except IOError:
        print("Cannot open " + str(file_name) + " for writing")


def save_stl_binary_multi(surface_list=(), **kwargs):
    """ Saves multiple surfaces as a binary .stl file.

    :param surface_list: list of surfaces to be saved
    :type surface_list: Multi.MultiAbstract

    Keyword Arguments:
        * file_name (str): name of the output file
        * vertex_spacing (int): size of the triangle edge in terms of points sampled on the surface

    """
    # Get keyword arguments
    file_name = kwargs.get('file_name', 'default.stl')
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    # Input validity checking
    if not isinstance(surface_list, Abstract.Multi):
        raise ValueError("Input must be a list of surfaces")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    try:
        with open(file_name, 'wb') as fp:
            # Loop through MultiSurface object
            triangles_list = []
            for surface in surface_list:
                if not isinstance(surface, Abstract.Surface):
                    warnings.warn("Encountered a non-surface object")
                    continue

                # Set surface delta
                surface.delta = surface_list.delta

                vertices, triangles = _gen_triangles_vertices(surface.surfpts,
                                                              surface.sample_size, surface.sample_size,
                                                              vertex_spacing)
                triangles_list += triangles

            # Write triangle list to the binary STL file
            fp.write(b'\0' * 80)  # header
            fp.write(struct.pack('<i', len(triangles_list)))  # number of triangles
            for t in triangles_list:
                fp.write(struct.pack('<3f', *t.normal))  # normal
                for v in t.vertices:
                    fp.write(struct.pack('<3f', *v.data))  # vertices
                fp.write(b'\0\0')  # attribute byte count
    except IOError:
        print("Cannot open " + str(file_name) + " for writing")


def save_off_single(surface=None, **kwargs):
    """ Saves a single surface as a .off file.

    :param surface: surface to be saved
    :type surface: Abstract.Surface

    Keyword Arguments:
        * file_name (str): name of the output file
        * vertex_spacing (int): size of the triangle edge in terms of points sampled on the surface

    """
    # Get keyword arguments
    file_name = kwargs.get('file_name', 'default.off')
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    # Input validity checking
    if not isinstance(surface, Abstract.Surface):
        raise ValueError("Input is not a surface")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    try:
        with open(file_name, 'w') as fp:
            fp.write("OFF\n")
            vertices, triangles = _gen_triangles_vertices(surface.surfpts,
                                                          surface.sample_size, surface.sample_size,
                                                          vertex_spacing)

            line = str(len(vertices) * len(vertices[0])) + " " + str(len(triangles)) + " 0\n"
            fp.write(line)
            # Write vertices
            for vert_row in vertices:
                for vert in vert_row:
                    line = str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
                    fp.write(line)

            # Write faces (zero-indexed)
            for t in triangles:
                vl = t.vertex_ids
                line = "3 " + str(vl[0] - 1) + " " + str(vl[1] - 1) + " " + str(vl[2] - 1) + "\n"
                fp.write(line)
    except IOError:
        print("Cannot open " + str(file_name) + " for writing")


def save_off_multi(surface_list=(), **kwargs):
    """ Saves multiple surfaces as a single .off file.

    :param surface_list: list of surfaces to be saved
    :type surface_list: Multi.MultiSurface

    Keyword Arguments:
        * file_name (str): name of the output file
        * vertex_spacing (int): size of the triangle edge in terms of points sampled on the surface

    """
    # Get keyword arguments
    file_name = kwargs.get('file_name', 'default.off')
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    # Input validity checking
    if not isinstance(surface_list, Multi.MultiSurface):
        raise ValueError("Input must be a list of surfaces")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    try:
        with open(file_name, 'w') as fp:
            vertex_offset = 0  # count the vertices to update the face numbers correctly

            # Initialize lists for vertices, vertex normals and faces
            str_v = []
            str_f = []

            # Loop through MultiSurface object
            for surface in surface_list:
                if not isinstance(surface, Abstract.Surface):
                    warnings.warn("Encountered a non-surface object")
                    continue

                # Set surface delta
                surface.delta = surface_list.delta

                # Generate triangles
                vertices, triangles = _gen_triangles_vertices(surface.surfpts,
                                                              surface.sample_size, surface.sample_size,
                                                              vertex_spacing)

                # Collect vertices
                for vert_row in vertices:
                    for vert in vert_row:
                        line = str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
                        str_v.append(line)

                # Collect faces (zero0indexed)
                for t in triangles:
                    vl = t.vertex_ids
                    line = "3 " + \
                           str(vl[0] - 1 + vertex_offset) + " " + \
                           str(vl[1] - 1 + vertex_offset) + " " + \
                           str(vl[2] - 1 + vertex_offset) + "\n"
                    str_f.append(line)

                # Update vertex offset
                vertex_offset = len(str_v)

            # Write file header
            fp.write("OFF\n")
            fp.write(str(len(str_v)) + " " + str(len(str_f)) + " 0\n")

            # Write all collected data to the file
            for line in str_v:
                fp.write(line)
            for line in str_f:
                fp.write(line)
    except IOError:
        print("Cannot open " + str(file_name) + " for writing")
