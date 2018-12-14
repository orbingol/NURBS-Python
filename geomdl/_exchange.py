"""
.. module:: _exchange
    :platform: Unix, Windows
    :synopsis: Helper functions for exchange module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import NURBS, compatibility


def import_smesh_single(file_name):
    """ Generates a NURBS surface from a surface mesh file.

    :param file_name: smesh file to read
    :type file_name: str
    :return: a NURBS surface
    :rtype: NURBS.Surface
    """
    try:
        with open(file_name, 'r') as fp:
            content = fp.readlines()
            content = [x.strip().split() for x in content]
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise

    # 1st line defines the dimension and it must be 3
    if int(content[0][0]) != 3:
        raise TypeError("Input smesh file" + str(file_name) + " is not a surface")

    # Create a NURBS surface instance and fill with the data read from smesh file
    surf = NURBS.Surface()

    # 2nd line is the degrees
    surf.degree_u = int(content[1][0])
    surf.degree_v = int(content[1][1])

    # 3rd line is the number of weighted control points in u and v directions
    dim_u = int(content[2][0])
    dim_v = int(content[2][1])
    ctrlpts_end = 5 + (dim_u * dim_v)

    # Starting from 6th line, we have the weighted control points
    ctrlpts_smesh = content[5:ctrlpts_end]

    # smesh files have the control points in u-row order format
    ctrlpts = compatibility.flip_ctrlpts_u(ctrlpts_smesh, dim_u, dim_v)

    # smesh files store control points in format (x, y, z, w) -- Rhino format
    ctrlptsw = compatibility.generate_ctrlptsw(ctrlpts)

    # Set control points
    surf.set_ctrlpts(ctrlptsw, dim_u, dim_v)

    # 4th and 5th lines are knot vectors
    surf.knotvector_u = [float(u) for u in content[3]]
    surf.knotvector_v = [float(v) for v in content[4]]

    # Return the surface instance
    return surf


def import_dict_crv(data):
    shape = NURBS.Curve()
    shape.degree = data['degree']
    shape.ctrlpts = data['control_points']['points']
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    shape.knotvector = data['knotvector']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    return shape


def export_dict_crv(obj):
    data = dict(
        degree=obj.degree,
        knotvector=list(obj.knotvector),
        control_points=dict(
            points=obj.ctrlpts
        ),
        delta=obj.delta
    )
    try:
        data['control_points']['weights'] = list(obj.weights)
    except AttributeError:
        # Not a NURBS curve
        pass
    return data


def import_dict_surf(data):
    shape = NURBS.Surface()
    shape.degree_u = data['degree_u']
    shape.degree_v = data['degree_v']
    shape.ctrlpts_size_u = data['size_u']
    shape.ctrlpts_size_v = data['size_v']
    shape.ctrlpts = data['control_points']['points']
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    shape.knotvector_u = data['knotvector_u']
    shape.knotvector_v = data['knotvector_v']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    return shape


def export_dict_surf(obj):
    data = dict(
        degree_u=obj.degree_u,
        degree_v=obj.degree_v,
        knotvector_u=list(obj.knotvector_u),
        knotvector_v=list(obj.knotvector_v),
        size_u=obj.ctrlpts_size_u,
        size_v=obj.ctrlpts_size_v,
        control_points=dict(
            points=obj.ctrlpts
        ),
        delta=obj.delta
    )
    try:
        data['control_points']['weights'] = list(obj.weights)
    except AttributeError:
        # Not a NURBS curve
        pass
    return data
