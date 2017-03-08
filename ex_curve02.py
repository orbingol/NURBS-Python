# -*- coding: utf-8 -*-

from nurbs import Curve as ns
from nurbs import utilities as utils
from matplotlib import pyplot as plt

# Create a NURBS curve instance
curve = ns.Curve()

# Set up the NURBS curve
curve.read_ctrlpts("data\CP_Curve2.txt")
curve.degree = 3
# Auto-generate the knot vector
curve.knotvector = utils.autogen_knotvector(curve.degree, len(curve.ctrlpts))

# Evaulate curve
curve.evaluate()

# Arrange curve points for plotting
curvepts_x = []
curvepts_y = []
for pt in curve.curvepts:
    curvepts_x.append(pt[0])
    curvepts_y.append(pt[1])

# Find tangent vector at u = 0.8
tanvec = curve.tangent(0.05, 5.0)

# Arrange tangent vector for plotting
tanlinepts_x = [tanvec[0][0], tanvec[1][0]]
tanlinepts_y = [tanvec[0][1], tanvec[1][1]]

# Plot using Matplotlib
plt.figure(figsize=(10.67, 8), dpi=96)
curveplt, = plt.plot(curvepts_x, curvepts_y, "r-")
tanline, = plt.plot(tanlinepts_x, tanlinepts_y, "b-")
plt.legend([curveplt, tanline], [" Calculated Curve", "Tangent Line"])
plt.show()

print("End of NURBS-Python Example")
