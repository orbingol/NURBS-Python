"""
.. module:: exchange
    :platform: Unix, Windows
    :synopsis: Provides CAD exchange and interoperability functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import os
import struct
import json
from io import StringIO
from . import compatibility, operations, elements, linalg
from . import _exchange as exch
from .exceptions import GeomdlException
from ._utilities import export


@export
def import_txt(file_name, two_dimensional=False, **kwargs):
    """ Reads control points from a text file and generates a 1-dimensional list of control points.

    The following code examples illustrate importing different types of text files for curves and surfaces:

    .. code-block:: python
        :linenos:

        # Import curve control points from a text file
        curve_ctrlpts = exchange.import_txt(file_name="control_points.txt")

        # Import surface control points from a text file (1-dimensional file)
        surf_ctrlpts = exchange.import_txt(file_name="control_points.txt")

        # Import surface control points from a text file (2-dimensional file)
        surf_ctrlpts, size_u, size_v = exchange.import_txt(file_name="control_points.txt", two_dimensional=True)

    If argument ``jinja2=True`` is set, then the input file is processed as a `Jinja2 <http://jinja.pocoo.org/>`_
    template. You can also use the following convenience template functions which correspond to the given mathematical
    equations:

    * ``sqrt(x)``:  :math:`\\sqrt{x}`
    * ``cubert(x)``: :math:`\\sqrt[3]{x}`
    * ``pow(x, y)``: :math:`x^{y}`

    You may set the file delimiters using the keyword arguments ``separator`` and ``col_separator``, respectively.
    ``separator`` is the delimiter between the coordinates of the control points. It could be comma
    ``1, 2, 3`` or space ``1 2 3`` or something else. ``col_separator`` is the delimiter between the control
    points and is only valid when ``two_dimensional`` is ``True``. Assuming that ``separator`` is set to space, then
    ``col_operator`` could be semi-colon ``1 2 3; 4 5 6`` or pipe ``1 2 3| 4 5 6`` or comma ``1 2 3, 4 5 6`` or
    something else.

    The defaults for ``separator`` and ``col_separator`` are *comma (,)* and *semi-colon (;)*, respectively.

    The following code examples illustrate the usage of the keyword arguments discussed above.

    .. code-block:: python
        :linenos:

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
    :raises GeomdlException: an error occurred reading the file
    """
    # Read file
    content = exch.read_file(file_name)

    # Are we using a Jinja2 template?
    j2tmpl = kwargs.get('jinja2', False)
    if j2tmpl:
        content = exch.process_template(content)

    # File delimiters
    col_sep = kwargs.get('col_separator', ";")
    sep = kwargs.get('separator', ",")

    return exch.import_text_data(content, sep, col_sep, two_dimensional)


@export
def export_txt(obj, file_name, two_dimensional=False, **kwargs):
    """ Exports control points as a text file.

    For curves the output is always a list of control points. For surfaces, it is possible to generate a 2-dimensional
    control point output file using ``two_dimensional``.

    Please see :py:func:`.exchange.import_txt()` for detailed description of the keyword arguments.

    :param obj: a spline geometry object
    :type obj: abstract.SplineGeometry
    :param file_name: file name of the text file to be saved
    :type file_name: str
    :param two_dimensional: type of the text file (only works for Surface objects)
    :type two_dimensional: bool
    :raises GeomdlException: an error occurred writing the file
    """
    # Check if the user has set any control points
    if obj.ctrlpts is None or len(obj.ctrlpts) == 0:
        raise exch.GeomdlException("There are no control points to save!")

    # Check the usage of two_dimensional flag
    if obj.pdimension == 1 and two_dimensional:
        # Silently ignore two_dimensional flag
        two_dimensional = False

    # File delimiters
    col_sep = kwargs.get('col_separator', ";")
    sep = kwargs.get('separator', ",")

    content = exch.export_text_data(obj, sep, col_sep, two_dimensional)
    return exch.write_file(file_name, content)


@export
def import_csv(file_name, **kwargs):
    """ Reads control points from a CSV file and generates a 1-dimensional list of control points.

    It is possible to use a different value separator via ``separator`` keyword argument. The following code segment
    illustrates the usage of ``separator`` keyword argument.

    .. code-block:: python
        :linenos:

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
    :raises GeomdlException: an error occurred reading the file
    """
    # File delimiters
    sep = kwargs.get('separator', ",")

    content = exch.read_file(file_name, skip_lines=1)
    return exch.import_text_data(content, sep)


@export
def export_csv(obj, file_name, point_type='evalpts', **kwargs):
    """ Exports control points or evaluated points as a CSV file.

    :param obj: a spline geometry object
    :type obj: abstract.SplineGeometry
    :param file_name: output file name
    :type file_name: str
    :param point_type: ``ctrlpts`` for control points or ``evalpts`` for evaluated points
    :type point_type: str
    :raises GeomdlException: an error occurred writing the file
    """
    if not 0 < obj.pdimension < 3:
        raise exch.GeomdlException("Input object should be a curve or a surface")

    # Pick correct points from the object
    if point_type == 'ctrlpts':
        points = obj.ctrlptsw if obj.rational else obj.ctrlpts
    elif point_type == 'evalpts':
        points = obj.evalpts
    else:
        raise exch.GeomdlException("Please choose a valid point type option. Possible types: ctrlpts, evalpts")

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
    return exch.write_file(file_name, line)


@export
def import_cfg(file_name, **kwargs):
    """ Imports curves and surfaces from files in libconfig format.

    .. note::

        Requires `libconf <https://pypi.org/project/libconf/>`_ package.

    Use ``jinja2=True`` to activate Jinja2 template processing. Please refer to the documentation for details.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of rational spline geometries
    :rtype: list
    :raises GeomdlException: an error occurred writing the file
    """
    def callback(data):
        return libconf.loads(data)

    # Check if it is possible to import 'libconf'
    try:
        import libconf
    except ImportError:
        raise exch.GeomdlException("Please install 'libconf' package to use libconfig format: pip install libconf")

    # Get keyword arguments
    delta = kwargs.get('delta', -1.0)
    use_template = kwargs.get('jinja2', False)

    # Read file
    file_src = exch.read_file(file_name)

    # Import data
    return exch.import_dict_str(file_src=file_src, delta=delta, callback=callback, tmpl=use_template)


@export
def export_cfg(obj, file_name):
    """ Exports curves and surfaces in libconfig format.

    .. note::

        Requires `libconf <https://pypi.org/project/libconf/>`_ package.

    Libconfig format is also used by the `geomdl command-line application <https://github.com/orbingol/geomdl-cli>`_
    as a way to input shape data from the command line.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry, multi.AbstractContainer
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    def callback(data):
        return libconf.dumps(data)

    # Check if it is possible to import 'libconf'
    try:
        import libconf
    except ImportError:
        raise exch.GeomdlException("Please install 'libconf' package to use libconfig format: pip install libconf")

    # Export data
    exported_data = exch.export_dict_str(obj=obj, callback=callback)

    # Write to file
    return exch.write_file(file_name, exported_data)


