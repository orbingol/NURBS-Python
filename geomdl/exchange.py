"""
.. module:: exchange
    :platform: Unix, Windows
    :synopsis: CAD exchange and interoperability module for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import os
import struct
import json
from . import abstract
from . import BSpline
from . import NURBS
from . import multi
from . import compatibility
from . import operations
from . import utilities
from . import convert


def import_txt(file_name, two_dimensional=False, **kwargs):
    """ Reads control points from a text file and generates a 1-dimensional list of control points.

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
    # Read file
    content = _read_file(file_name)

    # File delimiters
    col_sep = kwargs.get('col_separator', ";")
    sep = kwargs.get('separator', ",")

    return _import_text_data(content, sep, col_sep, two_dimensional)


def export_txt(obj, file_name, two_dimensional=False, **kwargs):
    """ Exports control points as a text file.

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
        raise ValueError("There are no control points to save!")

    # Check the usage of two_dimensional flag
    if isinstance(obj, abstract.Curve) and two_dimensional:
        # Silently ignore two_dimensional flag
        two_dimensional = False

    # File delimiters
    col_sep = kwargs.get('col_separator', ";")
    sep = kwargs.get('separator', ",")

    content = _export_text_data(obj, sep, col_sep, two_dimensional)
    return _write_file(file_name, content)


def import_csv(file_name, **kwargs):
    """ Reads control points from a CSV file and generates a 1-dimensional list of control points.

    It is possible to use a different value separator via ``separator`` keyword argument. The following code segment
    illustrates the usage of ``separator`` keyword argument.

    .. code-block:: python

        # By default, import_csv uses 'comma' as the value separator
        ctrlpts = exchange.import_csv("control_points.csv")

        # Alternatively, it is possible to import a file containing tab-separated values
        ctrlpts = exchange.import_csv("control_points.csv", separator="\\t")

    The only difference of this function from :py:func:`.exchange.import_txt()` is skipping the first line of the input
    file which generally contains the column headings.

    :param file_name: file name of the text file
    :type file_name: str
    :return: list of control points
    :rtype: list
    :raises IOError: an error occurred reading the file
    """
    # File delimiters
    sep = kwargs.get('separator', ",")

    content = _read_file(file_name, skip_lines=1)
    return _import_text_data(content, sep)


def export_csv(obj, file_name, point_type='evalpts', **kwargs):
    """ Exports control points or evaluated points as a CSV file.

    :param obj: a curve or a surface object
    :type obj: Abstract.Curve, Abstract.Surface
    :param file_name: output file name
    :type file_name: str
    :param point_type: ``ctrlpts`` for control points or ``evalpts`` for evaluated points
    :type point_type: str
    :raises IOError: an error occurred writing the file
    """
    if not isinstance(obj, (abstract.Curve, abstract.Surface)):
        raise ValueError("Input object should be a curve or a surface")

    # Pick correct points from the object
    if point_type == 'ctrlpts':
        points = obj.ctrlpts
    elif point_type == 'evalpts' or point_type == 'curvepts' or point_type == 'surfpts':
        points = obj.evalpts
    else:
        raise ValueError("Please choose a valid point type option. Possible types: ctrlpts, evalpts")

    # Prepare CSV header
    dim = len(points[0])
    line = "dim "
    for i in range(dim-1):
        line += str(i + 1) + ", dim "
    line += str(dim) + "\n"

    # Prepare values
    for pt in points:
        line += ",".join([str(p) for p in pt]) + "\n"

    # Write to file
    return _write_file(file_name, line)


def export_vtk(obj, file_name, point_type='evalpts'):
    """ Exports control points or evaluated points in legacy VTK format.

    Please see the following document for details: http://www.vtk.org/VTK/img/file-formats.pdf

    :param obj: a curve or a surface object
    :type obj: Abstract.Curve, Abstract.Surface
    :param file_name: output file name
    :type file_name: str
    :param point_type: ``ctrlpts`` for control points or ``evalpts`` for evaluated points
    :type point_type: str
    :raises IOError: an error occurred writing the file
    """
    if not isinstance(obj, (abstract.Curve, abstract.Surface)):
        raise ValueError("Input object should be a curve or a surface")

    # Pick correct points from the object
    if point_type == 'ctrlpts':
        points = obj.ctrlpts
    elif point_type == 'evalpts' or point_type == 'curvepts' or point_type == 'surfpts':
        points = obj.evalpts
    else:
        raise ValueError("Please choose a valid point type option. Possible types: ctrlpts, evalpts")

    # Prepare header
    line = "# vtk DataFile Version 3.0\n"
    line += repr(obj) + "\n"
    line += "ASCII\nDATASET POLYDATA\n"
    line += "POINTS " + str(len(points)) + " FLOAT\n"

    # Prepare values
    for pt in points:
        line += " ".join(str(c) for c in pt) + "\n"

    # Write to file
    return _write_file(file_name, line)


def import_cfg(file_name, **kwargs):
    """ Imports curves and surfaces from files in libconfig format.

    .. note::

        Requires `libconf <https://pypi.org/project/libconf/>`_ package.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of NURBS curve(s) or surface(s)
    :rtype: list
    :raises IOError: an error occurred writing the file
    """
    def callback(fp):
        return libconf.load(fp)

    # Check if it is possible to import 'libconf'
    try:
        import libconf
    except ImportError:
        print("Please install 'libconf' module to use libconfig format: pip install libconf")
        return

    # Get keyword arguments
    delta = kwargs.get('delta', -1.0)

    # Import data
    return _import_dict_all(file_name, delta, callback)


def export_cfg(obj, file_name):
    """ Exports curves and surfaces in libconfig format.

    .. note::

        Requires `libconf <https://pypi.org/project/libconf/>`_ package.

    :param obj: input curve(s) or surface(s)
    :type obj: Abstract.Curve, Abstract.Surface, Multi.MultiCurve or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """

    def callback(fp, data):
        fp.write(libconf.dumps(data))

    # Check if it is possible to import 'libconf'
    try:
        import libconf
    except ImportError:
        print("Please install 'libconf' module to use libconfig format: pip install libconf")
        return

    # Export data as a file
    _export_dict_all(obj, file_name, callback)


def import_yaml(file_name, **kwargs):
    """ Imports curves and surfaces from files in YAML format.

    .. note::

        Requires `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_ package.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of NURBS curve(s) or surface(s)
    :rtype: list
    :raises IOError: an error occurred reading the file
    """
    def callback(fp):
        yaml = YAML()
        return yaml.load(fp)

    # Check if it is possible to import 'ruamel.yaml'
    try:
        from ruamel.yaml import YAML
    except ImportError:
        print("Please install 'ruamel.yaml' module to use YAML format: pip install ruamel.yaml")
        return

    # Get keyword arguments
    delta = kwargs.get('delta', -1.0)

    # Import data
    return _import_dict_all(file_name, delta, callback)


def export_yaml(obj, file_name):
    """ Exports curves and surfaces in YAML format.

    .. note::

        Requires `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_ package.

    The YAML format is mainly used by the `geomdl command line app lication<https://github.com/orbingol/geomdl-cli>`_
    as a way to input data from the command line.

    :param obj: input curve(s) or surface(s)
    :type obj: Abstract.Curve, Abstract.Surface, Multi.MultiCurve or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    def callback(fp, data):
        yaml = YAML()
        yaml.dump(data, fp)

    # Check if it is possible to import 'ruamel.yaml'
    try:
        from ruamel.yaml import YAML
    except ImportError:
        print("Please install 'ruamel.yaml' module to use YAML format: pip install ruamel.yaml")
        return

    # Export data as a file
    _export_dict_all(obj, file_name, callback)


