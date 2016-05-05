"""
    NURBS Python Package

    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016
"""


# Import Python's abstract base class package
from abc import ABCMeta, abstractmethod


class Point(metaclass=ABCMeta):
    """Control point operations

    This is an Abstract Base Class (ABC) for control point operations.

    Attributes:
        dimension: the dimension of the coordinates (2 or 3)
    """

    def __init__(self, dimension):
        """Constructor of the Point class

        Args:
            dimension (int): '2' defines Curve and '3' defines Surface
        """
        self._num_points = 0  # Initialize number of control points
        self._P = []  # Control point array
        self._Pw = []  # Weighted control point array
        self._dimension = dimension # Defines the geometry is a curve or surface

    #
    # Properties
    #

    @property
    def wcp(self):
        """List[Dict[float]]: Property for holding weighted control points"""
        if not self._Pw:
            raise ValueError('Weighted control point list is empty!')
        else:
            return self._Pw

    @wcp.setter
    def wcp(self, Pw):
        if self._Pw:
            self._Pw.clear()
        self._Pw = Pw

    #
    # Methods to be implemented
    #

    @abstractmethod
    def input_cp(self):
        """Abstract method for control point retrieval."""
        pass

    #
    # Public methods
    #

    def update_cp(self):
        """Updates the global control points array from calculated weighted points."""
        # Clear the current control points array
        self._P.clear()
        for P in self._Pw:
            if self._dimension == 3:
                P_temp = []
                for p in P:
                    P_temp_row = {'x': p['xw'] / p['w'], 'y': p['yw'] / p['w'], 'z': p['zw'] / p['w']}
                    P_temp.append(P_temp_row)
            else:
                P_temp = {'x': P['xw'] / P['w'], 'y': P['yw'] / P['w']}
            self._P.append(P_temp)

    def get_cp(self):
        """Returns a list of control points.

            Returns:
                list: Control points
        """
        if not self._P:
            raise ValueError('Control point list is empty!')
        else:
            return self._P

    def create_wcp(self, weights):
        """Creates a list of weighted control points.

        Args:
            weights (List[float]): The weights list
        Returns:
            None
        """
        if self._dimension == 3:
            for P in self._P:
                Pw_temp_row = []
                for p, w in zip(P, weights):
                    Pw_temp = {'xw': p['x'] * w, 'yw': p['y'] * w, 'zw': p['z'] * w, 'w': w}
                    Pw_temp_row.append(Pw_temp)
                self._Pw.append(Pw_temp_row)
        else:
            for i in range(0, self._num_points, 1):
                Pw_temp = {'xw': self._P[i]['x'] * weights[i], 'yw': self._P[i]['y'] * weights[i], 'w': weights[i]}
                self._Pw.append(Pw_temp)


class PointFromCLI(Point):

    def __init__(self, dimension):
        """Constructor of the PointFromCLI class

        This class is used for reading Curve control points from the command line.

        Args:
            dimension (int): '2' defines Curve and '3' defines Surface
        """
        # Call parent class constructor
        super().__init__(dimension)

    def input_cp(self):
        # Allow user to enter number of control points
        num_points = input('Please enter number of control points: ')
        # Set number of control points as a global variable
        self._num_points = int(num_points)
        # Allow user to enter coordinates of the control points
        for i in range(0, self._num_points, 1):
            x_input = float(input('Enter x-coordinate of point ' + str(i + 1) + ': '))
            y_input = float(input('Enter y-coordinate of point ' + str(i + 1) + ': '))
            # Create a temporary dictionary for appending coordinates into P
            P_temp = {'x': x_input, 'y': y_input}
            # Add control points to the global control point list, P
            self._P.append(P_temp)


class PointFromFile(Point):

    def __init__(self, dimension, filename):
        """Constructor of the PointFromFile class

        This class is used for reading Curve control points from a file.

        Args:
            dimension (int): '2' defines Curve and '3' defines Surface
            filename (str): File name to be read
        """
        # Call parent class constructor
        super().__init__(dimension)
        self._filename = filename  # File which contains the control points

    def input_cp(self):
        try:
            # Open the file
            with open(self._filename, 'r') as fp:
                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    control_point = line.split(', ')
                    # Read x- and y-coordinates
                    x_input = int(control_point[0])
                    y_input = int(control_point[1])
                    # Create a temporary dictionary for appending coordinates into P
                    P_temp = {'x': x_input, 'y': y_input}
                    # Add control points to the global control point list, P
                    self._P.append(P_temp)
                    self._num_points += 1
        except IOError:
            print('Cannot open file ' + self._filename)


class PointFromFile3D(Point):

    def __init__(self, dimension, filename):
        """Constructor of the PointFromFile3D class

        This class is used for reading Surface control points from a file.

        Args:
            dimension (int): '2' defines Curve and '3' defines Surface
            filename (str): File name to be read
        """
        # Call parent class constructor
        super().__init__(dimension)
        self._filename = filename  # File which contains the control points
        self._num_points_u = 0
        self._num_points_v = 0

    def input_cp(self):
        try:
            # Open the file
            with open(self._filename, 'r') as fp:
                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    control_point_row = line.split('; ')
                    P_row = []
                    self._num_points_v = 0
                    for cpr in control_point_row:
                        control_point = cpr.split(', ')
                        # Read x- and y-coordinates
                        x_input = int(control_point[0])
                        y_input = int(control_point[1])
                        z_input = int(control_point[2])
                        # Create a temporary dictionary for appending coordinates into P
                        P_temp = {'x': x_input, 'y': y_input, 'z': z_input}
                        # Add control points to the global control point list, P
                        P_row.append(P_temp)
                        self._num_points_v += 1
                    self._P.append(P_row)
                    self._num_points_u += 1

        except IOError:
            print('Cannot open file ' + self._filename)

    def get_cp_v(self):
        """Returns P[v][u] formatted control points.

        Returns:
            list: Control points
        """
        return self._P

    def get_cp_u(self):
        """Returns P[u][v] formatted control points.

        Returns:
            list: Control points
        """
        P_new = []
        j = 0
        while j < self._num_points_u:
            i = 0
            temp = []
            while i < self._num_points_v:
                temp.append(self._P[i][j])
                i += 1
            P_new.append(temp)
            j += 1
        return P_new
