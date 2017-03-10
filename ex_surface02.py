# -*- coding: utf-8 -*-

"""
    Examples for the NURBS-Python Package
    Released under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2017
"""

from nurbs import Surface as ns
from nurbs import utilities as utils
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a NURBS surface instance
surf = ns.Surface()

# Set up the NURBS surface
surf.read_ctrlpts("data\CP_Surface2.txt")
surf.degree_u = 3
surf.degree_v = 3
surf.knotvector_u = utils.autogen_knotvector(surf.degree_u, 6)
surf.knotvector_v = utils.autogen_knotvector(surf.degree_v, 6)

# Evaluate surface
surf.evaluate_rational()

# Calculate 1st order surface derivative at the given u and v
u = 0.2
v = 0.9
surftan = surf.tangent(u, v)
print("* Surface point at u = %.2f and v = %.2f is (%.2f, %.2f, %.2f)" % (u, v, surftan[0][0], surftan[0][1], surftan[0][2]))
print("* First derivative w.r.t. u is (%.2f, %.2f, %.2f)" % (surftan[1][0], surftan[1][1], surftan[1][2]))
print("* First derivative w.r.t. v is (%.2f, %.2f, %.2f)\n" % (surftan[2][0], surftan[2][1], surftan[2][2]))
# Calculate normal at the given u and v
norm = surf.normal(u, v)
print("* Normal at u = %.2f and v = %.2f is [%.1f, %.1f, %.1f]\n" % (u, v, norm[0], norm[1], norm[2]))

# Arrange calculated surface data for plotting
surfpts_x = []
surfpts_y = []
surfpts_z = []
for spt in surf.surfpts:
    surfpts_x.append(spt[0])
    surfpts_y.append(spt[1])
    surfpts_z.append(spt[2])

# Plot using Matplotlib
fig = plt.figure(figsize=(10.67, 8), dpi=96)
ax = fig.gca(projection='3d')
#surfplt = ax.scatter(surfpts_x, surfpts_y, surfpts_z, c="green", s=10, depthshade=True) # 3D Scatter plot
surfplt = ax.plot_trisurf(surfpts_x, surfpts_y, surfpts_z, cmap=plt.cm.winter)  # 3D Tri-Surface plot
ax.set_xlim(-25, 25)
ax.set_ylim(-25, 25)
ax.set_zlim(-15, 15)
fig.show()

print("End of NURBS-Python Example")
