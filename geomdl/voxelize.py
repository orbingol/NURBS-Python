"""
.. module:: voxelize
    :platform: Unix, Windows
    :synopsis: Provides voxelization functions

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import struct
from . import _voxelize as vxl
from ._utilities import export


@export
def voxelize(obj, **kwargs):
    """ Generates binary voxel representation of the surfaces and volumes.

    Keyword Arguments:
        * ``grid_size``: size of the voxel grid. *Default: (8, 8, 8)*
        * ``padding``: voxel padding for in-outs finding. *Default: 10e-8*
        * ``use_cubes``: use cube voxels instead of cuboid ones. *Default: False*
        * ``num_procs``: number of concurrent processes for voxelization. *Default: 1*

    :param obj: input surface(s) or volume(s)
    :type obj: abstract.Surface or abstract.Volume
    :return: voxel grid and filled information
    :rtype: tuple
    """
    # Get keyword arguments
    grid_size = kwargs.pop('grid_size', (8, 8, 8))
    use_cubes = kwargs.pop('use_cubes', False)
    num_procs = kwargs.get('num_procs', 1)

    if not isinstance(grid_size, (list, tuple)):
        raise TypeError("Grid size must be a list or a tuple of integers")

    # Initialize result arrays
    grid = []
    filled = []

    # Should also work with multi surfaces and volumes
    for o in obj:
        # Generate voxel grid
        grid_temp = vxl.generate_voxel_grid(o.bbox, grid_size, use_cubes=use_cubes)
        args = [grid_temp, o.evalpts]

        # Find in-outs
        filled_temp = vxl.find_inouts_mp(*args, **kwargs) if num_procs > 1 else vxl.find_inouts_st(*args, **kwargs)

        # Add to result arrays
        grid += grid_temp
        filled += filled_temp

    # Return result arrays
    return grid, filled


def convert_bb_to_faces(voxel_grid):
    """ Converts a voxel grid defined by min and max coordinates to a voxel grid defined by faces.

    :param voxel_grid: voxel grid defined by the bounding box of all voxels
    :return: voxel grid with face data
    """
    new_vg = []
    for v in voxel_grid:
        # Vertices
        p1 = v[0]
        p2 = [v[1][0], v[0][1], v[0][2]]
        p3 = [v[1][0], v[1][1], v[0][2]]
        p4 = [v[0][0], v[1][1], v[0][2]]
        p5 = [v[0][0], v[0][1], v[1][2]]
        p6 = [v[1][0], v[0][1], v[1][2]]
        p7 = v[1]
        p8 = [v[0][0], v[1][1], v[1][2]]
        # Faces
        fb = [p1, p2, p3, p4]  # bottom face
        ft = [p5, p6, p7, p8]  # top face
        fs1 = [p1, p2, p6, p5]  # side face 1
        fs2 = [p2, p3, p7, p6]  # side face 2
        fs3 = [p3, p4, p8, p7]  # side face 3
        fs4 = [p1, p4, p8, p5]  # side face 4
        # Append to return list
        new_vg.append([fb, fs1, fs2, fs3, fs4, ft])
    return new_vg


@export
def save_voxel_grid(voxel_grid, file_name):
    """ Saves binary voxel grid as a binary file.

    The binary file is structured in little-endian unsigned int format.

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
