"""Test scripts for NURBS Python Package

    This script reads the curve control points from a file, applies knot insertion,
    and draws the control point polygons and the curves using Matplotlib.

    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016
"""

# Main script to execute NURBS curve calculations
from nurbs import Point, Knot, Curve, Weight

plot_result = True  # If we have matplotlib, we can draw the result
dimension = 2  # This is a curve

degree = input('Please enter the degree of the curve: ')

#
# Calculate the curve points using the NURBS package
#

# Control point operations
control_points = Point.PointFromFile(dimension, 'samples/cp_curve3.txt')
control_points.input_cp()
P = control_points.get_cp()
num_points = P.__len__()

# Knot vector and basis functions
U = Knot.Knot(dimension, degree, num_points)
U.create_knot_vector()
# Display and get knot vector
print('Knot vector: ')
knot_vector = U.get_knot_vector(True)
U.calculate_spans()
spans = U.get_spans()
U.calculate_basis_functions()
N = U.get_basis_functions()

# Curve point operations
C = Curve.Curve(degree, P, N, spans)
C.calculate()
C_points = C.get_result()
C.write()

# Control point polygon
x_coords_cp = []
y_coords_cp = []
for p in P:
    x_coords_cp.append(p['x'])
    y_coords_cp.append(p['y'])
# Curve
x_coords = []
y_coords = []
for c in C_points:
    x_coords.append(c['x'])
    y_coords.append(c['y'])

#
# Knot insertion
#

# Weights array operations
weights = Weight.Weight(num_points)
weights.calculate()
W = weights.get_result()

control_points.create_wcp(W)
Pw = control_points.wcp

knot_to_be_inserted = 0.1  # this is the knot to be inserted into the knot vector
r = 1  # insert the new knot into the knot vector "r" times

print('Adding knot vector a new knot ' + str(knot_to_be_inserted))
U.find_multiplicity(knot_to_be_inserted)
Pw_updated = U.insert_knot_curve(Pw, knot_to_be_inserted, r)
control_points.wcp = Pw_updated
control_points.update_cp()
P_new = control_points.get_cp()

# Get updated knot vector
print('Updated knot vector: ')
knot_vector_new = U.get_knot_vector(True)
U.calculate_spans()
spans_new = U.get_spans()
U.calculate_basis_functions()
N_new = U.get_basis_functions()

C_new = Curve.Curve(degree, P_new, N_new, spans_new)
C_new.calculate()
C_points_new = C_new.get_result()

# Control point polygon after knot insertion
x_coords_cp_new = []
y_coords_cp_new = []
for p in P_new:
    x_coords_cp_new.append(p['x'])
    y_coords_cp_new.append(p['y'])
# Curve after knot insertion
x_coords_new = []
y_coords_new = []
for c in C_points_new:
    x_coords_new.append(c['x'])
    y_coords_new.append(c['y'])

#
# Plotting the control point polygon and curve using MATPLOTLIB
#

# Try to import the MATPLOTLIB package
try:
    from matplotlib import pyplot as plt
except ImportError:
    plot_result = False

if plot_result:
    print('Plotting the result using MATPLOTLIB...')
    plt.clf()  # clear existing figure
    plot_cp, = plt.plot(x_coords_cp, y_coords_cp, 'r--', )  # Plot 2D Control point polygon
    plot_curve, = plt.plot(x_coords, y_coords, 'r*')  # Plot 2D Curve
    plot_cp_new, = plt.plot(x_coords_cp_new, y_coords_cp_new, 'b-', )  # Plot 2D Control point polygon after knot insert
    plot_curve_new, = plt.plot(x_coords_new, y_coords_new, 'g-')  # Plot 2D Curve after knot insert
    plt.axis([4, 71, 4, 61])  # Set axis intervals
    plt.xlabel('x')  # Set x-axis label
    plt.ylabel('y')  # Set y-axis label
    plt.title('Curve of degree ' + str(degree))  # Set plot title
    #plt.legend([plot_cp, plot_curve], ['Control Polygon', 'Curve'], loc='upper left')  # Set plot legend
    plt.legend([plot_cp, plot_cp_new, plot_curve, plot_curve_new], ['Control Polygon', 'Control Polygon Updated', 'Curve', 'Curve Updated'], loc='upper left')  # Set plot legend
    plt.show()  # Show the final figure
else:
    print('matplotlib is required for automatically plotting the result.')
    print('You can use the output file (*.out) to draw the result using another plotting software.\n')

# Pause before ending the script
input('Press Enter key to continue...')