def import_json(file_name, **kwargs):
    """ Imports curves and surfaces from files in JSON format.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of NURBS curve(s) or surface(s)
    :rtype: list
    :raises IOError: an error occurred reading the file
    """
    def callback(fp):
        return json.load(fp)

    # Get keyword arguments
    delta = kwargs.get('delta', -1.0)

    # Import data
    return _import_dict_all(file_name, delta, callback)


def export_json(obj, file_name):
    """ Exports curves and surfaces in JSON format.

    :param obj: input curve(s) or surface(s)
    :type obj: Abstract.Curve, Abstract.Surface, Multi.MultiCurve or Multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    def callback(fp, data):
        fp.write(json.dumps(data, indent=4))

    # Export data as a file
    _export_dict_all(obj, file_name, callback)


def export_obj(surface, file_name, **kwargs):
    """ Exports surface(s) as a .obj file.

    Keyword Arguments:
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 2*
        * ``return_as_str``: if True, return the file contents as a string. *Default: False*
        * ``vertex_normals``: if True, compute vertex normals. *Default: False*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: False*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    # Get keyword arguments
    vertex_spacing = kwargs.get('vertex_spacing', 2)
    return_as_str = kwargs.get('return_as_str', False)
    eval_ders = kwargs.get('vertex_normals', False)
    update_delta = kwargs.get('update_delta', False)

    # Input validity checking
    if not isinstance(surface, (abstract.Surface, multi.MultiSurface)):
        raise TypeError("Can only export surfaces")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Create the file and start saving triangulated surface points
    line = "# Generated by geomdl\n"
    vertex_offset = 0  # count the vertices to update the face numbers correctly

    # Initialize lists for vertices, vertex normals and faces
    str_v = []
    str_vn = []
    str_f = []

    # Loop through MultiSurface object
    for srf in surface:
        if not isinstance(srf, abstract.Surface):
            # Skip non-surface objects
            continue

        # Set surface evaluation delta
        if update_delta:
            srf.sample_size_u = surface.sample_size_u
            srf.sample_size_v = surface.sample_size_v

        # Tessellate surface
        srf.tessellate(vertex_spacing=vertex_spacing)
        vertices = srf.tessellator.vertices
        triangles = srf.tessellator.triangles

        # Collect vertices
        for vert in vertices:
            temp = "v " + str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
            str_v.append(temp)

        # Collect vertex normals
        if eval_ders:
            for vert in vertices:
                sn = operations.normal(srf, vert.uv)
                temp = "vn " + str(sn[1][0]) + " " + str(sn[1][1]) + " " + str(sn[1][2]) + "\n"
                str_vn.append(temp)

        # Collect faces
        for t in triangles:
            vl = t.vertex_ids
            temp = "f " + \
                   str(vl[0] + vertex_offset) + " " + \
                   str(vl[1] + vertex_offset) + " " + \
                   str(vl[2] + vertex_offset) + "\n"
            str_f.append(temp)

        # Update vertex offset
        vertex_offset = len(str_v)

    # Write all collected data to the file
    for lv in str_v:
        line += lv
    for lvn in str_vn:
        line += lvn
    for lf in str_f:
        line += lf

    if return_as_str:
        return line
    return _write_file(file_name, line)


