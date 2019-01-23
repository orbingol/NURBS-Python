"""
.. module:: exceptions
    :platform: Unix, Windows
    :synopsis: Defines custom exceptions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from ._utilities import export

ERROR_PREFIX = "GEOMDL ERROR: "


@export
class GeomdlException(Exception):
    """ Custom exception for controlling geometric errors.

    The error details can be retrieved by querying ``data`` class member. The following snippet illustrates a sample
    usage of this exception.

    .. code-example: python

        from geomdl import exceptions

        DEBUG = True

        # Catch the exception
        try:
            # Do something which can raise this exception
        except GeomdlException as e:
            print(e)
            if DEBUG:
                print(e.data)
            # Stop execution of the function
            return
    """
    def __init__(self, msg, data=None):
        super(GeomdlException, self).__init__(ERROR_PREFIX + msg)
        self.data = data
