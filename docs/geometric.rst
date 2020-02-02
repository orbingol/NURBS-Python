Common Geometric Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tangent of the Curve
====================

.. code-block:: python

    def curve_tangent(obj, u, normalize):
        """ Evaluates the curve tangent vector at the given parameter value.

        The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

        :param obj: input curve
        :param obj: Curve
        :param u: parameter
        :type u: float
        :param normalize: if True, the returned vector is converted to a unit vector
        :type normalize: bool
        :return: a list containing "point" and "vector" pairs
        :rtype: tuple
        """
        # 1st derivative of the curve gives the tangent
        ders = obj.derivatives([u], 1)

        point = ders[0]
        vector = linalg.vector_normalize(ders[1]) if normalize else ders[1]

        return tuple(point), tuple(vector)


Normal to the Tangent of the Curve
==================================

.. code-block:: python

    def curve_normal(obj, u, normalize):
        """ Evaluates the vector normal to the tangent vector at the input parameter, u.

        The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

        :param obj: input curve
        :type obj: Curve
        :param u: parameter
        :type u: float
        :param normalize: if True, the returned vector is converted to a unit vector
        :type normalize: bool
        :return: a list containing "point" and "vector" pairs
        :rtype: tuple
        """
        # Find 1st derivative
        ders = obj.derivatives([u], 1)

        # Find normal
        t = ders[1]
        tn = [0.0, 0.0, 1.0]
        n = linalg.vector_cross(t, tn)

        # Normalize the vector component
        vector = linalg.vector_normalize(n) if normalize else n
        point = ders[0]

        return tuple(point), tuple(vector)


Surface Normal
==============

.. code-block:: python

    def surface_normal(obj, uv, normalize):
        """ Evaluates the surface normal vector at the given (u, v) parameter pair.

        The output returns a list containing the starting point (i.e. origin) of the vector and the vector itself.

        :param obj: input surface
        :type obj: Surface
        :param uv: (u,v) parameter pair
        :type uv: list or tuple
        :param normalize: if True, the returned normal vector is converted to a unit vector
        :type normalize: bool
        :return: a list in the order of "surface point" and "normal vector"
        :rtype: list
        """
        # Take the 1st derivative of the surface
        skl = obj.derivatives(uv, 1)

        point = skl[0][0]
        vector = linalg.vector_cross(skl[1][0], skl[0][1])
        vector = linalg.vector_normalize(vector) if normalize else vector

        return tuple(point), tuple(vector)
