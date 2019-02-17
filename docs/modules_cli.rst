Command-line Application
^^^^^^^^^^^^^^^^^^^^^^^^

You can use NURBS-Python (geomdl) with the command-line application `geomdl-cli <https://pypi.org/project/geomdl.cli/>`_.
The command-line application is designed for automation and input files are highly customizable using
`Jinja2 <http://jinja.pocoo.org/>`_ templates.

``geomdl-cli`` is highly extensible via via the configuration file. It is very easy to generate custom commands as well as
variables to change behavior of the existing commands or independently use for the custom commands. Since it runs inside
the user's Python environment, it is possible to create commands that use the existing Python libraries and even integrate
NURBS-Python (geomdl) with these libraries.

Installation
============

The easiest method to install is via ``pip``. It will install all the required modules.

.. code-block: console

    $ pip install geomdl.cli

Please refer to `geomdl-cli documentation </projects/cli>`_ for more installation options.

Documentation
=============

``geomdl-cli`` has a very detailed `online documentation </projects/cli>`_ which describes the usage and customization
options of the command-line application.

References
==========

* **PyPI**: https://pypi.org/project/geomdl.cli
* **Documentation**: https://geomdl-cli.readthedocs.io
* **Development**: https://github.com/orbingol/geomdl-cli
