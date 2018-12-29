Shape Containers
^^^^^^^^^^^^^^^^

This module provides parametric curve, surface and volume containers which could be created

* As a result of a geometric operation, such as **splitting**
* As a result of file import, e.g. reading a file or a set of files containing multiple surfaces
* For advanced post-processing, such as visualization or file export

This module works with ``BSpline`` and ``NURBS`` modules and it contains the following classes:

* :py:class:`.AbstractContainer` abstract base class for all containers
* :py:class:`.CurveContainer` for storing multiple curves
* :py:class:`.SurfaceContainer` for storing multiple surfaces
* :py:class:`.VolumeContainer` for storing multiple volumes

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
