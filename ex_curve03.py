# -*- coding: utf-8 -*-

from nurbs import Curve as ns
from nurbs import utilities as utils
from matplotlib import pyplot as plt

# Create a NURBS curve instance
curve = ns.Curve()

# Set up the NURBS curve
curve.read_ctrlpts("data\CP_Curve3.txt")
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

# Arrange tangents for plotting
X = []
Y = []
U = []
V = []

# Evaluate curve tangent at u = 0.0
curvetan = curve.tangent(0.0)
nvec = utils.normalize_vector((curvetan[1][0], curvetan[1][1]))

# Arrange tangent vector for plotting
X.append(curvetan[0][0])
Y.append(curvetan[0][1])
U.append(nvec[0])
V.append(nvec[1])

# Evaluate curve tangent at u = 0.2
curvetan = curve.tangent(0.2)
nvec = utils.normalize_vector((curvetan[1][0], curvetan[1][1]))

# Arrange tangent vector for plotting
X.append(curvetan[0][0])
Y.append(curvetan[0][1])
U.append(nvec[0])
V.append(nvec[1])

# Evaluate curve tangent at u = 0.5
curvetan = curve.tangent(0.5)
nvec = utils.normalize_vector((curvetan[1][0], curvetan[1][1]))

# Arrange tangent vector for plotting
X.append(curvetan[0][0])
Y.append(curvetan[0][1])
U.append(nvec[0])
V.append(nvec[1])

# Evaluate curve tangent at u = 0.6
curvetan = curve.tangent(0.6)
nvec = utils.normalize_vector((curvetan[1][0], curvetan[1][1]))

# Arrange tangent vector for plotting
X.append(curvetan[0][0])
Y.append(curvetan[0][1])
U.append(nvec[0])
V.append(nvec[1])

# Evaluate curve tangent at u = 0.8
curvetan = curve.tangent(0.8)
nvec = utils.normalize_vector((curvetan[1][0], curvetan[1][1]))

# Arrange tangent vector for plotting
X.append(curvetan[0][0])
Y.append(curvetan[0][1])
U.append(nvec[0])
V.append(nvec[1])

# Evaluate curve tangent at u = 1.0
curvetan = curve.tangent(1.0)
nvec = utils.normalize_vector((curvetan[1][0], curvetan[1][1]))

# Arrange tangent vector for plotting
X.append(curvetan[0][0])
Y.append(curvetan[0][1])
U.append(nvec[0])
V.append(nvec[1])

# Arrange control points for plotting
ctrlpts_x = []
ctrlpts_y = []
for pt in curve.ctrlpts:
    ctrlpts_x.append(pt[0])
    ctrlpts_y.append(pt[1])

# Plot using Matplotlib
plt.figure(figsize=(10.67, 8), dpi=96)
yaxis = plt.plot((-1, 25), (0, 0), "k-")  # y-axis line
cppolygon, = plt.plot(ctrlpts_x, ctrlpts_y, "k-.")  # control points polygon
curveplt, = plt.plot(curvepts_x, curvepts_y, "g-")  # evaluated curve points
tanline = plt.quiver(X, Y, U, V, color="blue", angles='xy', scale_units='xy', scale=1, width=0.003)  # tangents
tanlinekey = plt.quiverkey(tanline, 23.75, -14.5, 1, "Tangent Vectors", coordinates='data', labelpos='W')
plt.legend([cppolygon, curveplt], ["Control Points Polygon", "Evaluated Curve"])
plt.axis([-1, 25, -15, 15])
plt.show()

print("End of NURBS-Python Example")