@export
def import_yaml(file_name, **kwargs):
    """ Imports curves and surfaces from files in YAML format.

    .. note::

        Requires `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_ package.

    Use ``jinja2=True`` to activate Jinja2 template processing. Please refer to the documentation for details.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of rational spline geometries
    :rtype: list
    :raises GeomdlException: an error occurred reading the file
    """
    def callback(data):
        yaml = YAML()
        return yaml.load(data)

    # Check if it is possible to import 'ruamel.yaml'
    try:
        from ruamel.yaml import YAML
    except ImportError:
        raise exch.GeomdlException("Please install 'ruamel.yaml' package to use YAML format: pip install ruamel.yaml")

    # Get keyword arguments
    delta = kwargs.get('delta', -1.0)
    use_template = kwargs.get('jinja2', False)

    # Read file
    file_src = exch.read_file(file_name)

    # Import data
    return exch.import_dict_str(file_src=file_src, delta=delta, callback=callback, tmpl=use_template)


@export
def export_yaml(obj, file_name):
    """ Exports curves and surfaces in YAML format.

    .. note::

        Requires `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_ package.

    YAML format is also used by the `geomdl command-line application <https://github.com/orbingol/geomdl-cli>`_
    as a way to input shape data from the command line.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry, multi.AbstractContainer
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    def callback(data):
        # Ref: https://yaml.readthedocs.io/en/latest/example.html#output-of-dump-as-a-string
        stream = StringIO()
        yaml = YAML()
        yaml.dump(data, stream)
        return stream.getvalue()

    # Check if it is possible to import 'ruamel.yaml'
    try:
        from ruamel.yaml import YAML
    except ImportError:
        raise exch.GeomdlException("Please install 'ruamel.yaml' package to use YAML format: pip install ruamel.yaml")

    # Export data
    exported_data = exch.export_dict_str(obj=obj, callback=callback)

    # Write to file
    return exch.write_file(file_name, exported_data)


@export
def import_json(file_name, **kwargs):
    """ Imports curves and surfaces from files in JSON format.

    Use ``jinja2=True`` to activate Jinja2 template processing. Please refer to the documentation for details.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of rational spline geometries
    :rtype: list
    :raises GeomdlException: an error occurred reading the file
    """
    def callback(data):
        return json.loads(data)

    # Get keyword arguments
    delta = kwargs.get('delta', -1.0)
    use_template = kwargs.get('jinja2', False)

    # Read file
    file_src = exch.read_file(file_name)

    # Import data
    return exch.import_dict_str(file_src=file_src, delta=delta, callback=callback, tmpl=use_template)


@export
def export_json(obj, file_name):
    """ Exports curves and surfaces in JSON format.

    JSON format is also used by the `geomdl command-line application <https://github.com/orbingol/geomdl-cli>`_
    as a way to input shape data from the command line.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry, multi.AbstractContainer
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    def callback(data):
        return json.dumps(data, indent=4)

    # Export data
    exported_data = exch.export_dict_str(obj=obj, callback=callback)

    # Write to file
    return exch.write_file(file_name, exported_data)