def export_stl(surface, file_name, **kwargs):
    """ Exports surface(s) as a .stl file in plain text or binary format.

    Keyword Arguments:
        * ``binary``: flag to generate a binary STL file. *Default: True*
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 2*
        * ``return_as_str``: if True, return the file contents as a string. *Default: False*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: False*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    binary = kwargs.get('binary', True)
    vertex_spacing = kwargs.get('vertex_spacing', 2)
    return_as_str = kwargs.get('return_as_str', False)
    update_delta = kwargs.get('update_delta', False)

    # Input validity checking
    if not isinstance(surface, (abstract.Surface, multi.MultiSurface)):
        raise TypeError("Can only export surfaces")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    triangles_list = []
    for srf in surface:
        if not isinstance(srf, abstract.Surface):
            # Skip non-surface objects
            continue

        # Set surface evaluation delta
        if update_delta:
            srf.sample_size_u = surface.sample_size_u
            srf.sample_size_v = surface.sample_size_v

        # Tessellate surface
        srf.tessellate(vertex_spacing=vertex_spacing)
        triangles = srf.tessellator.triangles

        triangles_list += triangles

    # Write triangle list to ASCII or  binary STL file
    if binary:
        line = b'\0' * 80  # header
        line += struct.pack('<i', len(triangles_list))  # number of triangles
        for t in triangles_list:
            line += struct.pack('<3f', *utilities.triangle_normal(t))  # normal
            for v in t.vertices:
                line += struct.pack('<3f', *v.data)  # vertices
            line += b'\0\0'  # attribute byte count
    else:
        line = "solid Surface\n"
        for t in triangles_list:
            nvec = utilities.triangle_normal(t)
            line += "\tfacet normal " + str(nvec[0]) + " " + str(nvec[1]) + " " + str(nvec[2]) + "\n"
            line += "\t\touter loop\n"
            for v in t.vertices:
                line += "\t\t\tvertex " + str(v.x) + " " + str(v.y) + " " + str(v.z) + "\n"
            line += "\t\tendloop\n"
            line += "\tendfacet\n"
        line += "endsolid Surface\n"

    if return_as_str:
        return line
    return _write_file(file_name, line, binary=binary)


def export_off(surface, file_name, **kwargs):
    """ Exports surface(s) as a .off file.

    Keyword Arguments:
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 2*
        * ``return_as_str``: if True, return the file contents as a string. *Default: False*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: False*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    # Get keyword arguments
    vertex_spacing = kwargs.get('vertex_spacing', 2)
    return_as_str = kwargs.get('return_as_str', False)
    update_delta = kwargs.get('update_delta', False)

    # Input validity checking
    if not isinstance(surface, (abstract.Surface, multi.MultiSurface)):
        raise TypeError("Can only export surfaces")
    if vertex_spacing < 1 or not isinstance(vertex_spacing, int):
        raise ValueError("Vertex spacing must be an integer value and it must be bigger than zero")

    # Count the vertices to update the face numbers correctly
    vertex_offset = 0

    # Initialize lists for vertices, vertex normals and faces
    str_v = []
    str_f = []

    for srf in surface:
        if not isinstance(srf, abstract.Surface):
            # Skip non-surface objects
            continue

        # Set surface evaluation delta
        if update_delta:
            srf.sample_size_u = surface.sample_size_u
            srf.sample_size_v = surface.sample_size_v

        # Tessellate surface
        srf.tessellate(vertex_spacing=vertex_spacing)
        vertices = srf.tessellator.vertices
        triangles = srf.tessellator.triangles

        # Collect vertices
        for vert in vertices:
            line = str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
            str_v.append(line)

        # Collect faces (zero-indexed)
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
    line = "OFF\n"
    line += str(len(str_v)) + " " + str(len(str_f)) + " 0\n"

    # Write all collected data to the file
    for lv in str_v:
        line += lv
    for lf in str_f:
        line += lf

    if return_as_str:
        return line
    return _write_file(file_name, line)


