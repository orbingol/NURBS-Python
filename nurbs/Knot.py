"""
    NURBS Python Package

    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016
"""


class Knot(object):
    """Knot vector operations

    Attributes:
        dimension: the dimension of the coordinates (2 or 3)
        degree: Degree of the curve
        num_points: Number of control points
    """

    # Small u increment value
    INCREMENT = 0.01

    def __init__(self, dimension, degree, num_points):
        """Constructor of the Knot class

        Args:
            dimension (int): '2' defines Curve and '3' defines Surface
            degree (str): Degree of the curve directly input by the user
            num_points (int): Number of control points
        """
        self._degree = int(degree)
        self._num_points = num_points
        # Define a global knot vector
        self._knot_vector = []
        # Store updated knot vector after knot insertion in a temporary variable
        # Current logic of this class creates a messy knot vector if a temporary variable is not used.
        self._knot_vector_updated = []
        # Define a span array
        self._spans = []
        # Define basis functions list
        self._basis_functions = []
        # Define a list containing all small u values
        self._all_u = []
        # Define multiplicity
        self._multiplicity = 0
        # Dimension means the input is a 2D (a.k.a. Curve) or 3D (a.k.a. Surface) list
        self._dimension = dimension

    #
    # Public methods
    #

    def create_knot_vector(self):
        """Creates a non-uniform knot vector."""
        # Find number of knots necessary in the knot vector
        number_of_knots = self._find_number_of_knots()

        # By definition, knot vectors start with 0 and end with 1
        knot_start = 0.0
        knot_end = 1.0

        # Define the size of variable knots in the knot vector.
        # Example: Number of elements in the dotted region of the knot vector; [0 0 0 0 ....... 1 1 1 1]
        mid_array_size = number_of_knots - (2 * (self._degree + 1))

        # Calculate increment between these variable knots
        increment = 1.0 / (mid_array_size + 1)

        # Temporary variable to define middle number inside the knot vector
        mid = 0.0

        # Create the first part of the knot vector
        for i in range(0, self._degree + 1, 1):
            self._knot_vector.append(knot_start)

        # Create the middle part of the knot vector
        for i in range(0, mid_array_size, 1):
            mid += increment
            self._knot_vector.append(round(mid, 3))

        # Create the final part of the knot vector
        for i in range(0, self._degree + 1, 1):
            self._knot_vector.append(knot_end)

    def get_knot_vector(self, display=False):
        """ Returns the knot vector

        Args:
            display (bool): Defined whether the knot vector is displayed or not. Defaults to False.

        Returns:
            List[float]: Knot vector
        """
        if display:
            print(str(self._knot_vector))
        return self._knot_vector

    def calculate_spans(self):
        """Calculates span values."""
        if self._spans:
            self._spans.clear()
        self._create_small_us()
        for u in self._all_u:
            span_val = self._find_span(u)
            self._spans.append(span_val)

    def get_spans(self):
        """Returns a list of spans

            Returns:
                List[float]: A list of spans calculated according to small u values (a.k.a. knot values)
        """
        return self._spans

    def calculate_basis_functions(self):
        """Calculates basis functions."""
        if self._basis_functions:
            self._basis_functions.clear()
        for u, s in zip(self._all_u, self._spans):
            bs_val = self._find_basis_functions(s, u)
            self._basis_functions.append(bs_val)

    def get_basis_functions(self):
        """Returns a list of basis functions

        Returns:
            List[float]: A list of basis functions calculated according to spans
        """
        return self._basis_functions

    def insert_knot_curve(self, Pw, u, r):
        """Curve knot insertion algorithm

        This algorithm is a part of the Algorithm A5.1 of The NURBS Book

        Args:
            Pw (Dict[float]): Dictionary of weighted control points
            u (float): Knot to be inserted
            r (int): How many times the knot will be inserted

        Returns:
            List[Dict[float]]: List of updated weighted control points
        """
        # Find span for the new knot
        span = self._find_span(u)
        # Get updated control points
        P_updated = self._insert_knot(Pw, u, r, span)
        # Update knot vector
        self._update_knot_vector()
        # Update number of points
        self._num_points += r
        # Return updated control points
        return P_updated

    def find_multiplicity(self, u):
        """Calculates multiplicity while knot insertion

        Args:
            u (float): Knot to be inserted
        """
        if self._multiplicity > 0:
            self._multiplicity = 0
        for i in range(0, self._knot_vector.__len__(), 1):
            if self._knot_vector[i] == u:
                self._multiplicity += 1

    def insert_knot_surface(self, Pw, u, r):
        """Surface knot insertion algorithm

        This algorithm is a part of the Algorithm A5.3 of The NURBS Book

        Args:
            Pw (Dict[float]): Dictionary of weighted control points
            u (float): Knot to be inserted
            r (int): How many times the knot will be inserted

        Returns:
            List[Dict[float]]: List of updated weighted control points
        """
        # Find span for the new knot
        span = self._find_span(u)
        # Create a container for updated control points
        Pw_new = []
        # Get updated control points
        for P in Pw:
            Pw_temp = self._insert_knot(P, u, r, span)
            Pw_new.append(Pw_temp)
        # Update knot vector
        self._update_knot_vector()
        # Update number of points
        self._num_points += r
        # Return updated control points
        return Pw_new

    #
    # Private methods
    #

    def _find_number_of_knots(self):
        """Finds number of knots in the global knot vector

        Calculates number of knots according to the formula "m = n + p + 1"
        where;
            p is the degree
            n+1 is the number of control points
            m+1 is the number of knots

        Returns:
            int: Number of knots
        """
        knots = self._degree + self._num_points + 1
        return knots

    def _update_knot_vector(self):
        """Updates the global knot vector after knot insertion

        Returns:
             None. Only updates the global knot vector
        """
        self._knot_vector.clear()
        self._knot_vector = self._knot_vector_updated

    def _create_small_us(self, increment=INCREMENT):
        """Iterates through the knot vector to create a list of numbers according to the given increment

        This list feeds curve point generator

        Args:
            increment (float): The increment value. Smaller creates more curve points.

        Returns:
            None. Only populates the global all_u list.
        """
        if self._all_u:
            self._all_u.clear()
        i = min(self._knot_vector)
        while i <= max(self._knot_vector):
            self._all_u.append(i)
            i += increment
            i = round(i, 3)  # Python has some floating point calculation errors, so truncating / rounding is necessary

    def _find_span(self, u):
        """Finds span of the given knot value

        Algorithm A2.1 of The NURBS Book on page 68

        Args:
            u (float): Knot value

        Returns:
            int: Span of the knot value
        """
        if self._knot_vector[self._num_points] == u:
            return self._num_points - 1

        low = self._degree
        high = self._num_points
        mid = int((low + high) / 2)

        while u < self._knot_vector[mid] or u >= self._knot_vector[mid + 1]:
            if u < self._knot_vector[mid]:
                high = mid
            else:
                low = mid
            mid = int((low + high) / 2)

        return mid

    def _find_basis_functions(self, span, u):
        """Finds basis functions

        This method is implemented according to Algorithm A2.2 of The NURBS Book on page 70

        Args:
            span (int): Span of the knot value below
            u (float): Knot value

        Returns:
            float: Basis function value
        """
        N = [0.0 for i in range(self._degree + 1)]

        left = [0.0 for i in range(self._degree + 1)]
        right = [0.0 for i in range(self._degree + 1)]

        # N[0] = 1.0 by definition
        N[0] = 1.0

        j = 1
        while j <= self._degree:
            left[j] = u - self._knot_vector[span + 1 - j]
            right[j] = self._knot_vector[span + j] - u
            saved = 0.0
            for r in range(0, j, 1):
                temp = N[r] / (right[r + 1] + left[j - r])
                N[r] = round(saved + (right[r + 1] * temp), 3)
                saved = left[j - r] * temp
            N[j] = round(saved, 3)
            j += 1

        return N

    def _insert_knot(self, Pw, u, r, span):
        """Knot insertion algorithm

        This algorithm is the a part of the Algorithm A5.1 and Algorithm A5.3 of The NURBS Book

        Args:
            Pw (Dict[float]): Dictionary of weighted control points
            u (float): Knot to be inserted
            r (int): How many times the knot will be inserted
            span (int): Span of the knot to be inserted (Denoted by 'k' in the algorithm)

        Returns:
            Dict[float]: Updated dictionary of the weighted control points
        """
        # Find number of knots
        mp = self._find_number_of_knots()

        # Container for the new knot vector
        Q = []
        # Containers for the new control points. They should be initialized in order to use __getitem__ (aka []) method
        Qw = [0.0 for i in range(self._num_points + r)]
        Rw = [0.0 for i in range(self._degree - self._multiplicity + 1)]

        # Load new knot vector
        i = 0
        while i <= span:
            Q.append(self._knot_vector[i])
            i += 1

        i = 1
        while i <= r:
            Q.append(u)
            i += 1

        i = span + 1
        while i < mp:
            Q.append(self._knot_vector[i])
            i += 1

        # Save unaltered control points
        i = 0
        while i <= span - self._degree:
            Qw[i] = Pw[i]
            i += 1

        i = span - self._multiplicity
        while i < self._num_points:  # Alternatively, range(span-multiplicity, num_points, 1)
            Qw[i + r] = Pw[i]
            i += 1

        i = 0
        while i <= self._degree - self._multiplicity:
            Rw[i] = Pw[span - self._degree + i]
            i += 1

        # Insert the knot r times
        j = 1
        while j <= r:
            L = span - self._degree + j
            i = 0
            while i <= self._degree - j - self._multiplicity:
                alpha = (u - self._knot_vector[L + i]) / (self._knot_vector[i + span + 1] - self._knot_vector[L + i])
                if self._dimension == 3:
                    Rw[i] = {'xw': Rw[i]['xw'], 'yw': Rw[i]['yw'], 'zw': Rw[i]['zw'], 'w': Rw[i]['w']}
                else:
                    Rw[i] = {'xw': Rw[i]['xw'], 'yw': Rw[i]['yw'], 'w': Rw[i]['w']}
                Rw[i]['xw'] = (alpha * Rw[i + 1]['xw']) + ((1.0 - alpha) * Rw[i]['xw'])
                Rw[i]['yw'] = (alpha * Rw[i + 1]['yw']) + ((1.0 - alpha) * Rw[i]['yw'])
                if self._dimension == 3:
                    Rw[i]['zw'] = (alpha * Rw[i + 1]['zw']) + ((1.0 - alpha) * Rw[i]['zw'])
                Rw[i]['w'] = (alpha * Rw[i + 1]['w']) + ((1.0 - alpha) * Rw[i]['w'])
                i += 1
            Qw[L] = Rw[0]
            Qw[span + r - j - self._multiplicity] = Rw[self._degree - j - self._multiplicity]
            j += 1

        # Load remaining control points
        i = L + 1
        while i < span - self._multiplicity:
            Qw[i] = Rw[i - L]
            i += 1

        # Create a weighted control points array
        Pw_new = []
        # Update weighted control points array
        for q in Qw:
            if self._dimension == 3:
                Pw_temp = {'xw': round(q['xw'], 3), 'yw': round(q['yw'], 3), 'zw': round(q['zw'], 3),
                           'w': round(q['w'], 3)}
            else:
                Pw_temp = {'xw': round(q['xw'], 3), 'yw': round(q['yw'], 3), 'w': round(q['w'], 3)}
            Pw_new.append(Pw_temp)

        # Copy the updated knot vector into a global variable
        self._knot_vector_updated = Q

        # Return updated weighted control points
        return Pw_new
