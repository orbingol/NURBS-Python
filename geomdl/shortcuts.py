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


def generate_curve(rational=False):
    if rational:
        return NURBS.Curve()
    return BSpline.Curve()


def generate_surface(rational=False):
    if rational:
        return NURBS.Surface()
    return BSpline.Surface()


def generate_volume(rational=False):
    if rational:
        return NURBS.Volume()
    return BSpline.Volume()


def generate_freeform():
    return freeform.Freeform()


def generate_container_curve():
    return multi.CurveContainer()


def generate_container_surface():
    return multi.SurfaceContainer()


def generate_container_volume():
    return multi.VolumeContainer()
