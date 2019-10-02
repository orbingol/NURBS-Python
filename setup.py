#!/usr/bin/env python

# NURBS-Python - Copyright (c) 2016-2018 Onur Rauf Bingol
# geomdl - Copyright (c) 2018-2019 Onur Rauf Bingol
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import setup
from setuptools import Extension
from setuptools.command.install import install as install_command
from setuptools.command.test import test as test_command
from distutils.command.clean import clean as clean_command
import sys
import os
import re
import shutil

# Global variables to control generation of optional Cython-compiled library core module
BUILD_FROM_CYTHON = False
BUILD_FROM_SOURCE = False


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


# Implemented from http://stackoverflow.com/a/41110107
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


class InstallCommand(install_command):
    """ Overrides pip install command to control generation of optional Cython-compiled library core module """
    user_options = install_command.user_options + [
        ('use-cython', None, 'Cythonize and compile geomdl.core'),
        ('use-source', None, 'Compile geomdl.core from the source files'),
        ('core-only', None, 'Compile and install geomdl.core only'),
    ]

    def initialize_options(self):
        install_command.initialize_options(self)
        self.use_cython = 0
        self.use_source = 0

    def finalize_options(self):
        install_command.finalize_options(self)

    def run(self):
        global BUILD_FROM_CYTHON, BUILD_FROM_SOURCE
        BUILD_FROM_CYTHON = True if self.use_cython > 0 else False
        BUILD_FROM_SOURCE = True if self.use_source > 0 else False
        install_command.run(self)


# Reference: https://docs.pytest.org/en/latest/goodpractices.html
class PyTest(test_command):
    """ Allows test command to call py.test """
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        test_command.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


class SetuptoolsClean(clean_command):
    """ Cleans Cython-generated source files and setuptools-generated directories """
    def run(self):
        # Call parent method
        clean_command.run(self)

        # Clean setuptools-generated directories
        st_dirs = ['dist', 'build', 'geomdl.egg-info', 'geomdl.core.egg-info']

        print("Removing setuptools-generated directories")
        for d in st_dirs:
            d_path = os.path.join(os.path.dirname(__file__), d)
            shutil.rmtree(d_path, ignore_errors=True)

        # Find list of files with .c extension
        flist_c, flist_c_path = read_files("geomdl", ".c")

        # Clean files with .c extensions
        if flist_c_path:
            print("Removing Cython-generated source files with .c extension")
            for f in flist_c_path:
                f_path = os.path.join(os.path.dirname(__file__), f)
                os.unlink(f_path)

        # Find list of files with .cpp extension
        flist_cpp, flist_cpp_path = read_files("geomdl", ".cpp")

        # Clean files with .cpp extensions
        if flist_cpp_path:
            print("Removing Cython-generated source files with .cpp extension")
            for f in flist_cpp_path:
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
        if os.path.isfile(f_path) and f.endswith(ext) and f != "__init__.py":
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


def make_dir(project):
    """ Creates the project directory for compiled modules. """
    project_path = os.path.join(os.path.dirname(__file__), project)
    # Delete the directory and the files inside it
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
    # Create the directory
    os.mkdir(project_path)
    # We need a __init__.py file inside the directory
    with open(os.path.join(project_path, '__init__.py'), 'w') as fp:
        fp.write('__version__ = "' + str(get_property('__version__', 'geomdl')) + '"\n')
        fp.write('__author__ = "' + str(get_property('__author__', 'geomdl')) + '"\n')
        fp.write('__license__ = "' + str(get_property('__license__', 'geomdl')) + '"\n')


def in_argv(arg_list):
    """ Checks if any of the elements of the input list is in sys.argv array. """
    for arg in sys.argv:
        for parg in arg_list:
            if parg == arg or arg.startswith(parg):
                return True
    return False


# Define setup.py commands to activate Cython compilation
possible_cmds = ['install', 'build', 'bdist']

# Use geomdl.core package only
if "--core-only" in sys.argv:
    package_name = "geomdl.core"
    package_dir = "geomdl/core"
    packages = []
    sys.argv.remove('--core-only')
    sys.argv.append('--use-cython')
else:
    package_name = package_dir = "geomdl"
    packages = ['geomdl', 'geomdl.visualization']

# geomdl.core compilation
# Ref: https://gist.github.com/ctokheim/6c34dc1d672afca0676a

# Use already Cythonized C code
if in_argv(possible_cmds) and '--use-source' in sys.argv:
    BUILD_FROM_SOURCE = True
    sys.argv.remove('--use-source')

# Use Cython to (re)generate C code (overrides "--use-source")
if in_argv(possible_cmds) and '--use-cython' in sys.argv:
    # Try to import Cython
    try:
        from Cython.Build import cythonize
    except ImportError:
        raise ImportError("Cython is required for this step. Please install it via 'pip install cython'")

    BUILD_FROM_CYTHON = True
    BUILD_FROM_SOURCE = False
    sys.argv.remove('--use-cython')

# We don't want to include any compiled files with the distribution
ext_modules = []

if BUILD_FROM_CYTHON or BUILD_FROM_SOURCE:
    # Choose the file extension
    file_ext = '.py' if BUILD_FROM_CYTHON else '.c'

    # Create Cython-compiled module directory
    make_dir('geomdl/core')

    # Create extensions
    optional_extensions = []
    fnames, fnames_path = read_files('geomdl', file_ext)
    for fname, fpath in zip(fnames, fnames_path):
        temp = Extension('geomdl.core.' + str(fname), sources=[fpath])
        optional_extensions.append(temp)

    # Call Cython when "python setup.py build_ext --use-cython" is executed
    if BUILD_FROM_CYTHON:
        ext_modules = cythonize(optional_extensions, compiler_directives={'language_level': sys.version_info[0]})

    # Compile from C source when "python setup.py build_ext --use-source" is executed
    if BUILD_FROM_SOURCE:
        ext_modules = optional_extensions

    # Add Cython-compiled module to the packages list
    packages.append('geomdl.core')

# Input for setuptools.setup
data = dict(
    name=package_name,
    version=get_property('__version__', package_dir),
    description=get_property('__description__', package_dir),
    long_description=read('DESCRIPTION.rst'),
    license=get_property('__license__', package_dir),
    author=get_property('__author__', package_dir),
    author_email='nurbs-python@googlegroups.com',
    url='https://github.com/orbingol/NURBS-Python',
    keywords=get_property('__keywords__', package_dir),
    packages=packages,
    install_requires=[],
    tests_require=['pytest>=3.6.0'],
    cmdclass={'install': InstallCommand, 'test': PyTest, 'clean': SetuptoolsClean},
    ext_modules=ext_modules,
    zip_safe=False,
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
