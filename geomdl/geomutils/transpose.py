"""
.. module:: geomutils.transpose
    :platform: Unix, Windows
    :synopsis: Provides transpose functionality

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

import copy
from ..base import export, GeomdlError


@export
def transpose(surf, **kwargs):
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
        degree_u_new = g.degree.v
        degree_v_new = g.degree.u
        kv_u_new = g.knotvector.v
        kv_v_new = g.knotvector.u

        # Find new control points
        ctrlpts_new = []
        for u in range(0, g.ctrlpts_size.v):
            for v in range(0, g.ctrlpts_size.u):
                ctrlpts_new.append(g.ctrlptsw[u, v])

        g.degree = (degree_u_new, degree_v_new)
        g.knotvector = (kv_u_new, kv_v_new)
        g.set_ctrlpts(ctrlpts_new, g.ctrlpts_size.v, g.ctrlpts_size.u)

    return geom


@export
def flip(surf, **kwargs):
    """ Flips the control points grid of the input surface(s).

    Keyword Arguments:
        * ``inplace``: if False, operation applied to a copy of the object. *Default: False*

    :param surf: input surface(s)
    :type surf: abstract.Surface
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

    for i, g in enumerate(geom):
        new_cpts = [[] for _ in range(g.ctrlptsw.count)]
        idx = g.ctrlptsw.count - 1
        for pt in g.ctrlptsw:
            new_cpts[idx] = pt
            idx -= 1
        geom[i].set_ctrlpts(new_cpts, g.ctrlpts_size.u, g.ctrlpts_size.v)

    return geom
