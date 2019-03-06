"""
.. module:: _tessellate
    :platform: Unix, Windows
    :synopsis: Helper functions and algorithms for tessellation operations

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import elements
from . import utilities
from . import ray
from .elements import Vertex, Triangle


# Initialize an empty __all__ for controlling imports
__all__ = []


def make_triangle_mesh(points, size_u, size_v, **kwargs):
    """ Generates a triangular mesh from an array of points.

    This function generates a triangular mesh for a NURBS or B-Spline surface on its parametric space.
    The input is the surface points and the number of points on the parametric dimensions u and v,
    indicated as row and column sizes in the function signature. This function should operate correctly if row and
    column sizes are input correctly, no matter what the points are v-ordered or u-ordered. Please see the
    documentation of ``ctrlpts`` and ``ctrlpts2d`` properties of the Surface class for more details on
    point ordering for the surfaces.

    This function accepts the following keyword arguments:

    * ``vertex_spacing``: Defines the size of the triangles via setting the jump value between points
    * ``trims``: List of trim curves passed to the tessellation function
    * ``tessellate_func``: Function called for tessellation (default is ``triangular_tessellation``)
    * ``tessellate_args``: Arguments passed to the tessellation function (as a dict)

    The tessellation function is designed to generate triangles from 4 vertices. It takes 4 :py:class:`.Vertex` objects,
    index values for setting the triangle and vertex IDs and additional parameters as its function arguments.
    It returns a tuple of :py:class:`.Vertex` and :py:class:`.Triangle` object lists generated from the input vertices.
    A default triangle generator is provided as a prototype for implementation in the source code.

    The return value of this function is a tuple containing two lists. First one is the list of vertices and the second
    one is the list of triangles.

    :param points: input points
    :type points: list, tuple
    :param size_u: number of elements on the u-direction
    :type size_u: int
    :param size_v: number of elements on the v-direction
    :type size_v: int
    :return: a tuple containing lists of vertices and triangles
    :rtype: tuple
    """
    def triangular_tessellation(v1, v2, v3, v4, vidx, tidx, trim_curves, tessellate_args):
        """ Default tessellation algorithm (triangular tessellation).

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
        :param trim_curves: trim curves
        :type: list, tuple
        :param tessellate_args: tessellation arguments
        :type tessellate_args: dict
        :return: lists of vertex and triangle objects in (vertex_list, triangle_list) format
        :type: tuple
        """
        # Triangulate vertices
        tris = polygon_triangulate(tidx, v1, v2, v3, v4)

        # Return vertex and triangle lists
        return [], tris

    def fix_numbering(vertex_list, triangle_list):
        # Initialize variables
        final_vertices = []

        # Get all vertices inside the triangle list
        tri_vertex_ids = []
        for tri in triangle_list:
            tri_vertex_ids += tri.vertex_ids

        # Find vertices used in triangles
        for vertex in vertex_list:
            if vertex.id in tri_vertex_ids:
                final_vertices.append(vertex)

        # Fix vertex numbering (automatically fixes triangle vertex numbering)
        vert_new_id = 1
        for vertex in final_vertices:
            vertex.id = vert_new_id
            vert_new_id += 1

        return final_vertices, triangle_list

    # Vertex spacing for triangulation
    vertex_spacing = kwargs.get('vertex_spacing', 1)  # defines the size of the triangles
    trim_curves = kwargs.get('trims', [])

    # Tessellation algorithm
    tsl_func = kwargs.get('tessellate_func')
    if tsl_func is None:
        tsl_func = triangular_tessellation
    tsl_args = kwargs.get('tessellate_args', dict())

    # Variable initialization
    vrt_idx = 1  # vertex index numbering start
    tri_idx = 1  # triangle index numbering start
    u_jump = (1.0 / float(size_u - 1)) * vertex_spacing  # for computing vertex parametric u value
    v_jump = (1.0 / float(size_v - 1)) * vertex_spacing  # for computing vertex parametric v value
    varr_size_u = int(round((float(size_u) / float(vertex_spacing)) + 10e-8))  # vertex array size on the u-direction
    varr_size_v = int(round((float(size_v) / float(vertex_spacing)) + 10e-8))  # vertex array size on the v-direction

    # Generate vertices directly from input points (preliminary evaluation)
    vertices = [Vertex() for _ in range(varr_size_v * varr_size_u)]
    u = 0.0
    for i in range(0, size_u, vertex_spacing):
        v = 0.0
        for j in range(0, size_v, vertex_spacing):
            idx = j + (i * size_v)
            vertices[vrt_idx - 1].id = vrt_idx
            vertices[vrt_idx - 1].data = points[idx]
            vertices[vrt_idx - 1].uv = [u, v]
            vrt_idx += 1
            v += v_jump
        u += u_jump

    #
    # Organization of vertices in a quad element on the parametric space:
    #
    # v4      v3
    # o-------o         i
    # |       |          |
    # |       |          |
    # |       |          |_ _ _
    # o-------o                 j
    # v1      v2
    #

    # Generate triangles and final vertices
    triangles = []
    for i in range(varr_size_u - 1):
        for j in range(varr_size_v - 1):
            # Find vertex indices for a quad element
            vertex1 = vertices[j + (i * varr_size_v)]
            vertex2 = vertices[j + 1 + (i * varr_size_v)]
            vertex3 = vertices[j + 1 + ((i + 1) * varr_size_v)]
            vertex4 = vertices[j + ((i + 1) * varr_size_v)]

            # Call tessellation function
            vlst, tlst = tsl_func(vertex1, vertex2, vertex3, vertex4, vrt_idx, tri_idx, trim_curves, tsl_args)

            # Add tessellation results to the return lists
            vertices += vlst
            triangles += tlst

            # Increment index values
            vrt_idx += len(vlst)
            tri_idx += len(tlst)

    # Fix vertex and triangle numbering (ID values)
    vertices, triangles = fix_numbering(vertices, triangles)

    return vertices, triangles


def polygon_triangulate(tri_idx, *args):
    """ Triangulates a monotone polygon defined by a list of vertices.

    The input vertices must form a convex polygon and must be arranged in counter-clockwise order.

    :param tri_idx: triangle numbering start value
    :type tri_idx: int
    :param args: list of Vertex objects
    :type args: elements.Vertex
    :return: list of Triangle objects
    :rtype: list
    """
    # Initialize variables
    tidx = 0
    triangles = []

    # Generate triangles
    for idx in range(1, len(args) - 1):
        tri = Triangle()
        tri.id = tri_idx + tidx
        tri.add_vertex(args[0], args[idx], args[idx + 1])
        triangles.append(tri)
        tidx += 1

    # Return generated triangles
    return triangles


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
    :type tessellate_args: dict
    :return: lists of vertex and triangle objects in (vertex_list, triangle_list) format
    :type: tuple
    """
    # Tolerance value
    tol = 10e-8

    # Start processing vertices
    vertices = [v1, v2, v3, v4]
    for idx in range(len(vertices)):
        for trim in trims:
            if wn_poly(vertices[idx].uv, trim.evalpts):
                if trim.opt['sense']:
                    if vertices[idx].opt_get('trim') is None or not vertices[idx].opt_get('trim'):
                        vertices[idx].inside = False
                        vertices[idx].opt = ['no_trim', True]  # always triangulate
                else:
                    vertices[idx].inside = True
                    vertices[idx].opt = ['trim', True]  # always trim
            else:
                if trim.opt['sense']:
                    if vertices[idx].opt_get('no_trim') is None or not vertices[idx].opt_get('no_trim'):
                        vertices[idx].inside = True

    # If all vertices are marked as inside, then don't generate triangles
    vertices_inside = [v1.inside, v2.inside, v3.inside, v4.inside]
    if all(vertices_inside):
        return [], []

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

            if isects:
                # Find minimum t value and therefore minimum uv value of the intersection
                t_min = 1.0 + tol
                uv_min = []
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
    tris = polygon_triangulate(tidx, *tris_vertices)

    # Check again if the barycentric coordinates of the triangles are inside
    for idx in range(len(tris)):
        tri_center = utilities.triangle_center(tris[idx], uv=True)
        for trim in trims:
            if wn_poly(tri_center, trim.evalpts):
                if trim.opt['sense']:
                    if tris[idx].opt_get('trim') is None or not tris[idx].opt_get('trim'):
                        tris[idx].inside = False
                        tris[idx].opt = ['no_trim', True]  # always triangulate
                else:
                    tris[idx].inside = True
                    tris[idx].opt = ['trim', True]  # always trim
            else:
                if trim.opt['sense']:
                    if tris[idx].opt_get('no_trim') is None or not tris[idx].opt_get('no_trim'):
                        tris[idx].inside = True

    # Extract triangles which are not inside the trim
    tris_final = []
    for tri in tris:
        if not tri.inside:
            tris_final.append(tri)

    return verts, tris_final
