Experimental Modules
^^^^^^^^^^^^^^^^^^^^

NURBS-Python comes with several optional modules. These modules might require installation of additional packages,
might come with extra requirements or their API might change between NURBS-Python releases. Therefore, even though
they are distributed with the package, due to these reasons they are considered as experimental. However, they are
mature enough to be used in production environments.

Visualization Module
^^^^^^^^^^^^^^^^^^^^

NURBS-Python provides an abstract base for visualization modules described under :doc:`Abstract <module_abstract>`
class reference. This abstract base is a part of the :doc:`Core Library <modules>` and it is considered as mature now.

In addition, NURBS-Python comes with a sample experimental visualization module which implements the core abstract base.
This experimental module uses several features of `Matplotlib <https://matplotlib.org/>`_  as its visualization backend.

.. toctree::
    :maxdepth: 1

    module_vis_mpl

Although there exists a visualization module, the users are completely free to use any visualization method
or visualization software. For instance, CSV exporting facility of the curve and surface classes can be used to plot
control points, curves and surfaces using a software, such as Paraview_.

Generating Common Shapes
^^^^^^^^^^^^^^^^^^^^^^^^

NURBS-Python provides an experimental module for automatic generation of the most commonly used curves and surfaces.

.. toctree::
    :maxdepth: 2

    module_shapes

.. _Paraview: https://www.paraview.org/
