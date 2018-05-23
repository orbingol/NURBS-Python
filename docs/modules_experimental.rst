Experimental Modules
^^^^^^^^^^^^^^^^^^^^

NURBS-Python comes with several optional modules. These modules might require installation of additional packages,
might come with extra requirements or their API might change between NURBS-Python releases. Therefore, even though
they are distributed with the package, due to these reasons they are considered as experimental. However, they are
mature enough to be used in production environments.

Visualization Modules
=====================

NURBS-Python provides an abstract base for visualization modules described under :doc:`Abstract <module_abstract>`
class reference. This abstract base is a part of the :doc:`Core Library <modules>` and it can be used to implement
various visualization backends.

NURBS-Python comes with the following visualization modules:

.. toctree::
    :maxdepth: 1

    module_vis_mpl
    module_vis_plotly

The users are not limited with these visualization backends. For instance, control points and evaluated points can be
exported via :py:func:`.export_csv()` or :py:func:`.export_vtk()` functions to plot with COTS software.

Generating Common Shapes
========================

NURBS-Python provides an experimental module for automatic generation of the most commonly used curves and surfaces.

.. toctree::
    :maxdepth: 2

    module_shapes
