Examples Repository
^^^^^^^^^^^^^^^^^^^

Although using NURBS-Python is straight-forward, it is always confusing to do the initial start with a new library.
To give you a headstart on working with NURBS-Python, an Examples_ repository over 50 example scripts which describe
usage scenarios of the library and its modules is provided. You can run the scripts from the command line, inside from
favorite IDE or copy them to a Jupyter notebook.

The Examples_ repository contains examples on

* Bézier curves and surfaces
* B-Spline & NURBS curves, surfaces and volumes
* Spline algorithms, e.g. knot insertion and removal, degree elevation and reduction
* Curve & surface splitting and Bézier decomposition (:doc:`info <visualization_splitting>`)
* Surface and curve fitting using interpolation and least squares approximation (:doc:`docs <module_fitting>`)
* Geometrical operations, e.g. tangent, normal, binormal (:doc:`docs <module_operations>`)
* Importing & exporting spline geometries into supported formats (:doc:`docs <module_exchange>`)
* Compatibility module for control points conversion (:doc:`docs <module_compatibility>`)
* Surface grid generators (:doc:`info <surface_generator>` and :doc:`docs <module_cpgen>`)
* Geometry containers (:doc:`docs <module_container>`)
* Automatic uniform knot vector generation via :py:func:`.knotvector.generate`
* Visualization components (:doc:`info <visualization>`, :doc:`Matplotlib <module_vis_mpl>`, :doc:`Plotly <module_vis_plotly>` and :doc:`VTK <module_vis_vtk>`)
* Ray operations (:doc:`docs <module_ray>`)
* Voxelization (:doc:`docs <module_voxelize>`)

Matplotlib and Plotly visualization modules are compatible with Jupyter notebooks but VTK visualization module is not.
Please refer to the `NURBS-Python wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-the-library-with-Jupyter-notebooks>`_
for more details on using NURBS-Python Matplotlib and Plotly visualization modules with Jupyter notebooks.


.. _Examples: https://github.com/orbingol/geomdl-examples
