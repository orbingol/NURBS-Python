Evaluators
^^^^^^^^^^

Evaluators (or geometric evaluation strategies) allow users to change shape evaluation strategy, i.e. the algorithms
that are used to evaluate curves, surfaces and volumes, take derivatives and more.
Therefore, the user can switch between the evaluation algorithms at runtime, implement and use different algorithms
or extend existing ones.

How to Use
==========

All geometry classes come with a default specialized ``evaluator`` class, the algorithms are generally different for
rational and non-rational geometries. The evaluator class instance can be accessed and/or updated using ``evaluator``
property. For instance, the following code snippet changes the evaluator of a B-Spline curve.

.. code-block:: python

    from geomdl import BSpline
    from geomdl import evaluators

    crv = BSpline.Curve()
    cevaltr = evaluators.CurveEvaluator2()
    crv.evaluator = cevaltr

    # Curve "evaluate" method will use CurveEvaluator2.evaluate() method
    crv.evaluate()

    # Get evaluated points
    curve_points = crv.evalpts

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
