"""Test scripts for NURBS Python Package

    This script reads the surface control points from a file, applies knot insertion to U direction,
    and draws the surfaces using Matplotlib.

    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016
"""

# Main script to execute NURBS surface calculations
from nurbs import Point, Knot, Surface, Weight

plot_result = True  # If we have matplotlib, we can draw the result
dimension = 3  # This is a surface

degree_p = input('Please enter the value of p: ')
degree_q = input('Please enter the value of q: ')

#
# Calculate the surface points using the NURBS package
#

# Control point operations
control_points = Point.PointFromFile3D(dimension, 'samples/cp_surface1.txt')
control_points.input_cp()
Pu = control_points.get_cp_u()
num_points_u = Pu.__len__()
Pv = control_points.get_cp_v()
num_points_v = Pv.__len__()

# Knot vector and basis functions for U direction
Up = Knot.Knot(dimension, degree_p, num_points_u)
Up.create_knot_vector()
# Display and get knot vector U
print('Knot vector U:')
knot_vector_p = Up.get_knot_vector(True)
Up.calculate_spans()
spans_p = Up.get_spans()
Up.calculate_basis_functions()
Np = Up.get_basis_functions()

# Knot vector and basis functions for V direction
Uq = Knot.Knot(dimension, degree_q, num_points_v)
Uq.create_knot_vector()
# Display and get knot vector V
print('Knot vector V:')
knot_vector_q = Uq.get_knot_vector(True)
Uq.calculate_spans()
spans_q = Uq.get_spans()
Uq.calculate_basis_functions()
Nq = Uq.get_basis_functions()

# Surface point operations
S = Surface.Surface(degree_p, degree_q, Pv, Np, Nq, spans_p, spans_q)
S.calculate()
S_points = S.get_result()
S.write()

# Get surface points
x_coords = []
y_coords = []
z_coords = []
for s in S_points:
    x_coords.append(s['x'])
    y_coords.append(s['y'])
    z_coords.append(s['z'])

#
# Knot insertion
#

# Weights array operations
weights_u = Weight.Weight(num_points_u)
weights_u.calculate()
Wu = weights_u.get_result()

control_points.create_wcp(Wu)
Pwu = control_points.wcp

knot_to_be_inserted = 0.6  # this is the knot to be inserted into the knot vector
r = 1  # insert the new knot into the knot vector "r" times

print('Adding knot vector U a new knot ' + str(knot_to_be_inserted))
Up.find_multiplicity(knot_to_be_inserted)
Pwu_updated = Up.insert_knot_surface(Pwu, knot_to_be_inserted, r)
control_points.wcp = Pwu_updated
control_points.update_cp()
Pu_new = control_points.get_cp()

print('Updated knot vector U: ')
knot_vector_p_new = Up.get_knot_vector(True)
Up.calculate_spans()
spans_p_new = Up.get_spans()
Up.calculate_basis_functions()
Np_new = Up.get_basis_functions()

S_new = Surface.Surface(degree_p, degree_q, Pu_new, Np_new, Nq, spans_p_new, spans_q)
S_new.calculate()
S_points_new = S_new.get_result()

# Surface points after knot insertion
x_coords_new = []
y_coords_new = []
z_coords_new = []
for s in S_points_new:
    x_coords_new.append(s['x'])
    y_coords_new.append(s['y'])
    z_coords_new.append(s['z'])

#
# Plotting the control point polygon and curve using MATPLOTLIB
#

# Try to import the MATPLOTLIB package
try:
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D as plt3D
except ImportError:
    plot_result = False

if plot_result:
    print('Plotting the result using MATPLOTLIB...')
    plt.clf()  # clear the existing figure
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf1 = ax.plot_trisurf(x_coords, y_coords, z_coords, cmap='hot', color='r', linewidth=0)  # Plot 3D Surface
    surf2 = ax.plot_trisurf(x_coords_new, y_coords_new, z_coords_new, cmap='copper', color='r', linewidth=0)  # Plot 3D Surface
    fig.show()  # Show the figure
else:
    print('matplotlib is required for automatically plotting the result.')
    print('You can use the output file (*.out) to draw the result using another plotting software.\n')

# Pause before ending the script
input('Press Enter key to continue...')
