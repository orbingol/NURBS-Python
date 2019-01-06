"""
.. module:: CPGen
    :platform: Unix, Windows
    :synopsis: A simple control points grid generator for parametric surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import random
import warnings
from ._utilities import export


@export
class Grid(object):
    """ Simple control points grid generator to use with non-rational surfaces.

    This class stores grid points in [x, y, z] format and the grid (control) points can be retrieved from the
    :py:attr:`grid` attribute. The z-coordinate of the control points can be set via the keyword argument ``z_value``
    while initializing the class.

    :param size_x: width of the grid
    :type size_x: float
    :param size_y: height of the grid
    :type size_y: float
    """

    def __init__(self, size_x, size_y, **kwargs):
        self._origin = [0.0, 0.0, 0.0]  # Grid origin (always set to the bottom left corner of the grid)
        self._size_x = float(size_x)  # width of the grid
        self._size_y = float(size_y)  # height of the grid
        self._size_u = 0  # grid size in x-direction
        self._size_v = 0  # grid size in y-direction
        self._z_value = kwargs.get('z_value', 0.0)  # z-coordinate of the grid points
        self._grid_points = []  # 2-dimensional grid (control) points
        self._delta = 10e-8  # default tolerance
        self._cache = {}  # cache dictionary

    def __len__(self):
        if not self._grid_points:
            return 0
        return len(self._grid_points) * len(self._grid_points[0])

    @property
    def grid(self):
        """ Grid points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the 2-dimensional list of points in [u][v] format
        """
        return self._grid_points

    # Resets the grid to its initial state
    def reset(self):
        """ Resets the grid. """
        if self._grid_points:
            self._grid_points[:] = []
            self._size_u = 0
            self._size_v = 0
            self._origin = [0.0, 0.0, 0.0]

    # Generates the grid using the input division parameters
    def generate(self, num_u, num_v):
        """ Generates grid using the input division parameters.

        :param num_u: number of divisions in x-direction
        :type num_u: int
        :param num_v: number of divisions in y-direction
        :type num_v: int
        """
        # Some error checking and fixing
        if num_u < 1:
            raise ValueError("Divisions in the x-direction (num_u) cannot be less than 1")

        if num_v < 1:
            raise ValueError("Divisions in the y-direction (num_v) cannot be less than 1")

        if not isinstance(num_u, int):
            num_u = int(num_u)
            warnings.warn("%d will be used as the value of num_u" % num_u, UserWarning)

        if not isinstance(num_v, int):
            num_v = int(num_v)
            warnings.warn("%d will be used as the value of num_v" % num_v, UserWarning)

        # Reset the grid
        self.reset()

        # Set the number of divisions for each direction
        spacing_x = self._size_x / num_u
        spacing_y = self._size_y / num_v

        # Set initial position for x
        current_x = self._origin[0]

        # Start looping
        for _ in range(0, num_u + 1):
            # Initialize a temporary list for storing the 3nd dimension
            row = []
            # Set initial position for y
            current_y = self._origin[1]
            for _ in range(0, num_v + 1):
                # Add the first point
                row.append([current_x, current_y, self._z_value])
                # Set the y value for the next row
                current_y = current_y + spacing_y
            # Update the list to be returned
            self._grid_points.append(row)
            # Set x the value for the next column
            current_x = current_x + spacing_x

        # Set class variables
        self._size_u = num_u
        self._size_v = num_v

    # Generates hills (a.k.a. bumps) on the grid
    def bumps(self, num_bumps, **kwargs):
        """ Generates arbitrary bumps (i.e. hills) on the 2-dimensional grid.
        
        This method generates hills on the grid defined by the **num_bumps** argument. It is possible to control the
        z-value using **bump_height** argument. **bump_height** can be a positive or negative numeric value or it can
        be a list of numeric values.
         
        Please note that, not all grids can be modified to have **num_bumps** number of bumps. Therefore, this function
        uses a brute-force algorithm to determine whether the bumps can be generated or not. For instance::
        
            test_grid = Grid(5, 10) # generates a 5x10 rectangle
            test_grid.generate(4, 4) # splits the rectangle into 2x2 pieces
            test_grid.bumps(100) # impossible, it will return an error message
            test_grid.bumps(1) # You will get a bump at the center of the generated grid

        This method accepts the following keyword arguments:

        * ``bump_height``: z-value of the generated bumps on the grid. *Default: 5.0*
        * ``base_extent``: extension of the hill base from its center in terms of grid points. *Default: 2*
        * ``base_adjust``: padding between the bases of the hills. *Default: 0*

        :param num_bumps: number of bumps (i.e. hills) to be generated on the 2D grid
        :type num_bumps: int
        """
        bump_height = kwargs.get("bump_height", 5.0)
        base_extent = kwargs.get("base_extent", 2)
        padding = kwargs.get('base_adjust', 0)
        max_trials = kwargs.get("max_trials", 25)

        # Check if the grid points are generated
        if not self._grid_points:
            raise RuntimeError("Grid must be generated before calling this function")

        if not isinstance(num_bumps, int):
            num_bumps = int(num_bumps)
            warnings.warn("Number of bumps must be an integer value. Automatically rounding to %d" % num_bumps,
                          UserWarning)

        if isinstance(bump_height, (list, tuple)):
            if len(bump_height) != num_bumps:
                raise ValueError("Number of bump heights must be equal to number of bumps")
            else:
                bump_height_is_array = True
        else:
            bump_height_is_array = False
            bump_height = [float(bump_height)]

        if base_extent < 1:
            raise ValueError("Base size must be bigger than 1 grid point")

        if (2 * base_extent) + padding > self._size_u \
                or (2 * base_extent) + padding > self._size_v:
            raise ValueError("The area of the base must be less than the area of the grid")

        # Initialize a list to store bumps
        bump_list = []

        # Find size of the grid
        len_u = len(self._grid_points)
        len_v = len(self._grid_points[0])

        # Set a max number of trials for the point finding algorithm
        max_trials = int(max_trials)

        # Try to generate bumps
        for _ in range(0, num_bumps):
            trials = 0
            while trials < max_trials:
                # Choose u and v positions inside the grid (i.e. not on the edges)
                u = random.randint(base_extent, (len_u - 1) - base_extent)
                v = random.randint(base_extent, (len_v - 1) - base_extent)
                temp = [u, v]
                if self._check_bump(bump_list, temp, base_extent, padding):
                    bump_list.append(temp)
                    trials = max_trials + 1  # set number of trials to a big value
                    break
                else:
                    trials = trials + 1
            if trials == max_trials:
                raise RuntimeError("Cannot generate %d bumps with a base extent of %d on this grid. "
                                   "You need to generate a grid larger than %dx%d."
                                   % (num_bumps, base_extent, self._size_u, self._size_v))

        idx = 0
        # Update the grid with the bumps
        for u, v in bump_list:
            h_increment = bump_height[idx] / base_extent
            height = h_increment
            for j in range(base_extent - 1, -1, -1):
                self._create_bump(u, v, j, height)
                height += h_increment
            if bump_height_is_array:
                idx += 1

    # Checks the possibility of placing the bump at the specified location
    def _check_bump(self, uv_list, to_be_checked_uv, base_extent, padding):
        # If input list is empty, return true
        if not uv_list:
            return True

        # Check the input point or its surroundings are close to the existing ones
        for uv in uv_list:
            u = to_be_checked_uv[0]
            v = to_be_checked_uv[1]
            check_list = []
            for ur in range(-(base_extent + 1 + padding), base_extent + 2 + padding):
                for vr in range(-(base_extent + 1 + padding), base_extent + 2 + padding):
                    check_list.append([u + ur, v + vr])
            for check in check_list:
                if abs(uv[0] - check[0]) < self._delta and abs(uv[1] - check[1]) < self._delta:
                    return False

        # Otherwise, return true
        return True

    def _create_bump(self, u, v, jump, height):
        # Find corner
        start_u = u - jump
        stop_u = u + jump + 1
        start_v = v - jump
        stop_v = v + jump + 1

        for i in range(start_u, stop_u):
            for j in range(start_v, stop_v):
                    self._grid_points[i][j][2] = height


@export
class GridWeighted(Grid):
    """ Simple control points grid generator to use with rational surfaces.

    This class stores grid points in [x*w, y*w, z*w, w] format and the grid (control) points can be retrieved from the
    :py:attr:`grid` attribute. The z-coordinate of the control points can be set via the keyword argument ``z_value``
    while initializing the class.

    :param size_x: width of the grid
    :type size_x: float
    :param size_y: height of the grid
    :type size_y: float
    """

    def __init__(self, size_x, size_y, **kwargs):
        super(GridWeighted, self).__init__(size_x, size_y, **kwargs)
        self._weights = []
        # Variables for caching
        self._cache['gridptsw'] = []

    @property
    def weight(self):
        """ Weight (w) component of the grid points.

        The input can be a single int or a float value, then all weights will be set to the same value.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the weights vector
        :setter: Sets the weights vector
        """
        return self._weights

    @weight.setter
    def weight(self, value):
        if not self._grid_points:
            raise ValueError("Generate the grid first")
        if isinstance(value, (int, float)):
            if value <= 0:
                raise ValueError("Weight value must be bigger than 0")
            self._weights = [float(value) for _ in range(len(self))]
        elif isinstance(value, (list, tuple)):
            if len(value) != len(self):
                raise ValueError("Input must be the same size with the grid points")
            if all(val <= 0 for val in value):
                raise ValueError("Weight values must be bigger than 0")
            self._weights = [float(val) for val in value]
        else:
            raise TypeError("The input should be a list, tuple or a single int, float value")

    def reset(self):
        """ Resets the grid. """
        super(GridWeighted, self).reset()
        if self._grid_points or self._weights:
            self._cache['gridptsw'][:] = []
            self._weights[:] = []

    @property
    def grid(self):
        """ Weighted grid points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the 2-dimensional list of weighted points in [u][v] format
        """
        # Generate default weights if they haven't been set
        if not self._weights :
            self._weights = [1.0 for _ in range(len(self))]

        # Start adding weights, if not cached
        if not self._cache['gridptsw']:
            for idx, cols in enumerate(self._grid_points):
                weighted_gp_row = []
                for row in cols:
                    temp = [r * self._weights[idx] for r in row]
                    temp.append(self._weights[idx])
                    weighted_gp_row.append(temp)
                self._cache['gridptsw'].append(weighted_gp_row)

        return self._cache['gridptsw']
