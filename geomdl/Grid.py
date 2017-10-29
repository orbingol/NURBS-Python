"""
.. module:: Grid
    :platform: Unix, Windows
    :synopsis: A simple control points grid generator to use with the nurbs.Surface module

.. moduleauthor:: Onur Rauf Bingol

"""

import sys
import math
import random


class Grid:
    """ Simple 2D grid generator to generate control points grid input for nurbs.Surface module.
    
    :param size_x: width of the 2D grid
    :type size_x: integer or float
    :param size_y: heigth of the 2D grid
    :type size_y: integer or float
    """
    def __init__(self, size_x, size_y):
        # Grid origin is always set to the bottom left corner of the grid
        self._origin = [0.0, 0.0, 0.0]
        self._size_x = float(size_x)
        self._size_y = float(size_y)
        # Initialize a list to store generated grid points
        self._gridpts = []
        # Set a default tolerance
        self._mDelta = 10e-8

    # Returns the generated grid
    def grid(self):
        """ Returns the generated grid.
        
        .. note:: The format of the control points grid is described in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.
        
        :return: 2D list of points ([x,y,z]) in [u][v] format
        """
        return self._gridpts

    # Generates the grid using the input division parameters
    def generate(self, num_u, num_v):
        """ Generates the 2D grid using the input division parameters.
            
        :param num_u: number of divisions in x-direction
        :type num_u: integer
        :param num_v: number of divisions in y-direction
        :type num_v: integer
        :return: None
        """
        # Some error checking and fixing
        if num_u < 1:
            raise ValueError("Divisions in the x-direction (num_u) cannot be less than 1!")

        if num_v < 1:
            raise ValueError("Divisions in the y-direction (num_v) cannot be less than 1!")

        if not isinstance(num_u, int):
            num_u = int(num_u)
            print("WARNING: Number of divisions must be an integer value. %d will be used as the value of num_u." % num_u)

        if not isinstance(num_v, int):
            num_v = int(num_v)
            print("WARNING: Number of divisions must be an integer value. %d will be used as the value of num_v." % num_v)

        # Set the number of divisions for each direction
        spacing_x = self._size_x / num_u
        spacing_y = self._size_y / num_v

        # Set initial position for x
        current_x = self._origin[0]

        # Start looping
        for u in range(0, num_u + 1):
            # Initialize a temporary list for storing the 3nd dimension
            row = []
            # Set initial position for y
            current_y = self._origin[1]
            for v in range(0, num_v + 1):
                # Add the first point
                row.append([current_x, current_y, 0.0])
                # Set the y value for the next row
                current_y = current_y + spacing_y
            # Update the list to be returned
            self._gridpts.append(row)
            # Set x the value for the next column
            current_x = current_x + spacing_x

    # Rotates the grid about the z-axis
    def rotate_z(self, angle=0):
        """ Rotates the grid about the z-axis.
        
        :param angle: angle of rotation about the z-axis
        :type angle: integer or float
        :return: None
        """
        # Get current origin / starting point (we need a copy of the self._origin)
        current_origin = list(self._origin)

        # Translate to the origin
        self.translate([0.0, 0.0, 0.0])

        # Then, rotate about the axis
        rot = math.radians(angle)
        for r in self._gridpts:
            for c in r:
                new_x = (c[0] * math.cos(rot)) - (c[1] * math.sin(rot))
                new_y = (c[1] * math.cos(rot)) + (c[0] * math.sin(rot))
                c[0] = new_x
                c[1] = new_y

        # Finally, translate back to the starting location
        self.translate(current_origin)

    # Rotates the grid about the y-axis
    def rotate_y(self, angle=0):
        """ Rotates the grid about the y-axis.

        :param angle: angle of rotation about the y-axis
        :type angle: integer or float
        :return: None
        """
        # Get current origin / starting point (we need a copy of the self._origin)
        current_origin = list(self._origin)

        # Translate to the origin
        self.translate([0.0, 0.0, 0.0])

        # Then, rotate about the axis
        rot = math.radians(angle)
        for r in self._gridpts:
            for c in r:
                new_x = (c[0] * math.cos(rot)) - (c[2] * math.sin(rot))
                new_z = (c[2] * math.cos(rot)) + (c[0] * math.sin(rot))
                c[0] = new_x
                c[2] = new_z

        # Finally, translate back to the starting location
        self.translate(current_origin)

    # Rotates the grid about the x-axis
    def rotate_x(self, angle=0):
        """ Rotates the grid about the x-axis.

        :param angle: angle of rotation about the x-axis
        :type angle: integer or float
        :return: None
        """
        # Get current origin / starting point (we need a copy of the self._origin)
        current_origin = list(self._origin)

        # Translate to the origin
        self.translate([0.0, 0.0, 0.0])

        # Then, rotate about the axis
        rot = math.radians(angle)
        for r in self._gridpts:
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
        # Find the difference between starting and the input point
        diff_x = pt[0] - self._origin[0]
        diff_y = pt[1] - self._origin[1]
        diff_z = pt[2] - self._origin[2]

        # Translate all points
        for r in self._gridpts:
            for c in r:
                c[0] = c[0] + diff_x
                c[1] = c[1] + diff_y
                c[2] = c[2] + diff_z

        # Update the origin (bottom left corner)
        self._origin = self._gridpts[0][0]

    # Saves the generated grid to a text file
    def save(self, file_name="grid.txt"):
        """ Saves the generated grid to a text file.
        
        .. note:: The format of the text files is described in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.
        
        :param file_name: File name to be saved
        :type file_name: string
        :return: None
        """
        # Some error checking
        if not self._gridpts:
            raise ValueError("Grid must be generated before saving it to a file!")

        if not isinstance(file_name, str):
            raise ValueError("File name must be a string!")

        # Open the file for writing
        target = open(file_name, 'w')
        # Clear file contents
        target.truncate()
        # Start saving the generated grid to the file
        for cols in self._gridpts:
            line = ""
            col_size = len(cols)
            counter = 0
            for rows in cols:
                line = line + str(rows[0]) + "," + str(rows[1]) + "," + str(rows[2])
                counter = counter + 1
                # Not the best way, but it works
                if counter != col_size:
                    line = line + ";"
            target.write(line)
            target.write("\n")

    # Generates hills (a.k.a. bumps) on the 2D grid
    def bumps(self, num_bumps=0, all_positive=False, bump_height=3):
        """ Generates random bumps (i.e. hills) on the 2D grid.
        
        This method generates hills on the grid defined by the **num_bumps** parameter. The direction of the generated hills
        are chosen randomly by default, but this behavior can be controlled by **all_positive** parameter. It is also 
        possible to control the z-value using **bump_height** parameter.
         
        Please note that, not all grids can be modified to have **num_bumps** number of bumps. Therefore, this function
        uses a trial-and-error method to determine whether the bumps can be generatable or not. For instance::
        
            testgrid = Grid(5, 10) # generates a 5x10 rectangle
            testgrid.generate(2, 2) # splits the rectangle into 4 pieces
            testgrid.bumps(100) # impossible, it will return an error message
            testgrid.bumps(1) # You will get a bump at the center of the generated grid
                
        :param num_bumps: Number of bumps (i.e. hills) to be generated on the 2D grid
        :type num_bumps: integer
        :param all_positive: Generate all bumps on the positive z direction
        :type all_positive: boolean
        :param bump_height: z-value of the generated bumps on the grid
        :type bump_height: integer or float
        :return: None
        """
        # Some error checking
        if num_bumps <= 0:
            print("No bumps are generated!")
            return

        if not isinstance(num_bumps, int):
            num_bumps = int(num_bumps)
            print("Number of bumps must be an integer value. Automatically rounding to %d." % num_bumps)

        if bump_height < 0:
            raise ValueError("Height must be a positive number")

        if not isinstance(all_positive, bool):
            raise ValueError("all_positive must be a boolean value!")

        # Initialize a list to store bumps
        bump_list = []

        # Find size of the grid
        len_u = len(self._gridpts)
        len_v = len(self._gridpts[0])

        # Set a max number of trials for the point finding algorithm
        max_trials = 25

        # Try to generate bumps
        for nb in range(1, num_bumps):
            trials = 0
            while trials < max_trials:
                # Choose u and v positions inside the grid (i.e. not on the edges)
                u = random.randint(1, len_u-2)
                v = random.randint(1, len_v-2)
                temp = [u, v]
                if not bump_list:
                    bump_list.append(temp)
                else:
                    if self._check_bump(bump_list, temp):
                        bump_list.append(temp)
                        trials = max_trials + 1  # set number of trials to a big value
                        break
                    else:
                        trials = trials + 1
            if trials == max_trials:
                print("Cannot generate %d bumps on this grid." % num_bumps)
                print("You might need to generate a grid with more divisions.")
                sys.exit(0)

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
            self._gridpts[u - 1][v - 1][2] = z_val / 2.0
            self._gridpts[u - 1][v][2] = z_val / 2.0
            self._gridpts[u - 1][v + 1][2] = z_val / 2.0
            self._gridpts[u][v - 1][2] = z_val / 2.0
            self._gridpts[u][v][2] = z_val
            self._gridpts[u][v + 1][2] = z_val / 2.0
            self._gridpts[u + 1][v - 1][2] = z_val / 2.0
            self._gridpts[u + 1][v][2] = z_val / 2.0
            self._gridpts[u + 1][v + 1][2] = z_val / 2.0

    # Checks the possibility of placing the bump at the specified location
    def _check_bump(self, uv_list=(), to_be_checked_uv=(0, 0)):
        # If input list is empty, return true
        if not uv_list:
            return True

        # Check the input point or its surroundings are close to the existing ones
        for uv in uv_list:
            u = to_be_checked_uv[0]
            v = to_be_checked_uv[1]
            check_list = [
                [u - 1, v - 1],
                [u - 1, v],
                [u - 1, v + 1],
                [u, v - 1],
                [u, v],
                [u, v + 1],
                [u + 1, v - 1],
                [u + 1, v],
                [u + 1, v + 1],
            ]
            for check in check_list:
                if abs(uv[0] - check[0]) < self._mDelta and abs(uv[1] - check[1]) < self._mDelta:
                    return False

        # Otherwise, return true
        return True
