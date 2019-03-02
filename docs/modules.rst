Core Modules
^^^^^^^^^^^^

The following modules are included in the core library:

.. toctree::
    :maxdepth: 1

    module_abstract
    module_freeform
    module_bspline
    module_nurbs
    module_evaluators
    module_operations
    module_utilities
    module_knotvector
    module_convert
    module_construct
    module_container
    module_compatibility
    module_fitting
    module_cpgen
    module_exchange
    module_tessellate
    module_voxelize
    module_elements
    module_ray

NURBS-Python takes *The NURBS Book 2nd Edition by Piegl & Tiller* as the main reference for the evaluation algorithms.
The users may want to use different algorithms and **Evaluators** serve directly to this purpose by allowing users
to switch evaluation algorithms (i.e. evaluation strategy) at runtime. Please see ``evaluator`` property documentation
for more details.
