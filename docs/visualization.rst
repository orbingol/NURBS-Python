Visualization
^^^^^^^^^^^^^

NURBS-Python comes with some visualization modules for direct plotting evaluated curves and surfaces. Examples_
repository contains examples on how to use the visualization components with surfaces and curves.

Examples
========

The following examples illustrate the visualization components which come with the NURBS-Python package and
the advanced visualization options using the scripts in the Examples_ repository.

Surfaces
--------

The following figures are generated using the following plotting libraries:

* `Matplotlib v2.2.2 <https://matplotlib.org>`_
* `Plotly v2.5.1 <https://plot.ly/python/>`_

The figures are generated from the scripts shared on the Examples_ repository.

ex_surface01.py
~~~~~~~~~~~~~~~

.. image:: images/ex_surface01_mpl.png
    :alt: Surface example 1 with Matplotlib

-----

.. image:: images/ex_surface01_plotly.png
    :alt: Surface example 1 with Plotly

-----

.. image:: images/ex_surface01_mpl_wf.png
    :alt: Surface example 1 - wireframe model

ex_surface02.py
~~~~~~~~~~~~~~~

.. image:: images/ex_surface02_mpl.png
    :alt: Surface example 2 with Matplotlib

-----

.. image:: images/ex_surface02_plotly.png
    :alt: Surface example 2 with Plotly

ex_surface03.py
~~~~~~~~~~~~~~~

.. image:: images/ex_surface03_mpl.png
    :alt: Surface example 3 with Matplotlib

-----

.. image:: images/ex_surface03_plotly.png
    :alt: Surface example 3 with Plotly

mpl_trisurf_vectors.py
~~~~~~~~~~~~~~~~~~~~~~

The following figure illustrates tangent and normal vectors on ``ex_surface02.py`` example.
The example script can be found in Examples_ repository under the ``visualization`` directory.

.. image:: images/ex_surface02_mpl_vectors.png
    :alt: Surface example 2 with tangent and normal vectors

2D Curves
---------

ex_curve01.py
~~~~~~~~~~~~~

.. image:: images/ex_curve01_vis.png
    :alt: 2D curve example 1

ex_curve02.py
~~~~~~~~~~~~~

.. image:: images/ex_curve02_vis.png
    :alt: 2D curve example 2

ex_curve03.py
~~~~~~~~~~~~~

.. image:: images/ex_curve03_vis.png
    :alt: 2D curve example 3

ex_curve04.py
~~~~~~~~~~~~~

.. image:: images/ex_curve04_vis.png
    :alt: 2D curve example 4


3D Curves
---------

The following examples illustrate the direct output of the visualization component, ``geomdl.visualization`` for 3D
curves.

ex_curve3d01.py
~~~~~~~~~~~~~~~

.. image:: images/ex_curve3d01_vis.png
    :alt: 3D curve example 1

ex_curve3d02.py
~~~~~~~~~~~~~~~

.. image:: images/ex_curve3d02_vis.png
    :alt: 3D curve example 2 with Matplotlib

-----

.. image:: images/ex_curve3d02_plotly.png
    :alt: 3D curve example 2 with Plotly

Advanced Visualization for 2D/3D Curves
---------------------------------------

The following example scripts can be found in Examples_ repository under the ``visualization`` directory.

mpl_curve2d_tangents.py
~~~~~~~~~~~~~~~~~~~~~~~

This example illustrates a more advanced visualization option for plotting the 2D curve tangents alongside with the
control points grid and the evaluated curve.

.. image:: images/ex_curve03_mpl.png
    :alt: 2D curve example 2 with tangent vector quiver plots

mpl_curve3d_tangents.py
~~~~~~~~~~~~~~~~~~~~~~~

This example illustrates a more advanced visualization option for plotting the 3D curve tangents alongside with the
control points grid and the evaluated curve.

.. image:: images/ex_curve3d01_mpl.png
    :alt: 3D curve example 1 with tangent vector quiver plots

mpl_curve3d_vectors.py
~~~~~~~~~~~~~~~~~~~~~~

This example illustrates a visualization option for plotting the 3D curve tangent, normal and binormal vectors
alongside with the control points grid and the evaluated curve.

Please note that binormal vector evaluation method for the curves is added on version *3.0.6*.

.. image:: images/ex_curve3d02_mpl.png
    :alt: 3D curve example 2 with tangent, normal and binormal vector quiver plots


.. _Examples: https://github.com/orbingol/NURBS-Python_Examples
