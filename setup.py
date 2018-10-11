#!/usr/bin/env python

"""
    NURBS-Python (geomdl) Setup Script
    NURBS-Python is released under the MIT License. Copyright (c) Onur Rauf Bingol.

    The setup script directly depends on "setuptools" package and it does not fallback to "distutils" which might
    cause issues on some Python distributions, especially on the embedded distributions.

    To solve this issue, you may want to start with installing "pip" using the "get_pip.py" script
    from the following link if it doesn't exist on your distribution:

    https://pip.pypa.io/en/stable/installing/

    Then, you may install "setuptools" package using the following command:

        pip install setuptools

    "setuptools" is a collection of enhancements to the Python's "distutils" package. You may check its documentation
    from the following link:

    http://setuptools.readthedocs.io/en/latest/setuptools.html#command-reference

    It also comes installed by default with the official Python.org distribution and in all "conda" environments.
    On the other hand, it might require an update. You may update your "setuptools" package using the following command:

        pip install setuptools --upgrade

    or

        conda update setuptools

    depending on the package manager that you are using.

    After installing "pip", you may also consider installing NURBS-Python (geomdl) via "pip install geomdl" or
    alternatively, you may use "conda" package on https://anaconda.org/orbingol/geomdl
"""

from setuptools import setup
from setuptools import Extension
from setuptools.command.test import test as TestCommand
from distutils.command.clean import clean
import sys
import os
import re
import shutil


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


# Implemented from http://stackoverflow.com/a/41110107
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


# Reference: https://docs.pytest.org/en/latest/goodpractices.html
class PyTest(TestCommand):
    """ Allows test command to call py.test """
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


class CythonClean(clean):
    """ Adds cleaning option for Cython generated .c files inside the module directory. """
    def run(self):
        # Call parent method
        clean.run(self)

        # Find list of files with .c extension
        flist, flist_path = read_files("cython_temp", ".c")

        # Clean files with .c extensions
        if flist_path:
            print("Removing Cython-generated source files")
            for f in flist_path:
                f_path = os.path.join(os.path.dirname(__file__), f)
                os.unlink(f_path)


def read_files(project, ext):
    """ Reads files inside the input project directory. """
    project_path = os.path.join(os.path.dirname(__file__), project)
    file_list = os.listdir(project_path)
    flist = []
    flist_path = []
    for f in file_list:
        f_path = os.path.join(project_path, f)
        if os.path.isfile(f_path) and f.endswith(ext):
            flist.append(f.split('.')[0])
            flist_path.append(f_path)
    return flist, flist_path


def copy_files(src, ext, dst):
    """  Copies files with extensions "ext" from "src" to "dst" directory. """
    src_path = os.path.join(os.path.dirname(__file__), src)
    dst_path = os.path.join(os.path.dirname(__file__), dst)
    file_list = os.listdir(src_path)
    for f in file_list:
        if f == '__init__.py':
            continue
        f_path = os.path.join(src_path, f)
        if os.path.isfile(f_path) and f.endswith(ext):
            shutil.copy(f_path, dst_path)


def make_dir(project, gen_init_py=True):
    """ Creates the project directory for compiled modules. """
    project_path = os.path.join(os.path.dirname(__file__), project)
    # Delete the directory and the files inside it
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
    # Create the directory
    os.mkdir(project_path)
    # We need a __init__.py file inside the directory
    if gen_init_py:
        with open(os.path.join(project_path, '__init__.py'), 'w') as fp:
            fp.write('__version__ = "' + str(get_property('__version__', 'geomdl')) + '"\n')
            fp.write('__license__ = "MIT"\n')


# Cython and compiled C module options
# Ref: https://gist.github.com/ctokheim/6c34dc1d672afca0676a
if '--use-source' in sys.argv:
    USE_SOURCE = True
    sys.argv.remove('--use-source')
else:
    USE_SOURCE = False

if '--use-cython' in sys.argv:
    # Try to import Cython
    try:
        from Cython.Build import cythonize
    except ImportError:
        raise ImportError("Cython is required for this step. Please install it via 'pip install cython'")

    USE_CYTHON = True
    sys.argv.remove('--use-cython')
    # Prepare files for compilation
    make_dir('cython_temp', gen_init_py=False)
    copy_files('geomdl', 'py', 'cython_temp')
else:
    USE_CYTHON = False

# We don't want to include any compiled files with the distribution
extensions = []

if USE_CYTHON or USE_SOURCE:
    # Choose the file extension
    file_ext = '.py' if USE_CYTHON else '.c'

    # Create Cython-compiled module directory
    make_dir('geomdl_core')

    # Create extensions
    optional_extensions = []
    fnames, fnames_path = read_files('cython_temp', file_ext)
    for fname, fpath in zip(fnames, fnames_path):
        temp = Extension('geomdl_core.' + str(fname), sources=[fpath])
        optional_extensions.append(temp)

    # Call Cython when "python setup.py build_ext --use-cython" is executed
    if USE_CYTHON:
        extensions = cythonize(optional_extensions)

    # Compile from C source when "python setup.py build_ext --use-source" is executed
    if USE_SOURCE:
        extensions = optional_extensions

# Add Enum type support for Python versions < 3.4
if sys.version_info[:2] < (3, 4):
    required = ['enum34']
else:
    required = []

data = dict(
    name='geomdl',
    version=get_property('__version__', 'geomdl'),
    description='Object-oriented B-Spline and NURBS evaluation library',
    long_description=read('DESCRIPTION.rst'),
    license='MIT',
    author='Onur Rauf Bingol',
    author_email='nurbs-python@googlegroups.com',
    url='https://github.com/orbingol/NURBS-Python',
    keywords='NURBS B-Spline curve surface CAD modeling visualization surface-generator',
    packages=['geomdl', 'geomdl.visualization', 'geomdl.shapes'],
    install_requires=['six>=1.9.0'] + required,
    extras_require={
        'visualization': ['matplotlib', 'plotly'],
    },
    tests_require=["pytest>=3.0.0"],
    cmdclass={"test": PyTest, 'clean': CythonClean},
    ext_modules=extensions,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    project_urls={
        'Documentation': 'http://nurbs-python.readthedocs.io/',
        'Source': 'https://github.com/orbingol/NURBS-Python',
        'Tracker': 'https://github.com/orbingol/NURBS-Python/issues',
    },
)


if __name__ == '__main__':
    setup(**data)
