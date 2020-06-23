"""
.. module:: fitting
    :platform: Unix, Windows
    :synopsis: Curve and surface fitting functions

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

# Disallow import-star (from XXX import *)
__all__ = []

from .interpolate_global import interpolate_curve
from .interpolate_global import interpolate_surface

from .approximate_global import approximate_curve
from .approximate_global import approximate_surface

