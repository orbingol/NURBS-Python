Tessellation
^^^^^^^^^^^^

The ``tessellate`` module provides tessellation algorithms for surfaces. The following example illustrates the usage
scenario of the tessellation algorithms with surfaces.

.. code-block:: python
    :linenos:

    from geomdl import NURBS
    from geomdl import tessellate

    # Create a surface instance
    surf = NURBS.Surface()

    # Set tessellation algorithm (you can use another algorithm)
    surf.tessellator = tessellate.TriangularTessellate()

    # Tessellate surface
    surf.tessellate()

NURBS-Python uses :py:class:`.TriangularTessellate` class for surface tessellation by default.

Abstract Tessellator
====================

.. autoclass:: geomdl.tessellate.AbstractTessellate
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Triangular Tessellator
======================

.. autoclass:: geomdl.tessellate.TriangularTessellate
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Trim Tessellator
================

.. versionadded:: 5.0

.. autoclass:: geomdl.tessellate.TrimTessellate
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
