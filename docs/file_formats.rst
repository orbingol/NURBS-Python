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

You may use :py:func:`.export_obj()` function to export a NURBS surface as a Wavefront .obj file.

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
    exchange.export_obj(surf, "bezier_surf.obj")

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
    exchange.export_obj(surf, "cylindirical_surf.obj")

STL Format
==========

Exporting to STL files works in the same way explained in OBJ Files section. To export a NURBS surface as a .stl file,
you may use :py:func:`.export_stl()` function. This function saves in binary format by default but there is an option to
change the save file format to plain text. Please see the :doc:`documentation <module_exchange>` for details.

Object File Format (OFF)
========================

Very similar to exporting as OBJ and STL formats, you may use :py:func:`.export_off()` function to export a NURBS surface
as a .off file.

Custom Formats (libconfig, YAML, JSON)
======================================

NURBS-Python provides several custom formats, such as libconfig, YAML and JSON, for importing and exporting complete
NURBS shapes (i.e. degrees, knot vectors and control points of single and multi curves/surfaces).

libconfig
---------

`libconfig <https://hyperrealm.github.io/libconfig/>`_ is a lightweight library for processing configuration files and
it is often used on C/C++ projects. The library doesn't define a format but it defines a syntax for the files it can
process. NURBS-Python uses :py:func:`.export_cfg()` and :py:func:`.import_cfg()` functions to exporting and importing
shape data which can be processed by libconfig-compatible libraries. Although exporting does not require any external
libraries, importing functionality depends on `libconf <https://pypi.org/project/libconf/>`_ module, which is a pure
Python library for parsing libconfig-formatted files.

YAML
----

`YAML <http://yaml.org/>`_ is a data serialization format and it is supported by the major programming languages.
NURBS-Python uses `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_ package as an external dependency for its YAML
support since the package is well-maintained and compatible with the latest YAML standards.
NURBS-Python supports exporting and importing NURBS data to YAML format with the functions :py:func:`.export_yaml()`
and :py:func:`.import_yaml()`, respectively.

JSON
----

`JSON <https://www.json.org/>`_ is also a serialization and data interchange format and it is **natively supported**
by Python via ``json`` module. NURBS-Python supports exporting and importing NURBS data to JSON format with the
functions :py:func:`.export_json()` and :py:func:`.import_json()`, respectively.

Format Definition
-----------------

Curve
~~~~~

THe following example illustrates a 2-dimensional NURBS curve. 3-dimensional NURBS curves are also supported and they
can be generated by updating the control points.

.. code-block:: yaml

    shape:
      type: curve
      data:
        - degree: 2
          knotvector: [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]
          control_points:
            points:  # cartesian coordinates of the control points
              - [0.0, -1.0]  # each control point is defined as a list
              - [-1.0, -1.0]
              - [-1.0, 0.0]
              - [-1.0, 1.0]
              - [0.0, 1.0]
              - [1.0, 1.0]
              - [1.0, 0.0]
              - [1.0, -1.0]
              - [0.0, -1.0]
            weights:  # weights vector
              - 1.0
              - 0.707
              - 1.0
              - 0.707
              - 1.0
              - 0.707
              - 1.0
              - 0.707
              - 1.0
          delta: 0.01  # evaluation delta

* **Shape section:** This section contains the single or multi NURBS data. ``type`` and ``data`` sections are mandatory.
* **Type section:** This section defines the type of the NURBS shape. For NURBS curves, it should be set to *curve*.
* **Data section:** This section defines the NURBS data, i.e. degrees, knot vectors and control_points. ``weights`` and ``delta`` sections are optional.

Surface
~~~~~~~

THe following examples illustrates a NURBS surface:

.. code-block:: yaml

    shape:
      type: surface  # define shape type
      data:
        - degree_u: 1  # degree of the u-direction
          degree_v: 2  # degree of the v-direction
          knotvector_u: [0.0, 0.0, 1.0, 1.0]
          knotvector_v: [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 1.0]
          size_u: 2  # number of control points on the u-direction
          size_v: 9  # number of control points on the v-direction
          control_points:
            points:  # cartesian coordinates (x, y, z) of the control points
              - [1.0, 0.0, 0.0]  # each control point is defined as a list
              - [1.0, 1.0, 0.0]
              - [0.0, 1.0, 0.0]
              - [-1.0, 1.0, 0.0]
              - [-1.0, 0.0, 0.0]
              - [-1.0, -1.0, 0.0]
              - [0.0, -1.0, 0.0]
              - [1.0, -1.0, 0.0]
              - [1.0, 0.0, 0.0]
              - [1.0, 0.0, 1.0]
              - [1.0, 1.0, 1.0]
              - [0.0, 1.0, 1.0]
              - [-1.0, 1.0, 1.0]
              - [-1.0, 0.0, 1.0]
              - [-1.0, -1.0, 1.0]
              - [0.0, -1.0, 1.0]
              - [1.0, -1.0, 1.0]
              - [1.0, 0.0, 1.0]
            weights:  # weights vector
              - 1.0
              - 0.7071
              - 1.0
              - 0.7071
              - 1.0
              - 0.7071
              - 1.0
              - 0.7071
              - 1.0
              - 1.0
              - 0.7071
              - 1.0
              - 0.7071
              - 1.0
              - 0.7071
              - 1.0
              - 0.7071
              - 1.0
          delta:
              - 0.05  # evaluation delta of the u-direction
              - 0.05  # evaluation delta of the v-direction

* **Shape section:** This section contains the single or multi NURBS data. ``type`` and ``data`` sections are mandatory.
* **Type section:** This section defines the type of the NURBS shape. For NURBS curves, it should be set to *surface*.
* **Data section:** This section defines the NURBS data, i.e. degrees, knot vectors and control_points. ``weights`` and ``delta`` sections are optional.

Example: Reading .cfg Files with libconf
----------------------------------------

The following example illustrates reading the exported .cfg file with `libconf <https://pypi.org/project/libconf/>`_
module as a reference for `libconfig <https://hyperrealm.github.io/libconfig/>`_-based systems in different programming
languages.

.. code-block:: python

    # Assuming that you have already installed 'libconf'
    import libconf

    # Skipping export steps and assuming that we have already exported the data as 'my_nurbs.cfg'
    with open("my_nurbs.cfg", "r") as fp:
        # Open the file and parse using libconf module
        ns = libconf.load(fp)

    # 'count' shows the number of shapes loaded from the file
    print(ns['shape']['count']

    # Traverse through the loaded shapes
    for n in ns['shape']['data']:
        # As an example, we get the control points
        ctrlpts = n['control_points']['points']

NURBS-Python exports data in the way that allows processing any number of curves or surfaces with a simple for loop.
This approach simplifies implementation of file reading routines for different systems and programming languages.
