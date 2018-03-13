File Formats
^^^^^^^^^^^^

NURBS-Python uses right-handed notation in input and output files.

TXT Files
=========

NURBS-Python library provides 2 functions in each class included for **reading** and **saving** the control points list.
These are:

* ``read_ctrlpts_from_txt``: Reads control points list from a text file
* ``save_ctrlpts_to_txt``: Saves control points list to a text file

The format of the text file depends on the type of the geometric element, i.e. curve or surface, that you are trying to
export. The following explains the file formats for `.txt` files which contain control points.

2D Curves
---------

To generate a 2D B-Spline Curve, you need a list of *(x, y)* coordinates representing the control points (P), where

* `x`: value representing the x-coordinate
* `y`: value representing the y-coordinate

The format of the control points file for generating 2D B-Spline curves is as follows:

+-------------+-------------+
|      x      |      y      |
+=============+=============+
| x\ :sub:`1` | y\ :sub:`1` |
+-------------+-------------+
| x\ :sub:`2` | y\ :sub:`2` |
+-------------+-------------+
| x\ :sub:`3` | y\ :sub:`3` |
+-------------+-------------+

The control points file format of the NURBS curves are very similiar to B-Spline ones with the difference of weights.
To generate a **2D NURBS curve**, you need a list of *(x\*w, y\*w, w)* coordinates representing the weighted control
points (P\ :sub:`w`) where,

* `x`: value representing the x-coordinate
* `y`: value representing the y-coordinate
* `w`: value representing the weight

The format of the control points file for generating **2D NURBS curves** is as follows:

+---------------------------+---------------------------+-------------+
|           x\*w            |           y\*w            |      w      |
+===========================+===========================+=============+
| x\ :sub:`1`\*w\ :sub:`1`  | y\ :sub:`1`\*w\ :sub:`1`  | w\ :sub:`1` |
+---------------------------+---------------------------+-------------+
| x\ :sub:`2`\*w\ :sub:`2`  | y\ :sub:`2`\*w\ :sub:`2`  | w\ :sub:`2` |
+---------------------------+---------------------------+-------------+
| x\ :sub:`3`\*w\ :sub:`3`  | y\ :sub:`3`\*w\ :sub:`3`  | w\ :sub:`3` |
+---------------------------+---------------------------+-------------+

.. note::

    :doc:`compatibility <module_compatibility>` module provides several functions to manipulate & convert control
    point arrays into NURBS-Python compatible ones and more.

3D Curves
---------

To generate a **3D B-Spline curve**, you need a list of *(x, y, z)* coordinates representing the control points (P),
where

* `x`: value representing the x-coordinate
* `y`: value representing the y-coordinate
* `z`: value representing the z-coordinate

The format of the control points file for generating 3D B-Spline curves is as follows:

+-------------+-------------+-------------+
|      x      |      y      |      z      |
+=============+=============+=============+
| x\ :sub:`1` | y\ :sub:`1` | z\ :sub:`1` |
+-------------+-------------+-------------+
| x\ :sub:`2` | y\ :sub:`2` | z\ :sub:`2` |
+-------------+-------------+-------------+
| x\ :sub:`3` | y\ :sub:`3` | z\ :sub:`3` |
+-------------+-------------+-------------+

To generate a **3D NURBS curve**, you need a list of *(x\*w, y\*w, z\*w, w)* coordinates representing the weighted
control points (P\ :sub:`w`) where,

* `x`: value representing the x-coordinate
* `y`: value representing the y-coordinate
* `z`: value representing the z-coordinate
* `w`: value representing the weight

The format of the control points file for generating 3D NURBS curves is as follows:

+---------------------------+---------------------------+---------------------------+-------------+
|            x\*w           |            y\*w           |            z\*w           |      w      |
+===========================+===========================+===========================+=============+
| x\ :sub:`1`\*w\ :sub:`1`  | y\ :sub:`1`\*w\ :sub:`1`  | z\ :sub:`1`\*w\ :sub:`1`  | w\ :sub:`1` |
+---------------------------+---------------------------+---------------------------+-------------+
| x\ :sub:`2`\*w\ :sub:`2`  | y\ :sub:`2`\*w\ :sub:`2`  | z\ :sub:`2`\*w\ :sub:`2`  | w\ :sub:`2` |
+---------------------------+---------------------------+---------------------------+-------------+
| x\ :sub:`3`\*w\ :sub:`3`  | y\ :sub:`3`\*w\ :sub:`3`  | z\ :sub:`3`\*w\ :sub:`3`  | w\ :sub:`3` |
+---------------------------+---------------------------+---------------------------+-------------+

.. note::

    :doc:`compatibility <module_compatibility>` module provides several functions to manipulate & convert control
    point arrays into NURBS-Python compatible ones and more.

Surfaces
--------

Control points file for generating B-Spline and NURBS has 2 options:

First option is very similar to the curve control
points files with one noticeable difference to process `u` and `v` indices. In this list, the `v` index varies first.
That is, a row of `v` control points for the first `u` value is found first. Then, the row of `v` control points for the
next `u` value.

The second option sets the rows as `v` and columns as `u`. To generate a **B-Spline surface** using this option, you
need a list of *(x, y, z)* coordinates representing the control points (P) where,

