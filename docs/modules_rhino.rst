Rhino Importer/Exporter
^^^^^^^^^^^^^^^^^^^^^^^

The **Rhino importer/exporter** module ``rw3dm`` is a `pybind11 <https://github.com/pybind/pybind11>`_-wrapped Python
package for `OpenNURBS <https://www.rhino3d.com/opennurbs>`_, only focused on reading and writing .3dm files.
:func:`.exchange.import_3dm` function uses ``rw3dm`` module to extract curve and surface data from .3dm files.
Similarly, :func:`.exchange.export_3dm` function uses ``rw3dm`` module to save NURBS data as .3dm files.

Installation
============

Please refer to the `rw3dm repository <https://github.com/orbingol/rw3dm>`_ for installation options.

References
==========

* **Development**: https://github.com/orbingol/rw3dm
