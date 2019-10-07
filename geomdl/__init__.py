""" GEOMDL - Object-oriented, self-contained, pure Python B-Spline and NURBS library

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>
.. moduleauthor:: The GEOMDL Contributors

"""

# Library version
__version__ = "6.0a1"

# Author and license
__author__ = "Onur R. Bingol and The GEOMDL Contributors"
__license__ = "MIT"

# Optional variables
__description__ = 'Object-oriented B-Spline and NURBS library'
__keywords__ = 'NURBS B-Spline curve surface CAD modeling visualization surface-generator'

# Support for "from geomdl import *"
# @see: https://stackoverflow.com/a/41895257
# @see: https://stackoverflow.com/a/35710527
__all__ = [
    'BSpline',
    'compatibility',
    'construct',
    'control_points',
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
