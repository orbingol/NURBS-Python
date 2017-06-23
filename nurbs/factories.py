"""
.. module:: factories
    :platform: Unix, Windows
    :synopsis: Facilitates creation of curves
"""
import nurbs
from nurbs import Curve as nc
from nurbs import Surface as ns
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


def load_floats_under_key_or(data, key0, key1, fallback):
    """ Loads an array from the dict under the given keys and casts to floats.
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
        subdata = data[key0] 
        return load_floats_or(subdata, key1, fallback)        
    except KeyError:
        return fallback


def from_dict(data):
    """ Creates a nurbs instance from the data provided in the dictionary.

    :param nurbdsdict: input data
    :type nurbdsdict: dict
    :return: Curve
    :raises: ValueError if content not adhering to schema.
    """ 
    # If dimensions are provided, this is a surface
    try:
        # (u,v)
        dim = (int(data['dim'][0]), int(data['dim'][1]))
    except KeyError:
        dim = None

    # Control points are required
    try:
        ctrlpts = data['controlpoints']
        ctrlptsx = ctrlpts['x']
        ctrlptsy = ctrlpts['y']
        num_ctrlpts = len(ctrlptsx)
        if dim:
            ctrlptsz = ctrlpts['z']
    except KeyError:
        raise ValueError('Control points are required')

    # Make the coordinate vector, 2D points for a curve and 3D for a surface
    try:
        if not dim:       
            # Curve     
            ctrlpts = [[float(ctrlptx), float(ctrlpty)] for ctrlptx, ctrlpty in zip(ctrlptsx, ctrlptsy)]
        else:
            # Surface
            ctrlpts = [[float(ctrlptx), float(ctrlpty), float(ctrlptz)] for \
              ctrlptx, ctrlpty, ctrlptz in zip(ctrlptsx, ctrlptsy, ctrlptsz)]    
            # Expects v[u] nested list
            ctrlpts = [[ctrlpts[v*dim[0]+u] for u in range(dim[0])] for v in range(dim[1])]
    except:
        raise ValueError('Invalid input format for control points')

    # Degree is optional
    if not dim:
        # Curve
        try:
            degree = int(data['degree']) 
        except KeyError:
            degree = DEGREE_FALLBACK
    else:
        # Surface
        try:
            degree = (int(data['degree'][0]), int(data['degree'][1]))
        except KeyError:
            degree = (DEGREE_FALLBACK, DEGREE_FALLBACK)        

    # Weigths and knots are optional    
    weights = load_floats_or(data, 'weights', [1.0] * num_ctrlpts)
    if not dim:
        # Curve        
        knotvector = load_floats_or(data, 'knots', utils.knotvector_autogen(degree, num_ctrlpts))
    else:
        # Surface
        knotvector_u = load_floats_under_key_or(data, 'knots', 'u', utils.knotvector_autogen(degree[0], dim[0]))
        knotvector_v = load_floats_under_key_or(data, 'knots', 'v', utils.knotvector_autogen(degree[1], dim[1]))
        

    #Create a NURBS instance
    if not dim:
        retval = nc.Curve()
        retval.degree = degree
    else:
        retval = ns.Surface()
        retval.degree_u = degree[0]
        retval.degree_v = degree[1]
    
    retval.ctrlpts = ctrlpts
    retval.weights = weights

    if not dim:
        retval.knotvector = knotvector
    else:
        retval.knotvector_u = knotvector_u
        retval.knotvector_v = knotvector_v

    return retval


def from_file(filename):
    """ Reads nurbs data from a json formatted file and returns instantiated object.

    .. note:: The format of the text files is described in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

    :param filename: input file name
    :type filename: string
    :return: Curve
    :raises: IOError if file is unavailable/invalid json and ValueError if content not adhering to schema.
    """ 
    try:
        with open(filename, 'r') as fp:
            data = json.load(fp)
    except:
        # raise this for both an invalid file and json parsing error
        raise IOError('Invalid json file ' + filename)
    
    return from_dict(data)


class TestJSONCurveFactory(unittest.TestCase):

    def setUp(self):
        self.ctrlptsx = [ 0, 0, 2, 3, 3.5, 2, 2, 4]
        self.ctrlptsy = [ 0, 2, 2.5, 1, 2.5, 3, 4, 3]
        self.weights = [ 1.4, 0.5, 1.6, 1.8, 0.7, 1.9, 1.5, 0.9]
        self.knots = [0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.degree = 3
        self.data = {'controlpoints': {'x': self.ctrlptsx, 'y': self.ctrlptsy}} 

    def test_ctrlpoints_only(self):  
        curve = from_dict(self.data)
        self.assertEqual(isinstance(curve, nurbs.Curve.Curve), True)
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
        self.assertEqual(curve.degree, self.degree)

    def test_with_weights(self): 
        self.data['weights'] = self.weights
        curve = from_dict(self.data)
        self.assertEqual(curve.weights, tuple(self.weights))   

    def test_with_knots(self): 
        self.data['degree'] = self.degree
        self.data['weights'] = self.weights
        self.data['knots'] = self.knots
        curve = from_dict(self.data)
        self.assertEqual(curve.knotvector, tuple(self.knots))


class TestJSONSurfaceFactory(unittest.TestCase):

    def setUp(self):
        self.ctrlptsx = [-25,-25,-25,-25,-25,-25,-15,-15,-15,-15,-15,-15,-5,-5,-5,-5,-5,-5,5,5,5,5,5,5,15,15,15,15,15,15,25,25,25,25,25,25]
        self.ctrlptsy = [-25,-15,-5,5,15,25,-25,-15,-5,5,15,25,-25,-15,-5,5,15,25,-25,-15,-5,5,15,25,-25,-15,-5,5,15,25,-25,-15,-5,5,15,25]
        self.ctrlptsz = [-10,-5,0,0,-5,-10,-8,-4,-4,-4,-4,-8,-5,-3,-8,-8,-3,-5,-3,-2,-8,-8,-2,-3,-8,-4,-4,-4,-4,-8,-10,-5,2,2,-5,-10]
        self.knots = [0.0, 0.0, 0.0, 0.0, 0.3, 0.6, 1.0, 1.0, 1.0, 1.0]
        self.degree = [3, 3]
        self.dim = [6, 6]
        self.data = {'dim': self.dim, 'controlpoints': {'x': self.ctrlptsx, 'y': self.ctrlptsy, 'z': self.ctrlptsz}} 

    def test_ctrlpoints_only(self): 
        surface = from_dict(self.data)
        self.assertEqual(isinstance(surface, nurbs.Surface.Surface), True)
        for i in range(len(self.ctrlptsx)):
            self.assertEqual(surface.ctrlpts[i][0], self.ctrlptsx[i])
            self.assertEqual(surface.ctrlpts[i][1], self.ctrlptsy[i])
            self.assertEqual(surface.ctrlpts[i][2], self.ctrlptsz[i])
        self.assertEqual(surface.degree_u, DEGREE_FALLBACK)
        self.assertEqual(surface.degree_v, DEGREE_FALLBACK)
        self.assertEqual(surface.weights, tuple([1.0] * len(self.ctrlptsx)))
        self.assertEqual(surface.knotvector_u, \
          tuple(utils.knotvector_autogen(DEGREE_FALLBACK, self.dim[0])))
        self.assertEqual(surface.knotvector_u, surface.knotvector_v)

    def test_with_degree(self): 
        self.data['degree'] = self.degree
        curve = from_dict(self.data)
        self.assertEqual(curve.degree_u, self.degree[0])
        self.assertEqual(curve.degree_v, self.degree[1])

    def test_with_knots(self):
        self.data['degree'] = self.degree
        self.data['knots'] = {'u': self.knots, 'v': self.knots}
        surface = from_dict(self.data)
        self.assertEqual(surface.knotvector_u, tuple(self.knots))
        self.assertEqual(surface.knotvector_v, tuple(self.knots))
        

if __name__ == '__main__':
    unittest.main()