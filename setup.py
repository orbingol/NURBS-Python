try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Implemented from http://stackoverflow.com/a/41110107
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


project_name = 'nurbs'
setup(
    name='NURBS-Python',
    version=get_property('__version__', project_name),
    description='NURBS curve and surface evaluation library in native Python',
    author='Onur Rauf Bingol',
    author_email='contact@onurbingol.net',
    license='MIT',
    url='https://github.com/orbingol/NURBS-Python',
    packages=['nurbs'],
    long_description=read('DESCRIPTION.rst'),
    keywords='NURBS B-Spline curve surface CAD modeling visualization',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization'
    ]
)
