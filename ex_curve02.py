# -*- coding: utf-8 -*-

"""
    Examples for the NURBS-Python Package
    Released under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2017
"""

from nurbs import Curve as ns
from nurbs import utilities as utils
from matplotlib import pyplot as plt

# Create a NURBS curve instance
curve = ns.Curve()

# Set up the NURBS curve
curve.read_ctrlpts("data\CP_Curve2.txt")
#curve.read_json("data\CP_Curve2.json")
curve.degree = 3
# Auto-generate the knot vector
curve.knotvector = utils.knotvector_autogen(curve.degree, len(curve.ctrlpts))

# Evaulate curve
curve.evaluate()

# Arrange curve points for plotting
curvepts_x = []
curvepts_y = []
for pt in curve.curvepts:
    curvepts_x.append(pt[0])
    curvepts_y.append(pt[1])

# Calculate curve tangent at u = 0.6
curvetan = curve.tangent(0.6)

# Extract slope
slope = curvetan[1][1] / curvetan[1][0]
# Increment is used to determine the line size
increment = 5.0
# We know the first point, ders[0], and we need the second point to draw the tangent line
new_x = curvetan[0][0] + increment
# Find y-point corresponding to the x-point "new_x"
new_y = (slope * (new_x - curvetan[0][0])) + curvetan[0][1]

# Arrange tangent vector for plotting
tanlinepts_x = [curvetan[0][0], new_x]
tanlinepts_y = [curvetan[0][1], new_y]

# Plot using Matplotlib
plt.figure(figsize=(10.67, 8), dpi=96)
curveplt, = plt.plot(curvepts_x, curvepts_y, "r-")
tanline, = plt.plot(tanlinepts_x, tanlinepts_y, "b-")
plt.legend([curveplt, tanline], ["Evaluated Curve", "Tangent Line (u=0.6)"])
plt.show()

print("End of NURBS-Python Example")
