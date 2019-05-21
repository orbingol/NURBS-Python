"""
.. module:: trimming
    :platform: Unix, Windows
    :synopsis: Provides helper functions for surface trimming

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import math
from . import linalg
from . import shortcuts
from .exceptions import GeomdlException
from ._utilities import export


@export
def map_trim_to_geometry(obj, trim_idx=-1, **kwargs):
    """ Generates 3-dimensional mapping of 2-dimensional trimming curves.

    **Description:**

    Trimming curves are defined on the parametric space of the surfaces. Therefore,
    all trimming curves are 2-dimensional. The coordinates of the trimming curves
    correspond to (u, v) parameters of the underlying surface geometry. When these
    (u, v) values are evaluated with respect to the underlying surface geometry,
    a 3-dimensional representation of the trimming curves is generated.

    The resultant 3-dimensional curve is described using :class:`.freeform.Freeform`
    class. Using the ``fitting`` module, it is possible to generate the B-spline
    form of the freeform curve.

    **Remarks:**

    If `trim_idx=-1`, the function maps all 2-dimensional trims to their 3-dimensional
    correspondants.

    :param obj: spline geometry
    :type obj: abstract.SplineGeometry
    :param trim_idx: index of the trimming curve in the geometry object
    :type trim_idx: int
    :return: 3-dimensional mapping of trimming curve(s)
    :rtype: freeform.Freeform
    """
    if obj.pdimension < 2:
        raise GeomdlException("Input geometry should be defined on, at least, 2-dimensional parametric space")

    # Get keyword arguments
    delta = kwargs.get('delta', -1.0)

    # Initialize return list
    ret = []

    # Process trims
    if trim_idx < 0:
        # Process all trims
        for trim in obj.trims:
            # Set delta
            if delta > 0:
                trim.delta = delta

            # Evaluate trim
            epts = obj.evaluate_list(trim.evalpts)
            fcurve = shortcuts.generate_freeform()
            fcurve.evaluate(points=epts)
            ret.append(fcurve)
    else:
        # Process a single trim
        try:
            trim = obj.trims[trim_idx]
        except KeyError:
            raise GeomdlException("Trim curve at index " + str(trim_idx) + " does not exist")

        # Set delta
        if delta > 0:
            trim.delta = delta

        # Evaluate trim
        epts = obj.evaluate_list(trim.evalpts)
        fcurve = shortcuts.generate_freeform()
        fcurve.evaluate(points=epts)
        ret.append(fcurve)

    # Return curves
    return ret


@export
def fix_multi_trim_curves(obj, **kwargs):
    """ Fixes direction, connectivity and similar issues of the trim curves.

    This function works for surface trims in curve containers, i.e. trims
    consisting of multiple curves.

    Keyword Arguments:
        * ``tol``: tolerance value for comparing floats. *Default: 10e-8*
        * ``delta``: evaluation delta of the trim curves. *Default: 0.05*

    :param obj: input surface
    :type obj: abstract.BSplineGeometry, multi.AbstractContainer
    :return: updated surface
    """
    if obj.pdimension != 2:
        raise GeomdlException("Can only work with surfaces")

    # Get keyword arguments
    tol = kwargs.get('tol', 10e-8)
    eval_delta = kwargs.get('delta', 0.05)

    # Loop through the surfaces
    for o in obj:
        # Get the trims
        trims = o.trims

        # Initialize a list for the connected trims
        new_trims = []

        # Traverse through the trims
        for trim in trims:
            trim_size = len(trim)

            # Directly add to the new trims array if the trim is a single curve
            if trim_size == 1:
                new_trims.append(trim)
                continue

            new_trim = []
            for idx in range(0, trim_size):
                # Close the loop
                if idx == trim_size - 1:
                    idx2 = 0
                else:
                    idx2 = idx + 1

                ###
                # Assuming that we have two curves with starting and ending positions defined as P1-P2 and P3-P4,
                # respectively. There are 5 possibilities:
                # 1. P2 = P3 (end of 1st and start of 2nd)
                # 2. P2 = P4 (end of 1st and end of 2nd)
                # 3. P1 = P3 (start of 1st and start of 2nd)
                # 4. P1 = P4 (start of 1st and end of 2nd)
                # 5. the ends of the curves are far away from each other
                ###

                # End of 1st curve vs start of 2nd curve
                if abs(trim[idx].evalpts[-1][0] - trim[idx2].evalpts[0][0]) <= tol and \
                        abs(trim[idx].evalpts[-1][1] - trim[idx2].evalpts[0][1]) <= tol:
                    # They are in the same direction
                    new_trim.append(trim[idx])
                # End of 1st curve vs end of 2nd curve
                elif abs(trim[idx].evalpts[-1][0] - trim[idx2].evalpts[-1][0]) <= tol and \
                        abs(trim[idx].evalpts[-1][1] - trim[idx2].evalpts[-1][1]) <= tol:
                    # Reverse the second curve inplace
                    trim[idx2].reverse()
                    new_trim.append(trim[idx])
                # Start of 1st curve and start of 2nd curve
                elif abs(trim[idx].evalpts[0][0] - trim[idx2].evalpts[0][0]) <= tol and \
                        abs(trim[idx].evalpts[0][1] - trim[idx2].evalpts[0][1]) <= tol:
                    # Reverse the first curve inplace
                    trim[idx].reverse()
                    new_trim.append(trim[idx])
                # Start of 1st curve and end of 2nd curve
                elif abs(trim[idx].evalpts[0][0] - trim[idx2].evalpts[-1][0]) <= tol and \
                        abs(trim[idx].evalpts[0][1] - trim[idx2].evalpts[-1][1]) <= tol:
                    # Reverse both curves inplace
                    trim[idx].reverse()
                    trim[idx2].reverse()
                    new_trim.append(trim[idx])
                # The trim curves are far away from each other
                else:
                    # Find which end is closer to the current trim curve's end point
                    dist1 = linalg.point_distance(trim[idx].evalpts[-1], trim[idx2].evalpts[0])
                    dist2 = linalg.point_distance(trim[idx].evalpts[-1], trim[idx2].evalpts[-1])

                    # Find start and end points of the connector curve
                    start_pt = trim[idx].evalpts[-1]
                    if dist1 < dist2:
                        end_pt = trim[idx2].evalpts[0]
                    else:
                        end_pt = trim[idx2].evalpts[-1]

                    # Generate the connector curve
                    crv = shortcuts.generate_curve()
                    crv.degree = 1
                    crv.ctrlpts = [start_pt, end_pt]
                    crv.knotvector = [0, 0, 1, 1]
                    crv.opt = ['reversed', trim[idx].opt_get('reversed')]

                    # Add trims
                    new_trim.append(trim[idx])
                    new_trim.append(crv)

            # Create a curve container from the new trim list
            cc = shortcuts.generate_container_curve()
            cc.add(new_trim)
            cc.opt = ['reversed', trim.opt_get('reversed')]
            cc.delta = eval_delta

            # Add curve container to the new trims list
            new_trims.append(cc)

        # Update input geometry
        o.trims = new_trims

    return obj


@export
def fix_trim_curves(obj):
    """ Fixes direction, connectivity and similar issues of the trim curves.

    This function works for surface trim curves consisting of a single curve.

    :param obj: input surface
    :type obj: abstract.Surface
    """
    # Validate input
    if obj.pdimension != 2:
        raise GeomdlException("Input geometry must be a surface")

    # Get trims of the surface
    for o in obj:
        trims = o.trims
        if not trims:
            continue

        # Get parameter space bounding box
        parbox = get_par_box(o.domain, True)

        # Check and update trim curves with respect to the underlying surface
        updated_trims = []
        for trim in trims:
            flag, trm = check_trim_curve(trim, parbox)
            if flag:
                if trm:
                    cont = shortcuts.generate_container_curve()
                    cont.add(trm)
                    updated_trims.append(cont)
                else:
                    updated_trims.append(trim)

        # Set updated trims
        obj.trims = updated_trims


def check_trim_curve(curve, parbox, **kwargs):
    """ Checks if the trim curve was closed and sense was set.

    :param curve: trim curve
    :param parbox: parameter space bounding box of the underlying surface
    :return: a tuple containing the status of the operation and list of extra trim curves generated
    :rtype: tuple
    """
    def next_idx(edge_idx, direction):
        tmp = edge_idx + direction
        if tmp < 0:
            return 3
        if tmp > 3:
            return 0
        return tmp

    # Keyword arguments
    tol = kwargs.get('tol', 10e-8)

    # First, check if the curve is closed
    dist = linalg.point_distance(curve.evalpts[0], curve.evalpts[-1])
    if dist <= tol:
        # Curve is closed
        return detect_sense(curve, tol), []
    else:
        # Define start and end points of the trim curve
        pt_start = curve.evalpts[0]
        pt_end = curve.evalpts[-1]

        # Search for intersections
        idx_spt = -1
        idx_ept = -1
        for idx in range(len(parbox) - 1):
            if detect_intersection(parbox[idx], parbox[idx + 1], pt_start, tol):
                idx_spt = idx
            if detect_intersection(parbox[idx], parbox[idx + 1], pt_end, tol):
                idx_ept = idx

        # Check result of the intersection
        if idx_spt < 0 or idx_ept < 0:
            # Curve does not intersect any edges of the parametric space
            # TODO: Extrapolate the curve using the tangent vector and find intersections
            return False, []
        else:
            # Get sense of the original curve
            c_sense = curve.opt_get('reversed')

            # If sense is None, then detect sense
            if c_sense is None:
                # Get evaluated points
                pts = curve.evalpts
                num_pts = len(pts)

                # Find sense
                tmp_sense = 0
                for pti in range(1, num_pts - 1):
                    tmp_sense = detect_ccw(pts[pti - 1], pts[pti], pts[pti + 1], tol)
                    if tmp_sense != 0:
                        break
                if tmp_sense == 0:
                    tmp_sense2 = detect_ccw(pts[int(num_pts/3)], pts[int(2*num_pts/3)], pts[-int(num_pts/3)], tol)
                    if tmp_sense2 != 0:
                        tmp_sense = -tmp_sense2
                    else:
                        # We cannot decide which region to trim. Therefore, ignore this curve.
                        return False, []

                c_sense = 0 if tmp_sense > 0 else 1

                # Update sense of the original curve
                curve.opt = ['reversed', c_sense]

            # Generate a curve container and add the original curve
            cont = [curve]

            move_dir = -1 if c_sense == 0 else 1

            # Curve intersects with the edges of the parametric space
            counter = 0
            while counter < 4:
                if idx_ept == idx_spt:
                    counter = 5
                    pt_start = curve.evalpts[0]
                else:
                    # Find next index
                    idx_ept = next_idx(idx_ept, move_dir)
                    # Update tracked last point
                    pt_start = parbox[idx_ept + 1 - c_sense]
                    # Increment counter
                    counter += 1

                # Generate the curve segment
                crv = shortcuts.generate_curve()
                crv.degree = 1
                crv.ctrlpts = [pt_end, pt_start]
                crv.knotvector = [0, 0, 1, 1]
                crv.opt = ['reversed', c_sense]

                pt_end = pt_start

                # Add it to the container
                cont.append(crv)

            # Update curve
            return True, cont


def get_par_box(domain, last=False):
    """ Returns the bounding box of the surface parametric domain in ccw direction.

    :param domain: parametric domain
    :type domain: list, tuple
    :param last: if True, adds the first vertex to the end of the return list
    :type last: bool
    :return: edges of the parametric domain
    :rtype: tuple
    """
    u_range = domain[0]
    v_range = domain[1]
    verts = [(u_range[0], v_range[0]), (u_range[1], v_range[0]), (u_range[1], v_range[1]), (u_range[0], v_range[1])]
    if last:
        verts.append(verts[0])
    return tuple(verts)


def detect_sense(curve, tol):
    """ Detects the sense, i.e. clockwise or counter-clockwise, of the curve.

    :param curve: 2-dimensional trim curve
    :type curve: abstract.Curve
    :param tol: tolerance value
    :type tol: float
    :return: True if detection is successful, False otherwise
    :rtype: bool
    """
    if curve.opt_get('reversed') is None:
        # Detect sense since it is unset
        pts = curve.evalpts
        num_pts = len(pts)
        for idx in range(1, num_pts - 1):
            sense = detect_ccw(pts[idx - 1], pts[idx], pts[idx + 1], tol)
            if sense < 0:  # cw
                curve.opt = ['reversed', 0]
                return True
            elif sense > 0:  # ccw
                curve.opt = ['reversed', 1]
                return True
            else:
                continue
        # One final test with random points to determine the orientation
        sense = detect_ccw(pts[int(num_pts/3)], pts[int(2*num_pts/3)], pts[-int(num_pts/3)], tol)
        if sense < 0:  # cw
            curve.opt = ['reversed', 0]
            return True
        elif sense > 0:  # ccw
            curve.opt = ['reversed', 1]
            return True
        else:
            # Cannot determine the sense
            return False
    else:
        # Don't touch the sense value as it has been already set
        return True


def detect_ccw(pt1, pt2, pt3, tol):
    vec1 = linalg.vector_generate(pt1, pt2)
    vec2 = linalg.vector_generate(pt2, pt3)
    cross = linalg.vector_cross(vec1, vec2)
    if cross[2] > tol:  # cw
        return -1
    elif cross[2] < -tol:  # ccw
        return 1
    return 0


def detect_intersection(start_pt, end_pt, test_pt, tol):
    dist_num = abs(((end_pt[1] - start_pt[1]) * test_pt[0]) - ((end_pt[0] - start_pt[0]) * test_pt[1]) +
                   (end_pt[0] * start_pt[1]) - (end_pt[1] * start_pt[0]))
    dist_denom = math.sqrt(math.pow(end_pt[1] - start_pt[1], 2) + math.pow(end_pt[0] - start_pt[0], 2))
    dist = dist_num / dist_denom
    if abs(dist) < tol:
        return True
    return False
