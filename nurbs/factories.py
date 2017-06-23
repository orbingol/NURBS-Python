"""
.. module:: factories
    :platform: Unix, Windows
    :synopsis: Facilitates creation of curves
"""

from nurbs import Curve as ns
from nurbs import utilities as utils
import json, sys, unittest

DEGREE_FALLBACK = 1


def load_floats_or(data, key, fallback):
    """ Loads an array from the dict under the given key and casts to floats.
    Returns fallback if key not present.

    :param data: input data
    :type data: dict
    :param key: key
    :param fallback: bailout value returned if key not present
    :type data: list of floats
    :return: list of floats
    :raises: ValueError if not able to cast array to array of floats.
    """ 
    try:
        vals = data[key]  
        try:
            vals = [float(val) for val in vals] 
            return vals           
        except:
            raise ValueError('Invalid input format for float array for ' + key)          
    except KeyError:
        return fallback

def from_dict(nurbdsdict):
    """ Creates a nurbs instance from the data provided in the dictionary.

    :param nurbdsdict: input data
    :type nurbdsdict: dict
    :return: Curve
    :raises: ValueError if content not adhering to schema.
    """ 
    #Create a NURBS curve instance
    curve = ns.Curve()

    # Degree is optional
    try:
        curve.degree = int(nurbdsdict['degree']) 
    except:
        curve.degree = DEGREE_FALLBACK

    # Control points are required
    try:
        ctrlpts = nurbdsdict['controlpoints']
        ctrlptsx = ctrlpts['x']
        ctrlptsy = ctrlpts['y']
    except KeyError:
        raise ValueError('No control points provided')

    try:
        ctrlpts = [[float(ctrlptx), float(ctrlpty)] for ctrlptx, ctrlpty in zip(ctrlptsx, ctrlptsy)]
    except:
        raise ValueError('Invalid input format for control points')

    curve.ctrlpts = ctrlpts

    # Weigths and knots are optional
    curve.weights = load_floats_or(nurbdsdict, 'weights', [1.0] * len(ctrlptsx))
    curve.knotvector = load_floats_or(nurbdsdict, 'knots', \
      utils.knotvector_autogen(curve.degree, len(curve.ctrlpts)))

    return curve

def from_file(filename):
    """ Reads nurbs data from a json formatted file and returns instantiated object.


    :param filename: input file name
    :type filename: string
    :return: Curve
    :raises: IOError if file is unavailable/invalid json and ValueError if content not adhering to schema.
    """ 
    try:
        with open(filename, 'r') as fp:
            jsonrepr = json.load(fp)
    except:
        # raise this for both an invalid file and json parsing error
        raise IOError('Invalid json file ' + filename)
    
    return from_dict(jsonrepr)

class TestJSONFactory(unittest.TestCase):

    def setUp(self):
        self.ctrlptsx = [ 0, 0, 2, 3, 3.5, 2, 2, 4]
        self.ctrlptsy = [ 0, 2, 2.5, 1, 2.5, 3, 4, 3]
        self.weights = [ 1.4, 0.5, 1.6, 1.8, 0.7, 1.9, 1.5, 0.9]
        self.knots = [ 1.4, 0.5, 1.6, 1.8, 0.7, 1.9, 1.5, 0.9]
        self.degree = 3
        self.data = {'controlpoints': {'x': self.ctrlptsx, 'y': self.ctrlptsy}} 

    def test_ctrlpoints_only(self):  
        curve = from_dict(self.data)
        for i in range(len(self.ctrlptsx)):
            self.assertEqual(curve.ctrlpts[i][0], self.ctrlptsx[i])
            self.assertEqual(curve.ctrlpts[i][1], self.ctrlptsy[i])
        self.assertEqual(curve.degree, DEGREE_FALLBACK)
        self.assertEqual(curve.weights, tuple([1.0] * len(self.ctrlptsx)))
        self.assertEqual(curve.knotvector, \
          tuple(utils.knotvector_autogen(DEGREE_FALLBACK, len(self.ctrlptsx))))

    def test_with_degree(self): 
        self.data['degree'] = self.degree
        curve = from_dict(self.data)
        self.assertEqual(curve.degree, 3)

    def test_with_weights(self): 
        self.data['weights'] = self.weights
        curve = from_dict(self.data)
        self.assertEqual(curve.weights, tuple(self.weights))   

    def test_with_knots(self): 
        self.data['degree'] = self.degree
        self.data['weights'] = self.weights
        self.data['knots'] = self.weights
        curve = from_dict(self.data)
        self.assertEqual(curve.weights, tuple(self.weights))
        

if __name__ == '__main__':
    unittest.main()