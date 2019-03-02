# Generate NURBS-Python (geomdl) download graphs using Plotly
import os
import plotly
from plotly import graph_objs as go


# Fix file path
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Initialize some variables
num_downloads = []
year_months = []

# Read file
with open("downloads.txt", 'r') as fp:
    # Read line by line
    for line in fp:
        # Remove whitespace
        line = line.strip()
        # Split the row into 2 pieces
        row = line.split(",")
        # Update data lists
        num_downloads.append(int(row[0]))
        ym_temp = row[1][0:4] + "-" + row[1][4:6]
        year_months.append(ym_temp)

# Create a bar chart
figure = go.Bar(x=year_months, y=num_downloads)

# Prepare data for plotting
plot_layout = go.Layout(
    hovermode=False,  # disable hover
    title='NURBS-Python PyPI Downloads',
    xaxis=dict(
        title='Months',
        type='category'
    ),
    yaxis=dict(
        title='Number of Downloads'
    ),
)
plot_data = [figure]
figure = go.Figure(data=plot_data, layout=plot_layout)

# Plot the figure (online)
plotly.plotly.plot(figure, filename="geomdl-downloads")

# # Plot the figure (offline)
# plotly.offline.plot(figure, filename="geomdl-downloads.html")
