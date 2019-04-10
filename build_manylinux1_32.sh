#!/bin/bash

# Builds "manylinux1" packages for geomdl
# Setup Docker: http://support.divio.com/local-development/docker/how-to-use-a-directory-outside-cusers-with-docker-toolboxdocker-for-windows
# Run Docker: docker run -it -v /home/docker/projects:/io quay.io/pypa/manylinux1_i686 /bin/bash

MODULE_NAME="geomdl"
PLATFORM_NAME="linux_i686"
PYTHON_VERSIONS="cp27-cp27m cp35-cp35m cp36-cp36m cp37-cp37m"
GIT_TAG_FULL=`git describe --tags`
GIT_TAG="${GIT_TAG_FULL:1}"

for pyver in $PYTHON_VERSIONS
do
  /opt/python/$pyver/bin/pip install cython
  /opt/python/$pyver/bin/python setup.py bdist_wheel --use-cython
  auditwheel repair dist/$MODULE_NAME-$GIT_TAG-$pyver-$PLATFORM_NAME.whl
  /opt/python/$pyver/bin/python setup.py clean --all
done
