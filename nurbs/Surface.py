"""
    NURBS Python Package

    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016
"""


class Surface(object):
    """Surface point calculations.

    Attributes:
        degree_p: Degree of curve, defined by the U direction.
        degree_q: Degree of curve, defined by the V direction.
        control_points: A list of control points.
        basis_functions_u: A list of calculated basis functions for U direction.
        basis_functions_v: A list of calculated basis functions for V direction.
        spans_u: A list of spans for U direction.
        spans_v: A list of spans for V direction.
    """

    def __init__(self, degree_p, degree_q, control_points, basis_functions_u, basis_functions_v, spans_u, spans_v):
        """Constructor of the Point class

        Args:
            degree_p (str): Degree of curve, defined by the U direction.
            degree_q (str): Degree of curve, defined by the V direction.
            control_points (List[Dict[float]]): A list of control points.
            basis_functions_u (List[List[float]]): A list of calculated basis functions for U direction.
            basis_functions_v (List[List[float]]): A list of calculated basis functions for V direction.
            spans_u (List[float]): A list of spans for U direction.
            spans_v (List[float]): A list of spans for V direction.
        """
        self._degree_p = int(degree_p)
        self._degree_q = int(degree_q)
        self._control_points = control_points
        self._basis_functions_u = basis_functions_u
        self._basis_functions_v = basis_functions_v
        self._spans_u = spans_u
        self._spans_v = spans_v
        # Define the curve coordinates array
        self._surface_coordinates = []

    #
    # Public methods
    #

    def calculate(self):
        """Calculates the surface points for all control points, basis functions and spans

        Returns:
             None. It only updates the global surface_coordinates variable
        """
        # Create lists to store coordinates
        x_coords = []
        y_coords = []
        z_coords = []

        # Structure is [[{'y': 0, 'x': 0, 'z': 0}, {'y': 1, 'x': 1, 'z': 0}], [{'y': 0, 'x': 0, 'z': 0}]]
        for row in self._control_points:
            x_coords_temp = []
            y_coords_temp = []
            z_coords_temp = []
            for column in row:
                x_coords_temp.append(column['x'])
                y_coords_temp.append(column['y'])
                z_coords_temp.append(column['z'])
            x_coords.append(x_coords_temp)
            y_coords.append(y_coords_temp)
            z_coords.append(z_coords_temp)

        # Loop through span lists to calculate surface points
        t = 0
        for sv in self._spans_v:
            k = 0
            for su in self._spans_u:
                sp_x = self._calculate_point(x_coords, self._basis_functions_u[k], self._basis_functions_v[t], su, sv)
                sp_y = self._calculate_point(y_coords, self._basis_functions_u[k], self._basis_functions_v[t], su, sv)
                sp_z = self._calculate_point(z_coords, self._basis_functions_u[k], self._basis_functions_v[t], su, sv)
                sp_coords = {'x': sp_x, 'y': sp_y, 'z': sp_z}
                self._surface_coordinates.append(sp_coords)
                k += 1
            t += 1

    def get_result(self):
        """Returns the calculated surface point list

        Returns:
            list: Calculated surface points list in [{'x': x-coordinate, 'y': y-coordinate, 'z': z-coordinate}]
        """
        return self._surface_coordinates

    def write(self, filename='surface.out'):
        """Writes calculated surface coordinates to a file

        Args:
            filename (str): File name to be written

        Returns:
             None. It only writes to the file
        """
        with open(filename, 'w') as fp:
            for s in self._surface_coordinates:
                fp.write(str(s['x']) + ', ' + str(s['y']) + ', ' + str(s['z']) + '\n')
        fp.close()

    #
    # Private methods
    #

    def _calculate_point(self, control_points, basis_functions_u, basis_functions_v, span_u, span_v):
        """Calculates a single surface point

        Args:
            control_points (List[List[float]]): A list of control points. Only includes a single axis (x- or y-axis)
            basis_functions_u (List(float)): A list of basis functions for U direction
            basis_functions_v (List(float)): A list of basis functions for V direction
            span_u (int): Position of the knot in the knot vector U
            span_v (int): Position of the knot in the knot vector V

        Returns:
            float: The surface point
        """
        sp = 0.0
        uind = span_u - self._degree_p
        l = 0
        while l <= self._degree_q:
            temp = 0.0
            vind = span_v - self._degree_q + 1
            k = 0
            while k <= self._degree_p:
                temp += basis_functions_u[k] * control_points[vind][uind+k]
                k += 1
            sp += basis_functions_v[l] * temp
            l += 1
        return sp
