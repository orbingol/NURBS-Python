# -*- coding: utf-8 -*-

from nurbs import Surface as ns
from nurbs import utilities as utils
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a NURBS surface instance
surf = ns.Surface()

# Set up the NURBS surface
surf.read_ctrlptsw("data/CPw_Surface3.txt")
surf.degree_u = 2
surf.degree_v = 1

surf.knotvector_u = [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]
surf.knotvector_v = [0, 0, 1, 1]

# Evaluate surface
surf.evaluate_rational()

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
surfplt = ax.scatter(surfpts_x, surfpts_y, surfpts_z, c="green", s=10, depthshade=True)  # 3D Scatter plot
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-1, 1)
fig.show()

print("End of NURBS-Python Example")
