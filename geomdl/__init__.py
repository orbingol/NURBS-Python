"""Object-oriented B-Spline and NURBS evaluation library in pure Python

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import pathlib


def geomdl_version():
    version_file = pathlib.Path(__file__).parent / "VERSION.txt"
    if version_file.exists():
        return version_file.read_text()
    return "0.0.0-dev"


# Library version
__version__ = geomdl_version()

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
