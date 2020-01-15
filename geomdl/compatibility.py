"""
.. module:: compatibility
    :platform: Unix, Windows
    :synopsis: Provides compatibility functions for CAD interoperability

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""


def flip_ctrlpts_u(ctrlpts, size_u, size_v):
    """ Flips a list of 1-dimensional control points from u-row order to v-row order.

    **u-row order**: each row corresponds to a list of u values

    **v-row order**: each row corresponds to a list of v values

    :param ctrlpts: control points in u-row order
    :type ctrlpts: list, tuple
    :param size_u: size in u-direction
    :type size_u: int
    :param size_v: size in v-direction
    :type size_v: int
    :return: control points in v-row order
    :rtype: list
    """
    new_ctrlpts = []
    for i in range(0, size_u):
        for j in range(0, size_v):
            temp = [float(c) for c in ctrlpts[i + (j * size_u)]]
            new_ctrlpts.append(temp)

    return new_ctrlpts


def flip_ctrlpts(ctrlpts, size_u, size_v):
    """ Flips a list of 1-dimensional control points from v-row order to u-row order.

    **u-row order**: each row corresponds to a list of u values

    **v-row order**: each row corresponds to a list of v values

    :param ctrlpts: control points in v-row order
    :type ctrlpts: list, tuple
    :param size_u: size in u-direction
    :type size_u: int
    :param size_v: size in v-direction
    :type size_v: int
    :return: control points in u-row order
    :rtype: list
    """
    new_ctrlpts = []
    for i in range(0, size_v):
        for j in range(0, size_u):
            temp = [float(c) for c in ctrlpts[i + (j * size_v)]]
            new_ctrlpts.append(temp)

    return new_ctrlpts


def flip_ctrlpts2d(ctrlpts2d, size_u=0, size_v=0):
    """ Flips a list of surface 2-D control points from *[u][v]* to *[v][u]* order.

    :param ctrlpts2d: 2-D control points
    :type ctrlpts2d: list, tuple
    :param size_u: size in U-direction (row length)
    :type size_u: int
    :param size_v: size in V-direction (column length)
    :type size_v: int
    :return: flipped 2-D control points
    :rtype: list
    """
    if size_u <= 0 or size_v <= 0:
        # Detect array shapes
        size_u = len(ctrlpts2d)
        size_v = len(ctrlpts2d[0])

    new_ctrlpts2d = [[[] for _ in range(size_u)] for _ in range(size_v)]
    for i in range(size_v):
        for j in range(size_u):
            new_ctrlpts2d[i][j] = [float(c) for c in ctrlpts2d[j][i]]

    return new_ctrlpts2d


def generate_ctrlptsw(ctrlpts):
    """ Generates weighted control points from unweighted ones in 1-D.

    This function

    #. Takes in a 1-D control points list whose coordinates are organized in (x, y, z, w) format
    #. converts into (x*w, y*w, z*w, w) format
    #. Returns the result

    :param ctrlpts: 1-D control points (P)
    :type ctrlpts: list
    :return: 1-D weighted control points (Pw)
    :rtype: list
    """
    # Multiply control points by weight
    new_ctrlpts = []
    for cpt in ctrlpts:
        temp = [float(pt * cpt[-1]) for pt in cpt]
        temp[-1] = float(cpt[-1])
        new_ctrlpts.append(temp)

    return new_ctrlpts


def generate_ctrlptsw2d(ctrlpts2d):
    """ Generates weighted control points from unweighted ones in 2-D.

    This function

    #. Takes in a 2D control points list whose coordinates are organized in (x, y, z, w) format
    #. converts into (x*w, y*w, z*w, w) format
    #. Returns the result

    Therefore, the returned list could be a direct input of the NURBS.Surface class.

    :param ctrlpts2d: 2-D control points (P)
    :type ctrlpts2d: list
    :return: 2-D weighted control points (Pw)
    :rtype: list
    """
    # Multiply control points by weight
    new_ctrlpts2d = []
    for row in ctrlpts2d:
        ctrlptsw_v = []
        for col in row:
            temp = [float(c * col[-1]) for c in col]
            temp[-1] = float(col[-1])
            ctrlptsw_v.append(temp)
        new_ctrlpts2d.append(ctrlptsw_v)

    return new_ctrlpts2d


def generate_ctrlpts_weights(ctrlpts):
    """ Generates unweighted control points from weighted ones in 1-D.

    This function

    #. Takes in 1-D control points list whose coordinates are organized in (x*w, y*w, z*w, w) format
    #. Converts the input control points list into (x, y, z, w) format
    #. Returns the result

    :param ctrlpts: 1-D control points (P)
    :type ctrlpts: list
    :return: 1-D weighted control points (Pw)
    :rtype: list
    """
    # Divide control points by weight
    new_ctrlpts = []
    for cpt in ctrlpts:
        temp = [float(pt / cpt[-1]) for pt in cpt]
        temp[-1] = float(cpt[-1])
        new_ctrlpts.append(temp)

    return new_ctrlpts


def generate_ctrlpts2d_weights(ctrlpts2d):
    """ Generates unweighted control points from weighted ones in 2-D.

    This function

    #. Takes in 2-D control points list whose coordinates are organized like (x*w, y*w, z*w, w)
    #. Converts the input control points list into (x, y, z, w) format
    #. Returns the result

    :param ctrlpts2d: 2-D control points (P)
    :type ctrlpts2d: list
    :return: 2-D weighted control points (Pw)
    :rtype: list
    """
    # Divide control points by weight
    new_ctrlpts2d = []
    for row in ctrlpts2d:
        ctrlptsw_v = []
        for col in row:
            temp = [float(c / col[-1]) for c in col]
            temp[-1] = float(col[-1])
            ctrlptsw_v.append(temp)
        new_ctrlpts2d.append(ctrlptsw_v)

    return new_ctrlpts2d


def flip_ctrlpts2d_file(file_in='', file_out='ctrlpts_flip.txt'):
    """ Flips u and v directions of a 2D control points file and saves flipped coordinates to a file.

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    :raises IOError: an error occurred reading or writing the file
    """
    # Read control points
    ctrlpts2d, size_u, size_v = _read_ctrltps2d_file(file_in)

    # Flip control points array
    new_ctrlpts2d = flip_ctrlpts2d(ctrlpts2d, size_u, size_v)

    # Save new control points
    _save_ctrlpts2d_file(new_ctrlpts2d, size_u, size_v, file_out)


def generate_ctrlptsw2d_file(file_in='', file_out='ctrlptsw.txt'):
    """ Generates weighted control points from unweighted ones in 2-D.

    This function

    #. Takes in a 2-D control points file whose coordinates are organized in (x, y, z, w) format
    #. Converts into (x*w, y*w, z*w, w) format
    #. Saves the result to a file

    Therefore, the resultant file could be a direct input of the NURBS.Surface class.

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    :raises IOError: an error occurred reading or writing the file
    """
    # Read control points
    ctrlpts2d, size_u, size_v = _read_ctrltps2d_file(file_in)

    # Multiply control points by weight
    new_ctrlpts2d = generate_ctrlptsw2d(ctrlpts2d)

    # Save new control points
    _save_ctrlpts2d_file(new_ctrlpts2d, size_u, size_v, file_out)


def generate_ctrlpts2d_weights_file(file_in='', file_out='ctrlpts_weights.txt'):
    """ Generates unweighted control points from weighted ones in 2-D.

    #. Takes in 2-D control points list whose coordinates are organized like (x*w, y*w, z*w, w)
    #. Converts the input control points list into (x, y, z, w) format
    #. Saves the result to a file

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    :raises IOError: an error occurred reading or writing the file
    """
    # Read control points
    ctrlpts2d, size_u, size_v = _read_ctrltps2d_file(file_in)

    # Divide control points by weight
    new_ctrlpts2d = generate_ctrlpts2d_weights(ctrlpts2d)

    # Save new control points
    _save_ctrlpts2d_file(new_ctrlpts2d, size_u, size_v, file_out)


def _read_ctrltps2d_file(file_in):
    ctrlpts = []
    size_u = 0
    size_v = 0

    try:
        with open(file_in, 'r') as fp:
            for line in fp:
                line = line.strip()
                control_point_row = line.split(';')
                size_v = 0
                ctrlpts_v = []
                for cpr in control_point_row:
                    cpt = cpr.split(',')
                    pt_temp = []
                    for pt in cpt:
                        pt_temp.append(float(pt.strip()))
                    ctrlpts_v.append(pt_temp)
                    size_v += 1
                ctrlpts.append(ctrlpts_v)
                size_u += 1
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise

    return ctrlpts, size_u, size_v


def _save_ctrlpts2d_file(ctrlpts2d, size_u, size_v, file_out):
    try:
        with open(file_out, 'w') as fp:
            fp.truncate()
            for i in range(size_u):
                line = ""
                for j in range(size_v):
                    for idx, coord in enumerate(ctrlpts2d[i][j]):
                        if idx:  # Add comma if we are not on the first element
                            line += ","
                        line += str(coord)
                    if j != size_u - 1:
                        line += ";"
                    else:
                        line += "\n"
                fp.write(line)
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise
