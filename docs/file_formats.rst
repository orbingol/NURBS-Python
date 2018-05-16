File Formats
^^^^^^^^^^^^

NURBS-Python uses right-handed notation in input and output files.

Text Files
==========

NURBS-Python library provides :py:func:`.read_txt()` function for reading control points of curves and surfaces from a
text file. The format of the text file depends on the type of the geometric element, i.e. curve or surface.
The following explains the file formats for `.txt` files which contain control points.

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

The control points file format of the NURBS curves are very similar to B-Spline ones with the difference of weights.
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

Comma-Separated (CSV)
=====================

NURBS-Python library provides :py:func:`.export_csv()` function for saving control points and/or evaluated points as a
CSV file.

VTK (Legacy) Format
===================

NURBS-Python library provides :py:func:`.export_vtk()` function for saving control points and/or evaluated points as a
VTK file (legacy format).

OBJ Format
==========

You may use :py:func:`.save_obj()` function to export a NURBS surface as a Wavefront .obj file.

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

STL Format
==========

Exporting to STL files works in the same way explained in OBJ Files section. To export a NURBS surface as a .stl file,
you may use :py:func:`.save_stl()` function. This function saves in binary format by default but there is an option to
change the save file format to plain text. Please see the :doc:`documentation <module_exchange>` for details.

Object File Format (OFF)
========================

Very similar to exporting as OBJ and STL formats, you may use :py:func:`.save_off()` function to export a NURBS surface
as a .off file.
