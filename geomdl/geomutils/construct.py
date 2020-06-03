"""
.. module:: geomutils.construct
    :platform: Unix, Windows
    :synopsis: Provides functions for constructing B-spline geometries

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import NURBS, control_points, knotvector
from ..base import GeomdlError


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
