# This file is necessary only for cython builds

from setuptools import setup
from setuptools import Extension
import os
import sys
import pathlib

# Allows command: SETUPTOOLS_USE_CYTHON=1 pip install -e .
USE_CYTHON = os.getenv("SETUPTOOLS_USE_CYTHON", "0") == "1"


def read_files(project: str, ext: str):
    project_path = pathlib.Path(__file__).resolve().parent / project
    relative_path = pathlib.Path(project)
    flist = []
    flist_path = []
    for file in project_path.iterdir():
        if file.is_file() and file.suffix == ext and file.name != "__init__.py":
            flist.append(file.stem)
            flist_path.append(str(relative_path / file.name))
    return flist, flist_path


# We don't want to include any compiled files with the distribution
ext_modules = []

if USE_CYTHON:
    # Set file extension
    file_ext = ".py"

    # Create module directory
    pathlib.Path("geomdl/core").mkdir(exist_ok=True)
    pathlib.Path("geomdl/core/__init__.py").touch(exist_ok=True)

    # Create extensions
    optional_extensions = []
    fnames, fnames_path = read_files("geomdl", file_ext)
    for fname, fpath in zip(fnames, fnames_path):
        temp = Extension("geomdl.core." + str(fname), sources=[fpath])
        optional_extensions.append(temp)

    # Run cython
    from Cython.Build import cythonize

    ext_modules = cythonize(
        optional_extensions, compiler_directives={"language_level": sys.version_info[0]}, build_dir="build"
    )

# Run setuptools
setup(ext_modules=ext_modules)
