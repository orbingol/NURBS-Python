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
