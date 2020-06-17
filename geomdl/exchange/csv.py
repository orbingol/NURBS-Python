"""
.. module:: exchange.csv
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for CSV file format

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import exc_helpers
from ..base import GeomdlError

# Initialize an empty __all__ for controlling imports
__all__ = []


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


def export_csv_str(obj, file_name, point_type='evalpts', **kwargs):
    """ Exports control points or evaluated points as a CSV file (string).

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

    return exc_helpers.export_text_data(obj, ',', line)


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
    return exc_helpers.write_file(file_name, export_csv_str(obj, file_name, point_type, **kwargs))
