"""
.. module:: utilities
    :platform: Unix, Windows
    :synopsis: Contains common utility functions for linear algebra, data validation, etc.

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import random

# Preserve the knot vector functions for compatibility
from . import knotvector
generate_knot_vector = knotvector.generate
check_knot_vector = knotvector.check
normalize_knot_vector = knotvector.normalize


def color_generator(seed=None):
    """ Generates random colors for control and evaluated curve/surface points plots.

    The ``seed`` argument is used to set the random seed by directly passing the value to ``random.seed()`` function.
    Please see the Python documentation for more details on the ``random`` module .

    Inspired from https://stackoverflow.com/a/14019260

    :param seed: Sets the random seed
    :return: list of color strings in hex format
    :rtype: list
    """
    def r_int():
        return random.randint(0, 255)
    if seed is not None:
        random.seed(seed)
    color_string = '#%02X%02X%02X'
    return [color_string % (r_int(), r_int(), r_int()), color_string % (r_int(), r_int(), r_int())]
