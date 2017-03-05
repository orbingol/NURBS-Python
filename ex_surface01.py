# -*- coding: utf-8 -*-

from nurbs import Surface as ns
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a NURBS surface instance
surf = ns.Surface()

# Set up the NURBS surface
surf.read_ctrlpts("data\CP_Surface1.txt")
surf.degree_u = 3
surf.degree_v = 3
surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]

# Calculate surface points
surf.calculate()

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
fig.show()

print("End of NURBS-Python Example")
