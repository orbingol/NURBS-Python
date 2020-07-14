"""
.. module:: exchange.txt
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for TXT file format

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import exc_helpers
from ..base import export, GeomdlError


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

        from geomdl.exchange import txt

        # Import control points from a text file
        ctrlpts = txt.import_txt("control_points.txt")

        # Import control points from a text file delimited with space
        ctrlpts = txt.import_txt("control_points.txt", separator=" ")

    :param file_name: file name of the text file
    :type file_name: str
    :return: list of control points
    :rtype: list
    :raises GeomdlException: an error occurred reading the file
    """
    # Read file
    content = exc_helpers.read_file(file_name)

    # Are we using a Jinja2 template?
    j2tmpl = kwargs.get('jinja2', False)
    if j2tmpl:
        content = exc_helpers.process_template(content)

    # File delimiters
    sep = kwargs.get('separator', ",")

    return exc_helpers.import_text_data(content, sep)


@export
def export_txt_str(obj, **kwargs):
    """ Exports control points in TXT format as a string.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :raises GeomdlException: an error occurred writing the file
    """
    # Check if the user has set any control points
    if obj.ctrlpts is None or len(obj.ctrlpts) == 0:
        raise GeomdlError("There are no control points to save!")

    # File delimiters
    sep = kwargs.get('separator', ",")

    return exc_helpers.export_text_data(obj, sep)


@export
def export_txt(obj, file_name, **kwargs):
    """ Exports control points as a text file.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :param file_name: file name of the text file to be saved
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    return exc_helpers.write_file(file_name, export_txt_str(obj, **kwargs))
