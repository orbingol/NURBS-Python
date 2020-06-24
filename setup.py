#!/usr/bin/env python

# NURBS-Python (geomdl) - Copyright (c) 2016-2020 Onur Rauf Bingol
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
from setuptools.command.test import test as test_command
from distutils.command.clean import clean as clean_command
import sys
import os
import re
import shutil


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


# Ref: http://stackoverflow.com/a/41110107
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


# Ref: https://docs.pytest.org/en/latest/goodpractices.html
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


# Input for setuptools.setup
data = dict(
    name="geomdl",
    version=get_property('__version__', "geomdl"),
    description=get_property('__description__', "geomdl"),
    long_description=read('DESCRIPTION.rst'),
    license=get_property('__license__', "geomdl"),
    author=get_property('__author__', "geomdl"),
    author_email='nurbs-python@googlegroups.com',
    url='https://github.com/orbingol/NURBS-Python',
    keywords=get_property('__keywords__', "geomdl"),
    packages=[
        'geomdl',
        'geomdl.algorithms',
        'geomdl.evaluators',
        'geomdl.examples',
        'geomdl.exchange',
        'geomdl.fitting',
        'geomdl.geomutils',
        'geomdl.visualization'
    ],
    install_requires=[],
    tests_require=['pytest>=3.6.0'],
    cmdclass={'test': PyTest, 'clean': SetuptoolsClean},
    ext_modules=[],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha'
        #'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    project_urls={
        'Documentation': 'http://nurbs-python.readthedocs.io/',
        'Source': 'https://github.com/orbingol/NURBS-Python',
        'Tracker': 'https://github.com/orbingol/NURBS-Python/issues',
    },
)


if __name__ == '__main__':
    setup(**data)
