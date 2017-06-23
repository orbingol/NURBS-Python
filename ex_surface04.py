# -*- coding: utf-8 -*-

"""
    Examples for the NURBS-Python Package
    Released under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2017

    This example is contributed by John-Eric Dufour (@jedufour)
"""

from nurbs import Surface as ns
from nurbs import utilities as utils
from nurbs import factories as fact
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a NURBS surface instance
#surf = fact.from_file("data/CP_Surface1.json")
surf = fact.from_file("data/CP_Surface2.json")
surf.evaluate()

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
#surfplt = ax.scatter(surfpts_x, surfpts_y, surfpts_z, c="red", s=10, depthshade=True)  # 3D Scatter plot
surfplt = ax.plot_trisurf(surfpts_x, surfpts_y, surfpts_z, cmap=plt.cm.viridis)  # 3D Tri-Surface plot
ax.set_xlim(-25, 25)
ax.set_ylim(-25, 25)
ax.set_zlim(-15, 15)
plt.show()

print("End of NURBS-Python Example")
