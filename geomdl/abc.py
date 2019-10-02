from __future__ import absolute_import

from abc import *
from . import _utilities as utl

@utl.add_metaclass(ABCMeta)
class GeomdlSequence(object):
    """ Abstract base for supported input types

    This class allows extensibility for registering additional input types
    e.g.

    import numpy as np
    GeomdlSequence.register(np.ndarray)
    """

GeomdlSequence.register(list)
GeomdlSequence.register(tuple)

