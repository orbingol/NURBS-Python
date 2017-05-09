# -*- coding: utf-8 -*-

"""
    Examples for the NURBS-Python Package - 2D Grid Generator
    Released under MIT License
    Developed by Onur Rauf Bingol (c) 2017
"""

from nurbs import Grid as gridgen

# Generate a 50x100 rectangle
mygrid = gridgen.Grid(50, 100)

# Split the width into 5 equal pieces and the height into 10 equal pieces
mygrid.generate(5, 10)

# Generate 4 bumps on the grid
mygrid.bumps(4)

# Save the file, by default as grid.txt
mygrid.save()

# Get the grid points for plotting
grid_data = mygrid.grid()

# Prepare data for plotting
x = []
y = []
z = []
for level1 in grid_data:
    for level2 in level1:
        x.append(level2[0])
        y.append(level2[1])
        z.append(level2[2])

# Plot using Matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10.67, 8), dpi=96)
ax = fig.gca(projection='3d')
# 3D Scatter plot
gridplt = ax.scatter(x, y, z, s=10, depthshade=False)
plt.show()
