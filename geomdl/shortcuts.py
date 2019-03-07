"""
.. module:: _shortcuts
    :platform: Unix, Windows
    :synopsis: Provides shortcut functions for creating new instances of the geomdl classes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline
from . import NURBS
from . import multi
from . import freeform


# Initialize an empty __all__ for controlling imports
__all__ = []


def generate_bspline_curve():
    return BSpline.Curve()


def generate_bspline_surface():
    return BSpline.Surface()


def generate_bspline_volume():
    return BSpline.Volume()


def generate_nurbs_curve():
    return NURBS.Curve()


def generate_nurbs_surface():
    return NURBS.Surface()


def generate_nurbs_volume():
    return NURBS.Volume()


def generate_freeform():
    return freeform.Freeform()


def generate_container_curve():
    return multi.CurveContainer()


def generate_container_surface():
    return multi.SurfaceContainer()


def generate_container_volume():
    return multi.VolumeContainer()
