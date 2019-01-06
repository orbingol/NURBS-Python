"""
.. module:: _utilities
    :platform: Unix, Windows
    :synopsis: Defines internal utility functions, such as decorators, context managers and similar

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import sys
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


def export(fn):
    """ Export decorator

    Please refer to the following SO article for details: https://stackoverflow.com/a/35710527
    """
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        mod.__all__.append(fn.__name__)
    else:
        mod.__all__ = [fn.__name__]
    return fn
