Rhino Importer/Exporter
^^^^^^^^^^^^^^^^^^^^^^^

The **Rhino importer/exporter**, ``rw3dm`` uses `OpenNURBS <https://www.rhino3d.com/opennurbs>`_
to read and write .3dm files.

``rw3dm`` comes with the following list of programs:

* ``on2json`` converts OpenNURBS .3dm files to geomdl JSON format
* ``json2on`` converts geomdl JSON format to OpenNURBS .3dm files

Use Cases
=========

* Import geometry data from .3dm files and use it with :func:`.exchange.import_json`
* Export geometry data with :func:`.exchange.export_json` and convert to a .3dm file
* Convert OpenNURBS file format to OBJ, STL, OFF and other formats supported by geomdl

Installation
============

Please refer to the `rw3dm repository <https://github.com/orbingol/rw3dm>`_ for installation options.
The binary files can be downloaded under `Releases <https://github.com/orbingol/rw3dm/releases>`_
section of the GitHub repository.

Using with geomdl
=================

The following code snippet illustrates importing the surface data converted from .3dm file:

.. code-block:: python
    :linenos:

    from geomdl import exchange
    from geomdl import multi
    from geomdl.visualization import VisMPL as vis

    # Import converted data
    data = exchange.import_json("converted_rhino.json")

    # Add the imported data to a surface container
    surf_cont = multi.SurfaceContainer(data)
    surf_cont.sample_size = 30

    # Visualize
    surf_cont.vis = vis.VisSurface(ctrlpts=False, trims=False)
    surf_cont.render()

References
==========

* **Development**: https://github.com/orbingol/rw3dm
* **Downloads**: https://github.com/orbingol/rw3dm/releases
