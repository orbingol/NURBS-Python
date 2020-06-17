"""
.. module:: exchange.json
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for JSON file format

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import json
from . import exc_helpers
from ..base import GeomdlError

# Initialize an empty __all__ for controlling imports
__all__ = []


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
    use_template = kwargs.get('jinja2', False)

    # Read file
    file_src = exc_helpers.read_file(file_name)

    # Import data
    return exc_helpers.import_dict_str(file_src=file_src, callback=callback, tmpl=use_template)


def export_json_str(obj, file_name):
    """ Exports curves and surfaces in JSON format (string).

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
    return exc_helpers.export_dict_str(obj=obj, callback=callback)


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
    # Write to file
    return exc_helpers.write_file(file_name, export_json_str(obj, file_name))
