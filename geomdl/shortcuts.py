"""
.. module:: _shortcuts
    :platform: Unix, Windows
    :synopsis: Provides shortcut functions for creating new instances of the geomdl classes

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import BSpline, NURBS, multi, freeform


# Initialize an empty __all__ for controlling imports
__all__ = []


def generate_curve(rational=False):
    """ Returns a curve instance

    :param rational: if True, returns a rational curve instance
    :type rational: bool
    """
    if rational:
        return NURBS.Curve()
    return BSpline.Curve()


def generate_surface(rational=False):
    """ Returns a surface instance

    :param rational: if True, returns a rational surface instance
    :type rational: bool
    """
    if rational:
        return NURBS.Surface()
    return BSpline.Surface()


def generate_volume(rational=False):
    """ Returns a volume instance

    :param rational: if True, returns a rational volume instance
    :type rational: bool
    """
    if rational:
        return NURBS.Volume()
    return BSpline.Volume()


def generate_freeform():
    """ Returns a freeform instance """
    return freeform.Freeform()


def generate_container_curve():
    """ Returns a curve container instance """
    return multi.CurveContainer()


def generate_container_surface():
    """ Returns a surface container instance """
    return multi.SurfaceContainer()


def generate_container_volume():
    """ Returns a volume container instance """
    return multi.VolumeContainer()
