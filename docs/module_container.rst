Surface and Curve Containers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This module provides curve and surface containers which could be created

* As a result of a geometric operation, such as **splitting**
* As a result of file import, e.g. reading a file or a set of files containing multiple surfaces
* For advanced post-processing, such as visualization or file export

This module works with ``BSpline`` and ``NURBS`` modules and it contains the following classes:

* :py:class:`.MultiAbstract` abstract base class for all containers
* :py:class:`.MultiCurve` 2D and 3D curve container class
* :py:class:`.MultiSurface` surface container class


.. automodule:: geomdl.Multi
    :members:
    :inherited-members:
    :show-inheritance:
