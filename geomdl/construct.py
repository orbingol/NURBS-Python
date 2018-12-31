"""
.. module:: construct
    :platform: Unix, Windows
    :synopsis: Contains functions for constructing parametric surfaces and volumes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import BSpline
from . import NURBS
from . import utilities
from . import convert


def construct_surface(*args, **kwargs):
    """ Generates NURBS surfaces from parametric curves.

    :return: NURBS surface
    :rtype: NURBS.Surface
    """
    # Get keyword arguments
    degree_v = kwargs.get('degree', 2)

    size_v = len(args)
    if size_v < 2:
        raise ValueError("You need to input at least 2 curves")

    # Construct the control points of the new surface
    degree_u = args[0].degree
    size_u = args[0].ctrlpts_size
    new_ctrlptsw = []
    for arg in args:
        if degree_u != arg.degree:
            raise ValueError("Input curves must have the same degrees")
        if size_u != arg.ctrlpts_size:
            raise ValueError("Input curves must have the same number of control points")
        nc = arg if arg.rational else convert.bspline_to_nurbs(arg)
        new_ctrlptsw += list(nc.ctrlptsw)

    # Generate the surface
    ns = NURBS.Surface()
    ns.degree_u = degree_u
    ns.degree_v = degree_v
    ns.ctrlpts_size_u = size_u
    ns.ctrlpts_size_v = size_v
    ns.ctrlptsw = new_ctrlptsw
    ns.knotvector_u = args[0].knotvector
    ns.knotvector_v = utilities.generate_knot_vector(degree_v, size_v)

    return ns


def construct_volume(*args, **kwargs):
    """ Generates NURBS volumes from parametric surfaces.

    :return: NURBS volume
    :rtype: NURBS.Volume
    """
    # Get keyword arguments
    degree_w = kwargs.get('degree', 1)

    size_w = len(args)
    if size_w < 2:
        raise ValueError("You need to input at least 2 surfaces")

    # Construct the control points of the new volume
    degree_u, degree_v = args[0].degree_u, args[0].degree_v
    size_u, size_v = args[0].ctrlpts_size_u, args[0].ctrlpts_size_v
    new_ctrlptsw = []
    for arg in args:
        if degree_u != arg.degree_u or degree_v != arg.degree_v:
            raise ValueError("Input surfaces must have the same degrees")
        if size_u != arg.ctrlpts_size_u or size_v != arg.ctrlpts_size_v:
            raise ValueError("Input surfaces must have the same number of control points")
        ns = arg if arg.rational else convert.bspline_to_nurbs(arg)
        new_ctrlptsw += list(ns.ctrlptsw)

    # Generate the volume
    nv = NURBS.Volume()
    nv.degree_u = degree_u
    nv.degree_v = degree_v
    nv.degree_w = degree_w
    nv.ctrlpts_size_u = size_u
    nv.ctrlpts_size_v = size_v
    nv.ctrlpts_size_w = size_w
    nv.ctrlptsw = new_ctrlptsw
    nv.knotvector_u = args[0].knotvector_u
    nv.knotvector_v = args[0].knotvector_v
    nv.knotvector_w = utilities.generate_knot_vector(degree_w, size_w)

    return nv


def extract_curves(psurf):
    """ Extracts curves from a parametric surface.

    :param psurf: input surface
    :type psurf: abstract.Surface
    :return: extracted curves
    :rtype: dict
    """
    if not isinstance(psurf, BSpline.abstract.Surface):
        raise TypeError("The input should be an instance of abstract.Surface")

    # Get data from the surface object
    surf_data = psurf.data
    rational = surf_data['rational']
    degree_u = surf_data['degree'][0]
    degree_v = surf_data['degree'][1]
    kv_u = surf_data['knotvector'][0]
    kv_v = surf_data['knotvector'][1]
    size_u = surf_data['size'][0]
    size_v = surf_data['size'][1]
    cpts = surf_data['control_points']

    # Determine object type
    obj = NURBS.Curve if rational else BSpline.Curve

    # v-direction
    crvlist_v = []
    for u in range(size_u):
        curve = obj()
        curve.degree = degree_v
        curve.set_ctrlpts([cpts[v + (size_v * u)] for v in range(size_v)])
        curve.knotvector = kv_v
        crvlist_v.append(curve)

    # u-direction
    crvlist_u = []
    for v in range(size_v):
        curve = obj()
        curve.degree = degree_u
        curve.set_ctrlpts([cpts[v + (size_v * u)] for u in range(size_u)])
        curve.knotvector = kv_u
        crvlist_u.append(curve)

    # Return shapes as a dict object
    return dict(u=crvlist_u, v=crvlist_v)


def extract_surfaces(pvol):
    """ Extracts surfaces from a parametric volume.

    :param pvol: input volume
    :type pvol: abstract.Volume
    :return: extracted surface
    :rtype: dict
    """
    if not isinstance(pvol, BSpline.abstract.Volume):
        raise TypeError("The input should be an instance of abstract.Volume")

    # Get data from the volume object
    vol_data = pvol.data
    rational = vol_data['rational']
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

    # Determine object type
    obj = NURBS.Surface if rational else BSpline.Surface

    # u-v plane
    surflist_uv = []
    for w in range(size_w):
        surf = obj()
        surf.degree_u = degree_u
        surf.degree_v = degree_v
        surf.ctrlpts_size_u = size_u
        surf.ctrlpts_size_v = size_v
        surf.ctrlpts2d = [[cpts[v + (size_v * (u + (size_u * w)))] for v in range(size_v)] for u in range(size_u)]
        surf.knotvector_u = kv_u
        surf.knotvector_v = kv_v
        surflist_uv.append(surf)

    # u-w plane
    surflist_uw = []
    for v in range(size_v):
        surf = obj()
        surf.degree_u = degree_u
        surf.degree_v = degree_w
        surf.ctrlpts_size_u = size_u
        surf.ctrlpts_size_v = size_w
        surf.ctrlpts2d = [[cpts[v + (size_v * (u + (size_u * w)))] for w in range(size_w)] for u in range(size_u)]
        surf.knotvector_u = kv_u
        surf.knotvector_v = kv_w
        surflist_uw.append(surf)

    # v-w plane
    surflist_vw = []
    for u in range(size_u):
        surf = obj()
        surf.degree_u = degree_v
        surf.degree_v = degree_w
        surf.ctrlpts_size_u = size_v
        surf.ctrlpts_size_v = size_w
        surf.ctrlpts2d = [[cpts[v + (size_v * (u + (size_u * w)))] for w in range(size_w)] for v in range(size_v)]
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

        # Create a surface container
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
    if not isinstance(pvol, BSpline.abstract.Volume):
        raise TypeError("The input should be an instance of abstract.Volume")

    # Extract surfaces from the parametric volume
    isosrf = extract_surfaces(pvol)

    # Return the isosurface
    return isosrf['uv'][0], isosrf['uv'][-1], isosrf['uw'][0], isosrf['uw'][-1], isosrf['vw'][0], isosrf['vw'][-1]