@export
def import_obj(file_name, **kwargs):
    """ Reads .obj files and generates faces.

    Keyword Arguments:
        * ``callback``: reference to the function that processes the faces for customized output

    The structure of the callback function is shown below:

    .. code-block:: python

        def my_callback_function(face_list):
            # "face_list" will be a list of elements.Face class instances
            # The function should return a list
            return list()

    :param file_name: file name
    :type file_name: str
    :return: output of the callback function (default is a list of faces)
    :rtype: list
    """
    def default_callback(face_list):
        return face_list

    # Keyword arguments
    callback_func = kwargs.get('callback', default_callback)

    # Read and process the input file
    content = exch.read_file(file_name)
    content_arr = content.split("\n")

    # Initialize variables
    on_face = False
    vertices = []
    triangles = []
    faces = []

    # Index values
    vert_idx = 1
    tri_idx = 1
    face_idx = 1

    # Loop through the data
    for carr in content_arr:
        carr = carr.strip()
        data = carr.split(" ")
        data = [d.strip() for d in data]
        if data[0] == "v":
            if on_face:
                on_face = not on_face
                face = elements.Face(*triangles, id=face_idx)
                faces.append(face)
                face_idx += 1
                vertices[:] = []
                triangles[:] = []
                vert_idx = 1
                tri_idx = 1
            vertex = elements.Vertex(*data[1:], id=vert_idx)
            vertices.append(vertex)
            vert_idx += 1
        if data[0] == "f":
            on_face = True
            triangle = elements.Triangle(*[vertices[int(fidx) - 1] for fidx in data[1:]], id=tri_idx)
            triangles.append(triangle)
            tri_idx += 1

    # Process he final face
    if triangles:
        face = elements.Face(*triangles, id=face_idx)
        faces.append(face)

    # Return the output of the callback function
    return callback_func(faces)


