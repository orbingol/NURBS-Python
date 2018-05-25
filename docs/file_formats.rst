Supported File Formats
^^^^^^^^^^^^^^^^^^^^^^

NURBS-Python supports several input and output formats for importing and exporting B-Spline/NURBS curves and surfaces.
Please note that NURBS-Python uses right-handed notation on input and output files.

Text Files
==========

NURBS-Python provides a simple way to import and export the control points and the evaluated control points as ASCII
text files. The details of the file format for curves and surfaces is described below:

.. toctree::
    :maxdepth: 2

    file_formats_txt

Comma-Separated (CSV)
=====================

You may use :py:func:`.export_csv()` function to save control points and/or evaluated points as a CSV file. This
function works with both curves and surfaces.

VTK (Legacy) Format
===================

You may use :py:func:`.export_vtk()` function to save control points and/or evaluated points as a VTK file
(legacy format). This function works with both curves and surfaces.

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
