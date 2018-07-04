Evaluators
^^^^^^^^^^

Evaluators (or evaluation strategies) allow users to change curve and/or surface evaluation strategy,
i.e. the algorithms that are used to evaluate the curve & surface, take derivatives and more.
Therefore, the user can switch between the evaluation algorithms at runtime, implement and use different algorithms
or improve existing ones.

Abstract Evaluators
===================

This class provides an abstract base for all evaluator classes.

.. autoclass:: geomdl.Abstract.Evaluator
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

The following classes provide curve and surface customizations for the abstract base.

.. autoclass:: geomdl.Abstract.CurveEvaluator
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. autoclass:: geomdl.Abstract.SurfaceEvaluator
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Included Evaluators
===================

These evaluators are implementations of the above abstract base classes and all are included in the NURBS-Python
package.

.. automodule:: geomdl.evaluators
    :members:
    :undoc-members:
