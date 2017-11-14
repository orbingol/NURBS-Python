File Formats
^^^^^^^^^^^^

Text Files for Control Points
=============================

NURBS-Python library provides 2 functions in each class included for reading and saving the control points list. These
are:

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

.. note:: The control points correspond to a right-handed coordinate system.
