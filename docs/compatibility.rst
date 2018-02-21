Compatibility
^^^^^^^^^^^^^

Most of the time, users experience problems in converting data between different software packages. To aid this problem
a little bit, NURBS-Python provides a ``compatibility`` module. The purpose of ``compatibility`` module is simple:
converting control points sets into NURBS-Python compatible ones.

The following example illustrates the usage of :code:`compatibility` module:

.. code-block:: python

    from geomdl import NURBS
    from geomdl import utilities as utils
    from geomdl import compatibility as compat

    from geomdl.visualization import VisMPL

    #
    # Surface exported from your CAD software
    #

    # Dimensions of the control points grid
    p_size_u = 4
    p_size_v = 3

    # Control points in u-row order
    p_ctrlpts = [[0, 0, 0], [1, 0, 6], [2, 0, 0], [3, 0, 0],
                 [0, 1, 0], [1, 1, 0], [2, 1, 0], [3, 1, -3],
                 [0, 2, -3], [1, 2, 0], [2, 2, 3], [3, 2, 0]]

    # Weights vector
    p_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    # Degrees
    p_degree_u = 3
    p_degree_v = 2


    #
    # Prepare data for import
    #

    # Combine weights vector with the control points list
    t_ctrlptsw = compat.combine_ctrlpts_weights(p_ctrlpts, p_weights)

    # Since NURBS-Python uses v-row order, we need to convert the exported ones
    n_ctrlptsw = compat.change_ctrlpts_row_order(t_ctrlptsw, p_size_u, p_size_v)

    # Since we have no information on knot vectors, let's auto-generate them
    n_knotvector_u = utils.generate_knot_vector(p_degree_u, p_size_u)
    n_knotvector_v = utils.generate_knot_vector(p_degree_v, p_size_v)


    #
    # Import surface to NURBS-Python
    #

    # Create a NURBS surface instance
    surf = NURBS.Surface()

    # Using __call__ method to fill the surface object
    surf(p_degree_u, p_degree_v, p_size_u, p_size_v, n_ctrlptsw, n_knotvector_u, n_knotvector_v)

    # Set evaluation delta
    surf.delta = 0.05

    # Set visualization component
    vis_comp = VisMPL.VisSurfTriangle()
    surf.vis = vis_comp

    # Render the surface
    surf.render()

Please see :doc:`Compatibility Module Documentation <module_compatibility>` for more details on manipulating and
exporting control points.

NURBS-Python has some other options for exporting and importing data. Please see :doc:`File Formats <file_formats>`
page for details.
