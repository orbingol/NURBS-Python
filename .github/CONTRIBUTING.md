# Contribution Guidelines

NURBS-Python (geomdl) is a free and open-source project released under [MIT License](../LICENSE).
You are always welcome to contribute!

The development started with the intentions of providing an object-oriented NURBS library in pure Python for
scientific and research purposes. The author and all the contributors volunteered their free time to develop and
improve this project, and I appreciate your time in using, developing and testing NURBS-Python (geomdl).

## Before you post, please read!

We have a nice [Code of Conduct](CODE_OF_CONDUCT.md) document and it describes pretty much everything you need to know
in the most appropriate way.

* Please be kind, respectful and reasonable in your posts
* Long posts are always appreciated and will be carefully read as long as they are related to the topic
* Horrible grammar, bad English, etc. are all okay, you will not be judged for those

It would be a nice gesture to open a new issue and discuss what you are planning to add/change before starting to code.

## What happens when you found a bug

* Read __Before You Post__ rules (right above)
* Make sure that you are using the latest version on the `master` (or `devmaster` if exists) branch
* Include all details and steps to reproduce the problem

## Coding Standards

The following is the list of cpdong standards you are expected to follow when developing for the
[Core Library](http://nurbs-python.readthedocs.io/en/latest/modules.html).

* Implement using pure python code, i.e. no compilable code, including C/C++ code using Python's C API, Cython, etc.
* For the core library (e.g. algorithms, geometrical operations), only use the modules that come with Python's standard library. Please note that NumPy, SciPy, etc. **are not** included in the standard library.
* The code should be compatible with Python versions 2.7.x, 3.4+ and higher.
* It is acceptable to use very well-known backporting and helper modules like [functools32](https://pypi.org/project/functools32/) only if critically necessary. These modules must be installable via `pip` on all platforms without any issues or additional requirements.
* Soft dependencies are acceptable; e.g. if some module is installed, then use the functionality. Otherwise, use a custom or simplified implementation of it.
* Please don't mix the data types (lists, tuples, arrays, etc.)
* All new code should come with the proper tests and they should be executable with `pytest`. If you are implementing alternative evaluation algorithms, then you should also include tests which compare the new algorithm(s) with the existing ones.

For new [Visualization](http://nurbs-python.readthedocs.io/en/latest/modules_visualization.html) modules or improvements
to the existing ones, the above list is still valid _with one exception_: You are free to use external libraries,
including NumPy.

It would be nice to create new modules, i.e. new Python files, for the new features you are going to implement.
You can use the following as a template for your new module:

```python
"""
.. module:: file name without the extension
    :platform: Unix, Windows
    :synopsis: Very brief description of the module

.. moduleauthor:: Your name <your@email.com>

"""

import abc
from . import abstract
from .exceptions import GeomdlException
from ._utilities import export, add_metaclass


@export
def exported_function(arg1, **kwargs):
    """ Brief explanation of the function's purpose

    Detailed explanation

    Keyword Arguments:
        *
        *

    :param arg1: description of the parameter
    :type arg1: type of the parameter (int, float, etc.)
    """
    # Code here
    pass


def not_exported_function():
    """ Function description """
    pass


@add_metaclass(abc.ABCMeta)
class NewAbstractClass(abstract.Geometry):
    """ Abstract class"""
    def __init__(self, **kwargs):
        super(NewAbstractClass, self).__init__(**kwargs)

    @abc.abstractmethod
    def my_method(self, *args, **kwargs):
        """ Docstrings """
        pass


@export
class ImpClass(NewAbstractClass):
    """ Extended from the abstract class """
    def __init__(self, **kwargs):
        super(ImpClass, self).__init__(**kwargs)

    def my_method(self, *args, **kwargs):
        # Implementation of the abstract method
        pass
```

## Pull requests

It is suggested to [create pull requests](https://help.github.com/articles/creating-a-pull-request/)
against relevant branch as described on the [wiki page](https://github.com/orbingol/NURBS-Python/wiki).

CI tools are set to test every pull request. The test results will become accessible in a short while under the
pull request page. If your code does not follow the standards as described under **Coding Standards** section, your PR
will not be considered for review at all.

I would appreciate if you could run a Python linter utility, e.g. `prospector`, and clean the warnings in the code
before opening the pull request.

All your changes will be reviewed and if they are accepted, they will be merged to the `master` branch in the next
subsequent release of NURBS-Python and your name will be added to the [CONTRIBUTORS](../CONTRIBUTORS.rst) file.

Feel free to open a ticket on the project issue tracker, if you have any questions.

## Tests

The `tests/` directory includes all automated tests. Implementing more tests that could validate the algorithms and
increase the code coverage are appreciated. All included tests are designed to run with
[pytest](https://pypi.org/project/pytest/).

## Documentation

Any contribution would be great, including the ones for the [NURBS-Python documentation](http://nurbs-python.readthedocs.io/en/latest/).
The latest development version of the documentation can be found [here](https://nurbs-python.readthedocs.io/en/devmaster/).
The documentation can be compiled using [Sphinx](https://pypi.org/project/Sphinx/). Please refer to the Sphinx
documentation for more details.

The repository is connected to [Read the Docs](https://readthedocs.org/) service.
Please refer to the [configuration file](https://github.com/orbingol/NURBS-Python/blob/master/.readthedocs.yml)
in the project repository and [Read the Docs documentation](https://docs.readthedocs.io/en/latest/) for details.

-----

As always, all contributions, including constructive comments, ideas, code improvements and tests are much appreciated.

Thanks in advance!
