"""
.. module:: _shortcuts
    :platform: Unix, Windows
    :synopsis: Provides shortcut functions for creating new instances of the geometry classes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import NURBS
from . import freeform


# Initialize an empty __all__ for controlling imports
__all__ = []


def generate_nurbs_curve():
    return NURBS.Curve()


def generate_nurbs_surface():
    return NURBS.Surface()


def generate_nurbs_volume():
    return NURBS.Volume()


def generate_freeform():
    return freeform.Freeform()
