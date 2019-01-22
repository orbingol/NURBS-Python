"""
.. module:: knotvector
    :platform: Unix, Windows
    :synopsis: Provides utility functions related to knot vector generation and validation

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from .linalg import linspace
from ._utilities import export


@export
def generate(degree, num_ctrlpts, **kwargs):
    """ Generates an equally spaced knot vector.

    It uses the following equality to generate knot vector: :math:`m = n + p + 1`

    where;

    * :math:`p`, degree
    * :math:`n + 1`, number of control points
    * :math:`m + 1`, number of knots

    Keyword Arguments:

        * ``clamped``: Flag to choose from clamped or unclamped knot vector options. *Default: True*

    :param degree: degree
    :type degree: int
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: int
    :return: knot vector
    :rtype: list
    """
    if degree == 0 or num_ctrlpts == 0:
        raise ValueError("Input values should be different than zero.")

    # Get keyword arguments
    clamped = kwargs.get('clamped', True)

    # Number of repetitions at the start and end of the array
    num_repeat = degree

    # Number of knots in the middle
    num_segments = num_ctrlpts - (degree + 1)

    if not clamped:
        # No repetitions at the start and end
        num_repeat = 0
        # Should conform the rule: m = n + p + 1
        num_segments = degree + num_ctrlpts - 1

    # First knots
    knot_vector = [0.0 for _ in range(0, num_repeat)]

    # Middle knots
    knot_vector += linspace(0.0, 1.0, num_segments + 2)

    # Last knots
    knot_vector += [1.0 for _ in range(0, num_repeat)]

    # Return auto-generated knot vector
    return knot_vector


@export
def normalize(knot_vector, decimals=18):
    """ Normalizes the input knot vector to [0, 1] domain.

    :param knot_vector: knot vector to be normalized
    :type knot_vector: list, tuple
    :param decimals: rounding number
    :type decimals: int
    :return: normalized knot vector
    :rtype: list
    """
    try:
        if knot_vector is None or len(knot_vector) == 0:
            raise ValueError("Input knot vector cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Knot vector must be a list or tuple")
    except Exception:
        raise

    first_knot = float(knot_vector[0])
    last_knot = float(knot_vector[-1])
    denominator = last_knot - first_knot

    knot_vector_out = [float(("{:." + str(decimals) + "f}").format((float(kv) - first_knot) / denominator))
                       for kv in knot_vector]

    return knot_vector_out


@export
def check(degree, knot_vector, num_ctrlpts):
    """ Checks the validity of the input knot vector.

    Please refer to The NURBS Book (2nd Edition), p.50 for details.

    :param degree: degree of the curve or the surface
    :type degree: int
    :param knot_vector: knot vector to be checked
    :type knot_vector: list, tuple
    :param num_ctrlpts: number of control points
    :type num_ctrlpts: int
    :return: True if the knot vector is valid, False otherwise
    :rtype: bool
    """
    try:
        if knot_vector is None or len(knot_vector) == 0:
            raise ValueError("Input knot vector cannot be empty")
    except TypeError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise TypeError("Knot vector must be a list or tuple")
    except Exception:
        raise

    # Check the formula; m = p + n + 1
    if len(knot_vector) != degree + num_ctrlpts + 1:
        return False

    # Check ascending order
    prev_knot = knot_vector[0]
    for knot in knot_vector:
        if prev_knot > knot:
            return False
        prev_knot = knot

    return True
