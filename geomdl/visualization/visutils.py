"""
.. module:: visualization.visutils
    :platform: Unix, Windows
    :synopsis: Provides utility functions for visualization module

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import random


def color_generator(num=1, seed=None):
    """ Generates random colors for visualization.

    The ``seed`` argument is used to set the random seed by directly passing the value to ``random.seed()`` function.
    Please see the Python documentation for more details on the ``random`` module .

    Inspired from https://stackoverflow.com/a/14019260

    :param num: number of color strings to be generated
    :param seed: Sets the random seed
    :return: list of color strings in hex format
    :rtype: list
    """
    def r_int():
        return random.randint(0, 255)
    if seed is not None:
        random.seed(seed)
    color_string = '#%02X%02X%02X'
    return [color_string % (r_int(), r_int(), r_int()) for _ in range(num)]
