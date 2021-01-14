#!/bin/bash

# Builds "manylinux2014" packages for geomdl
# How-to build:
#   1) Run Docker: docker run -it -v {local dir}:/project quay.io/pypa/manylinux2014_x86_64 /bin/bash
#   2) {local dir} is the directory of the geomdl project
#   3) Change directory inside container prompt: cd /project
#   4) Run script ./build_manylinux2014_x86-64.sh
#

MODULE_NAME="geomdl"
PLATFORM_NAME="linux_x86_64"
PYTHON_VERSIONS="cp36-cp36m cp37-cp37m cp38-cp38m"
GIT_TAG_FULL=`git describe --tags`
GIT_TAG="${GIT_TAG_FULL:1}"

for pyver in $PYTHON_VERSIONS
do
  /opt/python/$pyver/bin/pip install cython
  /opt/python/$pyver/bin/python setup.py bdist_wheel --use-cython
  auditwheel repair dist/$MODULE_NAME-$GIT_TAG-$pyver-$PLATFORM_NAME.whl
  /opt/python/$pyver/bin/python setup.py clean --all
done
