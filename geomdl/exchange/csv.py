"""
.. module:: exchange.csv
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for CSV file format

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import exc_helpers
from ..base import export, GeomdlError


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

    content = exc_helpers.read_file(file_name, skip_lines=1)
    return exc_helpers.import_text_data(content, sep)


@export
def export_csv_str(obj, **kwargs):
    """ Exports control points or evaluated points as a CSV string.

    This function exports evaluated points by default, ``point_type="evalpts"``.
    To export control points, use ``point_type="ctrlpts"``:

    .. code-block:: python
        :linenos:

        from geomdl.exchange import csv

        # weighted control points if rational
        csv_string = csv.export_csv_str(obj, point_type="ctrlpts")

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :raises GeomdlException: an error occurred writing the file
    """
    # Pick correct points from the object
    point_type = kwargs.get('point_type', "evalpts")
    if point_type == "ctrlpts":
        points = obj.ctrlptsw
    elif point_type == "evalpts":
        points = obj.evalpts
    else:
        raise GeomdlError("Please choose a valid point type option. Possible types: ctrlpts, evalpts")

    # Prepare CSV header
    dim = len(points[0])
    line = "dim "
    for i in range(dim-1):
        line += str(i + 1) + ", dim "
    line += str(dim) + "\n"

    return exc_helpers.export_text_data(obj, ',', line)


@export
def export_csv(obj, file_name, **kwargs):
    """ Exports control points or evaluated points as a CSV file.

    This function exports evaluated points by default, ``point_type="evalpts"``.
    To export control points, use ``point_type="ctrlpts"``:

    .. code-block:: python
        :linenos:

        from geomdl.exchange import csv

        # weighted control points if rational
        csv_string = csv.export_csv(obj, "my_geom_cpts.csv", point_type="ctrlpts")

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :param file_name: output file name
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    return exc_helpers.write_file(file_name, export_csv_str(obj, **kwargs))
