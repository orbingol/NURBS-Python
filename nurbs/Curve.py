"""
    NURBS Python Package

    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016
"""


class Curve(object):
    """Curve point calculations

    Attributes:
        degree: Degree of the curve directly input by the user
        control_points: A list of control points created by Point class or subclasses
        basis_functions: A list of calculated basis functions (N) calculated in Knot class
        spans: A list of span values calculated in Knot class
    """

    def __init__(self, degree, control_points, basis_functions, spans):
        """Constructor of the Curve class

        Args:
            degree (str): Degree of the curve to be calculated
            control_points (List[Dict[float]]): A list of control point coordinates in a dictionary
            basis_functions (List[List[float]]): A list of basis functions calculated for each span
            spans (List[int]): A list of span (position) values calculated for each knot increment inside the knot vector
        """
        self._degree = int(degree)
        self._control_points = control_points
        self._basis_functions = basis_functions
        self._spans = spans
        # Define the curve coordinates array
        self._curve_coordinates = []

    #
    # Public methods
    #

    def calculate(self):
        """Calculates the curve points for all control points, basis functions and spans

        Returns:
             None. It only updates the global curve_coordinates variable
        """
        x_coords = []
        y_coords = []
        if self._check_weight():
            w_coords = []

        # control_points should be like this [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
        for ctrlpts in self._control_points:
            if self._check_weight():
                x_coords.append(ctrlpts['xw'])
                y_coords.append(ctrlpts['yw'])
                w_coords.append(ctrlpts['w'])
            else:
                x_coords.append(ctrlpts['x'])
                y_coords.append(ctrlpts['y'])

        k = 0
        for s in self._spans:
            cp_x = self._calculate_point(x_coords, self._basis_functions[k], s)
            cp_y = self._calculate_point(y_coords, self._basis_functions[k], s)
            if self._check_weight():
                cp_w = self._calculate_point(w_coords, self._basis_functions[k], s)
                cp_x /= cp_w
                cp_y /= cp_w
            cp_coords = {'x': round(cp_x, 3), 'y': round(cp_y, 3)}
            self._curve_coordinates.append(cp_coords)
            k += 1

    def get_result(self):
        """Returns the calculated curve point list

        Returns:
            list: Calculated curve points list in [{'x': x-coordinate, 'y': y-coordinate}]
        """
        return self._curve_coordinates

    def write(self, filename='curve.out'):
        """Writes calculated curve coordinates to a file

        Args:
            filename (str): File name to be written

        Returns:
             None. It only writes to the file
        """
        with open(filename, 'w') as fp:
            for c in self._curve_coordinates:
                fp.write(str(c['x']) + ', ' + str(c['y']) + '\n')
        fp.close()

    #
    # Private methods
    #

    def _calculate_point(self, control_points, basis_functions, span):
        """Calculates a single curve point

        Args:
            control_points (List[float]): A list of control points. Only includes a single axis (x- or y-axis)
            basis_functions (List(float)): A list of basis functions calculated for the knots that see the above
                control points
            span (int): Position of the knot in the knot vector

        Returns:
            float: The curve point
        """
        cp = 0.0
        j = 0
        while j <= self._degree:
            cp += basis_functions[j] * control_points[span - self._degree + j]
            j += 1
        return cp

    def _check_weight(self):
        """Checks the key 'w' present in the control point list

        It tries to determine the input is weighted control points or not

        Returns:
            bool: True, if the key found. False, otherwise.
        """
        if 'w' in self._control_points[0]:
            return True
        else:
            return False
