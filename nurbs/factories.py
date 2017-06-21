"""
.. module:: factories
    :platform: Unix, Windows
    :synopsis: Facilitates creation of curves

.. moduleauthor:: Philipp Lang

"""

from nurbs import Curve as ns
from nurbs import utilities as utils
import json, sys

DEGREE_FALLBACK = 1

# Returnd control points and weigths(optional) from json dict representation
def from_file(filename):
    """ Reads control points from a json file - weigths are used if present.


    :param filename: input file name
    :type filename: string
    :return: Curve
    :raises: IOError if file is unavailable/invalid json and ValueError values not adhering to schema.
    """ 
    # Read file
    try:
        with open(filename, 'r') as fp:
            jsonrepr = json.load(fp)
    except:
        raise IOError('Invalid json file ' + filename)
    
    #Create a NURBS curve instance
    curve = ns.Curve()

    # Degree is optional
    try:
        curve.degree = int(jsonrepr['degree']) 
    except:
        curve.degree = DEGREE_FALLBACK

    # Control points are required
    try:
        ctrlpts = jsonrepr['controlpoints']
        ctrlptsx = ctrlpts['x']
        ctrlptsy = ctrlpts['y']
    except KeyError:
        raise ValueError('Unable to parse control points')

    try:
        ctrlpts = [[float(ctrlptx), float(ctrlpty)] for ctrlptx, ctrlpty in zip(ctrlptsx, ctrlptsy)]
    except:
        raise ValueError('Invalid input format for control points')

    curve.ctrlpts = ctrlpts

    # Weigths are optional
    ctrlptsw = [1.0] * len(ctrlptsx)
    try:
        ctrlptsw = jsonrepr['weights'] 
        try:
            ctrlptsw = [float(ctrlptw) for ctrlptw in ctrlptsw]            
        except:
            raise ValueError('Invalid input format for weights')           
    except KeyError:
        pass

    curve.weights = ctrlptsw          

    # Knots are optional
    knots = utils.knotvector_autogen(curve.degree, len(curve.ctrlpts))
    try:
        knots = jsonrepr['knots']            
    except KeyError:
        pass

    try:
        curve.knotvector = [float(knot) for knot in knots]            
    except:
        raise ValueError('Invalid input format for knots')

    return curve