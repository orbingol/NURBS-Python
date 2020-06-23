"""
.. module:: evaluators
    :platform: Unix, Windows
    :synopsis: B-spline evaulation and derivative algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

# Disallow import-star (from XXX import *)
__all__ = []

# Import functions for convenience
from .default import CurveEvaluator
from .default import CurveEvaluatorRational
from .default import SurfaceEvaluator
from .default import SurfaceEvaluatorRational
from .default import VolumeEvaluator
from .default import VolumeEvaluatorRational

from .default_ext import CurveEvaluator2
from .default_ext import SurfaceEvaluator2
