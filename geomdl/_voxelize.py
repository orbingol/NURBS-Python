"""
.. module:: _voxelize
    :platform: Unix, Windows
    :synopsis: Helper functions for voxelization module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from functools import partial
from . import linalg
from ._utilities import pool_context
from .exceptions import GeomdlException

# Initialize an empty __all__ for controlling imports
__all__ = []


def find_inouts_st(voxel_grid, datapts, **kwargs):
    """ Single-threaded ins and outs finding (default)

    :param voxel_grid: voxel grid
    :param datapts: data points
    :return: in-outs
    """
    tol = kwargs.get('tol', 10e-8)
    filled = [0 for _ in range(len(voxel_grid))]
    for idx, bb in enumerate(voxel_grid):
        pts_inside = is_point_inside_voxel(bb, datapts, tol=tol)
        if pts_inside:
            filled[idx] = 1
    return filled


def find_inouts_mp(voxel_grid, datapts, **kwargs):
    """ Multi-threaded ins and outs finding (using multiprocessing)

    :param voxel_grid: voxel grid
    :param datapts: data points
    :return: in-outs
    """
    tol = kwargs.get('tol', 10e-8)
    num_procs = kwargs.get('num_procs', 4)
    with pool_context(processes=num_procs) as pool:
        filled = pool.map(partial(is_point_inside_voxel, ptsarr=datapts, tol=tol), voxel_grid)
    return filled


def generate_voxel_grid(bbox, szval, use_cubes=False):
    """ Generates the voxel grid with the desired size.

    :param bbox: bounding box
    :type bbox: list, tuple
    :param szval: size in x-, y-, z-directions
    :type szval: list, tuple
    :param use_cubes: use cube voxels instead of cuboid ones
    :type use_cubes: bool
    :return: voxel grid
    :rtype: list
    """
    # Input validation
    if szval[0] <= 1 or szval[1] <= 1 or szval[2] <= 1:
        raise GeomdlException("Size values must be bigger than 1", data=dict(sizevals=szval))

    # Find step size for each direction
    steps = [float(bbox[1][idx] - bbox[0][idx]) / float(szval[idx] - 1) for idx in range(0, 3)]

    # It is possible to use cubes instead of cuboids
    if use_cubes:
        min_val = min(*steps)
        steps = [min_val for _ in range(0, 3)]

    # Find range in each direction
    ranges = [list(linalg.frange(bbox[0][idx], bbox[1][idx], steps[idx])) for idx in range(0, 3)]

    voxel_grid = []
    for u in ranges[0]:
        for v in ranges[1]:
            for w in ranges[2]:
                bbmin = [u, v, w]
                bbmax = [k + l for k, l in zip(bbmin, steps)]
                voxel_grid.append([bbmin, bbmax])
    return voxel_grid


def is_point_inside_voxel(bbox, ptsarr, **kwargs):
    """ Finds if any point is contained inside the voxel boundaries (inouts array).

    Ref: https://math.stackexchange.com/a/1552579

    :param bbox: bounding box of the voxel
    :type bbox: list, tuple
    :param ptsarr: points to be checked
    :type ptsarr: list, tuple
    :return: list of ins and outs
    :rtype: list
    """
    # Get keyword arguments
    tol = kwargs.get('tol', 10e-8)  # padding value

    # Make bounding box vertices more readable
    bbmin = [b - tol for b in bbox[0]]
    bbmax = [b + tol for b in bbox[1]]

    # Find basis vectors
    i = [bbmax[0] - bbmin[0], 0, 0]
    j = [0, bbmax[1] - bbmin[1], 0]
    k = [0, 0, bbmax[2] - bbmin[2]]

    # Find dot products
    idi = linalg.vector_dot(i, i)
    jdj = linalg.vector_dot(j, j)
    kdk = linalg.vector_dot(k, k)

    for pt in ptsarr:
        v = [p - b for p, b in zip(pt, bbmin)]
        # Bigger than and equal to will include the border and,
        # since we have a padding on the boundary box, we only
        # need to include the lower boundary below
        vdi = linalg.vector_dot(v, i)
        vdj = linalg.vector_dot(v, j)
        vdk = linalg.vector_dot(v, k)
        if idi > vdi >= 0.0 and jdj > vdj >= 0.0 and kdk > vdk >= 0.0:
            return 1
    return 0


def get_points_inside_voxel(bbox, ptsarr, **kwargs):
    """ Finds the list of points contained inside the voxel boundaries.

    Ref: https://math.stackexchange.com/a/1552579

    :param bbox: bounding box of the voxel
    :type bbox: list, tuple
    :param ptsarr: points to be checked
    :type ptsarr: list, tuple
    :return: list of points inside the voxel
    :rtype: list
    """
    # Get keyword arguments
    tol = kwargs.get('tol', 10e-8)

    # Make bounding box vertices more readable
    bbmin = [b - tol for b in bbox[0]]
    bbmax = [b + tol for b in bbox[1]]

    # Initialize an empty list
    points_inside = []

    # Find basis vectors
    i = [bbmax[0] - bbmin[0], 0, 0]
    j = [0, bbmax[1] - bbmin[1], 0]
    k = [0, 0, bbmax[2] - bbmin[2]]

    # Find dot products
    idi = linalg.vector_dot(i, i)
    jdj = linalg.vector_dot(j, j)
    kdk = linalg.vector_dot(k, k)

    for pt in ptsarr:
        v = [p - b for p, b in zip(pt, bbmin)]
        # Bigger than and equal to will include the border and,
        # since we have a padding on the boundary box, we only
        # need to include the lower boundary below
        vdi = linalg.vector_dot(v, i)
        vdj = linalg.vector_dot(v, j)
        vdk = linalg.vector_dot(v, k)
        if idi > vdi >= 0.0 and jdj > vdj >= 0.0 and kdk > vdk >= 0.0:
            points_inside.append(pt)
    return points_inside
