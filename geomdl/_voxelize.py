"""
.. module:: _voxelize
    :platform: Unix, Windows
    :synopsis: Helper functions for voxelization module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from functools import partial
from . import linalg
from ._utilities import pool_context


# Initialize an empty __all__ for controlling imports
__all__ = []


def find_inouts_st(voxel_grid, datapts, **kwargs):
    """ Single-threaded ins and outs finding (default)

    :param voxel_grid: voxel grid
    :param datapts: data points
    :return: in-outs
    """
    padding = kwargs.get('padding', 10e-8)
    filled = [0 for _ in range(len(voxel_grid))]
    for idx, bb in enumerate(voxel_grid):
        pts_inside = is_point_inside_voxel(bb, datapts, padding=padding)
        if pts_inside:
            filled[idx] = 1
    return filled


def find_inouts_mp(voxel_grid, datapts, **kwargs):
    """ Multi-threaded ins and outs finding (using multiprocessing)

    :param voxel_grid: voxel grid
    :param datapts: data points
    :return: in-outs
    """
    padding = kwargs.get('padding', 10e-8)
    num_procs = kwargs.get('num_procs', 4)
    with pool_context(processes=num_procs) as pool:
        filled = pool.map(partial(is_point_inside_voxel, ptsarr=datapts, padding=padding), voxel_grid)
    return filled


def generate_voxel_grid(bbox, size_u, size_v, size_w):
    """ Generates the voxel grid with the desired size.

    :param bbox: bounding box
    :type bbox: list, tuple
    :param size_u: size in x-direction
    :type size_u: int
    :param size_v: size in y-direction
    :type size_v: int
    :param size_w: size in z-direction
    :type size_w: int
    :return: voxel grid
    :rtype: list
    """
    if size_u <= 1 or size_v <= 1 or size_w <= 1:
        raise ValueError("Size values must be bigger than 1")

    # Find step size
    step_u = float(bbox[1][0] - bbox[0][0]) / float(size_u - 1)
    step_v = float(bbox[1][1] - bbox[0][1]) / float(size_v - 1)
    step_w = float(bbox[1][2] - bbox[0][2]) / float(size_w - 1)

    # Find range
    range_u = linalg.linspace(bbox[1][0], bbox[0][0], size_u)
    range_v = linalg.linspace(bbox[1][1], bbox[0][1], size_v)
    range_w = linalg.linspace(bbox[1][2], bbox[0][2], size_w)

    voxel_grid = []
    for u in range_u:
        for v in range_v:
            for w in range_w:
                bbmin = [u, v, w]
                bbmax = [u + step_u, v + step_v, w + step_w]
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
    padding = kwargs.get('padding', 10e-8)

    # Make bounding box vertices more readable
    bbmin = [b - padding for b in bbox[0]]
    bbmax = [b + padding for b in bbox[1]]

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
    padding = kwargs.get('padding', 10e-8)

    # Make bounding box vertices more readable
    bbmin = [b - padding for b in bbox[0]]
    bbmax = [b + padding for b in bbox[1]]

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
