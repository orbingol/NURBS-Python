# -*- coding: utf-8 -*-

from nurbs import Curve as ns
from nurbs import utilities as utils
from matplotlib import pyplot as plt

# Create a NURBS curve instance
curve = ns.Curve()

# Set up the NURBS curve
curve.read_ctrlpts("data\CP_Curve1.txt")
curve.degree = 4
# Auto-generate the knot vector
curve.knotvector = utils.autogen_knotvector(curve.degree, len(curve.ctrlpts))

# Calculate curve points
curve.calculatew()

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
plt.figure(figsize=(10.67, 8), dpi=96)
cppolygon, = plt.plot(ctrlpts_x, ctrlpts_y, "k-.")
curveplt, = plt.plot(curvepts_x, curvepts_y, "r-")
plt.legend([cppolygon, curveplt], ["Control Points Polygon", "Calculated Curve"])
plt.show()

print("End of NURBS-Python Example")
