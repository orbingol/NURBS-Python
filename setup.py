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

    The "setuptools" package comes installed by default with the official Python.org distribution and in all "conda"
    environments. On the other hand, it might require an update. You may update your "setuptools" package using
    the following command:

    pip install setuptools --upgrade

    After installing "pip", you may also consider installing NURBS-Python (geomdl) via "pip install geomdl".
"""

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import os
import re


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


# Implemented from http://stackoverflow.com/a/41110107
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


# Reference: https://docs.pytest.org/en/latest/goodpractices.html
class PyTest(TestCommand):
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


setup(
    name='geomdl',
    version=get_property('__version__', 'geomdl'),
    description='NURBS curve and surface evaluation library in pure python',
    author='Onur Rauf Bingol',
    author_email='contact@onurbingol.net',
    license='MIT',
    url='https://github.com/orbingol/NURBS-Python',
    packages=['geomdl', 'geomdl.visualization', 'geomdl.shapes'],
    extras_require={
        'visualization': ['matplotlib', 'plotly'],
    },
    tests_require=["pytest"],
    cmdclass={"test": PyTest},
    long_description=read('DESCRIPTION.rst'),
    keywords='NURBS B-Spline curve surface CAD modeling visualization',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    project_urls={
        'Documentation': 'http://nurbs-python.readthedocs.io/',
        'Source': 'https://github.com/orbingol/NURBS-Python',
        'Tracker': 'https://github.com/orbingol/NURBS-Python/issues',
    },
)
