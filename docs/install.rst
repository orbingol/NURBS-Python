Installation and Testing
^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    **You should remove NURBS-Python v2.x and v3.x before installing any version of v4.x.**
    Uninstalling packages via pip is as easy as executing ``pip uninstall NURBS-Python``.
    However, installation via ``setup.py`` requires manual removal of the packages from Python's ``site-packages``
    directory. Directories to delete: *nurbs* and/or *geomdl*.

**Installation via pip is the recommended method for all users.** Manual method is only recommended for advanced users.

Install via Pip
===============

You can find the NURBS-Python library on `Python Package Index <https://pypi.org/project/geomdl>`_ and easily install
via `pip <https://pip.pypa.io/en/stable/>`_.

``pip install geomdl``

Upgrading to the latest version:

``pip install geomdl --upgrade``

Manual Install
==============

Included *setup.py* script will take care of the installation and automatically copy the required files to
*site-packages* directory. Please run the following from the command line:

``python setup.py install``

If you don't want to put the files into your Python distribution's *site-packages* directory for some reason (e.g.
make extension development, bug fixing or testing easy), you can run

``python setup.py develop``

from the command line to generate a link to the package directory inside *site-packages*.

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
After installing the required packages, execute the following from your favorite IDE or from the command line:

``pytest``

pytest will automatically find the tests under ``tests/`` directory, execute them and show the results.
