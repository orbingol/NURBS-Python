"""
.. module:: _mp
    :platform: Unix, Windows
    :synopsis: Helper functions for multiprocessing support

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from contextlib import contextmanager
from multiprocessing import Pool


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
