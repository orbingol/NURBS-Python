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


def add_metaclass(metaclass):
    """ Class decorator for creating a class with a metaclass.

    Taken from ``six`` library version 1.12.0. Copyright (c) 2010-2018 Benjamin Peterson.
    ``six`` is licensed under the terms of MIT License.

    Please refer to the following GitHub repository for details: https://github.com/benjaminp/six

    :param metaclass: metaclass
    """
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        if hasattr(cls, '__qualname__'):
            orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


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
