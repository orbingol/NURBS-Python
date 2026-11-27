"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018-2021 Onur Rauf Bingol

    Requires "pytest" to run.
"""

from pytest import fixture, mark
from geomdl import fitting
import random

@fixture(scope='session')
def rng():
    return random.Random(1)

def random_param_vector(n, generator, min_separation=0.00001):
    """ Generates a random list of parameter locations (aka U-sub-ks).

    Entries range from 0.0 to 1.0 (which are always included). They are
    in monotonically increasing order and include no duplicates. Entries
    must be separated by at least min_separation.

    :param n: length of param vector
    :type n: int
    :param generator: instance of Random used for random data
    :type generator: Random
    :param min_separation: minimum distance of adjacent parameters
    :type min_separation: float
    """
    assert n > 2
    values = [generator.random() for _ in range(n - 2)]
    values.extend([0.0, 1.0])
    values.sort()
    if not all(b - a > min_separation for a, b in zip(values[:-1], values[1:])):
        # Failure is highly unlikely; just redo
        return random_param_vector(n, generator, min_separation)
    return values

def validate_knot_vector(knots, degree, num_cpts, params):
    """ Runs all available tests of knot vector quality and sanity.

    :param knots: knot vector
    :type knots: sequence of floats
    :param degree: curve fit degree
    :type degree: int
    :param num_cpts: number of control points
    :type num_cpts: int
    :param params: locations along the curve of data points, normalized to 0-1
    :type params: sequence of floats
    """
    validate_knot_vector_basics(knots, degree, num_cpts)
    validate_knot_vector_interleave(knots, degree, params)
    validate_knot_vector_symmetry(knots, degree, num_cpts, params)

def validate_knot_vector_basics(knots, degree, num_cpts):
    """ Verifies that a knot vector has the right number of entries, that
    every value is in the range 0-1 (not required in general, but should be
    the case for synthesized knot vectors), that the vector has the correct
    number of 0s and 1s at the ends, that there are no additional 0s or 1s,
    and that the values are monotonically increasing.

    :param knots: knot vector
    :type knots: sequence of floats
    :param degree: curve fit degree
    :type degree: int
    :param num_cpts: number of control points
    :type num_cpts: int
    """    
    assert len(knots) == num_cpts + degree + 1      # Right number
    assert all(0.0 <= k <= 1.0 for k in knots)      # Right value range
    assert all(k == 0.0 for k in knots[:degree+1])  # Right number of zeros
    assert all(k == 1.0 for k in knots[-degree-1:]) # Right number of ones
    assert all(0.0 < k < 1.0 for k in knots[degree+1:-degree-1])  # No extra 0s or 1s
    assert all(a <= b for a, b in zip(knots[:-1], knots[1:]))  # Monotonic

def validate_knot_vector_interleave(knots, degree, params):
    """ Verifies that every knot span includes at least one new data point.

    :param knots: knot vector
    :type knots: sequence of floats
    :param degree: curve fit degree
    :type degree: int
    :param params: locations along the curve of data points, normalized to 0-1
    :type params: sequence of floats
    """
    active_knots = knots[degree:-degree]
    knot_spans = zip(active_knots[:-1], active_knots[1:])
    def num_params_in_span(lo, hi):
        return len([x for x in params[1:-1] if lo <= x <= hi])
    assert all(num_params_in_span(a, b) > 0 for a, b in knot_spans)

def validate_knot_vector_symmetry(knots, degree, num_cpts, params):
    """ Verifies that inverting the parameter vector produces a knot vector
    that is the inverse of the vector produced in the forward direction.

    :param knots: knot vector
    :type knots: sequence of floats
    :param degree: curve fit degree
    :type degree: int
    :param num_cpts: number of control points
    :type num_cpts: int
    :param params: locations along the curve of data points, normalized to 0-1
    :type params: sequence of floats
    """
    revParams = [1 - param for param in reversed(params)]
    revKnots = fitting.compute_knot_vector2(degree, len(revParams), num_cpts, revParams)
    validate_knot_vector_basics(revKnots, degree, num_cpts)
    validate_knot_vector_interleave(revKnots, degree, revParams)
    invertedKnots = [1 - knot for knot in reversed(revKnots)]
    assert all(abs(a - b) < 0.000001 for a, b in zip(knots, invertedKnots))

@mark.parametrize("degree", [2, 3, 4, 5])
@mark.parametrize("num_dpts", [2, 3, 4, 5, 10, 20, 30, 40, 100])
def test_compute_knot_vector2(degree, num_dpts, rng):
    """ Exercise compute_knot_vector2 to verify that it is well behaved.

    :param degree: curve degree for fit
    :type degree: int
    :param num_dpts: number of data points
    :type num_dpts: int
    :param rng: random number generator
    :type rng: random.Random
    """
    # Need at least degree + 1 control points and at most num_dpts - 1
    for num_cpts in range(degree + 1, num_dpts):
        params = random_param_vector(num_dpts, rng)
        knots = fitting.compute_knot_vector2(degree, num_dpts, num_cpts, params)
        validate_knot_vector(knots, degree, num_cpts, params)

@fixture
def bad_points_1():
    points = [
        [2.844226598739624, -11.780293452192772, 0.09999999336045856],
        [2.7841949334192995, -11.766323767032048, 0.09999967816303046],
        [2.726926206709484, -11.752261321710279, 0.09999834367677496],
        [2.672275643786814, -11.73818458975435, 0.09999921155914912],
        [2.620158046052624, -11.72397519981413, 0.09999996191039656],
        [2.570553374917445, -11.709268999929673, 0.09999962409195731],
        [2.5232627391815186, -11.694355010986328, 0.10000000149011612],
        [2.478258938913115, -11.678929052642333, 0.09999946225906724],
        [2.435358747058011, -11.66315338641665, 0.09999991570513912],
        [2.394573211669922, -11.646668434143066, 0.10000000149011612],
        [2.355729818344116, -11.629592895507812, 0.10000000149011612],
        [2.3187353452599866, -11.611833538564408, 0.09999994560062432],
        [2.283545474902697, -11.59321500316845, 0.0999996723968506],
        [2.2499759197235107, -11.573817253112793, 0.10000000149011612],
        [2.217386549203785, -11.552999730025487, 0.09999874565806666],
        [2.1852133705257297, -11.530521281819617, 0.09999987781828826],
        [2.1537365913391113, -11.505938529968262, 0.10000000149011612],
        [2.122917890548706, -11.479263305664062, 0.10000000149011612],
        [2.092893351165359, -11.450263706561202, 0.09999973866089655],
        [2.0636894982676828, -11.418829252146876, 0.09999995528148392],
        [2.0354888439178467, -11.384699821472168, 0.10000000149011612],
        [2.0084729194641113, -11.34798812866211, 0.10000000149011612],
        [1.9837802648544312, -11.310267448425293, 0.10000000149011612],
        [1.9615306854248047, -11.272104263305664, 0.10000000149011612],
        [1.9416178464889526, -11.233770370483398, 0.10000000149011612],
        [1.9239351749420166, -11.195538520812988, 0.10000000149011612],
        [1.9083763360977173, -11.157683372497559, 0.10000000149011612],
        [1.894835114479065, -11.120477676391602, 0.10000000149011612],
        [1.8829901218414307, -11.083454132080078, 0.10000000149011612],
        [1.8725316644939427, -11.045799074770361, 0.09999994854771904],
        [1.8636144155532972, -11.007607214944535, 0.09999973105743598],
        [1.8561846017837524, -10.969038009643555, 0.10000000149011612],
        [1.8503996133333516, -10.930196091253926, 0.10000389344817495],
        [1.8471901202260397, -10.90117315661032, 0.1021130635318992],
        [1.8449852466583252, -10.872684478759766, 0.10844724625349045],
        [1.8437870740890503, -10.845902442932129, 0.11862903833389282],
        [1.843483992081289, -10.822776128482914, 0.13129674342530556],
        [1.8497409859620302, -10.79790687621756, 0.15000001355427042],
        [1.855139136314392, -10.781584739685059, 0.16294921934604645],
        [1.8570542447382592, -10.768168074449688, 0.17169737639867397],
        [1.8596694886032168, -10.754084788851447, 0.17936588915690657],
        [1.8629006147384644, -10.739490509033203, 0.18585821986198425],
        [1.866892695426941, -10.724578857421875, 0.19108659029006958],
        [1.8769696950912476, -10.694561004638672, 0.19784031808376312],
        [1.8894060850143433, -10.665621757507324, 0.20000000298023224],
        [1.9103977680206299, -10.627848625183105, 0.20000000298023224],
        [1.9356015920639038, -10.592745780944824, 0.20000000298023224],
        [1.9646819829940796, -10.56078052520752, 0.20000000298023224],
        [1.9972517490386963, -10.532379150390625, 0.20000000298023224],
        [2.032876968383789, -10.507918357849121, 0.20000000298023224],
        [2.071082830429077, -10.487727165222168, 0.20000000298023224],
        [2.111361265182495, -10.472070693969727, 0.20000000298023224],
        [2.153174877166748, -10.461159706115723, 0.20000000298023224],
        [2.195967197418213, -10.45513916015625, 0.20000000298023224],
        [2.239168167114258, -10.454089164733887, 0.20000000298023224],
        [2.2822024822235107, -10.458023071289062, 0.20000000298023224],
        [2.3244969844818115, -10.466890335083008, 0.20000000298023224],
        [2.365474916391236, -10.4806007670158, 0.1999998747902143],
        [2.4046443724843556, -10.498852355657805, 0.19999999233961327],
        [2.461829900741577, -10.526902198791504, 0.20000000298023224],
        [2.5210773944854736, -10.550283432006836, 0.20000000298023224],
        [2.5819969177246094, -10.568877220153809, 0.20000000298023224],
        [2.644202709197998, -10.582564353942871, 0.20000000298023224],
        [2.7073001861572266, -10.59126091003418, 0.20000000298023224],
        [2.7708895206451416, -10.594908714294434, 0.20000000298023224],
        [2.836341619491577, -10.596054077148438, 0.20000000298023224],
        [2.87705397605896, -10.59399700164795, 0.20000000298023224],
        [2.9171111583709717, -10.58643913269043, 0.20000000298023224],
        [2.9557740688323975, -10.573519706726074, 0.20000000298023224],
        [2.992328643798828, -10.555480003356934, 0.20000000298023224],
        [3.0261001586914062, -10.532649993896484, 0.20000000298023224],
        [3.0564651489257812, -10.505453109741211, 0.20000000298023224],
        [3.082862615585327, -10.474390983581543, 0.20000000298023224],
        [3.1048054695129395, -10.440035820007324, 0.20000000298023224],
        [3.1218883991241455, -10.403024673461914, 0.20000000298023224],
        [3.133796215057373, -10.364038467407227, 0.20000000298023224],
        [3.1403088569641113, -10.323798179626465, 0.20000000298023224],
        [3.141305923461914, -10.283045768737793, 0.20000000298023224],
        [3.1367692947387695, -10.242535591125488, 0.20000000298023224],
        [3.1267828941345215, -10.20301342010498, 0.20000000298023224],
        [3.1115307807922363, -10.165209770202637, 0.20000000298023224],
        [3.091294527053833, -10.1298246383667, 0.20000000298023224],
        [3.0664479732513428, -10.09750747680664, 0.20000000298023224],
        [3.037449598312378, -10.06885814666748, 0.20000000298023224],
        [3.0048351287841797, -10.044404029846191, 0.20000000298023224],
        [2.9692065715789795, -10.024596214294434, 0.20000000298023224],
        [2.9312217235565186, -10.00980281829834, 0.20000000298023224],
        [2.8915822505950928, -10.00029468536377, 0.20000000298023224]
    ]
    return points, 5, len(points) - 1

def test_compute_knot_vector2_with_known_problem_points(bad_points_1):
    points, degree, num_cpts = bad_points_1
    params = fitting.compute_params_curve(points)
    knots = fitting.compute_knot_vector2(degree, len(points), num_cpts, params)
    validate_knot_vector(knots, degree, num_cpts, params)

@fixture
def good_points_1():
    points = [
        [2.435358747058011, -11.66315338641665, 0.09999991570513912],
        [2.394573211669922, -11.646668434143066, 0.10000000149011612],
        [2.355729818344116, -11.629592895507812, 0.10000000149011612],
        [2.3187353452599866, -11.611833538564408, 0.09999994560062432],
        [2.283545474902697, -11.59321500316845, 0.0999996723968506],
        [2.2499759197235107, -11.573817253112793, 0.10000000149011612],
        [2.217386549203785, -11.552999730025487, 0.09999874565806666],
        [2.1852133705257297, -11.530521281819617, 0.09999987781828826],
        [2.1537365913391113, -11.505938529968262, 0.10000000149011612],
        [2.122917890548706, -11.479263305664062, 0.10000000149011612],
        [2.092893351165359, -11.450263706561202, 0.09999973866089655]
    ]
    return points, 5, len(points) - 1

def test_compute_knot_vector2_with_known_good_points(good_points_1):
    points, degree, num_cpts = good_points_1
    params = fitting.compute_params_curve(points)
    knots = fitting.compute_knot_vector2(degree, len(points), num_cpts, params)
    validate_knot_vector(knots, degree, num_cpts, params)

