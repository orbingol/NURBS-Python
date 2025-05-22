"""Object-oriented B-Spline and NURBS evaluation library in pure Python

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

# Library version
__version__ = "5.3.1"

# Support for "from geomdl import *"
# @see: https://stackoverflow.com/a/41895257
# @see: https://stackoverflow.com/a/35710527
__all__ = [
    "BSpline",
    "compatibility",
    "construct",
    "convert",
    "CPGen",
    "elements",
    "evaluators",
    "exchange",
    "exchange_vtk",
    "fitting",
    "helpers",
    "linalg",
    "multi",
    "NURBS",
    "operations",
    "ray",
    "tessellate",
    "utilities",
    "voxelize",
]


def geomdl_version():
    """Returns geomdl full version as a tuple"""
    return tuple(__version__.split("."))