@export
def export_obj(surface, file_name, **kwargs):
    """ Exports surface(s) as a .obj file.

    Keyword Arguments:
        * ``vertex_spacing``: size of the triangle edge in terms of surface points sampled. *Default: 2*
        * ``vertex_normals``: if True, then computes vertex normals. *Default: False*
        * ``parametric_vertices``: if True, then adds parameter space vertices. *Default: False*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: True*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.SurfaceContainer
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    content = export_obj_str(surface, **kwargs)
    return exch.write_file(file_name, content)


def export_obj_str(surface, **kwargs):
    """ Exports surface(s) as a .obj file (string).

    Keyword Arguments:
        * ``vertex_spacing``: size of the triangle edge in terms of surface points sampled. *Default: 2*
        * ``vertex_normals``: if True, then computes vertex normals. *Default: False*
        * ``parametric_vertices``: if True, then adds parameter space vertices. *Default: False*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: True*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.SurfaceContainer
    :return: contents of the .obj file generated
    :rtype: str
    """
    # Get keyword arguments
    vertex_spacing = int(kwargs.get('vertex_spacing', 1))
    include_vertex_normal = kwargs.get('vertex_normals', False)
    include_param_vertex = kwargs.get('parametric_vertices', False)
    update_delta = kwargs.get('update_delta', True)

    # Input validity checking
    if surface.pdimension != 2:
        raise exch.GeomdlException("Can only export surfaces")
    if vertex_spacing < 1:
        raise exch.GeomdlException("Vertex spacing should be bigger than zero")

    # Create the string and start adding triangulated surface points
    line = "# Generated by geomdl\n"
    vertex_offset = 0  # count the vertices to update the face numbers correctly

    # Initialize lists for geometry data
    str_v = []  # vertices
    str_vn = []  # vertex normals
    str_vp = []  # parameter space vertices
    str_f = []  # faces

    # Loop through SurfaceContainer object
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
            temp = "v " + str(vert.x) + " " + str(vert.y) + " " + str(vert.z) + "\n"
            str_v.append(temp)

        # Collect parameter space vertices
        if include_param_vertex:
            for vert in vertices:
                temp = "vp " + str(vert.uv[0]) + " " + str(vert.uv[1]) + "\n"
                str_vp.append(temp)

        # Compute vertex normals
        if include_vertex_normal:
            for vert in vertices:
                sn = operations.normal(srf, vert.uv)
                temp = "vn " + str(sn[1][0]) + " " + str(sn[1][1]) + " " + str(sn[1][2]) + "\n"
                str_vn.append(temp)

        # Collect faces (1-indexed)
        for t in triangles:
            vl = t.data
            temp = "f " + \
                   str(vl[0] + 1 + vertex_offset) + " " + \
                   str(vl[1] + 1 + vertex_offset) + " " + \
                   str(vl[2] + 1 + vertex_offset) + "\n"
            str_f.append(temp)

        # Update vertex offset
        vertex_offset = len(str_v)

    # Write all collected data to the return string
    for lv in str_v:
        line += lv
    for lvn in str_vn:
        line += lvn
    for lvp in str_vp:
        line += lvp
    for lf in str_f:
        line += lf

    return line


@export
def export_stl(surface, file_name, **kwargs):
    """ Exports surface(s) as a .stl file in plain text or binary format.

    Keyword Arguments:
        * ``binary``: flag to generate a binary STL file. *Default: True*
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 1*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: True*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.SurfaceContainer
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    binary = kwargs.get('binary', True)
    if 'binary' in kwargs:
        kwargs.pop('binary')
    content = export_stl_str(surface, binary=binary, **kwargs)
    return exch.write_file(file_name, content, binary=binary)


