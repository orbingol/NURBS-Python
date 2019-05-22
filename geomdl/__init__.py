""" Object-oriented B-Spline and NURBS evaluation library in pure Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

# Library version
__version__ = "5.2.6"

# Author and licence
__author__ = "Onur Rauf Bingol"
__license__ = "MIT"

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
