"""
.. module:: _exchange
    :platform: Unix, Windows
    :synopsis: Helper functions for exchange module

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import math
from . import utilities
from .base import GeomdlError

# Initialize an empty __all__ for controlling imports
__all__ = []


def process_template(file_src):
    """ Process Jinja2 template input

    :param file_src: file contents
    :type file_src: str
    """
    def tmpl_sqrt(x):
        """ Square-root of 'x' """
        return math.sqrt(x)

    def tmpl_cubert(x):
        """ Cube-root of 'x' """
        return x ** (1.0 / 3.0) if x >= 0 else -(-x) ** (1.0 / 3.0)

    def tmpl_pow(x, y):
        """ 'x' to the power 'y' """
        return math.pow(x, y)

    # Check if it is possible to import 'jinja2'
    try:
        import jinja2
    except ImportError:
        raise GeomdlError("Please install 'jinja2' package to use templated input: pip install jinja2")

    # Replace jinja2 template tags for compatibility
    fsrc = file_src.replace("{%", "<%").replace("%}", "%>").replace("{{", "<{").replace("}}", "}>")

    # Generate Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.BaseLoader(),
        trim_blocks=True,
        block_start_string='<%', block_end_string='%>',
        variable_start_string='<{', variable_end_string='}>'
    ).from_string(fsrc)

    # Load custom functions into the Jinja2 environment
    template_funcs = dict(
        knot_vector=utilities.generate_knot_vector,
        sqrt=tmpl_sqrt,
        cubert=tmpl_cubert,
        pow=tmpl_pow,
    )
    for k, v in template_funcs.items():
        env.globals[k] = v

    # Process Jinja2 template functions & variables inside the input file
    return env.render()


def read_file(file_name, **kwargs):
    binary = kwargs.get('binary', False)
    skip_lines = kwargs.get('skip_lines', 0)
    callback = kwargs.get('callback', None)
    try:
        with open(file_name, 'rb' if binary else 'r') as fp:
            for _ in range(skip_lines):
                next(fp)
            content = fp.read() if callback is None else callback(fp)
        return content
    except IOError as e:
        raise GeomdlError("An error occurred during reading '{0}': {1}".format(file_name, e.args[-1]))
    except Exception as e:
        raise GeomdlError("An error occurred: {0}".format(str(e)))


def write_file(file_name, content, **kwargs):
    binary = kwargs.get('binary', False)
    callback = kwargs.get('callback', None)
    try:
        with open(file_name, 'wb' if binary else 'w') as fp:
            if callback is None:
                fp.write(content)
            else:
                callback(fp, content)
        return True
    except IOError as e:
        raise GeomdlError("An error occurred during writing '{0}': {1}".format(file_name, e.args[-1]))
    except Exception as e:
        raise GeomdlError("An error occurred: {0}".format(str(e)))


def import_dict_crv(data):
    shape = shortcuts.generate_curve(rational=True)

    # Mandatory keys
    try:
        shape.degree = data['degree']
        shape.ctrlpts = data['control_points']['points']
        shape.knotvector = data['knotvector']
    except KeyError as e:
        raise RuntimeError("Required key does not exist in the input data: {}".format(e.args[-1]))

    # Optional keys
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    if 'id' in data:
        shape.id = data['id']
    if 'reversed' in data:  # trim curve sense
        shape.opt = ['reversed', data['reversed']]

    # Return curve
    return shape


def export_dict_crv(obj):
    data = dict(
        type="spline",
        rational=obj.rational,
        dimension=obj.dimension,
        degree=obj.degree,
        knotvector=list(obj.knotvector),
        control_points=dict(
            points=obj.ctrlpts
        ),
        delta=obj.delta
    )
    if obj.rational:
        data['control_points']['weights'] = list(obj.weights)

    # For trim curves
    sense = obj.get_opt('reversed')
    if sense is not None:
        data['reversed'] = sense

    return data


def import_dict_ff(data):
    shape = shortcuts.generate_freeform()

    # Mandatory keys
    try:
        shape.evaluate(points=data['points'])
    except KeyError as e:
        raise GeomdlError("Required key does not exist in the input data: {}".format(e.args[-1]))

    if 'name' in data:
        shape.name = data['name']
    if 'id' in data:
        shape.id = data['id']
    if 'reversed' in data:  # trim curve sense
        shape.opt = ['reversed', data['reversed']]

    return shape


def export_dict_ff(obj):
    data = dict(
        type="freeform",
        dimension=obj.dimension,
        points=obj.evalpts,
        name=obj.name
    )

    # For trim curves
    sense = obj.get_opt('reversed')
    if sense is not None:
        data['reversed'] = sense

    return data


def import_dict_multi_crv(data):
    shape = shortcuts.generate_container_curve()
    curve_typemap = dict(spline=import_dict_crv, freeform=import_dict_ff)
    for trim in data['data']:
        if trim['type'] in curve_typemap:
            tcurve = curve_typemap[trim['type']](trim)
            shape.add(tcurve)
    if 'name' in data:
        shape.name = data['name']
    if 'id' in data:
        shape.id = data['id']
    if 'reversed' in data:  # trim curve sense
        shape.opt = ['reversed', data['reversed']]
    return shape


def export_dict_multi_crv(obj):
    curve_typemap = dict(spline=export_dict_crv, freeform=export_dict_ff)
    curves = []
    for o in obj:
        if o.type in curve_typemap:
            tdata = curve_typemap[o.type](o)
        else:
            tdata = curve_typemap['freeform'](o)
        curves.append(tdata)

    data = dict(
        type="container",
        count=len(curves),
        data=curves
    )

    # For trim curves
    sense = obj.get_opt('reversed')
    if sense is not None:
        data['reversed'] = sense

    return data


def import_dict_surf(data):
    shape = shortcuts.generate_surface(rational=True)

    # Mandatory keys
    try:
        shape.degree_u = data['degree_u']
        shape.degree_v = data['degree_v']
        shape.ctrlpts_size_u = data['size_u']
        shape.ctrlpts_size_v = data['size_v']
        shape.ctrlpts = data['control_points']['points']
        shape.knotvector_u = data['knotvector_u']
        shape.knotvector_v = data['knotvector_v']
    except KeyError as e:
        raise GeomdlError("Required key does not exist in the input data: {}".format(e.args[-1]))

    # Optional keys
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    if 'id' in data:
        shape.id = data['id']
    if 'reversed' in data:  # surface sense
        shape.opt = ['reversed', data['reversed']]

    # Trim curves
    if 'trims' in data:
        trim_curve_typemap = dict(spline=import_dict_crv, freeform=import_dict_ff, container=import_dict_multi_crv)
        trim_curves = []
        for trim in data['trims']['data']:
            if trim['type'] in trim_curve_typemap:
                tcurve = trim_curve_typemap[trim['type']](trim)
                trim_curves.append(tcurve)
        shape.trims = trim_curves
    # Return surface
    return shape


def export_dict_surf(obj):
    data = dict(
        type="spline",
        rational=obj.rational,
        dimension=obj.dimension,
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
    if obj.rational:
        data['control_points']['weights'] = list(obj.weights)

    # Surface sense
    sense = obj.get_opt('reversed')
    if sense is not None:
        data['reversed'] = sense

    # Converter mapping for trim curves
    trim_curve_typemap = dict(
        spline=export_dict_crv,
        freeform=export_dict_ff,
        container=export_dict_multi_crv
    )

    # Trim curves
    if obj.trims:
        trim_curves = []
        for trim in obj.trims:
            if trim.type in trim_curve_typemap:
                tdata = trim_curve_typemap[trim.type](trim)
            else:
                tdata = trim_curve_typemap['freeform'](trim)
            trim_curves.append(tdata)
        trim_data = dict(
            count=len(trim_curves),
            data=trim_curves
        )
        data['trims'] = trim_data

    return data


def import_dict_vol(data):
    shape = shortcuts.generate_volume(rational=True)

    # Mandatory keys
    try:
        shape.degree_u = data['degree_u']
        shape.degree_v = data['degree_v']
        shape.degree_w = data['degree_w']
        shape.ctrlpts_size_u = data['size_u']
        shape.ctrlpts_size_v = data['size_v']
        shape.ctrlpts_size_w = data['size_w']
        shape.ctrlpts = data['control_points']['points']
        shape.knotvector_u = data['knotvector_u']
        shape.knotvector_v = data['knotvector_v']
        shape.knotvector_w = data['knotvector_w']
    except KeyError as e:
        raise GeomdlError("Required key does not exist in the input data: {}".format(e.args[-1]))

    # Optional keys
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    if 'id' in data:
        shape.id = data['id']

    # Return volume
    return shape


def export_dict_vol(obj):
    data = dict(
        type="spline",
        rational=obj.rational,
        dimension=obj.dimension,
        degree_u=obj.degree_u,
        degree_v=obj.degree_v,
        degree_w=obj.degree_w,
        knotvector_u=list(obj.knotvector_u),
        knotvector_v=list(obj.knotvector_v),
        knotvector_w=list(obj.knotvector_w),
        size_u=obj.ctrlpts_size_u,
        size_v=obj.ctrlpts_size_v,
        size_w=obj.ctrlpts_size_w,
        control_points=dict(
            points=obj.ctrlpts
        ),
        delta=obj.delta
    )
    if obj.rational:
        data['control_points']['weights'] = list(obj.weights)
    return data


def import_text_data(content, sep):
    lines = content.strip().split("\n")
    ctrlpts = []

    # Start reading file
    for line in lines:
        # Remove whitespace
        line = line.strip()
        # Clean and convert the values
        ctrlpts.append([float(c.strip()) for c in line.split(sep)])

    # Return control points
    return ctrlpts


def export_text_data(obj, sep, result=""):
    ctrlpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
    # Loop through points
    for pt in ctrlpts:
        result += sep.join(str(c) for c in pt) + "\n"
    return result


def import_dict_str(file_src, delta, callback, tmpl):
    mapping = {'curve': import_dict_crv, 'surface': import_dict_surf, 'volume': import_dict_vol}

    # Process template
    if tmpl:
        file_src = process_template(file_src)
    # Execute callback function
    imported_data = callback(file_src)

    # Process imported data
    ret_list = []
    for data in imported_data['shape']['data']:
        temp = mapping[imported_data['shape']['type']](data)
        if 0.0 < delta < 1.0:
            temp.delta = delta
        ret_list.append(temp)

    # Return imported data
    return ret_list


def export_dict_str(obj, callback):
    if obj.pdimension == 1:
        export_type = "curve"
        data = [export_dict_crv(o) for o in obj]
    elif obj.pdimension == 2:
        export_type = "surface"
        data = [export_dict_surf(o) for o in obj]
    elif obj.pdimension == 3:
        export_type = "volume"
        data = [export_dict_vol(o) for o in obj]
    else:
        raise GeomdlError("Cannot export input geometry")

    # Create the dictionary
    data = dict(
        shape=dict(
            type=export_type,
            count=len(obj),
            data=tuple(data)
        )
    )

    # Execute callback function
    exported_data = callback(data)

    return exported_data
