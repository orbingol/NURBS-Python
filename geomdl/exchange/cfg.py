"""
.. module:: exchange.cfg
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for CFG file format

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import exc_helpers
from ..base import export, GeomdlError


@export
def import_cfg(file_name, **kwargs):
    """ Imports curves and surfaces from files in libconfig format.

    .. note::

        Requires `libconf <https://pypi.org/project/libconf/>`_ package.

    Use ``jinja2=True`` to activate Jinja2 template processing. Please refer to the documentation for details.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of B-spline geometries
    :rtype: list
    """
    def callback(data):
        return libconf.loads(data)

    # Check if it is possible to import 'libconf'
    try:
        import libconf
    except ImportError:
        raise GeomdlError("Please install 'libconf' package to use libconfig format: pip install libconf")

    # Get keyword arguments
    use_template = kwargs.get('jinja2', False)

    # Read file
    file_src = exc_helpers.read_file(file_name)

    # Import data
    return exc_helpers.import_dict_str(file_src=file_src, callback=callback, tmpl=use_template)


@export
def export_cfg_str(obj):
    """ Exports curves and surfaces in libconfig format as a string.

    .. note::

        Requires `libconf <https://pypi.org/project/libconf/>`_ package.

    Libconfig format is also used by the `geomdl command-line application <https://github.com/orbingol/geomdl-cli>`_
    as a way to input shape data from the command line.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    """
    def callback(data):
        return libconf.dumps(data)

    # Check if it is possible to import 'libconf'
    try:
        import libconf
    except ImportError:
        raise GeomdlError("Please install 'libconf' package to use libconfig format: pip install libconf")

    # Export data
    return exc_helpers.export_dict_str(obj=obj, callback=callback)


@export
def export_cfg(obj, file_name):
    """ Exports curves and surfaces in libconfig format as a file.

    .. note::

        Requires `libconf <https://pypi.org/project/libconf/>`_ package.

    Libconfig format is also used by the `geomdl command-line application <https://github.com/orbingol/geomdl-cli>`_
    as a way to input shape data from the command line.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :param file_name: name of the output file
    :type file_name: str
    """
    # Write to file
    return exc_helpers.write_file(file_name, export_cfg_str(obj))
