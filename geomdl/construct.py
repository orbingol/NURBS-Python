"""
.. module:: construct
    :platform: Unix, Windows
    :synopsis: Provides functions for constructing and extracting spline geometries

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import NURBS, control_points, knotvector
from .base import GeomdlError


def construct_surface(direction, *args, **kwargs):
    """ Generates surfaces from curves.

    Arguments:
        * ``args``: a list of curve instances

    Keyword Arguments (optional):
        * ``degree``: degree of the 2nd parametric direction
        * ``knotvector``: knot vector of the 2nd parametric direction

    :param direction: the direction that the input curves lies, i.e. u or v
    :type direction: str
    :return: Surface constructed from the curves on the given parametric direction
    """
    # Input validation
    possible_dirs = ['u', 'v']
    if direction not in possible_dirs:
        raise GeomdlError("Possible direction values: " + ", ".join([val for val in possible_dirs]),
                          data=dict(input_dir=direction))

    size_other = len(args)
    if size_other < 2:
        raise GeomdlError("Input should be at least 2 curves")

    # Get keyword arguments
    degree_other = kwargs.get('degree', 2)
    knotvector_other = kwargs.get('knotvector', knotvector.generate(degree_other, size_other))
    rational = args[0].rational

    # Construct the control points of the new surface
    degree = args[0].degree.u
    num_ctrlpts = args[0].ctrlpts.count
    new_ctrlpts = []
    new_weights = []
    for idx, arg in enumerate(args):
        if degree != arg.degree.u:
            raise GeomdlError("Input curves must have the same degrees",
                              data=dict(idx=idx, degree=degree, degree_arg=arg.degree))
        if num_ctrlpts != arg.ctrlpts.count:
            raise GeomdlError("Input curves must have the same number of control points",
                              data=dict(idx=idx, size=num_ctrlpts, size_arg=arg.ctrlpts.count))
        new_ctrlpts += list(arg.ctrlpts)
        if rational:
            if not arg.weights:
                new_weights += [1.0 for _ in range(arg.ctrlpts.count)]
            else:
                new_weights += list(arg.weights)

    # Set variables w.r.t. input direction
    if direction == 'v':
        degree_u = degree
        degree_v = degree_other
        knotvector_u = args[0].knotvector.u
        knotvector_v = knotvector_other
        size_u = num_ctrlpts
        size_v = size_other
    else:
        degree_u = degree_other
        degree_v = degree
        knotvector_u = knotvector_other
        knotvector_v = args[0].knotvector.u
        size_u = size_other
        size_v = num_ctrlpts
        new_ctrlpts = [new_ctrlpts[i + (j * num_ctrlpts)] for i in range(num_ctrlpts) for j in range(size_other)]
        if rational:
            new_weights = [new_weights[i + (j * num_ctrlpts)] for i in range(num_ctrlpts) for j in range(size_other)]

    # Generate the surface
    ns = NURBS.Surface()
    ns.degree = (degree_u, degree_v)
    ns.knotvector = (knotvector_u, knotvector_v)
    cpm = control_points.CPManager(size_u, size_v)
    cpm.points = new_ctrlpts
    ns.ctrlpts = cpm
    if rational:
        ns.weights = new_weights

    # Return constructed surface
    return ns


def construct_volume(direction, *args, **kwargs):
    """ Generates volumes from surfaces.

    Arguments:
        * ``args``: a list of surface instances

    Keyword Arguments (optional):
        * ``degree``: degree of the 3rd parametric direction
        * ``knotvector``: knot vector of the 3rd parametric direction

    :param direction: the direction that the input surfaces lies, i.e. u, v, w
    :type direction: str
    :return: Volume constructed from the surfaces on the given parametric direction
    """
    # Input validation
    possible_dirs = ['u', 'v', 'w']
    if direction not in possible_dirs:
        raise GeomdlError("Possible direction values: " + ", ".join([val for val in possible_dirs]),
                          data=dict(input_dir=direction))

    size_other = len(args)
    if size_other < 2:
        raise GeomdlError("Input should be at least 2 surfaces")

    # Get keyword arguments
    degree_other = kwargs.get('degree', 1)
    knotvector_other = kwargs.get('knotvector', knotvector.generate(degree_other, size_other))
    rational = args[0].rational

    # Construct the control points of the new volume
    degree_u, degree_v = args[0].degree.u, args[0].degree.v
    size_u, size_v = args[0].ctrlpts_size.u, args[0].ctrlpts_size.v
    new_ctrlpts = []
    new_weights = []
    for idx, arg in enumerate(args):
        if degree_u != arg.degree.u or degree_v != arg.degree.v:
            raise GeomdlError("Input surfaces must have the same degrees",
                              data=dict(idx=idx, degree=(degree_u, degree_v), degree_arg=(arg.degree.u, arg.degree.v)))
        if size_u != arg.ctrlpts_size.u or size_v != arg.ctrlpts_size.v:
            raise GeomdlError("Input surfaces must have the same number of control points",
                              data=dict(idx=idx, size=(size_u, size_v), size_arg=(arg.ctrlpts_size.u, arg.ctrlpts_size.v)))
        new_ctrlpts += list(arg.ctrlpts)
        if rational:
            if not arg.weights:
                new_weights += [1.0 for _ in range(arg.ctrlpts.count)]
            else:
                new_weights += list(arg.weights)

    updated_ctrlpts = []
    updated_weights = []

    # Set variables w.r.t. input direction
    if direction == 'u':
        degree_u, degree_v, degree_w = degree_other, args[0].degree.u, args[0].degree.v
        size_u, size_v, size_w = size_other, args[0].ctrlpts_size.u, args[0].ctrlpts_size.v
        kv_u, kv_v, kv_w = knotvector_other, args[0].knotvector.u, args[0].knotvector.v
        # u => w, v => u, w => v
        for v in range(0, size_v):
            for w in range(0, size_w):
                for u in range(0, size_u):
                    temp_pt = new_ctrlpts[u + (v * size_u) + (w * size_u * size_v)]
                    updated_ctrlpts.append(temp_pt)
                    if rational:
                        temp_w = new_weights[u + (v * size_u) + (w * size_u * size_v)]
                        updated_weights.append(temp_w)
    elif direction == 'v':
        degree_u, degree_v, degree_w = args[0].degree.u, degree_other, args[0].degree.v
        size_u, size_v, size_w = args[0].ctrlpts_size.u, size_other, args[0].ctrlpts_size.v
        kv_u, kv_v, kv_w = args[0].knotvector.u, knotvector_other, args[0].knotvector.v
        # u => u, v => w, w => v
        for v in range(0, size_v):
            for u in range(0, size_u):
                for w in range(0, size_w):
                    temp_pt = new_ctrlpts[u + (v * size_v) + (w * size_u * size_v)]
                    updated_ctrlpts.append(temp_pt)
                    if rational:
                        temp_w = new_weights[u + (v * size_v) + (w * size_u * size_v)]
                        updated_weights.append(temp_w)
    else:  # direction == 'w'
        degree_u, degree_v, degree_w = args[0].degree.u, args[0].degree.v, degree_other
        size_u, size_v, size_w = args[0].ctrlpts_size.u, args[0].ctrlpts_size.v, size_other
        kv_u, kv_v, kv_w = args[0].knotvector.u, args[0].knotvector.v, knotvector_other
        updated_ctrlpts = new_ctrlpts
        if rational:
            updated_weights = new_weights

    # Generate the volume
    nv = NURBS.Volume()
    nv.degree = (degree_u, degree_v, degree_w)
    nv.knotvector = (kv_u, kv_v, kv_w)
    cpm = control_points.CPManager(size_u, size_v, size_w)
    cpm.points = new_ctrlpts
    nv.ctrlpts = cpm
    if rational:
        nv.weights = updated_weights

    return nv


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
