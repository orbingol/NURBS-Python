Core Modules
^^^^^^^^^^^^

The NURBS-Python library is more than a simple NURBS library. It includes n-variate surface and curve classes which
provide a convenient data structure implemented with Python properties as well as the evaluation, and export/exchange
functionality.

Following modules are included in the library:

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

Additionally, the following modules provide data structures for several operations contained in the library:

.. toctree::
    :maxdepth: 1

    module_elements

NURBS-Python takes *The NURBS Book 2nd Edition by Piegl & Tiller* as the main reference for the evaluation algorithms.
The users may want to use different algorithms and **Evaluators** serve directly to this purpose by allowing users
to switch evaluation algorithms (i.e. evaluation strategy) at runtime. Please see ``evaluator`` property documentation
for more details.

The **Operations** module contains specialized geometrical operations that can be directly applied to the B-Spline and
NURBS shapes.
