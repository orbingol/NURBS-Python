Core Modules
^^^^^^^^^^^^

The NURBS-Python library is more than a simple NURBS library. It includes surface and 2D/3D curve classes which
provide a convenient data structure implemented with Python properties as well as the evaluation, and export/exchange
functionality.

Following modules are included in this library:

.. toctree::
    :maxdepth: 1

    module_abstract
    module_bspline
    module_nurbs
    module_utilities
    module_cpgen
    module_container
    module_exchange

Visualization Module
^^^^^^^^^^^^^^^^^^^^

NURBS-Python provides an abstract base for visualization described under :doc:`Abstract <module_abstract>` class
reference. In addition, NURBS-Python comes with a sample module that uses `Matplotlib <https://matplotlib.org/>`_.

.. toctree::
    :maxdepth: 1

    module_vis_mpl

Although there exists a visualization module, the users are completely free to use any visualization method
or visualization software. For instance, CSV exporting facility of the curve and surface classes can be used to plot
control points, curves and surfaces using a software, such as Paraview_.

Generating Common Shapes
^^^^^^^^^^^^^^^^^^^^^^^^

NURBS-Python also provides a custom module for automatic generation of the most commonly used curves and surfaces.

.. toctree::
    :maxdepth: 2

    module_shapes

.. _Paraview: https://www.paraview.org/
