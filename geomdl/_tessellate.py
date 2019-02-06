"""
.. module:: _tessellate
    :platform: Unix, Windows
    :synopsis: Helper functions and algorithms for tessellation operations

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import elements
from . import utilities
from . import ray


# Initialize an empty __all__ for controlling imports
__all__ = []


def is_left(point0, point1, point2):
    """ Tests if a point is Left|On|Right of an infinite line.

    Ported from the C++ version: on http://geomalgorithms.com/a03-_inclusion.html

    :param point0: Point P0
    :param point1: Point P1
    :param point2: Point P2
    :return:
        >0 for P2 left of the line through P0 and P1
        =0 for P2 on the line
        <0 for P2 right of the line
    """
    return ((point1[0] - point0[0]) * (point2[1] - point0[1])) - ((point2[0] - point0[0]) * (point1[1] - point0[1]))


def wn_poly(point, vertices):
    """ Winding number test for a point in a polygon.

    Ported from the C++ version: http://geomalgorithms.com/a03-_inclusion.html

    :param point: point to be tested
    :type point: list, tuple
    :param vertices: vertex points of a polygon vertices[n+1] with vertices[n] = vertices[0]
    :type vertices: list, tuple
    :return: True if the point is inside the input polygon, False otherwise
    :rtype: bool
    """
    wn = 0  # the winding number counter

    v_size = len(vertices) - 1
    # loop through all edges of the polygon
    for i in range(v_size):  # edge from V[i] to V[i+1]
        if vertices[i][1] <= point[1]:  # start y <= P.y
            if vertices[i + 1][1] > point[1]:  # an upward crossing
                if is_left(vertices[i], vertices[i + 1], point) > 0:  # P left of edge
                    wn += 1  # have a valid up intersect
        else:  # start y > P.y (no test needed)
            if vertices[i + 1][1] <= point[1]:  # a downward crossing
                if is_left(vertices[i], vertices[i + 1], point) < 0:  # P right of edge
                    wn -= 1  # have a valid down intersect
    # return wn
    return bool(wn)


def surface_trim_tessellate(v1, v2, v3, v4, vidx, tidx, trims, tessellate_args):
    """ Trimmed surface tessellation algorithm.

    :param v1: vertex 1
    :type v1: Vertex
    :param v2: vertex 2
    :type v2: Vertex
    :param v3: vertex 3
    :type v3: Vertex
    :param v4: vertex 4
    :type v4: Vertex
    :param vidx: vertex numbering start value
    :type vidx: int
    :param tidx: triangle numbering start value
    :type tidx: int
    :param trims: trim curves
    :type trims: list, tuple
    :param tessellate_args: tessellation arguments
    :type tessellate_args: list, tuple
    :return: lists of vertex and triangle objects in (vertex_list, triangle_list) format
    :type: tuple
    """
    # Tolerance value
    tol = 10e-8

    # Check if all vertices are inside the trim, and if so, don't generate a triangle
    vertices = [v1, v2, v3, v4]
    for idx, vertex in enumerate(vertices):
        for trim_curve in trims:
            # Check if the vertex is inside the trimmed region
            is_inside_trim = wn_poly(vertex.uv, trim_curve.evalpts)
            if is_inside_trim:
                vertex.inside = True
    vertices_inside = [v1.inside, v2.inside, v3.inside, v4.inside]
    if all(vertices_inside):
        return [], []

    # # Generate triangles
    # return [], utilities.polygon_triangulate(tidx, v1, v2, v3, v4)

    # Generate edges as rays
    edge1 = ray.Ray(v1.uv, v2.uv)
    edge2 = ray.Ray(v2.uv, v3.uv)
    edge3 = ray.Ray(v3.uv, v4.uv)
    edge4 = ray.Ray(v4.uv, v1.uv)

    # Put all edge rays to a list
    edges = [edge1, edge2, edge3, edge4]

    # List of intersections
    intersections = []

    # Loop all trim curves
    for trim in trims:
        pts = trim.evalpts
        for idx in range(len(pts) - 1):
            # Generate a ray from trim curve's evaluated points
            trim_ray = ray.Ray(pts[idx], pts[idx + 1])

            # Intersection test of the trim curve's ray with all edges
            for idx2 in range(len(edges)):
                t1, t2, status = ray.intersect(edges[idx2], trim_ray)
                if status == ray.RayIntersection.INTERSECT:
                    if 0.0 - tol < t1 < 1.0 + tol and 0.0 - tol < t2 < 1.0 + tol:
                        intersections.append([idx2, t1, edges[idx2].eval(t=t1)])

    # Add first vertex to the end of the list
    vertices.append(v1)

    # Local vertex numbering index
    nvi = 0

    # Process vertices and intersections
    tris_vertices = []
    verts = []
    for idx in range(0, len(vertices) - 1):
        # If two consecutively-ordered vertices are inside the trim, there should be no intersection
        if vertices[idx].inside and vertices[idx + 1].inside:
            continue

        # If current vertex is not inside the trim, add it to the vertex list
        if not vertices[idx].inside:
            tris_vertices.append(vertices[idx])

        # If next vertex is inside the trim, there might be an intersection
        if (not vertices[idx].inside and vertices[idx + 1].inside) or \
                (vertices[idx].inside and not vertices[idx + 1].inside):
            # Try to find all intersections (multiple intersections are possible)
            isects = []
            for isect in intersections:
                if isect[0] == idx:
                    isects.append(isect)

            # Find minimum t value and therefore minimum uv value of the intersection
            t_min = 1.0
            uv_min = ()
            for isect in isects:
                if isect[1] < t_min:
                    t_min = isect[1]
                    uv_min = isect[2]

            # Create a vertex with the minimum uv value
            vert = elements.Vertex()
            vert.id = vidx + nvi
            vert.uv = uv_min

            # Add to lists
            tris_vertices.append(vert)
            verts.append(vert)

            # Increment local vertex numbering index
            nvi += 1

    # Triangulate vertices
    tris = utilities.polygon_triangulate(tidx, *tris_vertices)

    # Check again if the barycentric coordinates of the triangles are inside
    for idx in range(len(tris)):
        tri_center = utilities.triangle_center(tris[idx], uv=True)
        for trim in trims:
            if wn_poly(tri_center, trim.evalpts):
                tris[idx].inside = True

    # Extract triangles which are not inside the trim
    tris_final = []
    for tri in tris:
        if not tri.inside:
            tris_final.append(tri)

    return verts, tris_final
