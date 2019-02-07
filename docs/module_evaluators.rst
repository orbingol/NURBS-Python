Evaluators
^^^^^^^^^^

Evaluators (or geometric evaluation strategies) allow users to change shape evaluation strategy, i.e. the algorithms
that are used to evaluate curves, surfaces and volumes, take derivatives, knot and degree change operations and more.
Therefore, the user can switch between the evaluation algorithms at runtime, implement and use different algorithms
or extend existing ones.

Inheritance Diagram
===================

.. inheritance-diagram:: geomdl.evaluators

Abstract Base
=============

.. autoclass:: geomdl.evaluators.AbstractEvaluator
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Curve Evaluators
================

.. autoclass:: geomdl.evaluators.CurveEvaluator
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. autoclass:: geomdl.evaluators.CurveEvaluator2
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. autoclass:: geomdl.evaluators.CurveEvaluatorRational
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Surface Evaluators
==================

.. autoclass:: geomdl.evaluators.SurfaceEvaluator
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. autoclass:: geomdl.evaluators.SurfaceEvaluator2
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. autoclass:: geomdl.evaluators.SurfaceEvaluatorRational
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Volume Evaluators
=================

.. autoclass:: geomdl.evaluators.VolumeEvaluator
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. autoclass:: geomdl.evaluators.VolumeEvaluatorRational
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
