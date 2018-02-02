Package Name
^^^^^^^^^^^^

The package name is :code:`geomdl` which is the shortened version of *geometric modeling*.

Prior to v3.x series of the NURBS-Python library, the package name was :code:`nurbs`. However, using a generic name like
that might seem to cause conflicts with other packages, and therefore in v3.x of the library, it is renamed to
:code:`geomdl`.


Included Modules
^^^^^^^^^^^^^^^^

The NURBS-Python library is more than a simple NURBS library. It includes surface and 2D/3D curve classes which
provide a convenient data structure implemented with Python properties as well as the evaluation, and export/exchange
functionality.

Following modules are included in this library:

.. toctree::
    :maxdepth: 1

    module_bspline
    module_nurbs
    module_utilities
    module_cpgen
    module_exchange

Visualization
=============

NURBS-Python provides an optional-to-use visualization module with a sample implementation that uses
`Matplotlib <https://matplotlib.org/>`_. Please see the documentation of the following modules for details:

.. toctree::
    :maxdepth: 1

    module_vis_base
    module_vis_mpl

Although there exists a visualization component, the users are completely free to use any visualization method
or software. For instance, CSV exporting facility of the curve and surface classes can be used to draw control points,
curves and surfaces using a software, such as Paraview_.

Common Shapes
=============

NURBS-Python also provides a custom module for automatic generation of the most commonly used curves and surfaces.

.. toctree::
    :maxdepth: 2

    module_shapes


.. _Paraview: https://www.paraview.org/