* `x`: value representing the x-coordinate
* `y`: value representing the y-coordinate
* `z`: value representing the z-coordinate

The format of the control points file for generating B-Spline surfaces is as follows:

+--------+-----------+-----------+-----------+-----------+-----------+
|        |     v0    |     v1    |     v2    |     v3    |     v4    |
+========+===========+===========+===========+===========+===========+
| **u0** | (x, y, z) | (x, y, z) | (x, y, z) | (x, y, z) | (x, y, z) |
+--------+-----------+-----------+-----------+-----------+-----------+
| **u1** | (x, y, z) | (x, y, z) | (x, y, z) | (x, y, z) | (x, y, z) |
+--------+-----------+-----------+-----------+-----------+-----------+
| **u2** | (x, y, z) | (x, y, z) | (x, y, z) | (x, y, z) | (x, y, z) |
+--------+-----------+-----------+-----------+-----------+-----------+

To generate a **NURBS surface** using the 2nd option, you need a list of *(x\*w, y\*w, z\*w, w)* coordinates
representing the weighted control points (P\ :sub:`w`) where,

* `x`: value representing the x-coordinate
* `y`: value representing the y-coordinate
* `z`: value representing the z-coordinate
* `w`: value representing the weight

The format of the control points file for generating NURBS surfaces is as follows:

+--------+-----------------------+-----------------------+-----------------------+-----------------------+
|        |             v0        |           v1          |           v2          |           v3          |
+========+=======================+=======================+=======================+=======================+
| **u0** | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) |
+--------+-----------------------+-----------------------+-----------------------+-----------------------+
| **u1** | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) |
+--------+-----------------------+-----------------------+-----------------------+-----------------------+
| **u2** | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) | (x\*w, y\*w, z\*w, w) |
+--------+-----------------------+-----------------------+-----------------------+-----------------------+

.. note::

    :doc:`compatibility <module_compatibility>` module provides several functions to manipulate & convert control
    point arrays into NURBS-Python compatible ones and more.

CSV Files
=========

NURBS-Python library provides 2 functions in each class for exporting *control points* and *evaluted points* as CSV files.
These functions are:

For all classes:

* ``export_ctrlpts_to_csv``: Saves control points list as a CSV file

For ``Curve`` class:

* ``export_curvepts_to_csv``: Saves evaluated curve points as a CSV file

For ``Surface`` class:

* ``export_surfpts_to_csv``: Saves evaluted surface points as a CSV file

Customization Options
---------------------

The control points and the evaluated curve points list are always linear and there are no customization options. On the
other hand, CSV exports from surface classes have some customization options.

Surface Control Points
~~~~~~~~~~~~~~~~~~~~~~

The following modes are available via ``mode=`` parameter of the ``export_ctrlpts_to_csv`` method:

* ``linear``: Default mode, saves the stored point array without any change
* ``zigzag``: Generates a zig-zag shape
* ``wireframe``: Generates a wireframe

Evaluated Surface Points
~~~~~~~~~~~~~~~~~~~~~~~~

The following modes are available via ``mode=`` parameter of the ``export_surfpts_to_csv`` method:

* ``linear``: Default mode, saves the stored point array without any change
* ``zigzag``: Generates a zig-zag shape
* ``wireframe``: Generates a wireframe/quad mesh
* ``triangle``: Generates a triangular mesh

OBJ Files
=========

Starting from NURBS-Python v3.1.0, a new experimental module called :code:`exchange` has been added to the package. This
module provides functionality for exporting NURBS surfaces to common CAD exchange formats.

Example 1
---------

The following example demonstrates saving surfaces as .obj files:

.. code-block:: python

    # ex_bezier_surface.py
    from geomdl import BSpline
    from geomdl import utilities
    from geomdl import exchange

    # Create a BSpline surface instance
    surf = BSpline.Surface()

    # Set evaluation delta
    surf.delta = 0.01

    # Set up the surface
    surf.degree_u = 3
    surf.degree_v = 2
    control_points = [[0, 0, 0], [0, 1, 0], [0, 2, -3],
                      [1, 0, 6], [1, 1, 0], [1, 2, 0],
                      [2, 0, 0], [2, 1, 0], [2, 2, 3],
                      [3, 0, 0], [3, 1, -3], [3, 2, 0]]
    surf.set_ctrlpts(control_points, 4, 3)
    surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, 4)
    surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, 3)

    # Evaluate surface
    surf.evaluate()

    # Save surface as a .obj file
    exchange.save_obj(surf, "bezier_surf.obj")

Example 2
---------

The following example combines :code:`shapes` module together with :code:`exchange` module:

.. code-block:: python

    from geomdl.shapes import surface
    from geomdl import exchange

    # Generate cylindirical surface
    surf = surface.cylinder(radius=5, height=12.5)

    # Set evaluation delta
    surf.delta = 0.01

    # Evaluate the surface
    surf.evaluate()

    # Save surface as a .obj file
    exchange.save_obj(surf, "cylindirical_surf.obj")

STL Files
=========

Exporting to STL files works in the same way explained in OBJ Files section. To export a NURBS surface as a .stl file,
you can use :py:func:`.save_stl()` function. This function saves in binary format by default but there is an option to
change the save file format to plain text. Please see the :doc:`documentation <module_exchange>` for details.
