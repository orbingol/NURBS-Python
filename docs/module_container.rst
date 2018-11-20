Surface and Curve Containers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This module provides curve and surface containers which could be created

* As a result of a geometric operation, such as **splitting**
* As a result of file import, e.g. reading a file or a set of files containing multiple surfaces
* For advanced post-processing, such as visualization or file export

This module works with ``BSpline`` and ``NURBS`` modules and it contains the following classes:

* :py:class:`.Multi` abstract base class for all containers
* :py:class:`.MultiCurve` curve container class
* :py:class:`.MultiSurface` surface container class


Abstract Container
==================

.. autoclass:: geomdl.Multi.AbstractMulti
    :members:
    :inherited-members:
    :show-inheritance:

Curve Container
===============

.. automodule:: geomdl.Multi.MultiCurve
    :members:
    :inherited-members:
    :show-inheritance:

Surface Container
=================

.. automodule:: geomdl.Multi.MultiSurface
    :members:
    :inherited-members:
    :show-inheritance:
