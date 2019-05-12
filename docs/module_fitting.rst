Curve and Surface Fitting
^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 5.0

``fitting`` module provides functions for interpolating and approximating
B-spline curves and surfaces from data points. Approximation uses least
squares algorithm.

Please see the following functions for details:

* :py:func:`.interpolate_curve`
* :py:func:`.interpolate_surface`
* :py:func:`.approximate_curve`
* :py:func:`.approximate_surface`

Surface fitting generates control points grid defined in *u* and *v*
parametric dimensions. Therefore, the input requires number of data
points to be fitted in both parametric dimensions. In other words,
``size_u`` and ``size_v`` arguments are used to fit curves of the
surface on the corresponding parametric dimension.

In the array structure, the data points on the v-direction come the
first and u-direction points come. The index of the data points can
be found using the following formula:

.. math::

    index = v + (u * size_{v})

Function Reference
==================

.. automodule:: geomdl.fitting
    :members:
