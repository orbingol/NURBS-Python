"""Test scripts for NURBS Python Package

    This script reads the curve control points from a file,
    and draws the control point polygon and the curve using Matplotlib.

    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016
"""

# Main script to execute NURBS curve calculations
from nurbs import Point, Knot, Curve

plot_result = True  # If we have matplotlib, we can draw the result
dimension = 2  # This is a curve

degree = input('Please enter the degree of the curve: ')

#
# Calculate the curve points using the NURBS package
#

# Control point operations
control_points = Point.PointFromFile(dimension, 'samples/cp_curve2.txt')
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

#
# Plotting the control point polygon and curve using MATPLOTLIB
#

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

# Try to import the MATPLOTLIB package
try:
    from matplotlib import pyplot as plt
except ImportError:
    plot_result = False

if plot_result:
    print('Plotting the result using MATPLOTLIB...')
    plt.clf()  # clear existing figure
    plot_cp, = plt.plot(x_coords_cp, y_coords_cp, 'r-',)  # Plot 2D Control point polygon
    plot_curve, = plt.plot(x_coords, y_coords, 'y-')  # Plot 2D Curve
    plt.axis([4, 71, 4, 61])  # Set axis intervals
    plt.xlabel('x')  # Set x-axis label
    plt.ylabel('y')  # Set y-axis label
    plt.title('Curve of degree ' + str(degree))  # Set plot title
    plt.legend([plot_cp, plot_curve], ['Control Polygon', 'Curve'], loc='upper left')  # Set plot legend
    plt.show()  # Show the final figure
else:
    print('matplotlib is required for automatically plotting the result.')
    print('You can use the output file (*.out) to draw the result using another plotting software.\n')

# Pause before ending the script
input('Press Enter key to continue...')
