Package Name
^^^^^^^^^^^^

The package name is :code:`geomdl` which is the shortened version of *geometric modeling*.

Prior to v3.x series of the NURBS-Python library, the package name was :code:`nurbs`. However, using a generic name like
that might seem to cause conflicts with other packages, and therefore in v3.x of the library, it is renamed to :code:`geomdl`.


Included Modules
^^^^^^^^^^^^^^^^

The NURBS-Python library is more than a simple NURBS library. It includes 2D/3D curve and surface classes which contains
a convenient data structure implemented with Python properties and evaluation functionality. Everything is self-contained,
there is no need for loading external modules.

Following modules are included in this library:

.. toctree::
    :maxdepth: 1

    module_bspline
    module_nurbs
    module_utilities
    module_cpgen


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

.. _Paraview: https://www.paraview.org/
