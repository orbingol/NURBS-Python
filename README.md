# NURBS Curve and Surface Calculations

## Introduction

This project aims to implement the NURBS curve and surface calculation algorithms in native Python. It currently implements the following algorithms in **The NURBS Book** by Piegl & Tiller:

* Algorithm A2.1: FindSpan
* Algorithm A2.2: BasisFuns
* Algorithm A3.1: CurvePoint
* Algorithm A3.5: SurfacePoint
* Algorithm A4.1: CurvePoint
* Algorithm A5.1: CurveKnotIns
* Algorithm A5.3: SurfaceKnotIns

Initially developed for ME 625 Surface Modeling course offered at Iowa State University in Spring 2016 semester.

## Tested under
* Windows 10 64-bit
* Anaconda3 v4.0.0 (using Python 3.5.1) from [Continuum Analytics](https://www.continuum.io/downloads)
* Matplotlib v1.5.1 (included in Anaconda)

## Contents of the repository

* `nurbs` directory includes the NURBS libraries
* `samples` directory includes sample control points for curves and surfaces
* `curve-*.py` files are testing scripts for curve calculations
* `surface-*.py` files are testing scripts for surface calculations

## Documentation style

* [Google Style Python Docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

## Author

* Onur Rauf Bingol
