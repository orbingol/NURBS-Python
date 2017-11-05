# Contribution Guidelines

One of the major goals of this project is implementing all these algorithms with minimum dependencies. NURBS-Python 
package has no extra dependencies, like NumPy or similar, and all code can be executed on a plain Python installation. 
You might want to ask why this is necessary. Even though these packages are developed to ease up computations and 
evaluations, I realized that it becomes cumbersome to install or figure out the issues due to faulty installation of 
these external dependencies for people just trying get things done as soon as possible.

## How to Contribute

Below introduces some rules on contributing to this package.

### Contributions to the code

* Please check [README](README.rst) file before working on the code.
* All pull requests should be made to the `devmaster` branch.
* If you are implementing a reading function, please use `read_PURPOSE_METHOD` convention, such as `read_ctrlpts_json`.
* The inline documentation and all related .md files should be updated after adding a new method.
* If you are getting confused or would like to ask something on how to implement a new feature, please email the author 
first and we will discuss it.

### Contributions to the examples

* First of all, they are in a different repository. Please don't add any example scripts to this repository.
* Please check [README](README.rst) file for finding the repository for the examples.

### Contributions in general

You don't have to contribute to the code. All new ideas, comments and requests on improving this package are welcome. 
Please feel free to email the author or create a new issue on the issue tracker.

Thanks in advance for your contributions and comments.
