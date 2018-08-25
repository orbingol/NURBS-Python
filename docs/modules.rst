Core Modules
^^^^^^^^^^^^

The NURBS-Python library is more than a simple NURBS library. It includes n-variate surface and curve classes which
provide a convenient data structure implemented with Python properties as well as the evaluation, and export/exchange
functionality.

Following modules are included in this library:

.. toctree::
    :maxdepth: 1

    module_abstract
    module_bspline
    module_nurbs
    module_evaluators
    module_operations
    module_utilities
    module_convert
    module_compatibility
    module_cpgen
    module_container
    module_exchange


NURBS-Python takes *The NURBS Book 2nd Edition by Piegl & Tiller* as the main reference for the evaluation algorithms.
The users may want to use different algorithms and therefore, **Evaluator** module allows users to switch evaluation
algorithms (i.e. evaluation strategy) at runtime.

The **Operations** module contains specialized geometrical operations that can be directly applied to the B-Spline and
NURBS shapes.
