Exchange Module
^^^^^^^^^^^^^^^

This module allows users to export NURBS surfaces in common CAD exchange formats. The functions starting with *import_*
are used for generating B-spline and NURBS objects from the input files. The functions starting with *export_* are used
for saving B-spline and NURBS objects as files.

The following commands can only **import/export control points** or **export evaluated points**:

* :py:func:`.exchange.import_txt()`
* :py:func:`.exchange.import_csv()`
* :py:func:`.exchange.export_txt()`
* :py:func:`.exchange.export_csv()`
* :py:func:`.exchange.export_vtk()`

The following commands can only work with **single or multiple surfaces**:

* :py:func:`.exchange.export_obj()`
* :py:func:`.exchange.export_stl()`
* :py:func:`.exchange.export_off()`


The following commands can be used to **import/export complete NURBS shapes**:

* :py:func:`.exchange.import_yaml()`
* :py:func:`.exchange.import_cfg()`
* :py:func:`.exchange.import_json()`
* :py:func:`.exchange.import_smesh()`
* :py:func:`.exchange.export_yaml()`
* :py:func:`.exchange.export_cfg()`
* :py:func:`.exchange.export_json()`
* :py:func:`.exchange.export_smesh()`

Function Reference
==================

.. automodule:: geomdl.exchange
    :members:
    :undoc-members:
