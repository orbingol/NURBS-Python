"""
.. module:: exchange
    :platform: Unix, Windows
    :synopsis: Provides CAD exchange and interoperability functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import struct
import json
from io import StringIO
from . import operations, elements, linalg
from . import _exchange as exch
from .base import export, GeomdlError


@export
def import_txt(file_name, **kwargs):
    """ Reads control points from a text file and generates a 1-dimensional list of control points.

    If argument ``jinja2=True`` is set, then the input file is processed as a `Jinja2 <http://jinja.pocoo.org/>`_
    template. You can also use the following convenience template functions which correspond to the given mathematical
    equations:

    * ``sqrt(x)``:  :math:`\\sqrt{x}`
    * ``cubert(x)``: :math:`\\sqrt[3]{x}`
    * ``pow(x, y)``: :math:`x^{y}`

    The following code examples illustrate the function usage:

    .. code-block:: python
        :linenos:

        # Import control points from a text file
        ctrlpts = exchange.import_txt(file_name="control_points.txt")

        # Import control points from a text file delimited with space
        ctrlpts = exchange.import_txt(file_name="control_points.txt", separator=" ")

    :param file_name: file name of the text file
    :type file_name: str
    :return: list of control points
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
    sep = kwargs.get('separator', ",")

    return exch.import_text_data(content, sep)


@export
def export_txt(obj, file_name, **kwargs):
    """ Exports control points as a text file.

    Please see :py:func:`.exchange.import_txt()` for detailed description of the keyword arguments.

    :param obj: a spline geometry object
    :type obj: abstract.SplineGeometry
    :param file_name: file name of the text file to be saved
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    # Check if the user has set any control points
    if obj.ctrlpts is None or len(obj.ctrlpts) == 0:
        raise GeomdlError("There are no control points to save!")

    # File delimiters
    sep = kwargs.get('separator', ",")

    content = exch.export_text_data(obj, sep)
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
    # Pick correct points from the object
    if point_type == 'ctrlpts':
        points = obj.ctrlptsw if obj.rational else obj.ctrlpts
    elif point_type == 'evalpts':
        points = obj.evalpts
    else:
        raise GeomdlError("Please choose a valid point type option. Possible types: ctrlpts, evalpts")

    # Prepare CSV header
    dim = len(points[0])
    line = "dim "
    for i in range(dim-1):
        line += str(i + 1) + ", dim "
    line += str(dim) + "\n"

    content = exch.export_text_data(obj, ',', line)
    return exch.write_file(file_name, content)


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
        raise GeomdlError("Please install 'libconf' package to use libconfig format: pip install libconf")

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
        raise GeomdlError("Please install 'libconf' package to use libconfig format: pip install libconf")

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
        raise GeomdlError("Please install 'ruamel.yaml' package to use YAML format: pip install ruamel.yaml")

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
        raise GeomdlError("Please install 'ruamel.yaml' package to use YAML format: pip install ruamel.yaml")

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
        raise GeomdlError("Can only export surfaces")
    if vertex_spacing < 1:
        raise GeomdlError("Vertex spacing should be bigger than zero")

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
        raise GeomdlError("Can only export surfaces")
    if vertex_spacing < 1:
        raise GeomdlError("Vertex spacing should be bigger than zero")

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
