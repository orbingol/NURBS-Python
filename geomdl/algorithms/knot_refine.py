"""
.. module:: algorithms.knot_refine
    :platform: Unix, Windows
    :synopsis: Knot vector refinement algorithms

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .. import helpers
from ..base import GeomdlError, GeomdlTypeSequence

__all__ = []


def refine_knotvector(obj, param, **kwargs):
    """ Refines the knot vector(s) of a spline geometry.

    The following code snippet illustrates the usage of this function:

    .. code-block:: python

        # Refines the knot vector of a curve
        operations.refine_knotvector(curve, [1])

        # Refines the knot vector on the v-direction of a surface
        operations.refine_knotvector(surface, [0, 1])

        # Refines the both knot vectors of a surface
        operations.refine_knotvector(surface, [1, 1])

        # Refines the knot vector on the w-direction of a volume
        operations.refine_knotvector(volume, [0, 0, 1])

    The values of ``param`` argument can be used to set the *knot refinement density*. If *density* is bigger than 1,
    then the algorithm finds the middle knots in each internal knot span to increase the number of knots to be refined.

    **Example**: Let the degree is 2 and the knot vector to be refined is ``[0, 2, 4]`` with the superfluous knots
    from the start and end are removed. Knot vectors with the changing ``density (d)`` value will be:

    * ``d = 1``, knot vector ``[0, 1, 1, 2, 2, 3, 3, 4]``
    * ``d = 2``, knot vector ``[0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2, 2, 2.5, 2.5, 3, 3, 3.5, 3.5, 4]``

    The following code snippet illustrates the usage of knot refinement densities:

    .. code-block:: python

        # Refines the knot vector of a curve with density = 3
        operations.refine_knotvector(curve, [3])

        # Refines the knot vectors of a surface with density for
        # u-dir = 2 and v-dir = 3
        operations.refine_knotvector(surface, [2, 3])

        # Refines only the knot vector on the v-direction of a surface with density = 1
        operations.refine_knotvector(surface, [0, 1])

        # Refines the knot vectors of a volume with density for
        # u-dir = 1, v-dir = 3 and w-dir = 2
        operations.refine_knotvector(volume, [1, 3, 2])

    Please refer to :func:`.helpers.knot_refinement` function for more usage options.

    Keyword Arguments:
        * ``check_num``: enables/disables operation validity checks. *Default: True*

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param param: parametric dimensions to be refined in [u, v, w] format
    :type param: list, tuple
    :return: updated spline geometry
    """
    # Get keyword arguments
    check_num = kwargs.get('check_num', True)  # enables/disables input validity checks

    if check_num:
        if not isinstance(param, GeomdlTypeSequence):
            raise GeomdlError("Parametric dimensions argument (param) must be a list or a tuple")

        if len(param) != obj.pdimension:
            raise GeomdlError("The length of the param array must be equal to the number of parametric dimensions",
                              data=dict(pdim=obj.pdimension, param_len=len(param)))

    # Start curve knot refinement
    if obj.pdimension == 1:
        if param[0] > 0:
            cpts = obj.ctrlptsw
            new_cpts, new_kv = helpers.knot_refinement(obj.degree.u, obj.knotvector.u, cpts, density=param[0])

            # Update the curve
            obj.set_ctrlpts(new_cpts)
            obj.knotvector.u = new_kv

    # Start surface knot refinement
    if obj.pdimension == 2:
        # u-direction
        if param[0] > 0:
            # Get curves
            new_cpts = []
            new_cpts_size = 0
            new_kv = []
            cpts = obj.ctrlptsw
            for v in range(obj.ctrlpts_size.v):
                ccu = [cpts[u, v] for u in range(obj.ctrlpts_size.u)]
                ptmp, new_kv = helpers.knot_refinement(obj.degree.u, obj.knotvector.u, ccu, density=param[0])
                new_cpts_size = len(ptmp)
                new_cpts += ptmp

            # Update the surface
            obj.set_ctrlpts(new_cpts, new_cpts_size, obj.ctrlpts_size.v)
            obj.knotvector.u = new_kv

        # v-direction
        if param[1] > 0:
            # Get curves
            new_cpts = []
            new_cpts_size = 0
            new_kv = []
            cpts = obj.ctrlptsw
            for u in range(obj.ctrlpts_size.u):
                ccv = [cpts[u, v] for v in range(obj.ctrlpts_size.v)]
                ptmp, new_kv = helpers.knot_refinement(obj.degree.v, obj.knotvector.v, ccv, density=param[1])
                new_cpts_size = len(ptmp)
                new_cpts += ptmp

            # Update control points
            ctrlpts_new = []
            for v in range(new_cpts_size):
                for u in range(obj.ctrlpts_size.u):
                    ctrlpts_new.append(new_cpts[v + (u * new_cpts_size)])

            # Update the surface
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size.u, new_cpts_size)
            obj.knotvector.v = new_kv

    # Start volume knot refinement
    if obj.pdimension == 3:
        # u-direction
        if param[0] > 0:
            # Use Pw
            cpts = obj.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(obj.ctrlpts_size.u):
                temp_surf = []
                for v in range(obj.ctrlpts_size.v):
                    for w in range(obj.ctrlpts_size.w):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(obj.degree.u, obj.knotvector.u, cpt2d, density=param[0])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size.w):
                for v in range(obj.ctrlpts_size.v):
                    for u in range(new_cpts_size):
                        ctrlpts_new.append(ctrlpts_tmp[u][w + (v * obj.ctrlpts_size.w)])

            # Update the volume
            obj.set_ctrlpts(ctrlpts_new, new_cpts_size, obj.ctrlpts_size.v, obj.ctrlpts_size.w)
            obj.knotvector.u = kv_new

        # v-direction
        if param[1] > 0:
            # Use Pw if rational
            cpts = obj.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(obj.ctrlpts_size.v):
                temp_surf = []
                for u in range(obj.ctrlpts_size.u):
                    for w in range(obj.ctrlpts_size.w):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(obj.degree.v, obj.knotvector.v, cpt2d, density=param[1])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size.w):
                for v in range(new_cpts_size):
                    for u in range(obj.ctrlpts_size.u):
                        ctrlpts_new.append(ctrlpts_tmp[v][w + (u * obj.ctrlpts_size.w)])

            # Update the volume
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size.u, new_cpts_size, obj.ctrlpts_size.w)
            obj.knotvector.v = kv_new

        # w-direction
        if param[2] > 0:
            # Use Pw if rational
            cpts = obj.ctrlptsw

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(obj.ctrlpts_size.w):
                temp_surf = []
                for v in range(obj.ctrlpts_size.v):
                    for u in range(obj.ctrlpts_size.u):
                        temp_surf.append(cpts[u, v, w])
                cpt2d.append(temp_surf)

            # Apply knot refinement
            ctrlpts_tmp, kv_new = helpers.knot_refinement(obj.degree.w, obj.knotvector.w, cpt2d, density=param[2])
            new_cpts_size = len(ctrlpts_tmp)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(new_cpts_size):
                for v in range(obj.ctrlpts_size.v):
                    for u in range(obj.ctrlpts_size.u):
                        ctrlpts_new.append(ctrlpts_tmp[w][u + (v * obj.ctrlpts_size.u)])

            # Update the volume
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size.u, obj.ctrlpts_size.v, new_cpts_size)
            obj.knotvector.w = kv_new

    # Return updated geometry
    return obj
