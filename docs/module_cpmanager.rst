Control Points Manager
^^^^^^^^^^^^^^^^^^^^^^

The ``ptmanager`` module provides classes for managing control points. The classes are designed to eliminate
confusion when more than one parametric dimension is involved in generation of the spline geometry.

Usage Instructions
==================

:class:`.ptmanager.CPManager` class provides an easy way to set control points without knowing the internal data
structure of the geometry classes. The manager class is initialized with the number of control points in all parametric
dimensions.

For Curves
----------
B-spline curves are defined in one parametric dimension. Therefore, this manager class should be initialized with
a single integer value.

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Assuming that the curve has 10 control points
    manager = CPManager(10)

Getting the control points:

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Number of control points in all parametric dimensions
    size_u = crv.ctrlpts_size

    # Generate control points manager
    cpt_manager = CPManager(size_u)
    cpt_manager.ctrlpts = spline.ctrlpts

    # Control points array to be used externally
    control_points = []

    # Get control points from the spline geometry
    for u in range(size_u):
        pt = cpt_manager.get_ctrlpt(u)
        control_points.append(pt)

Setting the control points:

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Number of control points in all parametric dimensions
    size_u = 5

    # Create control points manager
    points = CPManager(size_u)

    # Set control points
    for u in range(size_u):
        # 'pt' is the control point, e.g. [10, 15, 12]
        points.set_ctrlpt(pt, u, v)

    # Create spline geometry
    curve = BSpline.Curve()

    # Set control points
    curve.ctrlpts = points.ctrlpts

For Surfaces
------------

B-spline surfaces are defined in two parametric dimensions. Therefore, the manager class should be initialized with
two integer values.

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Assuming that the surface has size_u = 5 and size_v = 7 control points
    manager = CPManager(5, 7)

Getting the control points:

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Number of control points in all parametric dimensions
    size_u = surf.ctrlpts_size_u
    size_v = surf.ctrlpts_size_v

    # Generate control points manager
    cpt_manager = CPManager(size_u, size_v)
    cpt_manager.ctrlpts = spline.ctrlpts

    # Control points array to be used externally
    control_points = []

    # Get control points from the spline geometry
    for u in range(size_u):
        for v in range(size_v):
            pt = cpt_manager.get_ctrlpt(u, v)
            control_points.append(pt)

Setting the control points:

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Number of control points in all parametric dimensions
    size_u = 5
    size_v = 3

    # Create control points manager
    points = CPManager(size_u, size_v)

    # Set control points
    for u in range(size_u):
        for v in range(size_v):
            # 'pt' is the control point, e.g. [10, 15, 12]
            points.set_ctrlpt(pt, u, v)

    # Create spline geometry
    surf = BSpline.Surface()

    # Set control points
    surf.ctrlpts = points.ctrlpts

For Volumes
-----------

B-spline volumes are defined in three parametric dimensions. Therefore, this manager class should be initialized with
there integer values.

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Assuming that the volume has size_u = 5, size_v = 12 and size_w = 3 control points
    manager = CPManager(5, 12, 3)

Gettting the control points:

.. code-block:: python

    # Number of control points in all parametric dimensions
    size_u = vol.ctrlpts_size_u
    size_v = vol.ctrlpts_size_v
    size_w = vol.ctrlpts_size_w

    # Generate control points manager
    cpt_manager = CPManager(size_u, size_v, size_w)
    cpt_manager.ctrlpts = spline.ctrlpts

    # Control points array to be used externally
    control_points = []

    # Get control points from the spline geometry
    for u in range(size_u):
        for v in range(size_v):
            for w in range(size_w):
                pt = cpt_manager.get_ctrlpt(u, v, w)
                control_points.append(pt)

Setting the control points:

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Number of control points in all parametric dimensions
    size_u = 5
    size_v = 3
    size_w = 2

    # Create control points manager
    points = CPManager(size_u, size_v, size_w)

    # Set control points
    for u in range(size_u):
        for v in range(size_v):
            for w in range(size_w):
                # 'pt' is the control point, e.g. [10, 15, 12]
                points.set_ctrlpt(pt, u, v, w)

    # Create spline geometry
    volume = BSpline.Volume()

    # Set control points
    volume.ctrlpts = points.ctrlpts

Dynamic attributes
------------------

:class:`.control_points.CPManager` class provides dynamically generated attributes for getting size of control points on
``u``, ``v`` and ``w`` parametric dimensions. The following code snippet demonstrates the usage of dynamic attributes:

.. code-block:: python

    from geomdl.ptmanager import CPManager

    # Generate a control points manager instance with 5, 7 and 10 control points in u, v and w dimensions, respectively
    cpt_man = CPManager(5, 7, 10)

    # Get number of control points on u
    num_ctrlpts_u = cpt_man.size_u

    # Get number of control points on v
    num_ctrlpts_v = cpt_man.size_v

    # Get number of control points on w
    num_ctrlpts_w = cpt_man.size_w

The dynamic attributes will also work for curves and surfaces. For surfaces, there will be ``size_u`` and ``size_v``
attributes. For curves, there will be only ``size_u`` attribute.

Class Reference
===============

.. automodule:: geomdl.ptmanager
    :members:
    :inherited-members:
    :exclude-members: next
    :show-inheritance:
