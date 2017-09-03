# Contribution Guidelines

One of the major goals of this project is implementing all these algorithms with minimum dependencies. Currently, the NURBS package can run with plain Python and therefore, it has no extra dependencies, like NumPy or similar. You might want to ask why this is necessary. Even though these packages are developed to ease up computations and evaluations, I realized that it becomes cumbersome to install or figure out the issues due to faulty installation of these external dependencies for people just trying get things done as soon as possible.

## How to Contribute

I would like to introduce some rules on contributing to this Python package.

### Contribution to the code

* Please read the [README.md](README.md) file before working on the code
* All pull requests should be made to the `devmaster` branch
* If you are implementing a reading function, please use `read_PURPOSE_METHOD` convention, such as `read_ctrlpts_json`
* The inline documentation and all related .md files should be updated after adding a new method
* If you are getting confused or would like to ask something on how to implement a new feature, please email the author first and we will discuss it

### Contribution to the examples

* First of all, they are in a different repository so, please don't add any example scripts to this repository
* Please see [README.md](README.md) file for finding the repository for the examples

### Contribution in general

You don't have to contribute to the code. All new ideas, comments and requests on improving this package are welcome. Please feel free to email the author or create a new issue on the issue tracker.

Thanks in advance for your contributions and comments.
