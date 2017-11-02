# Non-Uniform Rational Basis Spline (NURBS) Python Package

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.815011.svg)](https://doi.org/10.5281/zenodo.815011)
 [![Documentation Status](https://readthedocs.org/projects/nurbs-python/badge/?version=latest)](http://nurbs-python.readthedocs.io/en/latest/?badge=latest)

## Introduction

This project aims to implement B-Spline (NUBS) and NURBS curve and surface computation algorithms in native Python with minimum possible dependencies.

Currently, the `Curve` and `Surface` classes can be used for data storage and evaluation of B-Spline and NURBS curves and surfaces. Additionally, `Grid` class can be used to generate simple 2D control point grids for use with the `Surface` class.

## For Researchers

I would be glad if you cite this repository using the DOI provided as a badge at the top.

## Example Scripts

Please see [NURBS-Python Examples](https://github.com/orbingol/NURBS-Python_Examples) repository for example scripts and figures.

## Algorithms Implemented

NURBS-Python currently implements the following algorithms from **The NURBS Book (2nd Edition)** by Piegl & Tiller:

* Algorithm A2.1: FindSpan (page 68)
* Algorithm A2.2: BasisFuns (page 70)
* Algorithm A2.3: DersBasisFuns (pages 72,73)
* Algorithm A3.1: CurvePoint (page 82)
* Algorithm A3.2: CurveDerivsAlg1 (page 93)
* Algorithm A3.3: CurveDerivCpts (page 98)
* Algorithm A3.4: CurveDerivsAlg2 (pages 99,100)
* Algorithm A3.5: SurfacePoint (page 103)
* Algorithm A3.6: SurfaceDerivsAlg1 (pages 111,112)
* Algorithm A4.1: CurvePoint (page 124)
* Algorithm A4.2: RatCurveDerivs (page 127)
* Algorithm A4.3: SurfacePoint (page 134)
* Algorithm A4.4: RatSurfaceDerivs (pages 137,138)
* Algorithm A5.1: CurveKnotIns (page 151)
* Algorithm A5.3: SurfaceKnotIns (pages 155-157)

## Issues and Reporting

If you have any questions or comments related to the NURBS-Python package, please don't hesitate to contact the author by email or creating a new issue.

## Author

* Onur Rauf Bingol ([@orbingol](https://github.com/orbingol))

## Contributors

* John-Eric Dufour ([@jedufour](https://github.com/jedufour)), bug fixing and contribution of surface example 3
* Jan Heczko ([@heczis](https://github.com/heczis)), bug fixing

## License

[MIT](LICENSE)

## Acknowledgments

I would like to thank my PhD adviser, [Dr. Adarsh Krishnamurthy](https://www.me.iastate.edu/faculty/?user_page=adarsh), for his guidance and supervision throughout the course of this project. If you are interested in this Python package, please have a look at [our research group's web page](http://web.me.iastate.edu/idealab/) for more projects and contact information.
