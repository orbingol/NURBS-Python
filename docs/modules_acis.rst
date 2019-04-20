ACIS Importer
^^^^^^^^^^^^^

The **ACIS importer**, ``rwsat`` uses `3D ACIS Modeler <https://www.spatial.com/>`_
to convert .sat files to geomdl JSON format.

``rwsat`` comes with the following list of programs:

* ``sat2json`` converts ACIS .sat files to geomdl JSON format

Use Cases
=========

* Import geometry data from .sat files and use it with :func:`.exchange.import_json`
* Convert ACIS file format to OBJ, STL, OFF and other formats supported by geomdl

Installation
============

Please refer to the `rwsat repository <https://github.com/orbingol/rwsat>`_ for installation options.

Using with geomdl
=================

The following code snippet illustrates importing the surface data converted from .sat file:

.. code-block:: python
    :linenos:

    from geomdl import exchange
    from geomdl import multi
    from geomdl.visualization import VisMPL as vis

    # Import converted data
    data = exchange.import_json("converted_acis.json")

    # Add the imported data to a surface container
    surf_cont = multi.SurfaceContainer(data)
    surf_cont.sample_size = 30

    # Visualize
    surf_cont.vis = vis.VisSurface(ctrlpts=False, trims=False)
    surf_cont.render()

References
==========

* **Development**: https://github.com/orbingol/rwsat
