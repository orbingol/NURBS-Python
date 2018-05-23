Visualization Modules
^^^^^^^^^^^^^^^^^^^^^

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
