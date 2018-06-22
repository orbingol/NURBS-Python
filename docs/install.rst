Installation and Testing
^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    **You should remove NURBS-Python v2.x and v3.x before installing any version of v4.x.**
    Uninstalling packages via pip is as easy as executing ``pip uninstall NURBS-Python``.
    However, installation via ``setup.py`` requires manual removal of the packages from Python's ``site-packages``
    directory. Directories to delete: *nurbs* and/or *geomdl*.

**Installation via pip or conda is the recommended method for all users.**
Manual method is only recommended for advanced users.

Install via Pip
===============

You may find NURBS-Python on `Python Package Index <https://pypi.org/project/geomdl>`_ and install
via `pip <https://pip.pypa.io/en/stable/>`_.

``pip install geomdl``

Upgrading to the latest version:

``pip install geomdl --upgrade``

Install via Conda
=================

For your convenience, NURBS-Python has also been uploaded to `Anaconda Cloud <https://anaconda.org/orbingol/geomdl>`_.
You may use `conda <https://conda.io/>`_ package manager to install and/or upgrade NURBS-Python.

To install:

``conda install -c orbingol geomdl``

To upgrade:

``conda upgrade -c orbingol geomdl``

If you are experiencing problems with this method, you can try to upgrade ``conda`` package itself before
installing the NURBS-Python library.

Manual Install
==============

Included *setup.py* script will take care of the installation and automatically copy/link the required files to
your Python distribution's *site-packages* directory. First, you need to clone the repository to your computer.

The following command will copy NURBS-Python package to your Python distribution's *site-packages* directory:

``python setup.py install``

If you don't prefer copying for some reason (e.g. extension development, bug fixing and/or testing), you may run the
following from the command line to generate a link to the directory where you cloned NURBS-Python package inside your
Python distribution's *site-packages* directory:

``python setup.py develop``

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
    '3.6.1'
    >>>

Testing
=======

The package includes ``tests/`` directory which contains all the automated testing scripts.
These scripts require `pytest <https://pytest.readthedocs.io/en/latest>`_ installed on your Python distribution.
After installing the required packages, you may execute the following from your favorite IDE or from the command line:

``pytest``

pytest will automatically find the tests under ``tests/`` directory, execute them and show the results.
