# geomdl Changelog

## v5.2.6 released on 2019-05-21

* Fixed imports in `control_points` module

## v5.2.5 released on 2019-05-21

* Improved `linalg` module 
* Added `control_points` module for managing control points
* Bug fixes and improvements
* Documentation updates

## v5.2.4 released on 2019-04-22

* Reduced set control points restrictions for surfaces. `Surface.set_ctrlpts` now accepts 2-dimensional control points.
* Deprecated `save` and `load` methods defined in `BSpline` module in favor of `import_json` and `export_json`
* Generalized `operations.add_dimension` API call to work with all `SplineGeometry` subclasses
* Documentation updates

## v5.2.3 released on 2019-04-19

* Fix incorrect dict export of trims in trimmed surfaces
* Add analytic trim curve support to trimmed surface dict export
* Change `VolumeContainer` base class from `SurfaceContainer` to `AbstractContainer` and add missing methods
* Documentation updates
* Minor bug fixes and improvements

## v5.2.2 released on 2019-04-17

* Convert "sense" to "reversed" for better understanding of trim curve orientation (API change for surface trimming)
* Update curve degree elevation and reduction algorithms and operations API (no API change)
* Fix trim curve exporting in `exchange.export_json`
* Deprecate `exchange.export_3dm` and `exchange.import_3dm` in favor of [rw3dm v2.0](https://github.com/orbingol/rw3dm)
* Documentation updates

## v5.2.1 released on 2019-03-25

* Minor refactoring in `elements` module (no API change)
* Visualization figure objects are now accessible outside the geometry classes, `render` method returns the figure object
* `vertex_spacing` is set to 1 for consistency between the exchange and visualization modules
* `vertices` property of the `Surface` class returns the exact list of vertices used in generation of the triangles
* Minor bug fixes
* Documentation updates

## v5.2.0 released on 2019-03-22

* Moved some `six` module functions and `backports_functools_lru_cache` module under *geomdl* directory
* Removed `typing` dependency (no time to add all typing hints, see docs for input and output types)
* Refactored imports, minimized internal dependencies
* Code rearrangement for some internal functions
* Refactored `operations` module (no API change)
* Updated `multi` module
* Updated `elements` module to make it consistent between its classes (minor API change)
* Improved dict-type file formats (JSON, YAML, CFG) to support trim curves and more (backwards compatible)
* Updated `exchange_vtk.export_polydata` to support tessellated surfaces and geometry containers
* Refactored `tessellation` module (internal API change, user API is the same and comes with improvements)
* Added `tessellate.QuadTessellate` class
* Added `==` and `!=`operators to `SplineGeometry` classes
* Added `freeform` module
* Improved the surface trimming algorithm to handle edge cases
* Added `trimming` module to fix different types of trim curves (open, multi-curve, etc.)
* Added an option to set trim curve sense; i.e. `sense = 0` means trim inside, `sense = 1` means trim outside
* Improved VTK visualization module to better handle surface and volume plots
* Added voxel visualization option to VTK visualization module
* Registered mode keypress events to VTK visualization module
* Added an option to generate custom visualization configuration while generating the visualization object
* General bug fixes and performance improvements
* Added more tests
* Documentation updates

## v5.1.2 released on 2019-02-28

* Updated surface derivative algorithm to fill the return array completely
* Fixed variable initialization issue causing warnings during cython compilation

## v5.1.1 released on 2019-02-26

* Fixed a bug while computing the surface derivative

## v5.1.0 released on 2019-02-25

* Added `alpha` configuration directive to `VisMPL` to control opacity of the evaluated points
* Added knot refinement operation: `operations.refine_knotvector()`
* Minor bug fixes and coding improvements
* Documentation updates

## v5.0.3 released on 2019-02-22

* Fixed CI config which was failing to generate `geomdl.core` binaries for v5.0.2 and version bumped for user convenience

## v5.0.2 released on 2019-02-22

* Removed dependency `enum34` since it was causing problems with Python 3
* Fixed some minor bugs

## v5.0.1 released on 2019-02-22

* Fix an issue in setup.py causing generation of an incompatible wheel for Python 2.7
* conda-build configuration updates
* Documentation updates

## v5.0.0 released on 2019-02-21

* Includes all updates from v5.0b1 to v5.0b7
* Added knot removal for spline volumes
* Added `operations.degree_operations` function for degree elevation and reduction (still WIP)
* Added more surface decomposition options to `operations.decompose_surface` function
* Minor coding improvements and fixes
* Documentation updates

## v5.0b7 released on 2019-02-17

* Fixed a critical bug in smesh and vmesh importers
* Added an option to change knot insertion and removal algorithms in the geometry classes
* Documentation updates

## v5.0b6 released on 2019-02-16

* Added `exchange.import_obj` function
* Added knot removal, degree elevation and degree reduction algorithms
* Simplified evaluator API to make implementations easier
* Added `knotvector` module
* Added surface trimming algorithm
* Minor bug fixes and compatibility updates
* Documentation updates

## v5.0b5 released on 2019-01-17

* Minor API updates and fixes
* Added more convenience methods to spline geometry classes
* Minor fixes and updates in `exchange` module
* Documentation updates
* Added volume support to dict-based import and exports, i.e. cfg, yaml, json
* Updated CI configurations
  * Added CircleCI support for automation of deployment to PyPI, Anaconda Cloud and Docker Hub
  * Updated TravisCI support to use tox and tox environments
  * Updated AppVeyor support to generate Cython-compiled versions of geomdl as artifacts
* Added support for star imports, i.e. `from geomdl import *`

## v5.0b4 released on 2018-12-31

* Added `abstract.Geometry` and `abstract.SplineGeometry` classes
* Improved `multi` module reusability
* Added animate option to visualization component
* Minor bug fixes and staability improvements
* Documentation updates

## v5.0b3 released on 2018-12-28

* Added [Jinja2](http://jinja.pocoo.org/) template support to JSON, YAML and CFG importers
* Documentation updates and bug fixes

## v5.0b2 released on 2018-12-26

* Added `construct.extract_isosurface` function
* Updated `VisVTK` module
* Updated `vis.VisAbstract` class
* Minor fixes and updates

## v5.0b1 released on 2018-12-21

* Simplified `abstract` module and moved all abstract classes to their relevant modules
* Removed `curvept` and `surfpt` methods. Use `evaluate_single` instead.
* Added an option to enable/disable knot vector normalization. Initialize the class with `normalize_kv=False` to disable knot vector normalization.
* Added B-spline and NURBS volume support with visualization, `BSpline.Volume` and `NURBS.Volume`
* Refactored `convert` module to improve reusability and add support to volumes
* Refactored `exchange` module to improve reusability
* Rhino file export and import options, `export_3dm` and, `import_3dm` in `exchange` module
* Added `exchange.export_vmesh` for exporting NURBS volumes
* Add Jinja2 template support for `exchange.import_txt`
* Update the name of `utilities.check_uv` function to `utilities.check_params`
* Refactored `utilities` module and moved some functions to `linalg` module
* `VisMPL.VisSurfTriangle` is now an alias for `VisMPL.VisSurface`
* `fitting` module for curve and surface global interpolation + approximation (fitting)
* `construct` module for constructing surfaces and volumes + extracting surfaces and curves
* `linalg` module (generated by splitting `utilities` module)
* `VisVoxel` and `VisVolume` classes for volume visualization
* `VisVTK` visualization module

## v4.4.4 released on 2018-12-20

* Fix PyPI description

## v4.4.3 released on 2018-12-20

* Prepare for NURBS-Python v5 release

## v4.4.2 released on 2018-12-18

* Fix bugs in `export_csv` and `export_smesh` functions

## 4.4.1 released on 2018-11-15

* Updated Cython-compiled module location for more convenient binary package generation
* Major documentation update with more examples and API descriptions
* Added DockerFiles

## v4.4.0 released on 2018-11-10

* Added and updated import and export methods. Unfortunately, this update breaks .cfg exports prior to v4.4.x; therefore, you might need to re-export your .cfg exports.
  * `export_cfg`, `import_cfg`
  * `export_yaml`, `import_yaml`
  * `export_json`, `import_json`
* `exchange` module code optimizations

## v4.3.8 released on 2018-11-08

* Fixed a bug in bounding box computation
* Added bounding box plotting option to the visualization module (still WIP)

## v4.3.7 released on 2018-11-07

* Added `bbox` property to `Multi`-type classes
* Documentation updates

## v4.3.6 released on 2018-11-04

* Added `evalpts` property to `Multi` type of classes
* Updated conda-build recipe

## v4.3.5 released on 2018-11-03

* Updated `delta` and `sample_size` properties of `MultiCurve` and `MultiSurface` classes. They are now compatible with `Curve` and `Surface` classes.
* Added `exchange.export_yaml` function (experimental, designed to be used with [geomdl_cli](https://github.com/orbingol/geomdl-cli))
* Updated conda-build recipe
* Minor bug fixes
* Documentation updates

## v4.3.4 released on 2018-11-01

* Updated `operations.translate()` function to make it compatible with multi curves and surfaces
* Added conda-build recipe

## v4.3.3 released on 2018-10-31

* Fixed a typo in evaluated points definition of `VisMPL.VisSurfWireframe()` class
* Documentation updates

## v4.3.2 released on 2018-10-19

* Hodograph curve and surface computation: `operations.derivative_curve()` and `operations.derivative_surface()`
* LU-Factorization and Forward-Backward Substitution functions in `utilities` module
* Documentation update for compiling the package with Cython
* Added `axes_equal` and `evalpts` keyword arguments to visualization config class
* Added `set_plot_type` method to surface visualization classes
* Documentation updates
* Minor code improvements

## v4.3.1 released on 2018-10-06

* Fixed a bug causing Plotly surface visualization module to show extra lines
* Added `exchange.export_smesh()` function
* Minor bug fixes and documentation updates

## v4.3.0 released on 2018-10-01

* Added `Tessellate` class for customization of the surface tessellation algorithms
* Basic trimmed surface support (still work in progress)
* Updated `elements` module
* Visualization module improvements and added support for displaying trim curves for surfaces
* Added `evaluate_single` and `evaluate_list` methods
* Updated default evaluation delta to 0.01
* Minor bug fixes, algorithm and performance improvements

## v4.2.2 released on 2018-09-11

* Fixed a bug causing incorrect alignment of control points that generate the hills in the surface generator module
* Surface generator now generates more smooth hills
* Added an option to change the label on the visualization legend by setting the ``name`` property
* Updated ``Multi.MultiCurve`` and ``Multi.MultiSurface`` constructors to allow easy addition of the shapes to the container object

## v4.2.1 released on 2018-09-08

This release adds the functionality of finding control points involved in the evaluation of a curve/surface at the
specified parameter(s) using `operations.find_ctrlpts()`.

* Added `operations.find_ctrlpts()` function
* Minor improvements in the surface evaluation algorithm

## v4.2.0 released on 2018-09-07

This release moves some of the features from `BSpline` module to other modules since it is getting bigger and it has a lot of responsibilities which can be "globalized" to ease extensibility.

* Code reorganization and cleanup for Curve and Surface classes
* Removed plural-named methods, such as `tangents`, `normals`, etc and moved the functionality to singular methods (`normal`, `tangent`, etc.)
* Moved `translate`, `split` and `decompose` methods to `operations` module
* `derivatives` method is added as an abstract method to `Abstract.Curve` and `Abstract.Surface` since it is also a requirement for all `Evaluator` implementations. 

The following new and updated features are added with this release:

* New module: `operations`, it contains geometric operations that can be applied to curves and surfaces
* Added libconfig-type file export feature to `exchange` module
* Updated triangulation functions
* Updated `elements` module
* Updated `VisMPL.VisSurfTriangle()` class to use `utilities.make_triangle_mesh()` for triangulation
* Added colormap input to `VisMPL.VisSurfTriangle()` class
* Fixed deprecation errors for Plotly >= 3.0.0
* Added new vector and point operations to `utilities` module

## v4.1.0 released on 2018-07-31

* Added algorithms A2.4, A2.5, A3.7 and A3.8
* Added an option to generate knot vectors for unclamped shapes
* Bug fixes and minor updates
* Documentation updates

## v4.0.2 released on 2018-07-09

* Bug fix: Fixed an inconsistent behavior while setting `delta` and `sample_size` properties

## v4.0.1 released on 2018-07-08

* Bug fix: Use `six` package to maintain Python 2 and 3 interoperability for meta classes
* Bug fix: Updated `order` property for curves and `order_u`, `order_v`, `delta` properties for surfaces by removing excess conditional checks from their setters
* Updated error messages
* Updated documentation
* Updated tests
* Various minor updates and bug fixes

## v4.0.0 released on 2018-07-04

This is the official release of NURBS-Python (geomdl) v4.0.0. The following list summarizes the new and the updated features.

* Added [Plotly](https://plot.ly/python/) visualization module
* Improved algorithms
* Reorganized `exchange` module and added new export file types
* Export to file and no window options for the Visualization component
* NURBS module now allows setting control points and weights separately
* Load and save functionality
* New `Evaluator` module for changing evaluation algorithms at runtime
* New `convert` module for converting B-Spline objects to NURBS objects
* Improved the surface generator module
* Added more examples to the Examples repository: https://github.com/orbingol/NURBS-Python_Examples
* Documentation updates and improvements: http://nurbs-python.readthedocs.io/
* Bug fixes, code cleaning and compatibility updates
* New unit and function tests with [codecov.io](https://codecov.io/gh/orbingol/NURBS-Python) integration

## v4.0b10 released on 2018-07-03

* Fix a bug in surface generator causing miscalculation of the grid boundaries when users add padding via `base_adjust` argument
* Renamed surface control points row order changing functions (flipping)
* Updated smesh file importing API calls
* Minor updates in error messages and exceptions
* Documentation updates

## v4.0b9 released on 2018-07-02

* Bug fix release for Surface Generator module

## v4.0b8 released on 2018-07-01

* Bug fix release (surface generator)

## v4.0b7 released on 2018-07-01

* `NURBS.ctrlptsw` now returns a tuple
* Algorithm and compatibility updates to surface grid generator
* Add more tests

## v4.0b6 released on 2018-06-29

* Fixed an issue which causes figure display problems during rendering curves and surfaces in `Multi`-type classes
* Coding improvements in `utilities` module
* Added more tests, increasing the code coverage to 47%

## v4.0b5 released on 2018-06-22

* New feature: Exporting plots as image files
* Documentation: Added [exporting plots](http://nurbs-python.readthedocs.io/en/latest/visualization_export.html) section with code examples
* Documentation: Updated [load-save](http://nurbs-python.readthedocs.io/en/latest/load_save.html) section with some code examples

## v4.0b4 released on 2018-06-20

* Bug fix: The sample generator function was not considering the starting value

## v4.0b3 released on 2018-06-16

* `exchange` module updates
* Documentation updates

## v4.0b2 released on 2018-06-14

* Several bug fixes and compatibility updates
* Documentation updates

## v4.0b1 released on 2018-06-04

This is the first **beta version** of NURBS-Python v4.x series. 

* Updated `NURBS` class control points / weights getters and setters
* Rearranged / updated some functions and properties to clean up the `BSpline` and `NURBS` class structure
* Control points reading and CSV export functionality are moved to `exchange` module
* Added more tests
* Updated examples
* Evaluation algorithms speed improvements

* Added [Plotly](https://plot.ly/python/) visualization module
* Updated documentation and added more details
* Added new export file formats
* Added B-Spline to NURBS converters

4.x update might break `NURBS` class API a little bit due to the updates in getters and setters but the fix would be very easy: Please see the `ctrlptsw` and `ctrlpts` properties for details.

## v3.7.8 released on 2018-06-04

* Minor updates

## v3.7.7 released on 2018-05-06

* Minor update related to generating a python source package

## v3.7.6 released on 2018-05-03

* `VisMPL` module displays all figures in the correct aspect ratio

## v3.7.5 released on 2018-04-26

* Bug fix release

## v3.7.4 released on 2018-04-26

* Fixed a bug when `_reset_ctrlpts` function resets the bounding box

## v3.7.3 released on 2018-04-25

* Bug fix release

## v3.7.2 released on 2018-04-20

* Bug fix release

## v3.7.1 released on 2018-04-19

* Removed unnecessary evaluations while setting `sample_size` and `delta` properties.

## v3.7.0 released on 2018-04-19

* Added `delta_u` and `delta_v` properties to Surface classes. This change allows different sampling in u- and v-directions
* Fixed some bugs related to `sample_size` property
* Replaced `delta` with `sample_size` in Multi classes. `sample_size` property directly corresponds to `num` argument in [numpy.linspace](https://docs.scipy.org/doc/numpy/reference/generated/numpy.linspace.html) function.

These changes may cause a small API break in your existing code, especially if you are visualizing using the `geomdl.visualization.VisMPL` component.
Please see the examples repository and check any example for the updated usage scenarios.

## v3.6.7 released on 2018-04-07

* Added `sample_size` property.

`sample_size` works very similar to `numpy.linspace`. In `numpy.linspace`, you define start and end positions with the number or samples to generate between them.
This property automatically sets the `delta` property, so after setting `sample_size`, there is no need to play with `delta`.

## v3.6.6 released on 2018-04-04

* Bug fixes and compatibility updates
* Added new tests

## v3.6.5 released on 2018-03-29

* Added Object File Format (OFF) export support to `exchange` module

## v3.6.4 released on 2018-03-28

* Code reorganization
* Bug fixes

## v3.6.3 released on 2018-03-18

* Updated NURBS module to have an extensible variable cache
* Minor bug fixes

## v3.6.2 released on 2018-03-14

* Fixed a bug in Multi module `render` method which fails to work after `VisMPL` update.
* Fixed a bug in `frange` function which sometimes fails to generate correct output with bigger delta values

## v3.6.1 released on 2018-03-09

* Bug fixes

## v3.6.0 released on 2018-03-06

The new version comes with performance improvements and documentation updates.
It also adds `bbox` property for evaluation and storage of curve and surface bounding box.

## v3.5.3 released on 2018-02-24

* Minor improvements

## v3.5.2 released on 2018-02-23

* Bug fixes and improvements

## v3.5.1 released on 2018-02-23

* Performance improvements

## v3.5.0 released on 2018-02-23

* `compatibility` module
* Performance improvements
* Compatibility fixes and updates
* Documentation updates
* Code reorganization (no API break)

## v3.4.7 released on 2018-02-21

* `compatibility` module enhancements

## v3.4.6 released on 2018-02-21

* Removed super restrictive knot vector checks
* Improvements in curve/surface evaluation functions

## v3.4.4 released on 2018-02-19

* Performance improvements

## v3.4.3 released on 2018-02-19

* Bug fixes
* Documentation updates

## v3.4.2 released on 2018-02-18

* Added `compatibility` module for control points manipulation
* Updated documentation

## v3.4.1 released on 2018-02-16

* Added remove axes option to Matplotlib visualization module
* Added `translate` wrapper to abstract Multi class

## v3.4.0 released on 2018-02-15

* Code clean-up and reorganization
* Bug fixes

## v3.3.2 released on 2018-02-14

* Bug fix release

## v3.3.1 released on 2018-02-13

* Fixed a point of failure in VisCurve3D when it takes a 2D input instead of a 3D one

## v3.3.0 released on 2018-02-12

* Save surfaces as .stl file
* Surface and curve splitting
* Surface and curve Bézier decomposition
* Surface and curve translate by a vector functionality

## v3.2.2 released on 2018-02-09

* Added an option to save .stl files in binary format

## v3.2.1 released on 2018-02-09

* Fixed some bugs in `exchange` module
* Fixed some bugs in `utilities` module
* Added experimental _Export surfaces as .stl_ support, with `exchange.save_stl()`

## v3.2.0 released on 2018-02-09

* The core library now utilizes `Abstract` and `Multi` modules
* Curve classes now have `split()` method for curve splitting at the given parameter and `decompose()` method for Bézier decomposition
* Shapes module upgrades

## v3.1.4 released on 2018-02-08

* Added `decompose` method to curve classes for applying Bézier decomposition
* Added `add_list` method to `Multi` module

## v3.1.3 released on 2018-02-08

* Minor bug fixes
* Added `translate()` function to curve classes

## v3.1.2 released on 2018-02-07

* Fix a control points copy error in `insert_knot()` methods
* Increased stability of `generate_knot_vector()` function
* Some other minor fixes in `exchange` module
* `save_obj` can save single or multiple surfaces to a single .obj file
* Curve and Curve2D classes have a new method, `split()`. This method splits the curve and returns 2 new instances as the split pieces of the initial curve. It doesn't modify the initial curve.
* `Multi` module is designed to operate on multiple curves and surfaces. Currently, it can only do multi curve and multi surface visualization (in 2D and 3D) on the same window. Documentation will come soon.
* `Abstract` module provides a base for further development of the NURBS algorithms. It will become the base class for B-Spline and NURBS curves and surfaces represented in NURBS-Python. Unfortunately, the module is still WIP and it could remain like that for a while.

## v3.1.1 released on 2018-02-03

* Performance improvements
* Documentation updates

## v3.1.0 released on 2018-02-02

This version comes with stability updates and more tests to cover the majority of the module functionality. The documentation is also improved.

* Added `exchange` module with the capability to save surfaces as .obj files
* Added `shapes` module to automatically generate well-defined NURBS curves and surfaces
* More configurable `visualization` module
* Bug and stability fixes
* Documentation updates

## v3.0.21 released on 2018-01-31

* Bug fix release

## v3.0.20 released on 2018-01-31

* Added new parameters to `evaluate()` functions
* Updated documentation

## v3.0.19 released on 2018-01-28

* Bug fix release

## v3.0.18 released on 2018-01-28

* Marker updates on curve and surface plots
* Fixed a PyPI glitch

## v3.0.17 released on 2018-01-28

* Fixed a problem with surface setters (no API break)
* Visualization module updates
* Added more tests

## v3.0.15 released on 2018-01-26

* Added `utilities.vector_generate` function
* Fixed some compatibility issues (related to future releases)

## v3.0.14 released on 2018-01-26

* Bug fixes in `make_triangle`
* Add `VisSurface` class to visualization module

## v3.0.13 released on 2018-01-26

* Added `make_triangle` function
* Updated visualization module

## v3.0.12 released on 2018-01-24

* Minor updates

## v3.0.10 released on 2018-01-23

* Bug fix release

## v3.0.9 released on 2018-01-22

* PyPI description update (requires version bump)
* Minor updates and bug fixes

## v3.0.8 released on 2018-01-21

* Reorganize and update Matplotlib visualization component, `VisMPL`

Please note that updates to `VisMPL` component might cause a small API break on the visualization module, and therefore it is marked as experimental from now on. Updates to visualization component do not affect NURBS evaluation components.

Currently, `VisMPL` has the following classes:

* `VisCurve2D` for 2D curves
* `VisCurve3D` for 3D curves
* `VisSurfWireframe` for surfaces (uses `plot_wireframe` function)
* `VisSurfTriangle` for surfaces (uses `plot_trisurf` function)
* `VisSurfScatter` for surfaces (uses 3D `scatter` function)

## v3.0.7 released on 2018-01-19

* Added checks to knot vector assignments
* Added 'tangents', 'normals' and 'binormals' methods to Curve classes
* Added 'tangents' and 'normals' methods to Surface classes
* A new example added to documentation

## v3.0.6 released on 2018-01-17

* `normal` method of the `Surface` type classes has been updated. It now returns a list containing 2 elements. First one is the starting point (or origin) of the normal vector and the second one is the normal vector itself.
* Added `normal` and `binormal` methods to the `Curve` and `Curve2D` type classes
* Minor fixes to the inline documentation
* Visualization figure updates

## v3.0.5 released on 2018-01-14

* Bug fixes in `Surface` classes
* Added tests
* AppVeyor and Travis-CI integration
* Documentation updates
* Style updates and code reformatting after pylint

## v3.0.4 released on 2018-01-12

* Bug fixes
* Documentation updates

## v3.0.3 released on 2018-01-12

* Documentation updates

## v3.0.2 released on 2018-01-11

* Minor updates to `VisMPL`, a visualization module which implements Matplotlib
* Documentation updates

## v3.0.1 released on 2018-01-11

* Version bump for fixing issues on Python Package Index (PyPI).

## v2.3.8 released on 2018-01-11

* Version bump for Python Package Index (PyPI) upload.

## v3.0.0 released on 2018-01-10

* Initial stable release of NURBS-Python v3.0.0
* Added the library to Python Package Index (PyPI).

## v3.0b3 released on 2018-01-09

* Bug fixes
* Update visualization component

## v3.0b2 released on 2018-01-08

* Added visualization module.

Visualization module is an optional module for NURBS-Python. In other words, you don't need to import it to evaluate surfaces and curves.

The visualization module currently includes a base class `VisABC` which can be used to create new visualization components, and `VisMPL` component that implements [Matplotlib](https://matplotlib.org/) for 2D and 3D plotting.

Please see the following  for usage examples:

* [ex_curve01.py](https://github.com/orbingol/NURBS-Python_Examples/blob/master/curve2d/ex_curve01.py) - 2D Curve
* [ex_curve3d01.py](https://github.com/orbingol/NURBS-Python_Examples/blob/master/curve3d/ex_curve3d01.py) - 3D curve
* Surface visualization component is also complete but currently there are no examples. Please check the [examples repository](https://github.com/orbingol/NURBS-Python_Examples) for more details.

## v3.0b1 released on 2018-01-07

This is the first beta release of NURBS-Python after a huge set of new features and updates. Unfortunately, there has been some API changes between _v2.x_ and _v3.x_ series but these changes are not too big, so you might only need to change the import statements to make things working again.

The _v2.x_ code is moved to `2.x` branch. This version will not receive any updates, since I would like to focus on _v3.x_ branch from now on.

* Please check the README file and the [documentation](http://nurbs-python.readthedocs.io/en/latest/) for changes in the implementation. I updated the class structure and now the code has different classes for 2D and 3D curves. I also added different classes for B-Spline (NUBS) and NURBS implementations of curves and surfaces.
* There are more file reading and writing routines, such as different types of TXT formats and CSV export for using the data for various visualization software.
* Of course, new version fixes some of the bugs and reorganizes the code
* The documentation is reorganized and vastly improved: http://nurbs-python.readthedocs.io/en/latest/ -- You can still access _v2.x_ series documentation [here](http://nurbs-python.readthedocs.io/en/2.x/).
* __New functionality:__ Knot insertion in curves and surfaces
* JSON support (will be extended/merged from the existing branch)
* An optional visualization module using [Matplotlib](https://matplotlib.org/). Visualization module can be extended to use other visualization tools.
* New CSV and TXT export modes
* Documentation improvements and more examples

The examples repository is also updated with some nice visualization examples using Matplotlib and demonstrating new TXT and CSV export features.
Please check it out here: https://github.com/orbingol/NURBS-Python_Examples

## v2.3.6 released on 2018-01-07

* Added `order` property

## v2.3.5.1 released on 2017-09-03

* Minor updates in documentation
* Moved examples to a different repository

## v2.3.5 released on 2017-06-20

* Bug fixes

## v2.3.4 released on 2017-05-19

* Fixed a bug in `Curve::evaluate_rational()` method which causes erroneous NURBS curve evaluation
* Added a new NURBS curve example (ex_curve04.py) on evaluation of a full circle
* Documentation updates

## v2.3.3 released on 2017-05-11

* Documentation updates for the [ReadTheDocs](http://nurbs-python.readthedocs.io/en/latest/) page

## v2.3.2 released on 2017-05-10

* Added `rotate_x` and `rotate_y` functions to the Grid class
* Updated documentation
* Minor bug fixes

## v2.3.1 released on 2017-05-09

* Added `read_ctrlptsw()` method to the `Curve` class
* Some minor documentation updates

## v2.3.0 released on 2017-05-09

* Added a 2D grid generator
* Minor bug fixes
