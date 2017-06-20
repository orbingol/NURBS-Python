# -*- coding: utf-8 -*-

"""
    Examples for the NURBS-Python Package
    Released under MIT License
    Developed by Onur Rauf Bingol (c) 2017
"""

from nurbs import Curve as ns
from nurbs import utilities as utils
from matplotlib import pyplot as plt

# Create a NURBS curve instance
curve = ns.Curve()

# The full circle with NURBS
#curve.read_ctrlptsw("data\CPw_Curve4.txt")
#curve.read_json("data\CPw_Curve4.json")
curve.degree = 2
# Use a specialized knot vector
curve.knotvector = [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]

# Calculate NURBS curve points
curve.evaluate_rational()

# Arrange control points for plotting
ctrlpts_x = []
ctrlpts_y = []
for pt in curve.ctrlpts:
    ctrlpts_x.append(pt[0])
    ctrlpts_y.append(pt[1])

# Arrange curve points for plotting
curvepts_x = []
curvepts_y = []
for pt in curve.curvepts:
    curvepts_x.append(pt[0])
    curvepts_y.append(pt[1])

# Plot using Matplotlib
plt.figure(figsize=(8, 8), dpi=96)
cppolygon, = plt.plot(ctrlpts_x, ctrlpts_y, "k-.")
curveplt, = plt.plot(curvepts_x, curvepts_y, "r-")
plt.legend([cppolygon, curveplt], ["Control Points Polygon", "Evaluated Curve"])
plt.show()

print("End of NURBS-Python Example")
