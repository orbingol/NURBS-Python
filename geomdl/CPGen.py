"""
.. module:: CPGen
    :platform: Unix, Windows
    :synopsis: A simple control points generator to use with the B-Spline and NURBS surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import math
from . import random
from . import warnings


class Grid(object):
    """ Simple grid generator to use with B-Spline surfaces.

    This class stores grid points in [x, y, z] format.

    .. note:: Additional details on the file formats can be found in the documentation.

    :param size_x: width of the grid
    :type size_x: float
    :param size_y: height of the grid
    :type size_y: float
    """

    def __init__(self, size_x, size_y):
        # Grid origin is always set to the bottom left corner of the grid
        self._origin = [0.0, 0.0, 0.0]
        self._size_x = float(size_x)
        self._size_y = float(size_y)
        # Grid size
        self._size_u = 0
        self._size_v = 0
        # Initialize a list to store generated grid points
        self._grid_points = []
        # Set a default tolerance
        self._delta = 10e-8
        self._dimension = 3
        self._no_change = False

    # Returns the generated grid
    def grid(self):
        """ Returns the generated grid.

        :return: 2D list of points in [u][v] format
        """
        return self._grid_points

    # Generates the grid using the input division parameters
    def generate(self, num_u, num_v):
        """ Generates grid using the input division parameters.
            
        :param num_u: number of divisions in x-direction
        :type num_u: int
        :param num_v: number of divisions in y-direction
        :type num_v: int
        :return: None
        """

        # Check if we could update the grid
        if self._no_change:
            raise RuntimeError("Grid cannot be updated due to an irreversible operation (e.g. adding weights)")

        # Some error checking and fixing
        if num_u < 1:
            raise ValueError("Divisions in the x-direction (num_u) cannot be less than 1")

        if num_v < 1:
            raise ValueError("Divisions in the y-direction (num_v) cannot be less than 1")

        if not isinstance(num_u, int):
            num_u = int(num_u)
            warnings.warn("Number of divisions must be an integer value. %d will be used as the value of num_u" % num_u,
                          UserWarning)

        if not isinstance(num_v, int):
            num_v = int(num_v)
            warnings.warn("Number of divisions must be an integer value. %d will be used as the value of num_v" % num_v,
                          UserWarning)

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
                row.append([current_x, current_y, 0.0])
                # Set the y value for the next row
                current_y = current_y + spacing_y
            # Update the list to be returned
            self._grid_points.append(row)
            # Set x the value for the next column
            current_x = current_x + spacing_x

        # Set class variables
        self._size_u = num_u
        self._size_v = num_v

    # Rotates the grid about the z-axis
    def rotate_z(self, angle=0.0):
        """ Rotates the grid about the z-axis.
        
        :param angle: angle of rotation about the z-axis
        :type angle: float
        :return: None
        """
        # Check if we could update the grid
        if self._no_change:
            raise RuntimeError("Grid cannot be updated due to an irreversible operation (e.g. adding weights)")

        # Check if the grid points are generated
        if not self._grid_points:
            raise RuntimeError("Grid must be generated before calling this function")

        # Get current origin / starting point (we need a copy of the self._origin)
        current_origin = list(self._origin)

        # Translate to the origin
        self.translate([0.0, 0.0, 0.0])

        # Then, rotate about the axis
        rot = math.radians(angle)
        for r in self._grid_points:
            for c in r:
                new_x = (c[0] * math.cos(rot)) - (c[1] * math.sin(rot))
                new_y = (c[1] * math.cos(rot)) + (c[0] * math.sin(rot))
                c[0] = new_x
                c[1] = new_y

        # Finally, translate back to the starting location
        self.translate(current_origin)

    # Rotates the grid about the y-axis
    def rotate_y(self, angle=0.0):
        """ Rotates the grid about the y-axis.

        :param angle: angle of rotation about the y-axis
        :type angle: float
        :return: None
        """
        # Check if we could update the grid
        if self._no_change:
            raise RuntimeError("Grid cannot be updated due to an irreversible operation (e.g. adding weights)")

        # Check if the grid points are generated
        if not self._grid_points:
            raise RuntimeError("Grid must be generated before calling this function")

        # Get current origin / starting point (we need a copy of the self._origin)
        current_origin = list(self._origin)

        # Translate to the origin
        self.translate([0.0, 0.0, 0.0])

        # Then, rotate about the axis
        rot = math.radians(angle)
        for r in self._grid_points:
            for c in r:
                new_x = (c[0] * math.cos(rot)) - (c[2] * math.sin(rot))
                new_z = (c[2] * math.cos(rot)) + (c[0] * math.sin(rot))
                c[0] = new_x
                c[2] = new_z

        # Finally, translate back to the starting location
        self.translate(current_origin)

    # Rotates the grid about the x-axis
    def rotate_x(self, angle=0.0):
        """ Rotates the grid about the x-axis.

        :param angle: angle of rotation about the x-axis
        :type angle: float
        :return: None
        """
        # Check if we could update the grid
        if self._no_change:
            raise RuntimeError("Grid cannot be updated due to an irreversible operation (e.g. adding weights)")

        # Check if the grid points are generated
        if not self._grid_points:
            raise RuntimeError("Grid must be generated before calling this function")

        # Get current origin / starting point (we need a copy of the self._origin)
        current_origin = list(self._origin)

        # Translate to the origin
        self.translate([0.0, 0.0, 0.0])

        # Then, rotate about the axis
        rot = math.radians(angle)
        for r in self._grid_points:
            for c in r:
                new_y = (c[1] * math.cos(rot)) - (c[2] * math.sin(rot))
                new_z = (c[2] * math.cos(rot)) + (c[1] * math.sin(rot))
                c[1] = new_y
                c[2] = new_z

        # Finally, translate back to the starting location
        self.translate(current_origin)

    # Translates the grid origin to the input position
    def translate(self, pt=(0.0, 0.0, 0.0)):
        """ Translates the grid origin to the input position.
        
        Grid origin is (0, 0, 0) at instantiation and always represents the bottom left corner of the 2D grid.
        
        :param pt: new origin point
        :type pt: list
        :return: None
        """
        # Check if we could update the grid
        if self._no_change:
            raise RuntimeError("Grid cannot be updated due to an irreversible operation (e.g. adding weights)")

        # Check if the grid points are generated
        if not self._grid_points:
            raise ValueError("Grid must be generated before calling this function")

        # Find the difference between starting and the input point
        diff_x = pt[0] - self._origin[0]
        diff_y = pt[1] - self._origin[1]
        diff_z = pt[2] - self._origin[2]

        # Translate all points
        for r in self._grid_points:
            for c in r:
                c[0] = c[0] + diff_x
                c[1] = c[1] + diff_y
                c[2] = c[2] + diff_z

        # Update the origin (bottom left corner)
        self._origin = self._grid_points[0][0]

    # Saves the generated grid to a text file
    def save(self, filename="grid.txt"):
        """ Saves the generated grid to a text file.

        :param filename: File name to be saved
        :type filename: str
        :return: True if grid is saved correctly, False otherwise
        :rtype: bool
        """
        # Check if the grid points are generated
        if not self._grid_points:
            raise RuntimeError("Grid must be generated before calling this function")

        if not isinstance(filename, str):
            raise TypeError("File name must be a string")

        # Initialize the return value
        ret_check = True

        # Open the file for writing
        try:
            with open(filename, 'w') as fp:
                # Clear file contents
                fp.truncate()
                # Start saving the generated grid to the file
                for cols in self._grid_points:
                    line = ""
                    col_size = len(cols)
                    counter = 0
                    for rows in cols:
                        for idx, coord in enumerate(rows):
                            if idx:  # Add comma if we are not on the first element
                                line += ","
                            line += str(coord)
                        counter += 1
                        # Not the best way, but it works
                        if counter != col_size:
                            line += ";"
                    line += "\n"
                    fp.write(line)

        except IOError:
            # Show a warning on failure to open file
            warnings.warn("File " + ("(empty)" if not filename else str(filename)) + " cannot be opened for saving",
                          UserWarning)
            ret_check = False

        return ret_check

    # Generates hills (a.k.a. bumps) on the grid
    def bumps(self, num_bumps, **kwargs):
        """ Generates arbitrary bumps (i.e. hills) on the 2D grid.
        
        This method generates hills on the grid defined by the **num_bumps** argument. The direction of the generated
        hills are chosen randomly by default, but this behavior can be controlled by **all_positive** argument.
        It is also possible to control the z-value using **bump_height** argument.
         
        Please note that, not all grids can be modified to have **num_bumps** number of bumps. Therefore, this function
        uses a brute-force algorithm to determine whether the bumps can be generated or not. For instance::
        
            testgrid = Grid(5, 10) # generates a 5x10 rectangle
            testgrid.generate(2, 2) # splits the rectangle into 4 pieces
            testgrid.bumps(100) # impossible, it will return an error message
            testgrid.bumps(1) # You will get a bump at the center of the generated grid

        This method accepts the following keyword arguments:

        * ``all_positive``: generate all bumps on the positive z direction. *Default: False*
        * ``bump_height``: z-value of the generated bumps on the grid. *Default: 5.0*
        * ``base_extent``: extension of the hill base from its center in terms of grid points. *Default: 3*
        * ``base_adjust``: moves hills to the center or outside the surface boundaries. *Default: 0*

        :param num_bumps: number of bumps (i.e. hills) to be generated on the 2D grid
        :type num_bumps: int
        """
        all_positive = kwargs.get("all_positive", False)
        bump_height = kwargs.get("bump_height", 5.0)
        base_extent = kwargs.get("base_extent", 3)
        base_adjust = kwargs.get("base_adjust", 0)
        max_trials = kwargs.get("max_trials", 25)

        # Check if we can update the grid
        if self._no_change:
            raise RuntimeError("Grid cannot be updated due to an irreversible operation (e.g. adding weights)")

        # Check if the grid points are generated
        if not self._grid_points:
            raise RuntimeError("Grid must be generated before calling this function")

        # Some error checking
        if num_bumps <= 0:
            warnings.warn("No bumps were generated!", UserWarning)
            return

        if not isinstance(num_bumps, int):
            num_bumps = int(num_bumps)
            warnings.warn("Number of bumps must be an integer value. Automatically rounding to %d" % num_bumps,
                          UserWarning)

        if bump_height < 0:
            raise ValueError("Height must be a positive number")

        if not isinstance(all_positive, bool):
            raise ValueError("all_positive must be a boolean value!")

        if base_extent < 1:
            raise ValueError("Base size must be bigger than 1 grid point")

        if (2 * base_extent) > self._size_u or (2 * base_extent) > self._size_v:
            raise ValueError("The area of the base must be less than the area of the grid")

        if abs(base_adjust) >= math.floor(base_extent / 2):
            raise ValueError("base_adjust cannot be bigger than and equal to floor(base_extent / 2)")

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
                u = random.randint(0 + base_extent - base_adjust, len_u - base_extent - 1 + base_adjust)
                v = random.randint(0 + base_extent - base_adjust, len_v - base_extent - 1 + base_adjust)
                temp = [u, v]
                if self._check_bump(bump_list, temp, base_extent):
                    bump_list.append(temp)
                    trials = max_trials + 1  # set number of trials to a big value
                    break
                else:
                    trials = trials + 1
            if trials == max_trials:
                raise RuntimeError("Cannot generate %d bumps with a base extent of %d on this grid. "
                                   "You need to generate a grid larger than %dx%d."
                                   % (num_bumps, base_extent, self._size_u, self._size_v))

        # Update the grid with the bumps
        for u, v in bump_list:
            # Toss a coin to find the bump direction
            if all_positive:
                roll = 1
            else:
                roll = random.randint(0, 1)
            if roll:
                z_val = float(bump_height)
            else:
                z_val = float(-1 * bump_height)

            # Update the grid points
            for ur in range(-base_extent+1, base_extent):
                for vr in range(-base_extent+1, base_extent):
                    denominator = 1 if ur == 0 and vr == 0 else (abs(ur) + abs(vr))
                    self._grid_points[u + ur][v + vr][2] = z_val / denominator

    # Checks the possibility of placing the bump at the specified location
    def _check_bump(self, uv_list, to_be_checked_uv, base_extent):
        # If input list is empty, return true
        if not uv_list:
            return True

        # Check the input point or its surroundings are close to the existing ones
        for uv in uv_list:
            u = to_be_checked_uv[0]
            v = to_be_checked_uv[1]
            check_list = []
            for ur in range(-base_extent, base_extent + 1):
                for vr in range(-base_extent, base_extent + 1):
                    check_list.append([u + ur, v + vr])
            for check in check_list:
                if abs(uv[0] - check[0]) < self._delta and abs(uv[1] - check[1]) < self._delta:
                    return False

        # Otherwise, return true
        return True


class GridWeighted(Grid):
    """ Simple grid generator to use with NURBS surfaces.

    This class stores grid points in [x*w, y*w, z*w, w] format.

    .. note:: Additional details for the file formats can be found in the documentation.

    :param size_x: width of the grid
    :type size_x: float
    :param size_y: height of the grid
    :type size_y: float
    """

    def __init__(self, size_x, size_y):
        super(GridWeighted, self).__init__(size_x, size_y)
        # Override dimension variable
        self._dimension = 4

    def add_weight(self, w=1.0):
        """ Adds a uniform weight to grid points.

        All grid points are divided by the input weight and weight value is added as the last element of the coordinate
        array. Grid points can be accessed via :func:`.grid()` function and can be saved as a text file via
        :func:`.save()` function.

        :param w: weight value to be added
        :type w: float
        :return: None
        """
        # Check if the input weight is valid
        if w <= 0:
            raise ValueError("Weight value must be bigger than 0")

        # Check if we have already added weights
        if len(self._grid_points[0][0]) == self._dimension:
            raise RuntimeError("Please use modify_weight() to change the weight value")

        # Start adding weights
        weighted_gp = []
        for cols in self._grid_points:
            weighted_gp_row = []
            for row in cols:
                temp = row
                temp[:] = [tmp / w for tmp in temp]
                temp.append(w)
                weighted_gp_row.append(temp)
            weighted_gp.append(weighted_gp_row)

        # Update class variables
        self._no_change = True
        self._grid_points = weighted_gp

    def modify_weight(self, w=1.0):
        """ Modifies weight value of the grid points.

        :param w: weight value to be added
        :type w: float
        :return: None
        """
        # Check if the input weight is valid
        if w <= 0:
            raise ValueError("Weight value must be bigger than 0")

        # Check if we have already added weights
        if len(self._grid_points[0][0]) != self._dimension:
            raise RuntimeError("Need to add weights first")

        # Start modifying weights
        weighted_gp = []
        for cols in self._grid_points:
            weighted_gp_row = []
            for row in cols:
                temp = row[0:self._dimension - 1]
                temp[:] = [tmp * row[-1] for tmp in temp]
                temp[:] = [tmp / w for tmp in temp]
                temp.append(w)
                weighted_gp_row.append(temp)
            weighted_gp.append(weighted_gp_row)

        # Update grid points
        self._grid_points = weighted_gp