def export_stl_str(surface, **kwargs):
    """ Exports surface(s) as a .stl file in plain text or binary format (string).

    Keyword Arguments:
        * ``binary``: flag to generate a binary STL file. *Default: False*
        * ``vertex_spacing``: size of the triangle edge in terms of points sampled on the surface. *Default: 1*
        * ``update_delta``: use multi-surface evaluation delta for all surfaces. *Default: False*

    :param surface: surface or surfaces to be saved
    :type surface: abstract.Surface or multi.SurfaceContainer
    :return: contents of the .stl file generated
    :rtype: str
    """
    binary = kwargs.get('binary', False)
    vertex_spacing = int(kwargs.get('vertex_spacing', 1))
    update_delta = kwargs.get('update_delta', True)

    # Input validity checking
    if surface.pdimension != 2:
        raise exch.GeomdlException("Can only export surfaces")
    if vertex_spacing < 1:
        raise exch.GeomdlException("Vertex spacing should be bigger than zero")

    triangles_list = []
    for srf in surface:
        # Set surface evaluation delta
        if update_delta:
            srf.sample_size_u = surface.sample_size_u
            srf.sample_size_v = surface.sample_size_v

        # Tessellate surface
        srf.tessellate(vertex_spacing=vertex_spacing)
        triangles = srf.tessellator.faces

        triangles_list += triangles

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
    return exch.write_file(file_name, content)


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
        raise exch.GeomdlException("Can only export surfaces")
    if vertex_spacing < 1:
        raise exch.GeomdlException("Vertex spacing should be bigger than zero")

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


@export
def import_smesh(file):
    """ Generates NURBS surface(s) from surface mesh (smesh) file(s).

    *smesh* files are some text files which contain a set of NURBS surfaces. Each file in the set corresponds to one
    NURBS surface. Most of the time, you receive multiple *smesh* files corresponding to an complete object composed of
    several NURBS surfaces. The files have the extensions of ``txt`` or ``dat`` and they are named as

    * ``smesh.X.Y.txt``
    * ``smesh.X.dat``

    where *X* and *Y* correspond to some integer value which defines the set the surface belongs to and part number of
    the surface inside the complete object.

    :param file: path to a directory containing mesh files or a single mesh file
    :type file: str
    :return: list of NURBS surfaces
    :rtype: list
    :raises GeomdlException: an error occurred reading the file
    """
    imported_elements = []
    if os.path.isfile(file):
        imported_elements.append(exch.import_surf_mesh(file))
    elif os.path.isdir(file):
        files = sorted([os.path.join(file, f) for f in os.listdir(file)])
        for f in files:
            imported_elements.append(exch.import_surf_mesh(f))
    else:
        raise exch.GeomdlException("Input is not a file or a directory")
    return imported_elements


