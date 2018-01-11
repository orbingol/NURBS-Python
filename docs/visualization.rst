Visualization
^^^^^^^^^^^^^

Visualization Component
=======================

NURBS-Python v3.x series included an optional visualization module for plotting evaluated curves and surfaces. Examples_
repository contains some examples on how to use the visualization component with surfaces and 2D/3D curves which are

* ``curve2d/ex_curve01.py``
* ``curve2d/ex_curve02.py``
* ``curve2d/ex_curve03.py``
* ``curve3d/ex_curve3d01.py``
* ``surface/ex_surface01.py``

Advanced Visualization Options
==============================

``visualization/`` directory in the Examples_ repository contains customizable scripts for more advanced visualization
using `Matplotlib <https://matplotlib.org>`_.

Examples
========

The following examples illustrate the visualization component which comes with the NURBS-Python package and
the advanced visualization options using the scripts in the Examples_ repository.

Surfaces
--------

The following figures are generated using `Matplotlib v2.1.0 <https://matplotlib.org>`_ from the outputs of the examples
shared in the Examples_ repository. Please see :doc:`File Formats <file_formats>` section on details of CSV exporting
capabilities. Visualization scripts can be found in the Examples_ repository under ``visualization`` directory.

ex_surface01.py
~~~~~~~~~~~~~~~

* Control points CSV export mode: ``wireframe``
* Surface points CSV export mode: ``linear``
* Evaluation delta: 0.05
* Script used: ``mpl_wframe_trisurf.py``

.. image:: images/ex_surface01_mpl.png
    :alt: Surface example 1

ex_surface02.py
~~~~~~~~~~~~~~~

* Control points CSV export mode: ``wireframe``
* Surface points CSV export mode: ``linear``
* Evaluation delta: 0.05
* Script used: ``mpl_wframe_trisurf.py``

.. image:: images/ex_surface02_mpl.png
    :alt: Surface example 2

ex_surface03.py
~~~~~~~~~~~~~~~

* Control points CSV export mode: ``linear``
* Surface points CSV export mode: ``wireframe``
* Evaluation delta: 0.05
* Script used: ``mpl_scatter_wframe.py``

.. image:: images/ex_surface03_mpl.png
    :alt: Surface example 3

Curves
------

The following examples use the visualization component which comes with the NURBS-Python package.

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

ex_curve3d01.py
~~~~~~~~~~~~~~~

.. image:: images/ex_curve3d01_vis.png
    :alt: 3D curve example 1

mpl_curve_tangents.py
~~~~~~~~~~~~~~~~~~~~~

This example illustrates a more advanced visualization option for plotting the curve tangents alongside with the control
points grid and the evaluated curve. The example script can be found in Examples_ repository under ``visualization``
directory.

.. image:: images/ex_curve02_mpl.png
    :alt: 2D curve example 2 with tangent vector quiver plots


.. _Examples: https://github.com/orbingol/NURBS-Python_Examples
