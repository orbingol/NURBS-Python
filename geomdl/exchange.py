"""
.. module:: exchange
    :platform: Unix, Windows
    :synopsis: CAD exchange and interoperability module for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import os
from . import warnings
from . import struct
from . import Abstract
from . import NURBS
from . import Multi
from . import compatibility
from . import operations
from . import utilities


def import_txt(file_name, two_dimensional=False, **kwargs):
    """ Reads control points from a text file and generates a 1-D list of control points.

    The following code examples illustrate importing different types of text files for curves and surfaces:

    .. code-block:: python

        # Import curve control points from a text file
        curve_ctrlpts = exchange.import_txt(file_name="control_points.txt")

        # Import surface control points from a text file (1-dimensional file)
        surf_ctrlpts = exchange.import_txt(file_name="control_points.txt")

        # Import surface control points from a text file (2-dimensional file)
        surf_ctrlpts, size_u, size_v = exchange.import_txt(file_name="control_points.txt", two_dimensional=True)

    You may set the file delimiters using the keyword arguments ``separator`` and ``col_separator``, respectively.
    ``separator`` is the delimiter between the coordinates of the control points. It could be comma
    ``1, 2, 3`` or space ``1 2 3`` or something else. ``col_separator`` is the delimiter between the control
    points and is only valid when ``two_dimensional`` is ``True``. Assuming that ``separator`` is set to space, then
    ``col_operator`` could be semi-colon ``1 2 3; 4 5 6`` or pipe ``1 2 3| 4 5 6`` or comma ``1 2 3, 4 5 6`` or
    something else.

    The defaults for ``separator`` and ``col_separator`` are *comma (,)* and *semi-colon (;)*, respectively.

    The following code examples illustrate the usage of the keyword arguments discussed above.

    .. code-block:: python

        # Import curve control points from a text file delimited with space
        curve_ctrlpts = exchange.import_txt(file_name="control_points.txt", separator=" ")

        # Import surface control points from a text file (2-dimensional file) w/ space and comma delimiters
        surf_ctrlpts, size_u, size_v = exchange.import_txt(file_name="control_points.txt", two_dimensional=True,
                                                           separator=" ", col_separator=",")

    Please note that this function does not check whether the user set delimiters to the same value or not.

    :param file_name: file name of the text file
    :type file_name: str
    :param two_dimensional: type of the text file
    :type two_dimensional: bool
    :return: list of control points, if two_dimensional, then also returns size in u- and v-directions
    :rtype: list
    :raises IOError: an error occurred reading the file
    """
    # File delimiters
    col_sep = kwargs.get('col_separator', ";")
    sep = kwargs.get('separator', ",")

    # Initialize an empty list to store control points
    ctrlpts = []

    # Try opening the file for reading
    try:
        with open(file_name, 'r') as fp:
                if two_dimensional:
                    # Start reading file
                    size_u = 0
                    size_v = 0
                    for line in fp:
                        # Remove whitespace
                        line = line.strip()
                        # Convert the string containing the coordinates into a list
                        control_point_row = line.split(col_sep)
                        # Clean and convert the values
                        size_v = 0
                        for cpr in control_point_row:
                            ctrlpts.append([float(c.strip()) for c in cpr.split(sep)])
                            size_v += 1
                        size_u += 1

                    # Return control points, size in u- and v-directions
                    return ctrlpts, size_u, size_v
                else:
                    # Start reading file
                    for line in fp:
                        # Remove whitespace
                        line = line.strip()
                        # Clean and convert the values
                        ctrlpts.append([float(c.strip()) for c in line.split(sep)])

                    # Return control points
                    return ctrlpts
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def export_txt(obj, file_name, two_dimensional=False, **kwargs):
    """ Saves control points to a text file.

    For curves the output is always a list of control points. For surfaces, it is possible to generate a 2-D control
    point output file using ``two_dimensional`` flag. Please see the supported file formats for more details on the
    text file format.

    Please see :py:func:`.exchange.import_txt()` for detailed description of the keyword arguments.

    :param obj: a curve or a surface object
    :type obj: Abstract.Curve, Abstract.Surface
    :param file_name: file name of the text file to be saved
    :type file_name: str
    :param two_dimensional: type of the text file (only works for Surface objects)
    :type two_dimensional: bool
    :raises IOError: an error occurred writing the file
    """
    # Check if the user has set any control points
    if obj.ctrlpts is None or len(obj.ctrlpts) == 0:
        warnings.warn("There are no control points to save!")
        return

    # Check the usage of two_dimensional flag
    if isinstance(obj, Abstract.Curve) and two_dimensional:
        warnings.warn("Ignoring two_dimensional flag since it only makes difference with surface objects...")
        two_dimensional = False

    # File delimiters
    col_sep = kwargs.get('col_separator', ";")
    sep = kwargs.get('separator', ",")

    # Try opening the file for writing
    try:
        with open(file_name, 'w') as fp:
            if two_dimensional:
                for i in range(0, obj.ctrlpts_size_u):
                    line = ""
                    for j in range(0, obj.ctrlpts_size_v):
                        for idx, coord in enumerate(obj.ctrlpts2d[i][j]):
                            if idx:  # check for the first element
                                line += sep
                            line += str(coord)
                        if j != obj.ctrlpts_size_v - 1:
                            line += col_sep
                        else:
                            line += "\n"
                    fp.write(line)
            else:
                for pt in obj.ctrlpts:
                    line = sep.join(str(c) for c in pt) + "\n"
                    fp.write(line)
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def export_csv(obj, file_name, point_type='evalpts'):
    """ Exports control points or evaluated points as a CSV file.

    :param obj: a curve or a surface object
    :type obj: Abstract.Curve, Abstract.Surface
    :param file_name: output file name
    :type file_name: str
    :param point_type: ``ctrlpts`` for control points or ``evalpts`` for evaluated points
    :type point_type: str
    :raises IOError: an error occurred writing the file
    """
    if not isinstance(obj, (Abstract.Curve, Abstract.Surface)):
        raise ValueError("Input object should be a curve or a surface")

    # Pick correct points from the object
    if point_type == 'ctrlpts':
        points = obj.ctrlpts
    elif point_type == 'evalpts' or point_type == 'curvepts' or point_type == 'surfpts':
        points = obj.evalpts
    else:
        warnings.warn("Please choose a valid point type option")
        return

    # Prepare CSV header
    dim = len(points[0])
    header = "dim "
    for i in range(dim-1):
        header += str(i + 1) + ", dim "
    header += str(dim) + "\n"

    # Try opening the file for writing
    try:
        with open(file_name, 'w') as fp:
            # Write header to the file
            fp.write(header)

            # Loop through points
            for pt in points:
                # Fill coordinates
                line = ", ".join(str(c) for c in pt) + "\n"
                # Write line to file
                fp.write(line)
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def export_vtk(obj, file_name, point_type='evalpts'):
    """ Exports control points or evaluated points as a VTK file (legacy format).

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    :param obj: a curve or a surface object
    :type obj: Abstract.Curve, Abstract.Surface
    :param file_name: output file name
    :type file_name: str
    :param point_type: ``ctrlpts`` for control points or ``evalpts`` for evaluated points
    :type point_type: str
    :raises IOError: an error occurred writing the file
    """
    if not isinstance(obj, (Abstract.Curve, Abstract.Surface)):
        raise ValueError("Input object should be a curve or a surface")

    # Pick correct points from the object
    if point_type == 'ctrlpts':
        points = obj.ctrlpts
    elif point_type == 'evalpts' or point_type == 'curvepts' or point_type == 'surfpts':
        points = obj.evalpts
    else:
        warnings.warn("Please choose a valid point type option")
        return

    # Try opening the file for writing
    try:
        with open(file_name, 'w') as fp:
            # Write header to the file
            fp.write("# vtk DataFile Version 3.0\n")
            fp.write(repr(obj) + "\n")
            fp.write("ASCII\nDATASET POLYDATA\n")
            fp.write("POINTS " + str(len(points)) + " FLOAT\n")

            # Loop through points
            for pt in points:
                line = " ".join(str(c) for c in pt) + "\n"
                fp.write(line)
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def export_cfg(obj, file_name):
    """ Exports curves and surfaces in libconfig format.

    :param obj: input curve or surface
    :type obj: Abstract.Curve or Abstract.Surface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """

    if isinstance(obj, Abstract.Curve):
        _export_cfg_single(obj, file_name, _prepare_cfg_export_curve)
    elif isinstance(obj, Abstract.Surface):
        _export_cfg_single(obj, file_name, _prepare_cfg_export_surface)
    elif isinstance(obj, Multi.MultiCurve):
        _export_cfg_multi(obj, file_name, _prepare_cfg_export_curve)
    elif isinstance(obj, Multi.MultiSurface):
        _export_cfg_multi(obj, file_name, _prepare_cfg_export_surface)
    else:
        raise NotImplementedError("Cannot export " + obj.__class__.__name__ + " type in libconfig format")


def _export_cfg_single(obj, file_name, func):
    try:
        with open(file_name, 'w') as fp:
            # File header
            fp.write("# Generated by NURBS-Python\n")
            fp.write("# file: " + file_name + "\n\n")

            # Number of shapes is always 1 in this case
            fp.write("count: 1;\n\n")

            # Start listing
            fp.write("shapes: \n(\n\n")
            fp.write("{\n")

            # Write object properties
            fp.write(func(obj))

            # End listing
            fp.write("}\n\n")
            fp.write(");\n")
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _export_cfg_multi(obj, file_name, func):
    try:
        with open(file_name, 'w') as fp:
            # File header
            fp.write("# Generated by NURBS-Python\n")
            fp.write("# file: " + file_name + "\n\n")

            # Number of shapes in the container
            cont_sz = len(obj)
            fp.write("count: " + str(cont_sz) + ";\n\n")

            # Start listing
            fp.write("shapes: \n(\n\n")

            # Write object properties
            for idx, shp in enumerate(obj):
                fp.write("{\n")
                fp.write(func(shp))
                fp.write("}" + ("" if idx == cont_sz - 1 else ",") + "\n\n")

            # End listing
            fp.write(");\n")
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _prepare_cfg_export_curve(obj):
    """ Prepares curve object for libconfig-type export.

    :param obj: curve object
    :return: curve data as a string
    """
    line = ""

    # Start exporting object
    line += "\ttype = \"curve\";\n"
    line += "\tdegree = " + str(obj.degree) + ";\n"
    line += "\tknotvector = [" + ", ".join(str(kv) for kv in obj.knotvector) + "];\n"
    line += "\tcontrol_points = ("
    ctrlpts_size = len(obj.ctrlpts)
    for idx, pt in enumerate(obj.ctrlpts):
        line += " (" + ", ".join(str(p) for p in pt) + ")"
        line += " " if idx == ctrlpts_size - 1 else ","
    line += ");\n"
    try:
        line += "\tweights = [" + ", ".join(str(w) for w in obj.weights) + "];\n"
    except AttributeError:
        line += "\tweights = 0;\n"

    # Export misc info
    line += "\tmisc: \n\t{\n"
    line += "\t\tname = \"" + obj.name + "\";\n"
    line += "\t\tsample_size = " + str(obj.sample_size) + ";\n"
    line += "\t};\n"

    return line


def _prepare_cfg_export_surface(obj):
    """ Prepares surface object for libconfig-type export.

    :param obj: surface object
    :return: surface data as a string
    """
    line = ""

    # Start exporting object
    line += "\ttype = \"surface\";\n"
    line += "\tdegree_u = " + str(obj.degree_u) + ";\n"
    line += "\tdegree_v = " + str(obj.degree_v) + ";\n"
    line += "\tknotvector_u = [" + ", ".join(str(kv) for kv in obj.knotvector_u) + "];\n"
    line += "\tknotvector_v = [" + ", ".join(str(kv) for kv in obj.knotvector_v) + "];\n"
    line += "\tcontrol_points_size_u = " + str(obj.ctrlpts_size_u) + ";\n"
    line += "\tcontrol_points_size_v = " + str(obj.ctrlpts_size_v) + ";\n"
    line += "\tcontrol_points = ("
    ctrlpts_size = len(obj.ctrlpts)
    for idx, pt in enumerate(obj.ctrlpts):
        line += " (" + ", ".join(str(p) for p in pt) + ")"
        line += " " if idx == ctrlpts_size - 1 else ","
    line += ");\n"
    try:
        line += "\tweights = [" + ", ".join(str(w) for w in obj.weights) + "];\n"
    except AttributeError:
        line += "\tweights = 0;\n"

    # Export misc info
    line += "\tmisc: \n\t{\n"
    line += "\t\tname = \"" + obj.name + "\";\n"
    line += "\t\tsample_size_u = " + str(obj.sample_size_u) + ";\n"
    line += "\t\tsample_size_v = " + str(obj.sample_size_v) + ";\n"
    line += "\t};\n"

    return line


def import_cfg(file_name):
    """ Imports curves and surfaces from files in libconfig format.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of NURBS curve(s) or surface(s)
    :rtype: list
    :raises ImportError: cannot find 'libconf' module
    :raises IOError: an error occurred writing the file
    """
    # Check if it is possible to import 'libconf'
    try:
        import libconf
    except ImportError as e:
        print("Please install 'libconf' module to import from libconfig format: pip install libconf")
        raise e

    type_map = {'curve': _prepare_cfg_import_curve, 'surface': _prepare_cfg_import_surface}

    # Try to read the input file
    try:
        with open(file_name, 'r') as fp:
            # Get all shapes
            imported_data = libconf.load(fp)

            # Process imported data
            ret_list = []
            for data in imported_data.shapes:
                temp = type_map[data.type](data)
                ret_list.append(temp)

            # Return processed data
            return ret_list
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _prepare_cfg_import_curve(data):
    shape = NURBS.Curve()
    shape.degree = data.degree
    shape.ctrlpts = data.control_points
    if isinstance(data.weights, (list, tuple)):
        shape.weights = data.weights
    shape.knotvector = data.knotvector
    return shape


def _prepare_cfg_import_surface(data):
    shape = NURBS.Surface()
    shape.degree_u = data.degree_u
    shape.degree_v = data.degree_v
    shape.ctrlpts_size_u = data.control_points_size_u
    shape.ctrlpts_size_v = data.control_points_size_v
    shape.ctrlpts = data.control_points
    if isinstance(data.weights, (list, tuple)):
        shape.weights = data.weights
    shape.knotvector_u = data.knotvector_u
    shape.knotvector_v = data.knotvector_v
    return shape


def export_obj(surf_in, file_name, **kwargs):
    """ Exports surface(s) as a .obj file.

    Keyword Arguments:
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 2*

    :param surf_in: surface or surfaces to be saved
    :type surf_in: Abstract.Surface or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    if isinstance(surf_in, Multi.MultiSurface):
        _export_obj_multi(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
    else:
        _export_obj_single(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)


def export_stl(surf_in, file_name, **kwargs):
    """ Exports surface(s) as a .stl file in plain text or binary format.

    Keyword Arguments:
        * ``binary``: flag to generate a binary STL file. *Default: True*
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 2*

    :param surf_in: surface or surfaces to be saved
    :type surf_in: Abstract.Surface or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    binary = kwargs.get('binary', True)
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    if isinstance(surf_in, Multi.MultiSurface):
        if binary:
            _export_stl_binary_multi(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
        else:
            _export_stl_ascii_multi(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
    else:
        if binary:
            _export_stl_binary_single(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
        else:
            _export_stl_ascii_single(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)


def export_off(surf_in, file_name, **kwargs):
    """ Exports surface(s) as a .off file.

    Keyword Arguments:
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 2*

    :param surf_in: surface or surfaces to be saved
    :type surf_in: Abstract.Surface or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    vertex_spacing = kwargs.get('vertex_spacing', 2)

    if isinstance(surf_in, Multi.MultiSurface):
        _export_off_multi(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)
    else:
        _export_off_single(surf_in, file_name=file_name, vertex_spacing=vertex_spacing)


def import_smesh(file):
    """ Generates NURBS surface(s) from smesh file(s).

    *smesh* files are some text files which contain a set of NURBS surfaces. Each file in the set corresponds to one
    NURBS surface. Most of the time, you receive multiple *smesh* files corresponding to an complete object composed of
    several NURBS surfaces. The files have the extensions of ``txt`` or ``dat`` and they are named as

    * ``smesh.X.Y.txt``
    * ``smesh.X.dat``

    where *X* and *Y* correspond to some integer value which defines the set the surface belongs to and part number of
    the surface inside the complete object.

    :param file: path to a directory containing smesh files or a single smesh file
    :type file: str
    :return: NURBS surface(s)
    :rtype: NURBS.Surface or Multi.MultiSurface
    :raises IOError: an error occurred reading the file
    """
    if os.path.isfile(file):
        return _import_smesh_single(file)
    elif os.path.isdir(file):
        return _import_smesh_multi(file)
    else:
        raise IOError("Input is not a file or a directory")


def _export_obj_single(surface, **kwargs):
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
            vertices, triangles = utilities.make_triangle(surface.evalpts,
                                                          surface.sample_size_u, surface.sample_size_v,
                                                          vertex_spacing=vertex_spacing)

            # Write vertices
            for vert_row in vertices:
                for vert in vert_row:
                    line = "v " + str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
                    fp.write(line)

            # Write vertex normals
            for vert_row in vertices:
                for vert in vert_row:
                    sn = operations.normal(surface, vert.uv)
                    line = "vn " + str(sn[1][0]) + " " + str(sn[1][1]) + " " + str(sn[1][2]) + "\n"
                    fp.write(line)

            # Write faces
            for t in triangles:
                vl = t.vertex_ids
                line = "f " + str(vl[0]) + " " + str(vl[1]) + " " + str(vl[2]) + "\n"
                fp.write(line)
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _export_obj_multi(surface_list, **kwargs):
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

                # Set surface evaluation delta
                if surface_list.sample_size_u != 0:
                    surface.sample_size_u = surface_list.sample_size_u
                if surface_list.sample_size_v != 0:
                    surface.sample_size_v = surface_list.sample_size_v

                # Generate triangles
                vertices, triangles = utilities.make_triangle(surface.evalpts,
                                                              surface.sample_size_u, surface.sample_size_v,
                                                              vertex_spacing=vertex_spacing)

                # Collect vertices
                for vert_row in vertices:
                    for vert in vert_row:
                        line = "v " + str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
                        str_v.append(line)

                # Collect vertex normals
                for vert_row in vertices:
                    for vert in vert_row:
                        sn = operations.normal(surface, vert.uv)
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
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _export_stl_ascii_single(surface, **kwargs):
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
            vertices, triangles = utilities.make_triangle(surface.evalpts,
                                                          surface.sample_size_u, surface.sample_size_v,
                                                          vertex_spacing=vertex_spacing)

            fp.write("solid Surface\n")
            for t in triangles:
                nvec = utilities.triangle_normal(t)
                line = "\tfacet normal " + str(nvec[0]) + " " + str(nvec[1]) + " " + str(nvec[2]) + "\n"
                fp.write(line)
                fp.write("\t\touter loop\n")
                for v in t.vertices:
                    line = "\t\t\tvertex " + str(v.x) + " " + str(v.y) + " " + str(v.z) + "\n"
                    fp.write(line)
                fp.write("\t\tendloop\n")
                fp.write("\tendfacet\n")
            fp.write("endsolid Surface\n")
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _export_stl_ascii_multi(surface_list, **kwargs):
    """ Saves multiple surfaces as an ASCII .stl file.

    :param surface_list: list of surfaces to be saved
    :type surface_list: Multi.MultiSurface

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

                # Set surface evaluation delta
                if surface_list.sample_size_u != 0:
                    surface.sample_size_u = surface_list.sample_size_u
                if surface_list.sample_size_v != 0:
                    surface.sample_size_v = surface_list.sample_size_v

                vertices, triangles = utilities.make_triangle(surface.evalpts,
                                                              surface.sample_size_u, surface.sample_size_v,
                                                              vertex_spacing=vertex_spacing)

                for t in triangles:
                    nvec = utilities.triangle_normal(t)
                    line = "\tfacet normal " + str(nvec[0]) + " " + str(nvec[1]) + " " + str(nvec[2]) + "\n"
                    fp.write(line)
                    fp.write("\t\touter loop\n")
                    for v in t.vertices:
                        line = "\t\t\tvertex " + str(v.x) + " " + str(v.y) + " " + str(v.z) + "\n"
                        fp.write(line)
                    fp.write("\t\tendloop\n")
                    fp.write("\tendfacet\n")

            fp.write("endsolid Surface\n")
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _export_stl_binary_single(surface, **kwargs):
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
            vertices, triangles = utilities.make_triangle(surface.evalpts,
                                                          surface.sample_size_u, surface.sample_size_v,
                                                          vertex_spacing=vertex_spacing)

            # Write triangle list to the binary STL file
            fp.write(b'\0' * 80)  # header
            fp.write(struct.pack('<i', len(triangles)))  # number of triangles
            for t in triangles:
                fp.write(struct.pack('<3f', *utilities.triangle_normal(t)))  # normal
                for v in t.vertices:
                    fp.write(struct.pack('<3f', *v.data))  # vertices
                fp.write(b'\0\0')  # attribute byte count
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _export_stl_binary_multi(surface_list, **kwargs):
    """ Saves multiple surfaces as a binary .stl file.

    :param surface_list: list of surfaces to be saved
    :type surface_list: Multi.MultiSurface

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

                # Set surface evaluation delta
                if surface_list.sample_size_u != 0:
                    surface.sample_size_u = surface_list.sample_size_u
                if surface_list.sample_size_v != 0:
                    surface.sample_size_v = surface_list.sample_size_v

                vertices, triangles = utilities.make_triangle(surface.evalpts,
                                                              surface.sample_size_u, surface.sample_size_v,
                                                              vertex_spacing=vertex_spacing)
                triangles_list += triangles

            # Write triangle list to the binary STL file
            fp.write(b'\0' * 80)  # header
            fp.write(struct.pack('<i', len(triangles_list)))  # number of triangles
            for t in triangles_list:
                fp.write(struct.pack('<3f', *utilities.triangle_normal(t)))  # normal
                for v in t.vertices:
                    fp.write(struct.pack('<3f', *v.data))  # vertices
                fp.write(b'\0\0')  # attribute byte count
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _export_off_single(surface, **kwargs):
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
            vertices, triangles = utilities.make_triangle(surface.evalpts,
                                                          surface.sample_size_u, surface.sample_size_v,
                                                          vertex_spacing=vertex_spacing)

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
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _export_off_multi(surface_list, **kwargs):
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

                # Set surface evaluation delta
                if surface_list.sample_size_u != 0:
                    surface.sample_size_u = surface_list.sample_size_u
                if surface_list.sample_size_v != 0:
                    surface.sample_size_v = surface_list.sample_size_v

                # Generate triangles
                vertices, triangles = utilities.make_triangle(surface.evalpts,
                                                              surface.sample_size_u, surface.sample_size_v,
                                                              vertex_spacing=vertex_spacing)

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
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _import_smesh_single(file_name):
    """ Generates a NURBS surface from a smesh file.

    :param file_name: smesh file to read
    :type file_name: str
    :return: a NURBS surface
    :rtype: NURBS.Surface
    """
    try:
        with open(file_name, 'r') as fp:
            content = fp.readlines()
            content = [x.strip().split() for x in content]
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise

    # 1st line defines the dimension and it must be 3
    if int(content[0][0]) != 3:
        warnings.warn("Input smesh file" + str(file_name) + " is not a surface", UserWarning)
        return

    # Create a NURBS surface instance and fill with the data read from smesh file
    surf = NURBS.Surface()

    # 2nd line is the degrees
    surf.degree_u = int(content[1][0])
    surf.degree_v = int(content[1][1])

    # 3rd line is the number of weighted control points in u and v directions
    dim_u = int(content[2][0])
    dim_v = int(content[2][1])
    ctrlpts_end = 5 + (dim_u * dim_v)

    # Starting from 6th line, we have the weighted control points
    ctrlpts_smesh = content[5:ctrlpts_end]

    # smesh files have the control points in u-row order format
    ctrlpts = compatibility.flip_ctrlpts_u(ctrlpts_smesh, dim_u, dim_v)

    # smesh files store control points in format (x, y, z, w) -- Rhino format
    ctrlptsw = compatibility.generate_ctrlptsw(ctrlpts)

    # Set control points
    surf.set_ctrlpts(ctrlptsw, dim_u, dim_v)

    # 4th and 5th lines are knot vectors
    surf.knotvector_u = [float(u) for u in content[3]]
    surf.knotvector_v = [float(v) for v in content[4]]

    # Return the surface instance
    return surf


def _import_smesh_multi(file_path):
    """ Generates NURBS surfaces from smesh files contained in the input directory.

    :param file_path: path to the directory containing smesh files
    :type file_path: str
    :return: a MultiSurface instance containing all NURBS surfaces
    :rtype: Multi.MultiSurface
    """
    files = sorted([os.path.join(file_path, f) for f in os.listdir(file_path)])
    surf = Multi.MultiSurface()
    for f in files:
        surf.add(_import_smesh_single(f))
    return surf
