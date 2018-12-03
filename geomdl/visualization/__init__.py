""" Visualization Modules for NURBS-Python

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

__author__ = "Onur Rauf Bingol"
__version__ = "1.0.0"
__license__ = "MIT"


try:
    import numpy as np
except ImportError:
    print("Visualization modules require a working installation of Numerical Python (NumPy)")
    exit(0)
