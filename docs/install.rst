Installation and Testing
^^^^^^^^^^^^^^^^^^^^^^^^

**Installation via pip or conda is the recommended method for all users.**
Manual method is only recommended for advanced users. Please note that if you have used any of these methods to install
NURBS-Python, please use the same method to upgrade to the latest version.

.. note::

    On some Linux and MacOS systems, you may encounter 2 different versions of Python installed. In that case Python 2.x
    package would use ``python2`` and ``pip2``, whereas Python 3.x package would use ``python3`` and ``pip3``. The
    default ``python`` and ``pip`` commands could be linked to one of those. Please check your installed Python version
    via ``python -V`` to make sure that you are using the correct Python package.

Install via Pip
===============

The easiest method to install/upgrade NURBS-Python is using `pip <https://pip.pypa.io/en/stable/>`_. The following
commands will download and install NURBS-Python from `Python Package Index <https://pypi.org/project/geomdl>`_.

.. code-block:: console

    $ pip install geomdl

Upgrading to the latest version:

.. code-block:: console

    $ pip install geomdl --upgrade

Installing a specific version:

.. code-block:: console

    $ pip install geomdl==5.0.0

Install via Conda
=================

NURBS-Python can also be installed/upgraded via `conda <https://conda.io/>`_ package manager from the
`Anaconda Cloud <https://anaconda.org/orbingol/geomdl>`_ repository.

Installing:

.. code-block:: console

    $ conda install -c orbingol geomdl

Upgrading to the latest version:

.. code-block:: console

    $ conda upgrade -c orbingol geomdl

If you are experiencing problems with this method, you can try to upgrade ``conda`` package itself before
installing the NURBS-Python library.

Manual Install
==============

The initial step of the manual install is cloning the repository via ``git`` or downloading the ZIP archive from the
`repository page <https://github.com/orbingol/NURBS-Python>`_ on GitHub. The package includes a *setup.py* script
which will take care of the installation and automatically copy/link the required files to your Python distribution's
*site-packages* directory.

The most convenient method to install NURBS-Python manually is using ``pip``:

.. code-block:: console

    $ pip install .

To upgrade, please pull the latest commits from the repository via ``git pull --rebase`` and then execute the above
command.

Development Mode
================

The following command enables development mode by creating a link from the directory where you cloned NURBS-Python
repository to your Python distribution's *site-packages* directory:

.. code-block:: console

    $ pip install -e .

Since this command only generates a link to the library directory, pulling the latest commits from the repository
would be enough to update the library to the latest version.

Checking Installation
=====================

If you would like to check if you have installed the package correctly, you may try to print ``geomdl.__version__``
variable after import. The following example illustrates installation check on a Windows PowerShell instance::

    Windows PowerShell
    Copyright (C) Microsoft Corporation. All rights reserved.

    PS C:\> python
    Python 3.6.2 (v3.6.2:5fd33b5, Jul  8 2017, 04:57:36) [MSC v.1900 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import geomdl
    >>> geomdl.__version__
    '4.0.2'
    >>>

Testing
=======

The package includes ``tests/`` directory which contains all the automated testing scripts.
These scripts require `pytest <https://pytest.readthedocs.io/en/latest>`_ installed on your Python distribution.
Then, you can execute the following from your favorite IDE or from the command line:

.. code-block:: console

    $ pytest

pytest will automatically find the tests under ``tests/`` directory, execute them and show the results.

Compile with Cython
===================

To improve performance, the :doc:`Core Library <modules>` of NURBS-Python can be compiled and installed using the
following command along with the pure Python version.

.. code-block:: console

    $ pip install . --install-option="--use-cython"

This command will generate .c files (i.e. cythonization) and compile the .c files into binary Python modules.

The following command can be used to directly compile and install from the existing .c files, skipping the cythonization
step:

.. code-block:: console

    $ pip install . --install-option="--use-source"

To update the compiled module with the latest changes, you need to re-cythonize the code.

To enable Cython-compiled module in development mode;

.. code-block:: console

    $ python setup.py build_ext --use-cython --inplace

After the successful execution of the command, the you can import and use the compiled library as follows:

.. code-block:: python
    :linenos:

    # Importing NURBS module
    from geomdl.core import NURBS
    # Importing visualization module
    from geomdl.visualization import VisMPL as vis

    # Creating a curve instance
    crv = NURBS.Curve()

    # Make a quadratic curve
    crv.degree = 2

    #######################################################
    # Skipping control points and knot vector assignments #
    #######################################################

    # Set the visualization component and render the curve
    crv.vis = vis.VisCurve3D()
    crv.render()

Before Cython compilation, please make sure that you have `Cython <https://cython.org/>`_ module and a valid compiler
installed for your operating system.

Docker Containers
=================

A collection of Docker containers is provided on `Docker Hub <https://hub.docker.com/r/idealabisu/nurbs-python/>`_
containing NURBS-Python, Cython-compiled core and the `command-line application <https://geomdl-cli.readthedocs.io>`_.
To get started, first install `Docker <https://www.docker.com/>`_ and then run the following on the Docker command
prompt to pull the image prepared with Python v3.5:

.. code-block:: console

    $ docker pull idealabisu/nurbs-python:py35

On the `Docker Repository <https://hub.docker.com/r/idealabisu/nurbs-python/>`_ page, you can find containers tagged for
Python versions and `Debian <https://www.debian.org/>`_ (no suffix) and `Alpine Linux <https://alpinelinux.org/>`_
(``-alpine`` suffix) operating systems. Please change the tag of the pull command above for downloading your preferred
image.

After pulling your preferred image, run the following command:

.. code-block:: console

    $ docker run --rm -it --name geomdl -p 8000:8000 idealabisu/nurbs-python:py35

In all images, Matplotlib is set to use ``webagg`` backend by default. Please follow the instructions on the command
line to view your figures.

Please refer to the `Docker documentation <https://docs.docker.com/>`_ for details on using Docker.
