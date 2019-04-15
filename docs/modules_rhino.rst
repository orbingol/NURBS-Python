Rhino Importer/Exporter
^^^^^^^^^^^^^^^^^^^^^^^

The **Rhino importer/exporter**, ``rw3dm`` uses `OpenNURBS <https://www.rhino3d.com/opennurbs>`_
to read and write .3dm files. It comes with 2 separate convenient binaries:

* ``on2json``, converts OpenNURBS .3dm files to geomdl JSON format
* ``json2on``, converts geomdl JSON format to OpenNURBS .3dm files

Use Cases
=========

* Import geometry data from .3dm files and use it with :func:`.exchange.import_json`
* Export geometry data with :func:`.exchange.export_json` and convert to a .3dm file
* Convert OpenNURBS file format (.3dm) to OBJ, STL, OFF and other formats supported by geomdl

Installation
============

Please refer to the `rw3dm repository <https://github.com/orbingol/rw3dm>`_ for installation options.

References
==========

* **Development**: https://github.com/orbingol/rw3dm
* **Downloads**: https://github.com/orbingol/rw3dm/releases
