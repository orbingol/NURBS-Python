Visualization Modules
^^^^^^^^^^^^^^^^^^^^^

NURBS-Python provides an abstract base for visualization modules. It is a part of the :doc:`Core Library <modules>`
and it can be used to implement various visualization backends.

NURBS-Python comes with the following visualization modules:

.. toctree::
    :maxdepth: 1

    module_vis_abstract
    module_vis_mpl
    module_vis_plotly
    module_vis_vtk

The users are not limited with these visualization backends. For instance, control points and evaluated points can be
in various formats. Please refer to the :doc:`Exchange module documentation <module_exchange>` for details.
