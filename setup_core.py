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
from setuptools import Extension
from distutils.command.clean import clean as clean_command
import sys
import os
import re
import shutil
import textwrap
from Cython.Build import cythonize


# List of packages to be compiled
packages = [
    'geomdl.core',
    'geomdl.core.algorithms',
    'geomdl.core.evaluators',
    'geomdl.core.examples',
    'geomdl.core.exchange',
    'geomdl.core.fitting',
    'geomdl.core.geomutils',
    'geomdl.core.tessellate',
    'geomdl.core.voxelate'
]


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


# Implemented from http://stackoverflow.com/a/41110107
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


class CleanCommand(clean_command):
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


        for p in packages:
            # Fix paths
            p_split = p.split('.')
            if len(p_split) == 2:
                dir_name = p_split[0]
            else:
                dir_name = p_split[0] + "/" + p_split[2]

            # Find list of files with .c extension
            flist_c, flist_c_path = read_files(dir_name, '.c')

            # Clean files with .c extensions
            if flist_c_path:
                for f in flist_c_path:
                    f_path = os.path.join(os.path.dirname(__file__), f)
                    os.unlink(f_path)

            # Find list of files with .cpp extension
            flist_cpp, flist_cpp_path = read_files(dir_name, '.cpp')

            # Clean files with .cpp extensions
            if flist_cpp_path:
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
        fp.write('__keywords__ = "' + str(get_property('__keywords__', 'geomdl')) + '"\n')


# Prepare for cythonize
exts = []
for p in packages:
    # Create Cython-compiled module directory
    make_dir(p.replace('.', '/'))

    # Fix paths
    p_split = p.split('.')
    if len(p_split) == 2:
        dir_name = p_split[0]
    else:
        dir_name = p_split[0] + "/" + p_split[2]

    # Create extensions
    fnames, fnames_path = read_files(dir_name, '.py')
    for fname, fpath in zip(fnames, fnames_path):
        temp = Extension(p + '.' + str(fname), sources=[fpath])
        exts.append(temp)


# Input for setuptools.setup
data = dict(
    name='geomdl.core',
    version=get_property('__version__', 'geomdl/core'),
    description="Cython-compiled version of geomdl",
    long_description=textwrap.dedent("""\
        Cython-compiled version of NURBS-Python (geomdl)
    """),
    license=get_property('__license__', 'geomdl/core'),
    author=get_property('__author__', 'geomdl/core'),
    author_email='nurbs-python@googlegroups.com',
    url='https://github.com/orbingol/NURBS-Python',
    keywords=get_property('__keywords__', 'geomdl/core'),
    packages=[],
    install_requires=['cython'],
    tests_require=['pytest>=3.6.0'],
    cmdclass={'clean': CleanCommand},
    ext_modules=cythonize(exts, compiler_directives={'language_level': sys.version_info[0]}),
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
