"""
.. module:: _utilities
    :platform: Unix, Windows
    :synopsis: Defines internal utility functions, such as decorators, context managers and similar

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from contextlib import contextmanager
from multiprocessing import Pool


# Initialize an empty __all__ for controlling imports
__all__ = []


@contextmanager
def pool_context(*args, **kwargs):
    """ Context manager for multiprocessing.Pool class (for compatibility with Python 2.7.x) """
    pool = Pool(*args, **kwargs)
    try:
        yield pool
    except Exception as e:
        raise e
    finally:
        pool.terminate()
