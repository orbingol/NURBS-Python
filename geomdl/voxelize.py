"""
.. module:: voxelize
    :platform: Unix, Windows
    :synopsis: Provides voxelization functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import struct
from functools import partial
from contextlib import contextmanager
from multiprocessing import Pool
from . import utilities


# Context manager for multiprocessing.Pool (for compatibility with Python 2.7.x)
@contextmanager
def poolcontext(*args, **kwargs):
    pool = Pool(*args, **kwargs)
    try:
        yield pool
    except Exception as e:
        raise e
    finally:
        pool.terminate()


def voxelize(obj, **kwargs):
    """ Generates binary voxel representation of the surface and volumes.

    Keyword Arguments:
        * ``grid_size``: size of the voxel grid. *Default: (8, 8, 8)*
        * ``padding``: voxel padding for in-outs finding. *Default: 10e-8*
        * ``use_mp``: flag to activate multi-threaded voxelization. *Default: False*
        * ``num_procs``: number of concurrent processes for multi-threaded voxelization. *Default: 4*

    :param obj: input surface(s) or volume(s)
    :type obj: abstract.Surface or abstract.Volume
    :return: voxel grid and filled information
    :rtype: tuple
    """
    # Get keyword arguments
    grid_size = kwargs.get('grid_size', (8, 8, 8))
    use_mp = kwargs.get('use_mp', False)

    if not isinstance(grid_size, (list, tuple)):
        raise TypeError("Grid size must be a list or a tuple of integers")

    # Initialize result arrays
    grid = []
    filled = []

    # Should also work with multi surfaces and volumes
    for o in obj:
        # Generate voxel grid
        grid_temp = _generate_voxel_grid(o.bbox, *grid_size)
        args = [grid_temp, o.evalpts]

        # Find in-outs
        filled_temp = _voxelize_mp(*args, **kwargs) if use_mp else _voxelize_st(*args, **kwargs)

        # Add to result arrays
        grid += grid_temp
        filled += filled_temp

    # Return result arrays
    return grid, filled


def _voxelize_st(voxel_grid, datapts, **kwargs):
    """ Single-threaded in-out finding (default)

    :param voxel_grid: voxel grid
    :param datapts: data points
    :return: in-outs
    """
    padding = kwargs.get('padding', 10e-8)
    filled = [0 for _ in range(len(voxel_grid))]
    for idx, bb in enumerate(voxel_grid):
        pts_inside = _find_points_inside_voxel(bb, datapts, padding=padding)
        if pts_inside:
            filled[idx] = 1
    return filled


def _voxelize_mp(voxel_grid, datapts, **kwargs):
    """ Multi-threaded in-out finding (using multiprocessing)

    :param voxel_grid: voxel grid
    :param datapts: data points
    :return: in-outs
    """
    padding = kwargs.get('padding', 10e-8)
    num_procs = kwargs.get('num_procs', 4)
    with poolcontext(processes=num_procs) as pool:
        filled = pool.map(partial(_find_points_inside_voxel, ptarr=datapts, padding=padding), voxel_grid)
    return filled


def save(voxel_grid, file_name):
    """ Saves binary voxel grid as a binary file

    The binary file would be structured in little-endian unsigned int format.

    :param voxel_grid: binary voxel grid
    :type voxel_grid: list, tuple
    :param file_name: file name to save
    :type file_name: str
    """
    try:
        with open(file_name, 'wb') as fp:
            for voxel in voxel_grid:
                fp.write(struct.pack("<I", voxel))
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def _generate_voxel_grid(bbox, size_u, size_v, size_w):
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
    range_u = utilities.linspace(bbox[1][0], bbox[0][0], size_u)
    range_v = utilities.linspace(bbox[1][1], bbox[0][1], size_v)
    range_w = utilities.linspace(bbox[1][2], bbox[0][2], size_w)

    voxel_grid = []
    for u in range_u:
        for v in range_v:
            for w in range_w:
                bbmin = [u, v, w]
                bbmax = [u + step_u, v + step_v, w + step_w]
                voxel_grid.append([bbmin, bbmax])
    return voxel_grid


def _find_points_inside_voxel(bbox, ptarr, **kwargs):
    """ Finds the points contained inside the voxel boundaries.

    Ref: https://math.stackexchange.com/a/1552579

    :param bbox: bounding box of the voxel
    :type bbox: list, tuple
    :param ptarr: points to be checked
    :type ptarr: list, tuple
    :return: list of points inside the voxel
    :rtype: list
    """
    # Get keyword arguments
    padding = kwargs.get('padding', 10e-8)
    get_inout = kwargs.get('inout', True)

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
    idi = utilities.vector_dot(i, i)
    jdj = utilities.vector_dot(j, j)
    kdk = utilities.vector_dot(k, k)

    for pt in ptarr:
        v = [p - b for p, b in zip(pt, bbmin)]
        # Bigger than and equal to will include the border and,
        # since we have a padding on the boundary box, we only
        # need to include the lower boundary below
        vdi = utilities.vector_dot(v, i)
        vdj = utilities.vector_dot(v, j)
        vdk = utilities.vector_dot(v, k)
        if idi > vdi >= 0.0 and jdj > vdj >= 0.0 and kdk > vdk >= 0.0:
            if get_inout:
                return 1
            else:
                points_inside.append(pt)

    if get_inout:
        return 0
    return points_inside
