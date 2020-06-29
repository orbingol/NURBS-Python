"""
.. module:: geomutils.extract
    :platform: Unix, Windows
    :synopsis: Provides functions for extracting B-spline geometries

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import NURBS
from ..base import GeomdlError


def extract_curves(psurf, **kwargs):
    """ Extracts curves from a surface.

    The return value is a ``dict`` object containing the following keys:

    * ``u``: the curves which generate u-direction (or which lie on the v-direction)
    * ``v``: the curves which generate v-direction (or which lie on the u-direction)

    As an example; if a curve lies on the u-direction, then its knotvector is equal to surface's knotvector on the
    v-direction and vice versa.

    The curve extraction process can be controlled via ``extract_u`` and ``extract_v`` boolean keyword arguments.

    :param psurf: input surface
    :type psurf: abstract.Surface
    :return: extracted curves
    :rtype: dict
    """
    if psurf.pdimension != 2:
        raise GeomdlError("The input should be a spline surface")
    if len(psurf) != 1:
        raise GeomdlError("Can only operate on single spline surfaces")

    # Get keyword arguments
    extract_u = kwargs.get('extract_u', True)
    extract_v = kwargs.get('extract_v', True)

    # Get data from the surface object
    surf_data = psurf.data
    degree_u = surf_data['degree'][0]
    degree_v = surf_data['degree'][1]
    kv_u = surf_data['knotvector'][0]
    kv_v = surf_data['knotvector'][1]
    size_u = surf_data['size'][0]
    size_v = surf_data['size'][1]
    cpts = surf_data['control_points']

    # v-direction
    crvlist_v = []
    if extract_v:
        for u in range(size_u):
            curve = NURBS.Curve()
            curve.degree = degree_v
            curve.set_ctrlpts([cpts[u + (size_u * v)] for v in range(size_v)])
            curve.knotvector = kv_v
            crvlist_v.append(curve)

    # u-direction
    crvlist_u = []
    if extract_u:
        for v in range(size_v):
            curve = NURBS.Curve()
            curve.degree = degree_u
            curve.set_ctrlpts([cpts[u + (size_u * v)] for u in range(size_u)])
            curve.knotvector = kv_u
            crvlist_u.append(curve)

    # Return shapes as a dict object
    return dict(u=crvlist_u, v=crvlist_v)


def extract_surfaces(pvol):
    """ Extracts surfaces from a volume.

    :param pvol: input volume
    :type pvol: abstract.Volume
    :return: extracted surface
    :rtype: dict
    """
    if pvol.pdimension != 3:
        raise GeomdlError("The input should be a spline volume")
    if len(pvol) != 1:
        raise GeomdlError("Can only operate on single spline volumes")

    # Get data from the volume object
    vol_data = pvol.data
    degree_u = vol_data['degree'][0]
    degree_v = vol_data['degree'][1]
    degree_w = vol_data['degree'][2]
    kv_u = vol_data['knotvector'][0]
    kv_v = vol_data['knotvector'][1]
    kv_w = vol_data['knotvector'][2]
    size_u = vol_data['size'][0]
    size_v = vol_data['size'][1]
    size_w = vol_data['size'][2]
    cpts = vol_data['control_points']

    # u-v plane
    surflist_uv = []
    for w in range(size_w):
        surf = NURBS.Surface()
        surf.degree_u = degree_u
        surf.degree_v = degree_v
        surf.ctrlpts_size_u = size_u
        surf.ctrlpts_size_v = size_v
        surf.ctrlpts2d = [[cpts[u + (size_u * (v + (size_v * w)))] for v in range(size_v)] for u in range(size_u)]
        surf.knotvector_u = kv_u
        surf.knotvector_v = kv_v
        surflist_uv.append(surf)

    # u-w plane
    surflist_uw = []
    for v in range(size_v):
        surf = NURBS.Surface()
        surf.degree_u = degree_u
        surf.degree_v = degree_w
        surf.ctrlpts_size_u = size_u
        surf.ctrlpts_size_v = size_w
        surf.ctrlpts2d = [[cpts[u + (size_u * (v + (size_v * w)))] for w in range(size_w)] for u in range(size_u)]
        surf.knotvector_u = kv_u
        surf.knotvector_v = kv_w
        surflist_uw.append(surf)

    # v-w plane
    surflist_vw = []
    for u in range(size_u):
        surf = NURBS.Surface()
        surf.degree_u = degree_v
        surf.degree_v = degree_w
        surf.ctrlpts_size_u = size_v
        surf.ctrlpts_size_v = size_w
        surf.ctrlpts2d = [[cpts[u + (size_u * (v + (size_v * w)))] for w in range(size_w)] for v in range(size_v)]
        surf.knotvector_u = kv_v
        surf.knotvector_v = kv_w
        surflist_vw.append(surf)

    # Return shapes as a dict object
    return dict(uv=surflist_uv, uw=surflist_uw, vw=surflist_vw)


def extract_isosurface(pvol):
    """ Extracts the largest isosurface from a volume.

    The following example illustrates one of the usage scenarios:

    .. code-block:: python
        :linenos:

        from geomdl import construct, multi
        from geomdl.visualization import VisMPL

        # Assuming that "myvol" variable stores your spline volume information
        isosrf = construct.extract_isosurface(myvol)

        # Create a surface container to store extracted isosurface
        msurf = multi.SurfaceContainer(isosrf)

        # Set visualization components
        msurf.vis = VisMPL.VisSurface(VisMPL.VisConfig(ctrlpts=False))

        # Render isosurface
        msurf.render()

    :param pvol: input volume
    :type pvol: abstract.Volume
    :return: isosurface (as a tuple of surfaces)
    :rtype: tuple
    """
    if pvol.pdimension != 3:
        raise GeomdlError("The input should be a spline volume")
    if len(pvol) != 1:
        raise GeomdlError("Can only operate on single spline volumes")

    # Extract surfaces from the parametric volume
    isosrf = extract_surfaces(pvol)

    # Return the isosurface
    return isosrf['uv'][0], isosrf['uv'][-1], isosrf['uw'][0], isosrf['uw'][-1], isosrf['vw'][0], isosrf['vw'][-1]