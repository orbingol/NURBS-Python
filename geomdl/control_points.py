"""
.. module:: control_points
    :platform: Unix, Windows
    :synopsis: Provides helper classes for managing control points

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from functools import reduce
from .base import export, GeomdlBase, GeomdlDict, GeomdlList, GeomdlFloat, GeomdlTypeSequence, GeomdlError

# Initialize an empty __all__ for controlling imports
__all__ = []


def default_find_index(pts_size, *args):
    """ Finds the array index from the input parametric position.

    .. code-block:: python

        from geomdl.control_points import find_index

        # parametric position: u=2, v=1, w=5
        # ctrlpts_size: number of control points in all parametric dimensions, e.g. (6, 7, 11)
        idx = find_index((6, 7, 11), 2, 1, 5)

    :param pts_size: number of control points in all parametric dimensions
    :type pts_size: list, tuple
    :param args: position in the parametric space
    :type args: tuple
    :return: index of the control points at the specified parametric position
    :rtype: int
    """
    idx = 0
    for i, arg in enumerate(args):
        mul_res = 1
        if i > 0:
            for j in pts_size[:i]:
                mul_res *= j
        idx += arg * mul_res
    return idx


def default_ctrlpts_init(num_ctrlpts, **kwargs):
    """ Initializes the control points container (default)

    Default functions use the container types included in the Python Standard Library.

    :param num_ctrlpts: total number of control points
    :type num_ctrlpts: int
    :return: a tuple containing initialized control points (as a ``list``) and data dictionary (as a ``dict``)
    :rtype: tuple
    """
    points = [() for _ in range(num_ctrlpts)]
    points_data = GeomdlDict()
    for k, v in kwargs.items():
        if v > 1:
            points_data[k] = [[GeomdlFloat(0.0) for _ in range(v)] for _ in range(num_ctrlpts)]
        else:
            points_data[k] = [GeomdlFloat(0.0) for _ in range(num_ctrlpts)]
    return points, points_data


def default_ctrlpts_set(pts_in, dim, pts_out):
    """ Fills the control points container with the input points (default)

    Default functions use the container types included in the Python Standard Library.

    :param pts_in: input list of control points
    :type pts_in: list, tuple
    :param dim: spatial dimension
    :type dim: int
    :param pts_out: output list of control points
    :type pts_out: list
    :return: ``pts_out`` will be returned
    :rtype: list
    """
    for idx, cpt in enumerate(pts_in):
        if not isinstance(cpt, GeomdlTypeSequence):
            raise GeomdlError("input[" + str(idx) + "] not valid. Must be a sequence.")
        if len(cpt) != dim:
            raise GeomdlError(str(cpt) + " not valid. Must be a " + str(dim) + "-dimensional list.")
        default_ctrlpt_set(pts_out, idx, cpt)
    return pts_out


def default_ctrlpt_set(pts_arr, idx, cpt):
    """ Assigns value to a single control point position inside the container (default)

    :param pts_arr: control points container
    :type pts_arr: list
    :param idx: container index
    :type idx: int
    :param cpt: control point
    :type cpt: list, tuple
    """
    pts_arr[idx] = [GeomdlFloat(c) for c in cpt]


def extract_ctrlpts2d(cm):
    """ Extracts control points in u- and v-dimensions

    :param cm: control points manager
    :type cm: CPManager
    """
    ptd = {
        'points_u': [],
        'points_v': []
    }

    for v in range(cm.size_v):
        ptd['points_u'] += [cm[u, v] for u in range(cm.size_u)]

    for u in range(cm.size_u):
        ptd['points_v'] += [cm[u, v] for v in range(cm.size_v)]

    return ptd


def extract_ctrlpts3d(cm):
    """ Extracts control points in u-, v- and w-dimensions

    :param cm: control points manager
    :type cm: CPManager
    """
    ptd = {
        'points_u': [],
        'points_v': [],
        'points_w': []
    }

    for w in range(cm.size_w):
        for v in range(cm.size_v):
            ptd['points_u'] += [cm[u, v, w] for u in range(cm.size_u)]

    for w in range(cm.size_w):
        for u in range(cm.size_u):
            ptd['points_v'] += [cm[u, v, w] for v in range(cm.size_v)]

    for v in range(cm.size_v):
        for u in range(cm.size_u):
            ptd['points_w'] += [cm[u, v, w] for w in range(cm.size_w)]

    return ptd


@export
def combine_ctrlpts_weights(ctrlpts, weights=()):
    """ Multiplies control points by the weights to generate weighted control points.

    This function is dimension agnostic, i.e. control points can be in any dimension but weights should be 1-dimensional.

    The ``weights`` function parameter can be set to None to let the function generate a weights vector composed of
    1.0 values. This feature can be used to convert B-Spline basis to NURBS basis.

    :param ctrlpts: unweighted control points
    :type ctrlpts: list, tuple
    :param weights: weights vector; if set to None, a weights vector of 1.0s will be automatically generated
    :type weights: list, tuple or None
    :return: weighted control points
    :rtype: list
    """
    if not weights:
        weights = [GeomdlFloat(1.0) for _ in range(len(ctrlpts))]

    ctrlptsw = [[] for _ in range(len(ctrlpts))]
    for idx, (pt, w) in enumerate(zip(ctrlpts, weights)):
        ctrlptsw[idx] = [GeomdlFloat(c * w) for c in pt] + [GeomdlFloat(w)]
    return ctrlptsw

@export
def separate_ctrlpts_weights(ctrlptsw):
    """ Divides weighted control points by weights to generate unweighted control points and weights vector.

    This function is dimension agnostic, i.e. control points can be in any dimension but the last element of the array
    should indicate the weight.

    :param ctrlptsw: weighted control points
    :type ctrlptsw: list, tuple
    :return: unweighted control points and weights vector
    :rtype: list
    """
    ctrlpts = [[] for _ in range(len(ctrlptsw))]
    weights = [1.0 for _ in range(len(ctrlptsw))]
    for idx, ptw in enumerate(ctrlptsw):
        ctrlpts[idx] = [GeomdlFloat(pw / ptw[-1]) for pw in ptw[:-1]]
        weights[idx] = GeomdlFloat(ptw[-1])
    return ctrlpts, weights


@export
class CPManager(GeomdlBase):
    """ Control points manager class

    Control points manager class provides an easy way to set control points without knowing the internal data structure
    of the geometry classes. The manager class is initialized with the number of control points in all parametric
    dimensions.

    This class inherits the following properties:

    * :py:attr:`type`
    * :py:attr:`id`
    * :py:attr:`name`
    * :py:attr:`dimension`
    * :py:attr:`opt`

    This class inherits the following methods:

    * :py:meth:`get_opt`
    * :py:meth:`reset`

    This class inherits the following keyword arguments:

    * ``id``: object ID (as an integer). *Default: 0*
    * ``name``: object name. *Default: name of the class*

    This class provides the following properties:

    * :py:attr:`points`
    * :py:attr:`points_data`
    * :py:attr:`size`
    * :py:attr:`count`
    * :py:attr:`dimension`

    This class provides the following methods:

    * :py:meth:`pt`
    * :py:meth:`set_pt`
    * :py:meth:`ptdata`
    * :py:meth:`set_ptdata`
    * :py:meth:`reset`

    This class provides the following keyword arguments:

    * ``func_pts_init``: function to initialize the control points container. *Default:* ``default_ctrlpts_init``
    * ``func_pts_set``: function to fill the control points container. *Default:* ``default_ctrlpts_set``
    * ``func_pt_set``: function to assign a single control point. *Default:* ``default_ctrlpt_set``
    * ``func_find_index``: function to find the index of the control point/vertex. *Default:* ``default_find_index``
    """
    __slots__ = ('_size', '_pts', '_ptsd', '_iter_index')

    def __init__(self, *args, **kwargs):
        super(CPManager, self).__init__(*args, **kwargs)
        # Update configuration dictionary
        self._cfg['func_pts_init'] = kwargs.pop('func_pts_init', default_ctrlpts_init)  # points init function
        self._cfg['func_pts_set'] = kwargs.pop('func_pts_set', default_ctrlpts_set)  # points set function
        self._cfg['func_pt_set'] = kwargs.pop('func_pt_set', default_ctrlpt_set)  # single point set function
        self._cfg['func_find_index'] = kwargs.pop('func_find_index', default_find_index)  # index finding function
        # Prepare and update size
        sz = [int(arg) for arg in args] if args else [0]
        self._size = GeomdlList(*sz, attribs=('u', 'v', 'w'), cb=[self.reset])
        # Initialize the control points and the associated data container
        self._pts, self._ptsd = self._cfg['func_pts_init'](self.count, **kwargs)

    def __call__(self, points):
        self.points = points

    def __reduce__(self):
        return (self.__class__, (self.points,))

    def __next__(self):
        try:
            result = self._pts[self._iter_index]
        except IndexError:
            raise StopIteration
        self._iter_index += 1
        return result

    def __len__(self):
        return self.count

    def __reversed__(self):
        return reversed(self._pts)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._pts[item]
        if isinstance(item, tuple):
            if len(item) != len(self.size):
                raise ValueError("The n-dimensional indices must be equal to number of parametric dimensions")
            idx = self._cfg['func_find_index'](self.size, *item)
            return self._pts[idx]
        raise TypeError(self.__class__.__name__ + " indices must be integer or tuple, not " + item.__class__.__name__)

    def __setitem__(self, key, value):
        # The input value must be a sequence type
        if not isinstance(value, GeomdlTypeSequence):
            raise TypeError("RHS must be a sequence")
        # If dimension is not set, try to find it
        if self.dimension < 1:
            self._dimension = len(value)
        # Always make sure that new input conforms with the existing dimension value
        if len(value) != self.dimension:
            raise ValueError("Input points must be " + str(self.dimension) + "-dimensional")

        # Set the item
        if isinstance(key, int):
            self._cfg['func_pt_set'](self._pts, key, value)
        elif isinstance(key, tuple):
            if len(key) != len(self.size):
                raise ValueError("The n-dimensional indices must be equal to number of parametric dimensions")
            idx = self._cfg['func_find_index'](self.size, *key)
            self._cfg['func_pt_set'](self._pts, idx, value)
        else:
            raise TypeError(self.__class__.__name__ + " indices must be integer or tuple, not " + key.__class__.__name__)

    @property
    def points(self):
        """ Control points

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points (as a ``tuple``)
        :setter: Sets the control points
        """
        return tuple(self._pts)

    @points.setter
    def points(self, value):
        # Check input type
        if not isinstance(value, GeomdlTypeSequence):
            raise GeomdlError("Control points input must be a sequence")
        # Check input length
        if len(value) != self.count:
            raise GeomdlError("Number of control points must be " + str(self.count))
        # Update dimension
        self._dimension = len(value[0])
        # Set control points
        self._cfg['func_pts_set'](value, self.dimension, self._pts)

    @property
    def points_data(self):
        return self._ptsd

    @property
    def size(self):
        """ Number of the control points in all parametric dimensions

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the number of the control points
        :setter: Sets the number of the control points
        """
        return self._size

    @size.setter
    def size(self, value):
        self._size.data = value.data if isinstance(value, GeomdlList) else value if isinstance(value, GeomdlTypeSequence) else [value]

    @property
    def count(self):
        """ Total number of the control points

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the total number of the control points (as an ``int``)
        """
        return reduce(lambda x, y: x * y, self.size)

    def reset(self, **kwargs):
        """ Resets the control points """
        # Call parent method
        super(CPManager, self).reset(**kwargs)
        # Reinitialize the control points and the associated data container
        self._pts, self._ptsd = self._cfg['func_pts_init'](self.count, **kwargs)

    def pt(self, *args):
        """ Gets the control point from the input position """
        return self[args]

    def set_pt(self, pt, *args):
        """ Puts the control point to the input position

        :param pt: control point
        :type pt: list, tuple
        """
        self[args] = pt

    def ptdata(self, dkey, *args):
        """ Gets the data attached to the control point

        :param dkey: key of the data dictionary
        :param dkey: str
        """
        # Find the index
        idx = self._cfg['func_find_index'](self.size, *args)
        # Return the attached data
        try:
            return self._ptsd[dkey][idx]
        except IndexError:
            return None
        except KeyError:
            return None

    def set_ptdata(self, adct, *args):
        """ Attaches the data to the control point

        :param adct: data dictionary
        :param adct: dict
        """
        # Find the index
        idx = self._cfg['func_find_index'](self.size, *args)
        # Attach the data to the control point
        try:
            for k, val in adct.items():
                if k in self._ptsd:
                    if isinstance(val, GeomdlTypeSequence):
                        for j, v in enumerate(val):
                            self._ptsd[k][idx][j] = v
                    else:
                        self._ptsd[k][idx] = val
                else:
                    raise GeomdlError("Invalid key: " + str(k))
        except IndexError:
            raise GeomdlError("Index is out of range")
