"""
.. module:: algorithms
    :platform: Unix, Windows
    :synopsis: Geometry algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

# Disallow import-star (from XXX import *)
__all__ = []

# Import functions for convenience
from .knot_insert import insert_knot
from .knot_remove import remove_knot
from .knot_refine import refine_knotvector
from .derivative import derivative_curve, derivative_surface
from .split import split_curve, split_surface_u, split_surface_v
from .decompose import decompose_curve, decompose_surface
from .degree import degree_operations
