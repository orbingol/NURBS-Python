# Contribution Guidelines

NURBS-Python is a free and open-source project released under [MIT License](../LICENSE). You are always welcome to 
contribute to NURBS-Python and it could happen in many ways!

The development started with the intentions of providing an object-oriented NURBS library in pure Python for 
scientific and research purposes. The author and all the contributors volunteered their free time to develop and 
improve this project, and I appreciate your time in using, developing and testing NURBS-Python.

Before you post, I would like to recommend some resources for starters:

* [Code of Conduct](CODE_OF_CONDUCT.md)
* [README file](../README.rst)
* [Official Documentation](http://nurbs-python.readthedocs.io/en/latest/)
* [The NURBS Book](http://www.springer.com/gp/book/9783642973857)


## Before you post, please read!

We have a nice [Code of Conduct](CODE_OF_CONDUCT.md) document and it describes pretty much everything you need to know
in the most appropriate way. Please see [Code of Conduct](CODE_OF_CONDUCT.md) for details.

In summary, it would be good to remember these before you post to the issue tracker or email the author:

* Remember that you are talking to humans
* Adhere to the same standards of behavior that you follow in your real life as you are talking to complete strangers
* Please be kind and respectful in your posts
* Please and please don't use stingy words or phrases
* Double-check your attitude in your posts
* Be reasonable
* Feel free to explain the problem as long as or as detailed as you would like to
* Simply, __be nice__!

The following will **NOT** be tolerated in any way:

* Any sort of offensive comment
* Contempt in explicit and/or implicit ways
* Any sort of accusation directed to the authors and/or contributors (that's why we have the LICENSE file)
* Complaints about implementation choices (instead, please ask about the reason nicely or fix it and create a PR)
* "Bad" tone in writing (i.e. please triple-check how you say what you want to say)
* A strange thought that people who read the issue tracker have ability to read your mind (happens all the time)

I would like to remind that all authors and contributors spend their free time to put some effort on development of 
this package. Their free time is as valuable as your free time, the time you spend outside of your regular work doing 
non-work and completely unrelated things. Therefore, please show some respect in your messages. Horrible grammar, 
bad English, long explanations, etc. are all okay, no worries :-)

In case of any confusions or problems, please follow [this link](http://lmgtfy.com/?q=netiquette).

## What happens when you found a bug

* Please read __Before You Post__ rules (right above)
* Please make sure that you are using the latest version on the `master` branch.
* Please try to explain the problem as much as possible. I would be glad if you could write the steps to reproduce the
issue.
* If you have used `pip` to install the package, please indicate the version that you are using.
* Did I say details are very important?

**Note:** There will be no bug fixes and updates to `v2.x` branch.

## Feature requests

It could be always possible to add new features and the same rules are effective as if you have found a bug.
**I would be very much glad if you could directly develop the new features and make a pull request
instead of asking me to implement them** :)

## Pull requests

Please [create pull requests](https://help.github.com/articles/creating-a-pull-request/) against `devmaster` branch.
CI tools are set to test every pull request, and I would appreciate if you could add tests for your changes and test
your code with a Python linter utility, e.g. `pylint` and/or `prospector`.
 
All your changes will be reviewed and if they are accepted, they will be merged to the `master` branch in the next 
subsequent release of NURBS-Python 
and your name will be added under the *Contributors* section of the [README](../README.rst) file.

Feel free to open an issue on the project issue tracker, if you have any questions.

## Tests

The project includes automated tests under `'tests/` directory and all tests are designed to run with `pytest`.
I would appreciate if you could contribute more tests to increase their code coverage.

Just to present some code coverage metrics, it was around 70% after running all the included tests and 
the examples in the [Examples Repository](https://github.com/orbingol/NURBS-Python_Examples)
at the end of January 2018 (metrics acquired with the [coverage](https://pypi.python.org/pypi/coverage) tool).

-----

As always, all contributions, such as constructive comments, ideas, code improvements and tests are much appreciated.

Thanks in advance!
