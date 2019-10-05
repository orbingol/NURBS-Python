""" Object-oriented B-Spline and NURBS evaluation library in pure Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

# Library version
__version__ = "5.2.9"

# Author and license
__author__ = "Onur Rauf Bingol"
__license__ = "MIT"

# Optional variables
__description__ = 'Object-oriented B-Spline and NURBS evaluation library'
__keywords__ = 'NURBS B-Spline curve surface CAD modeling visualization surface-generator'

# Support for "from geomdl import *"
# @see: https://stackoverflow.com/a/41895257
# @see: https://stackoverflow.com/a/35710527
__all__ = [
    'BSpline',
    'compatibility',
    'construct',
    'convert',
    'CPGen',
    'elements',
    'evaluators',
    'exchange',
    'exchange_vtk',
    'fitting',
    'helpers',
    'linalg',
    'multi',
    'NURBS',
    'operations',
    'ray',
    'tessellate',
    'utilities',
    'voxelize'
]

# Register default types for isinstance() checking
from .base import GeomdlTypeSequence, GeomdlTypeString

# Default types for sequences
GeomdlTypeSequence.register(list)
GeomdlTypeSequence.register(tuple)

# Default types for strings
GeomdlTypeString.register(str)
