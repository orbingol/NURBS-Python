"""
.. module:: operations
    :platform: Unix, Windows
    :synopsis: Provides various operations that can be applied to B-Spline and NURBS shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import copy
from . import BSpline
from . import Multi
from . import helpers
from . import utilities


def split_curve(obj, u, **kwargs):
    """ Splits the curve at the input parametric coordinate.

    This method splits the curve into two pieces at the given parametric coordinate, generates two different
    curve objects and returns them. It doesn't change anything on the initial curve.

    :param obj: Curve to be split
    :type obj: BSpline.Curve or NURBS.Curve
    :param u: parametric coordinate
    :type u: float
    :return: a list of curves as the split pieces of the initial curve
    :rtype: Multi.MultiCurve
    """
    if not isinstance(obj, BSpline.Curve):
        raise TypeError("Input shape must be an instance of any Curve class")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Validate input data
    if u == 0.0 or u == 1.0:
        raise ValueError("Cannot split on the corner points")
    utilities.check_uv(u)

    # Find multiplicity of the knot and define how many times we need to add the knot
    ks = span_func(obj.degree, obj.knotvector, len(obj.ctrlpts), u) - obj.degree + 1
    s = helpers.find_multiplicity(u, obj.knotvector)
    r = obj.degree - s

    # Create backups of the original curve
    temp_obj = copy.deepcopy(obj)

    # Insert knot
    temp_obj.insert_knot(u, r, check_r=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree, temp_obj.knotvector, len(temp_obj.ctrlpts), u) + 1
    curve1_kv = list(temp_obj.knotvector[0:knot_span])
    curve1_kv.append(u)
    curve2_kv = temp_obj.knotvector[knot_span:]
    for _ in range(0, temp_obj.degree + 1):
        curve2_kv.insert(0, u)

    # Control points
    curve1_ctrlpts = temp_obj.ctrlpts[0:ks + r]
    curve2_ctrlpts = temp_obj.ctrlpts[ks + r - 1:]

    # Create a new curve for the first half
    curve1 = temp_obj.__class__()
    curve1.degree = temp_obj.degree
    curve1.ctrlpts = curve1_ctrlpts
    curve1.knotvector = curve1_kv

    # Create another curve fot the second half
    curve2 = temp_obj.__class__()
    curve2.degree = temp_obj.degree
    curve2.ctrlpts = curve2_ctrlpts
    curve2.knotvector = curve2_kv

    # Create a MultiCurve
    ret_val = Multi.MultiCurve()
    ret_val.add(curve1)
    ret_val.add(curve2)

    # Return the new curves as a MultiCurve object
    return ret_val


def decompose_curve(obj):
    """ Decomposes the curve into Bezier curve segments of the same degree.

    This operation does not modify the input curve, instead it returns the split curve segments.

    :param obj: Curve to be decomposed
    :type obj: BSpline.Curve or NURBS.Curve
    :return: a list of curve objects arranged in Bezier curve segments
    :rtype: Multi.MultiCurve
    """
    if not isinstance(obj, BSpline.Curve):
        raise TypeError("Input shape must be an instance of any Curve class")

    curve_list = Multi.MultiCurve()
    curve = copy.deepcopy(obj)
    knots = curve.knotvector[curve.degree + 1:-(curve.degree + 1)]
    while knots:
        knot = knots[0]
        curves = split_curve(curve, u=knot)
        curve_list.add(curves[0])
        curve = curves[1]
        knots = curve.knotvector[curve.degree + 1:-(curve.degree + 1)]
    curve_list.add(curve)

    return curve_list


def add_dimension(obj, **kwargs):
    """ Converts x-D curve to a (x+1)-D curve.

    Useful when converting a 2-D curve to a 3-D curve.

    :param obj: Curve
    :type obj: BSpline.Curve or NURBS.Curve
    :return: updated Curve
    :rtype: BSpline.Curve or NURBS.Curve
    """
    if not isinstance(obj, BSpline.Curve):
        raise TypeError("Input shape must be an instance of any Curve class")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    # Update control points
    new_ctrlpts = []
    for point in obj.ctrlpts:
        temp = [float(p) for p in point[0:obj.dimension]]
        temp.append(0.0)
        new_ctrlpts.append(temp)

    if inplace:
        obj.ctrlpts = new_ctrlpts
        return obj
    else:
        ret = copy.deepcopy(obj)
        ret.ctrlpts = new_ctrlpts
        return ret


def translate(obj, vec, **kwargs):
    """ Translates the shape by the input vector.

    :param obj: Curve or surface to be translated
    :type obj: Abstract.Curve or Abstract.Surface
    :param vec: translation vector
    :type vec: list, tuple
    """
    if not vec or not isinstance(vec, (tuple, list)):
        raise ValueError("The input must be a list or a tuple")

    if len(vec) != obj.dimension:
        raise ValueError("The input must have " + str(obj.dimension) + " elements")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)

    # Translate control points
    new_ctrlpts = []
    for point in obj.ctrlpts:
        temp = [v + vec[i] for i, v in enumerate(point)]
        new_ctrlpts.append(temp)

    if inplace:
        obj.ctrlpts = new_ctrlpts
        return obj
    else:
        ret = copy.deepcopy(obj)
        ret.ctrlpts = new_ctrlpts
        return ret