@export
def export_smesh(surface, file_name, **kwargs):
    """ Exports surface(s) as surface mesh (smesh) files.

    Please see :py:func:`.import_smesh()` for details on the file format.

    :param surface: surface(s) to be exported
    :type surface: abstract.Surface or multi.SurfaceContainer
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    # Input validity checking
    if surface.pdimension != 2:
        raise exch.GeomdlException("Can only export surfaces")

    # Get keyword arguments
    decimals = kwargs.get('decimals', 18)

    # Split file name and extension
    fname, fext = os.path.splitext(file_name)

    # Enumerate file name only if we are working with multiple surfaces
    numerate_file = True if len(surface) > 1 else False

    for idx, s in enumerate(surface):
        if s.rational:
            pts = s.ctrlptsw
        else:
            pts = compatibility.combine_ctrlpts_weights(s.ctrlpts)
        line = str(s.dimension) + "\n"
        line += str(s.degree_u) + " " + str(s.degree_v) + "\n"
        line += str(s.ctrlpts_size_u) + " " + str(s.ctrlpts_size_v) + "\n"
        line += " ".join([("{:." + str(decimals) + "f}").format(k) for k in s.knotvector_u]) + "\n"
        line += " ".join([("{:." + str(decimals) + "f}").format(k) for k in s.knotvector_v]) + "\n"
        # Flip control points
        ctrlptsw = compatibility.flip_ctrlpts(pts, s.ctrlpts_size_u, s.ctrlpts_size_v)
        # Convert control points into (x, y, z, w) format
        ctrlptsw = compatibility.generate_ctrlpts_weights(ctrlptsw)
        for ptw in ctrlptsw:
            line += " ".join([("{:." + str(decimals) + "f}").format(p) for p in ptw]) + "\n"
        # Open or closed?
        line += "1\n"

        # Write to file
        fname_curr = fname + "." + str(idx + 1) if numerate_file else fname
        exch.write_file(fname_curr + fext, line)


@export
def import_vmesh(file):
    """ Imports NURBS volume(s) from volume mesh (vmesh) file(s).

    :param file: path to a directory containing mesh files or a single mesh file
    :type file: str
    :return: list of NURBS volumes
    :rtype: list
    :raises GeomdlException: an error occurred reading the file
    """
    imported_elements = []
    if os.path.isfile(file):
        imported_elements.append(exch.import_vol_mesh(file))
    elif os.path.isdir(file):
        files = sorted([os.path.join(file, f) for f in os.listdir(file)])
        for f in files:
            imported_elements.append(exch.import_vol_mesh(f))
    else:
        raise exch.GeomdlException("Input is not a file or a directory")
    return imported_elements


@export
def export_vmesh(volume, file_name, **kwargs):
    """ Exports volume(s) as volume mesh (vmesh) files.

    :param volume: volume(s) to be exported
    :type volume: abstract.Volume
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    if volume.pdimension != 3:
        raise exch.GeomdlException("Can only export volumes")

    # Get keyword arguments
    decimals = kwargs.get('decimals', 18)

    # Split file name and extension
    fname, fext = os.path.splitext(file_name)

    # Enumerate file name only if we are working with multiple volumes
    numerate_file = True if len(volume) > 1 else False

    for idx, v in enumerate(volume):
        if v.rational:
            pts = v.ctrlptsw
        else:
            pts = compatibility.combine_ctrlpts_weights(v.ctrlpts)
        line = str(v.dimension) + "\n"
        line += str(v.degree_u) + " " + str(v.degree_v) + " " + str(v.degree_w) + "\n"
        line += str(v.ctrlpts_size_u) + " " + str(v.ctrlpts_size_v) + " " + str(v.ctrlpts_size_w) + "\n"
        line += " ".join([("{:." + str(decimals) + "f}").format(k) for k in v.knotvector_u]) + "\n"
        line += " ".join([("{:." + str(decimals) + "f}").format(k) for k in v.knotvector_v]) + "\n"
        line += " ".join([("{:." + str(decimals) + "f}").format(k) for k in v.knotvector_w]) + "\n"
        # Convert control points into (x, y, z, w)
        ctrlptsw = []
        for w in range(v.ctrlpts_size_w):
            srfpts = pts[(w * v.ctrlpts_size_u * v.ctrlpts_size_v):((w + 1) * v.ctrlpts_size_u * v.ctrlpts_size_v)]
            # Flip control points
            ctrlptsw += compatibility.flip_ctrlpts(srfpts, v.ctrlpts_size_u, v.ctrlpts_size_v)
        # Convert control points into (x, y, z, w) format
        ctrlptsw = compatibility.generate_ctrlpts_weights(ctrlptsw)
        for ptw in ctrlptsw:
            line += " ".join([("{:." + str(decimals) + "f}").format(p) for p in ptw]) + "\n"
        # Open or closed?
        line += "1\n"

        # Write to file
        fname_curr = fname + "." + str(idx + 1) if numerate_file else fname
        exch.write_file(fname_curr + fext, line)


@export
def import_3dm(file_name, **kwargs):
    """ Imports curves and surfaces from Rhinoceros/OpenNURBS .3dm files.

    .. deprecated:: 5.2.2

        ``rw3dm`` Python module is replaced by ``on2json``. It can be used to convert .3dm files to geomdl JSON format.
        Please refer to https://github.com/orbingol/rw3dm for more details.

    :param file_name: input file name
    :type file_name: str
    """
    raise GeomdlException("This API call has been deprecated. Please refer to https://github.com/orbingol/rw3dm")


@export
def export_3dm(obj, file_name, **kwargs):
    """ Exports NURBS curves and surfaces to Rhinoceros/OpenNURBS .3dm files.

    .. deprecated:: 5.2.2

        ``rw3dm`` Python module is replaced by ``json2on``. It can be used to convert geomdl JSON format to .3dm files.
        Please refer to https://github.com/orbingol/rw3dm for more details.

    :param obj: curves/surfaces to be exported
    :type obj: abstract.Curve, abstract.Surface, multi.CurveContainer, multi.SurfaceContainer
    :param file_name: file name
    :type file_name: str
    """
    raise GeomdlException("This API call has been deprecated. Please refer to https://github.com/orbingol/rw3dm")
