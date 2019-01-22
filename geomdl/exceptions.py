"""
.. module:: exceptions
    :platform: Unix, Windows
    :synopsis: Defines custom exceptions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from ._utilities import export


@export
class GeomdlNotPossibleException(Exception):
    """ Raised when called operation is not possible """
    pass
