Shape Containers
^^^^^^^^^^^^^^^^

This module provides object containers for curves, surfaces and volumes. A container is a holder object that stores a
collection of other objects, i.e. its elements. In NURBS-Python, containers can be generated as a result of

* A geometric operation, such as **splitting**
* File import, e.g. reading a file or a set of files containing multiple surfaces

Additionally, they can be used for advanced post-processing, such as visualization or file export.

This module works with ``BSpline`` and ``NURBS`` modules and it contains the following classes:

* :py:class:`.AbstractContainer` abstract base class for containers
* :py:class:`.CurveContainer` for storing multiple curves
* :py:class:`.SurfaceContainer` for storing multiple surfaces
* :py:class:`.VolumeContainer` for storing multiple volumes

Inheritance Diagram
===================

.. inheritance-diagram:: geomdl.multi

Abstract Container
==================

.. autoclass:: geomdl.multi.AbstractContainer
    :members:
    :inherited-members:
    :show-inheritance:

Curve Container
===============

.. autoclass:: geomdl.multi.CurveContainer
    :members:
    :inherited-members:
    :show-inheritance:

Surface Container
=================

.. autoclass:: geomdl.multi.SurfaceContainer
    :members:
    :inherited-members:
    :show-inheritance:

Volume Container
=================

.. autoclass:: geomdl.multi.VolumeContainer
    :members:
    :inherited-members:
    :show-inheritance:
