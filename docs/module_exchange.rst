Import and Export Data
^^^^^^^^^^^^^^^^^^^^^^

This module allows users to export/import NURBS shapes in common CAD exchange formats. The functions starting with
*import_* are used for generating B-spline and NURBS objects from the input files. The functions starting with
*export_* are used for saving B-spline and NURBS objects as files.

The following functions can only **import/export control points** or **export evaluated points**:

* :py:func:`.exchange.import_txt()`
* :py:func:`.exchange.export_txt()`
* :py:func:`.exchange.import_csv()`
* :py:func:`.exchange.export_csv()`

The following functions can only work with **single or multiple surfaces**:

* :py:func:`.exchange.export_obj()`
* :py:func:`.exchange.export_stl()`
* :py:func:`.exchange.export_off()`
* :py:func:`.exchange.import_smesh()`
* :py:func:`.exchange.export_smesh()`


The following functions can be used to **import/export complete NURBS shapes**:

* :py:func:`.exchange.import_yaml()`
* :py:func:`.exchange.export_yaml()`
* :py:func:`.exchange.import_cfg()`
* :py:func:`.exchange.export_cfg()`
* :py:func:`.exchange.import_json()`
* :py:func:`.exchange.export_json()`

Function Reference
==================

.. automodule:: geomdl.exchange
    :members:

VTK Support
===========

The following functions export control points and evaluated points as VTK files (in legacy format).

.. automodule:: geomdl.exchange_vtk
    :members:
