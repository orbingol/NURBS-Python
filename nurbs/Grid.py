"""
.. module:: Grid
    :platform: Unix, Windows
    :synopsis: A simple control points grid generator to use with the nurbs.Surface module

.. moduleauthor:: Onur Rauf Bingol

"""

import math


class Grid:
    """ Simple 2D grid generator to generate control points grid input for nurbs.Surface module.
    
    This class is designed to be a **very simple** grid generator for generating input files for the :class:`.Surface` class.
    Currently, it is not a fully-featured grid generator which can fit any purpose, but as always, contributions are welcome! :-)
    """
    def __init__(self, size_x, size_y):
        """ Default constructor.
        
        :param size_x: width of the 2D grid
        :param size_y: heigth of the 2D grid
        """
        self._origin = [0.0, 0.0, 0.0]
        self._size_x = size_x
        self._size_y = size_y
        self._gridpts = []

    def grid(self):
        """ Returns the generated grid.
        
        .. note:: The format of the control points grid is described in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.
        
        :return: 2D list of points ([x,y,z]) in [u][v] format
        """
        return self._gridpts

    def generate(self, num_u, num_v):
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

    def rotate_z(self, angle=0):
        """ Rotates the grid about the z-axis.
        
        :param angle: angle of rotation about the z-axis 
        :return: None
        """
        # Get current origin / starting point (we need a copy of the self._origin)
        current_origin = list(self._origin)

        # Translate to the origin
        self.translate([0.0, 0.0, 0.0])

        # Then, rotate about the z-axis
        rot = math.radians(angle)
        for r in self._gridpts:
            for c in r:
                new_x = (c[0] * math.cos(rot)) - (c[1] * math.sin(rot))
                new_y = (c[1] * math.cos(rot)) + (c[0] * math.sin(rot))
                c[0] = new_x
                c[1] = new_y

        # Finally, translate back to the starting location
        self.translate(current_origin)

    def translate(self, pt=(0.0, 0.0, 0.0)):
        """ Translates the grid origin to the input point.
        
        Grid origin is (0, 0, 0) at instantiation and always represents the bottom left corner of the 2D grid.
        :param pt: new origin point
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

    def save(self, file_name="grid.txt"):
        """ Saves the generated grid to a text file.
        
        .. note:: The format of the text files is described in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.
        
        :param file_name: File name to be saved
        :return: None
        """
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
