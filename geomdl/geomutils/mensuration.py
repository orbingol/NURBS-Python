"""
.. module:: geomutils.mensuration
    :platform: Unix, Windows
    :synopsis: Provides measurement functionality

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

# Ref 1: https://www.merriam-webster.com/dictionary/mensuration
# Ref 2: https://en.wikipedia.org/wiki/Mensuration

from .. import linalg
from ..base import GeomdlError

__all__ = []


def length_curve(obj):
    """ Computes the approximate length of the parametric curve.

    Uses the following equation to compute the approximate length:

    .. math::

        \\sum_{i=0}^{n-1} \\sqrt{P_{i + 1}^2-P_{i}^2}

    where :math:`n` is number of evaluated curve points and :math:`P` is the n-dimensional point.

    :param obj: input curve
    :type obj: abstract.Curve
    :return: length
    :rtype: float
    """
    if obj.pdimension != 1:
        raise GeomdlError("Input is not a curve")

    length = 0.0
    evalpts = obj.evalpts
    num_evalpts = len(obj.evalpts)
    for idx in range(num_evalpts - 1):
        length += linalg.point_distance(evalpts[idx], evalpts[idx + 1])
    return length
