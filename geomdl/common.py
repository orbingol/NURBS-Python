"""
.. module:: common
    :platform: Unix, Windows
    :synopsis: Common utility functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""


def linspace(start, stop, num, decimals=6):
    """ Returns a list of evenly spaced numbers over a specified interval.

    Inspired from Numpy's linspace function: https://github.com/numpy/numpy/blob/master/numpy/core/function_base.py

    :param start: starting value
    :type start: float
    :param stop: end value
    :type stop: float
    :param num: number of samples to generate
    :type num: int
    :param decimals: number of significands
    :type decimals: int
    :return: a list of equally spaced numbers
    :rtype: list
    """
    start = float(start)
    stop = float(stop)
    num = int(num)
    div = num - 1
    delta = stop - start
    return [float(("%0." + str(decimals) + "f") % (float(x) * delta / div)) for x in range(num)]
