"""
.. module:: _convert
    :platform: Unix, Windows
    :synopsis: Helper functions for convert module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

# Initialize an empty __all__ for controlling imports
__all__ = []


def convert_curve(incrv, outtype):
    outcrv = outtype.Curve()
    outcrv.degree = incrv.degree
    outcrv.ctrlpts = incrv.ctrlpts
    outcrv.knotvector = incrv.knotvector
    return outcrv


def convert_surface(insrf, outtype):
    outsrf = outtype.Surface()
    outsrf.degree_u = insrf.degree_u
    outsrf.degree_v = insrf.degree_v
    outsrf.ctrlpts_size_u = insrf.ctrlpts_size_u
    outsrf.ctrlpts_size_v = insrf.ctrlpts_size_v
    outsrf.ctrlpts = insrf.ctrlpts
    outsrf.knotvector_u = insrf.knotvector_u
    outsrf.knotvector_v = insrf.knotvector_v
    return outsrf


def convert_volume(invol, outtype):
    outvol = outtype.Volume()
    outvol.degree_u = invol.degree_u
    outvol.degree_v = invol.degree_v
    outvol.degree_w = invol.degree_w
    outvol.ctrlpts_size_u = invol.ctrlpts_size_u
    outvol.ctrlpts_size_v = invol.ctrlpts_size_v
    outvol.ctrlpts_size_w = invol.ctrlpts_size_w
    outvol.ctrlpts = invol.ctrlpts
    outvol.knotvector_u = invol.knotvector_u
    outvol.knotvector_v = invol.knotvector_v
    outvol.knotvector_w = invol.knotvector_w
    return outvol