def import_smesh(file):
    """ Generates NURBS surface(s) from surface mesh (smesh) file(s).

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
    :rtype: NURBS.Surface or multi.MultiSurface
    :raises IOError: an error occurred reading the file
    """
    if os.path.isfile(file):
        return _import_smesh_single(file)
    elif os.path.isdir(file):
        files = sorted([os.path.join(file, f) for f in os.listdir(file)])
        surf = multi.MultiSurface()
        for f in files:
            surf.add(_import_smesh_single(f))
        return surf
    else:
        raise IOError("Input is not a file or a directory")


def export_smesh(surface, file_name):
    """ Exports surface(s) as surface mesh (smesh) files.

    Please see :py:func:`.import_smesh()` for details on the file format.

    :param surface: surface(s) to be exported
    :type surface: abstract.Surface or multi.MultiSurface
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    if not isinstance(surface, (abstract.Surface, multi.MultiSurface)):
        raise TypeError("Can only work with single or multi surfaces")

    # Split file name and extension
    fname, fext = os.path.splitext(file_name)

    for idx, s in enumerate(surface):
        if not s.rational:
            surf = convert.bspline_to_nurbs(s)
        else:
            surf = s
        line = str(surf.dimension) + "\n"
        line += str(surf.degree_u) + " " + str(surf.degree_v) + "\n"
        line += str(surf.ctrlpts_size_u) + " " + str(surf.ctrlpts_size_v) + "\n"
        line += " ".join([str(k) for k in surf.knotvector_u]) + "\n"
        line += " ".join([str(k) for k in surf.knotvector_v]) + "\n"
        # Flip control points
        ctrlptsw = compatibility.flip_ctrlpts(surf.ctrlptsw, surf.ctrlpts_size_u, surf.ctrlpts_size_v)
        # Convert control points into (x, y, z, w) format
        ctrlptsw = compatibility.generate_ctrlpts_weights(ctrlptsw)
        for ptw in ctrlptsw:
            line += " ".join([str(p) for p in ptw]) + "\n"

        # Write to file
        fname_curr = fname + "." + str(idx + 1)
        _write_file(fname_curr + fext, line)


def export_vmesh(volume, file_name):
    """ Exports volume(s) as volume mesh (vmesh) files.

    :param volume: volume(s) to be exported
    :type volume: abstract.Volume
    :param file_name: name of the output file
    :type file_name: str
    :raises IOError: an error occurred writing the file
    """
    if not isinstance(volume, abstract.Volume):
        raise TypeError("Can only work with volumes")

    # Split file name and extension
    fname, fext = os.path.splitext(file_name)

    for idx, v in enumerate(volume):
        if not v.rational:
            vol = convert.bspline_to_nurbs(v)
        else:
            vol = v
        line = str(vol.dimension) + "\n"
        line += str(vol.degree_u) + " " + str(vol.degree_v) + " " + str(vol.degree_w) + "\n"
        line += str(vol.ctrlpts_size_u) + " " + str(vol.ctrlpts_size_v) + " " + str(vol.ctrlpts_size_w) + "\n"
        line += " ".join([str(k) for k in vol.knotvector_u]) + "\n"
        line += " ".join([str(k) for k in vol.knotvector_v]) + "\n"
        line += " ".join([str(k) for k in vol.knotvector_w]) + "\n"
        # Convert control points into (x, y, z, w)
        ctrlptsw = []
        for w in range(vol.ctrlpts_size_w):
            surf = vol.ctrlptsw[(w * vol.ctrlpts_size_u * vol.ctrlpts_size_v):((w + 1) * vol.ctrlpts_size_u * vol.ctrlpts_size_v)]
            # Flip control points
            ctrlptsw += compatibility.flip_ctrlpts(surf, vol.ctrlpts_size_u, vol.ctrlpts_size_v)
        # Convert control points into (x, y, z, w) format
        ctrlptsw = compatibility.generate_ctrlpts_weights(ctrlptsw)
        for ptw in ctrlptsw:
            line += " ".join([str(p) for p in ptw]) + "\n"

        # Write to file
        fname_curr = fname + "." + str(idx + 1)
        _write_file(fname_curr + fext, line)


def import_3dm(file_name, **kwargs):
    """ Imports Rhinoceros/OpenNURBS .3dm file format.

    .. note::

        Requires ``rw3dm`` module: https://github.com/orbingol/rw3dm

    :param file_name: input file name
    :type file_name: str
    """
    try:
        from rw3dm import rw3dm
    except ImportError:
        print("Please install 'rw3dm' module: https://github.com/orbingol/rw3dm")
        return

    res3dm = []
    rw3dm.read(file_name, res3dm, **kwargs)

    res = []
    for r in res3dm:
        if r['shape_type'] == "curve":
            tmp = NURBS.Curve()
            tmp.degree = r['degree']
            tmp.ctrlpts = r['control_points']['points']
            if 'weights' in r:
                tmp.weights = r['control_points']['weights']
            tmp.knotvector = [r['knotvector'][0]] + r['knotvector'] + [r['knotvector'][-1]]
            res.append(tmp)
        if r['shape_type'] == "surface":
            tmp = NURBS.Surface()
            tmp.degree_u = r['degree_u']
            tmp.degree_v = r['degree_v']
            tmp.ctrlpts_size_u = r['size_u']
            tmp.ctrlpts_size_v = r['size_v']
            tmp.ctrlpts = r['control_points']['points']
            if 'weights' in r:
                tmp.weights = r['control_points']['weights']
            tmp.knotvector_u = [r['knotvector_u'][0]] + r['knotvector_u'] + [r['knotvector_u'][-1]]
            tmp.knotvector_v = [r['knotvector_v'][0]] + r['knotvector_v'] + [r['knotvector_v'][-1]]
            res.append(tmp)

    return res


def export_3dm(obj, file_name, **kwargs):
    """ Exports NURBS curves and surfaces in Rhinoceros/OpenNURBS .3dm format.

    .. note::

        Requires ``rw3dm`` module: https://github.com/orbingol/rw3dm

    :param obj: curves/surfaces to be exported
    :type obj: Abstract.Curve, Abstract.Surface, Multi.MultiCurve, Multi.MultiSurface
    :param file_name: file name
    :type file_name: str
    """
    try:
        from rw3dm import rw3dm
    except ImportError:
        print("Please install 'rw3dm' module: https://github.com/orbingol/rw3dm")
        return

    res3dm = []
    for o in obj:
        if isinstance(o, abstract.Curve):
            rd = dict(
                shape_type="curve",
                degree=o.degree,
                knotvector=o.knotvector[1:-1],
                control_points=dict(
                    points=o.ctrlpts
                )
            )
            try:
                rd['control_points']['weights'] = o.weights
            except AttributeError:
                pass
            res3dm.append(rd)
        if isinstance(o, abstract.Surface):
            rd = dict(
                shape_type="surface",
                degree_u=o.degree_u,
                degree_v=o.degree_v,
                knotvector_u=o.knotvector_u[1:-1],
                knotvector_v=o.knotvector_v[1:-1],
                size_u=o.ctrlpts_size_u,
                size_v=o.ctrlpts_size_v,
                control_points=dict(
                    points=o.ctrlpts
                )
            )
            try:
                rd['control_points']['weights'] = o.weights
            except AttributeError:
                pass
            res3dm.append(rd)

    rw3dm.write(res3dm, file_name)


def _read_file(file_name, **kwargs):
    binary = kwargs.get('binary', False)
    skip_lines = kwargs.get('skip_lines', 0)
    fp_callback = kwargs.get('callback', None)
    try:
        with open(file_name, 'rb' if binary else 'r') as fp:
            for _ in range(skip_lines):
                next(fp)
            content = fp.read() if fp_callback is None else fp_callback(fp)
        return content
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _write_file(file_name, content, **kwargs):
    binary = kwargs.get('binary', False)
    callback = kwargs.get('callback', None)
    try:
        with open(file_name, 'wb' if binary else 'w') as fp:
            fp.write(content) if callback is None else callback(fp, content)
        return True
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _import_text_data(content, sep, col_sep=";", two_dimensional=False):
    lines = content.strip().split("\n")
    ctrlpts = []
    if two_dimensional:
        # Start reading file
        size_u = 0
        size_v = 0
        for line in lines:
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
        for line in lines:
            # Remove whitespace
            line = line.strip()
            # Clean and convert the values
            ctrlpts.append([float(c.strip()) for c in line.split(sep)])

        # Return control points
        return ctrlpts


def _export_text_data(obj, sep, col_sep=";", two_dimensional=False):
    result = ""
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
            result += line
    else:
        # B-spline or NURBS?
        try:
            ctrlpts = obj.ctrlptsw
        except AttributeError:
            ctrlpts = obj.ctrlpts
        # Loop through points
        for pt in ctrlpts:
            result += sep.join(str(c) for c in pt) + "\n"

    return result


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
        raise TypeError("Input smesh file" + str(file_name) + " is not a surface")

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


def _prepare_import_dict_curve(data):
    shape = NURBS.Curve()
    shape.degree = data['degree']
    shape.ctrlpts = data['control_points']['points']
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    shape.knotvector = data['knotvector']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    return shape


def _prepare_export_dict_curve(obj):
    data = dict(
        degree=obj.degree,
        knotvector=list(obj.knotvector),
        control_points=dict(
            points=obj.ctrlpts
        ),
        delta=obj.delta
    )
    try:
        data['control_points']['weights'] = list(obj.weights)
    except AttributeError:
        # Not a NURBS curve
        pass
    return data


def _prepare_import_dict_surface(data):
    shape = NURBS.Surface()
    shape.degree_u = data['degree_u']
    shape.degree_v = data['degree_v']
    shape.ctrlpts_size_u = data['size_u']
    shape.ctrlpts_size_v = data['size_v']
    shape.ctrlpts = data['control_points']['points']
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    shape.knotvector_u = data['knotvector_u']
    shape.knotvector_v = data['knotvector_v']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    return shape


def _prepare_export_dict_surface(obj):
    data = dict(
        degree_u=obj.degree_u,
        degree_v=obj.degree_v,
        knotvector_u=list(obj.knotvector_u),
        knotvector_v=list(obj.knotvector_v),
        size_u=obj.ctrlpts_size_u,
        size_v=obj.ctrlpts_size_v,
        control_points=dict(
            points=obj.ctrlpts
        ),
        delta=obj.delta
    )
    try:
        data['control_points']['weights'] = list(obj.weights)
    except AttributeError:
        # Not a NURBS curve
        pass
    return data


def _import_dict_all(file_name, delta, callback):
    type_map = {'curve': _prepare_import_dict_curve, 'surface': _prepare_import_dict_surface}

    # Callback function
    imported_data = _read_file(file_name, callback=callback)

    # Process imported data
    ret_list = []
    for data in imported_data['shape']['data']:
        temp = type_map[imported_data['shape']['type']](data)
        if 0.0 < delta < 1.0:
            temp.delta = delta
        ret_list.append(temp)

    # Return imported data
    return ret_list


def _export_dict_all(obj, file_name, callback):
    count = 1
    if isinstance(obj, abstract.Curve):
        export_type = "curve"
        data = [_prepare_export_dict_curve(obj)]
    elif isinstance(obj, abstract.Surface):
        export_type = "surface"
        data = [_prepare_export_dict_surface(obj)]
    elif isinstance(obj, multi.MultiCurve):
        export_type = "curve"
        data = [_prepare_export_dict_curve(o) for o in obj]
        count = len(obj)
    elif isinstance(obj, multi.MultiSurface):
        export_type = "surface"
        data = [_prepare_export_dict_surface(o) for o in obj]
        count = len(obj)
    else:
        raise NotADirectoryError("Object type is not defined for dict export")

    # Create the dictionary
    data = dict(
        shape=dict(
            type=export_type,
            count=count,
            data=tuple(data)
        )
    )

    return _write_file(file_name, data, callback=callback)
