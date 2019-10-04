"""
.. module:: abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract base classes for representing the geometries

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from __future__ import absolute_import

import abc
from . import _utilities as utl


@utl.add_metaclass(abc.ABCMeta)
class GeomdlSequence(object):
    """ Abstract base for supported input types

    This class allows extensibility for registering additional input types
    e.g.

    import numpy as np
    GeomdlSequence.register(np.ndarray)
    """
    pass


GeomdlSequence.register(list)
GeomdlSequence.register(tuple)
