"""
.. module:: geomutils.transpose
    :platform: Unix, Windows
    :synopsis: Provides transpose functionality

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from ..base import GeomdlError

__all__ = []


def apply_transpose(surf, **kwargs):
    """ Transposes the input surface(s) by swapping u and v parametric directions.

    Keyword Arguments:
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param surf: input surface(s)
    :type surf: abstract.Surface, multi.SurfaceContainer
    :return: transposed surface(s)
    """
    if surf.pdimension != 2:
        raise GeomdlError("Can only transpose surfaces")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    if not inplace:
        geom = copy.deepcopy(surf)
    else:
        geom = surf

    for g in geom:
        # Get existing data
        degree_u_new = g.degree_v
        degree_v_new = g.degree_u
        kv_u_new = g.knotvector_v
        kv_v_new = g.knotvector_u
        ctrlpts2d_old = g.ctrlpts2d

        # Find new control points
        ctrlpts2d_new = []
        for v in range(0, g.ctrlpts_size_v):
            ctrlpts_u = []
            for u in range(0, g.ctrlpts_size_u):
                temp = ctrlpts2d_old[u][v]
                ctrlpts_u.append(temp)
            ctrlpts2d_new.append(ctrlpts_u)

        g.degree_u = degree_u_new
        g.degree_v = degree_v_new
        g.ctrlpts2d = ctrlpts2d_new
        g.knotvector_u = kv_u_new
        g.knotvector_v = kv_v_new

    return geom


def apply_flip(surf, **kwargs):
    """ Flips the control points grid of the input surface(s).

    Keyword Arguments:
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param surf: input surface(s)
    :type surf: abstract.Surface, multi.SurfaceContainer
    :return: flipped surface(s)
    """
    if surf.pdimension != 2:
        raise GeomdlError("Can only flip surfaces")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    if not inplace:
        geom = copy.deepcopy(surf)
    else:
        geom = surf

    for g in geom:
        size_u = g.ctrlpts_size_u
        size_v = g.ctrlpts_size_v
        cpts = g.ctrlptsw if g.rational else g.ctrlpts
        new_cpts = [[] for _ in range(g.ctrlpts_size)]
        idx = g.ctrlpts_size - 1
        for pt in cpts:
            new_cpts[idx] = pt
            idx -= 1
        g.set_ctrlpts(new_cpts, size_u, size_v)

    return geom
