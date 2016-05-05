"""
    NURBS Python Package

    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016
"""


class Weight(object):
    """Calculates weights to create weighted control points.

    Arguments:
        num_points: Number of control points.
    """

    def __init__(self, num_points):
        """Constructor of the Weight class.

        Arguments:
            num_points (int): Number of control points.
        """
        # Number of control points define the size of the weight vector
        self._num_points = num_points
        # Define a weight vector
        self._weight_vector = []

    def calculate(self):
        """Calculates a random weight vector."""
        for i in range(0, self._num_points, 1):
            if i < self._num_points/2:
                self._weight_vector.append(1.0)
            else:
                self._weight_vector.append(2.0)

    def get_result(self):
        """Returns the weight vector.

        Returns:
            List[float]: A list of weights.
        """
        return self._weight_vector
