# Contribution Guidelines

NURBS-Python is a free and open-source project released under [MIT License](../LICENSE). You are always welcome to 
contribute to NURBS-Python and it could happen in many ways!

The development started with the intentions of providing an object-oriented NURBS library in pure Python for 
scientific and research purposes. The author and all the contributors volunteered their free time to develop and 
improve this project, and I appreciate your time in using, developing and testing NURBS-Python.

Before you post, I would like to recommend some resources for starters:

* [Code of Conduct](CODE_OF_CONDUCT.md)
* [README file](../README.rst)
* [LICENSE file](../LICENSE)
* [Official Documentation](http://nurbs-python.readthedocs.io/en/latest/)
* [The NURBS Book](http://www.springer.com/gp/book/9783642973857)


## Before you post, please read!

We have a nice [Code of Conduct](CODE_OF_CONDUCT.md) document and it describes pretty much everything you need to know
in the most appropriate way.

In addition, it would be good to remember the following:

* Please be kind, respectful and reasonable in your posts
* Long posts are always appreciated and will be carefully read as long as they are related to the topic
* Horrible grammar, bad English, etc. are all okay, you will not be judged for these

The following will **NOT** be tolerated in any way:

* Any sort of offensive and harmful behavior or tone in writing, including, but not limited to, contempt, anger, hate, sarcasm in explicit and/or implicit ways
* Improperly opened tickets on the issue tracker (e.g. no body, no title, unrelated talk)
* Any kind of behavior against [Code of Conduct](CODE_OF_CONDUCT.md)

## What happens when you found a bug

* Read __Before You Post__ rules (right above)
* Make sure that you are using the latest version on the `master` (or `devmaster` if exists) branch
* Include all details and steps to reproduce the problem

## Coding Standards

You must follow the standards below when developing for the
[Core Library](http://nurbs-python.readthedocs.io/en/latest/modules.html) without any exceptions.

* Implement using pure python code, i.e. no compilable code, including C/C++ code using Python's C API, Cython, etc.
* For the core library (e.g. algorithms, geometrical operations), only use the modules that come with Python's standard library. Please note that NumPy, SciPy, etc. **are not** included in the standard library.
* The code should be compatible with Python versions 2.7.x, 3.3.5+ and above all together.
* It is acceptable to use very well-known backporting and helper modules like [functools32](https://pypi.org/project/functools32/) only if critically necessary. These modules must be installable via `pip` on all platforms without any issues or additional requirements.
* Soft dependencies are acceptable; e.g. if some module is installed, then use the functionality. Otherwise, use a custom or simplified implementation of it.
* Please don't mix the data types (lists, tuples, arrays, etc.)
* The Python 2 and 3 compatibility library [six](https://pypi.org/project/six/) is added as a project dependency and will be installed during the package installation. You may use it freely, if it is required.
* All new code should come with the proper tests and they should be executable with `pytest`. If you are implementing alternative evaluation algorithms, then you should also include tests which compare the new algorithm(s) with the existing ones.

For new [Visualization](http://nurbs-python.readthedocs.io/en/latest/modules_visualization.html) modules or improvements
to the existing ones, the above list is still valid _with one exception_: You are free to use external libraries,
including NumPy. You don't need to add them to `setup.py` as direct install requirements but you may add them under 
`visualization` package list in `extras_require` argument. Please note that all new Visualization modules should extend
the [Visualization Base](http://nurbs-python.readthedocs.io/en/latest/module_vis_abstract.html) classes and should
include classes capable of visualization of surfaces and 2- and 3-dimensional curves.

I would be glad if you could follow these standards while developing for NURBS-Python. Failure to follow may cause
rejection of your contributions (as pull requests or other methods).

## Feature requests

It could be always possible to add new features and the same rules are effective as if you have found a bug.
**I would be very much glad if you could directly develop the new features and make a pull request
instead of asking me to implement them** :)

## Pull requests

It would be suggested to [create pull requests](https://help.github.com/articles/creating-a-pull-request/)
against relevant branch as descibed below:

* NURBS-Python v4.x, PR against `devmaster` (`master`, if it does not exist)
* NURBS-Python v3.x, PR against `3.x-dev` (`3.x`, if it does not exist)
* NURBS-Python v2.x is not maintained anymore

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
