# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Other imports
import numpy as np
from library.structures import Grid
from library.functions import load_data
import matplotlib.pyplot as plt
from matplotlib import cm
import pickle

### === Options ===

year = 2016
days = 100
fps = 10
vmin, vmax = 0, 0.5
output_filename = f'{year}_{days}d.mp4'

### === End options ===

metadata = load_data("pde", year, days, '0.1x0.1_0.01', 'metadata')
matrix = load_data("pde", year, days, '0.1x0.1_0.01', 100)[0] #Contains the matrix and the vectorfield at each timestep!


dx, dy = metadata['dx'], float(metadata['dy'])
dt = 0.01
simLengthDays = days

masked_matrix = np.ma.masked_less(matrix, 0.02) #5 times as much

# Create a colormap and set the "bad" (masked) color to white or gray
cmap = cm.viridis.copy()
cmap.set_bad(color='white')  # Values exceeding lower bound are seethrough.

plt.figure(figsize=[8, 3], dpi=180)
plt.title(f"Grid step {dx}x{dy}, dt={dt}. {simLengthDays} days simulation")
# Use masked matrix and custom colormap
plt.imshow(masked_matrix, origin='lower', extent=[-29, -11, 42, 47],
           aspect=1, vmin=vmin, vmax=vmax, cmap=cmap) #5 times as high

# lon_grid, lat_grid = np.meshgrid(grid.x_s, grid.y_s)
# plt.quiver(lon_grid[::3, ::3], lat_grid[::3, ::3], vf_x[::3, ::3], vf_y[::3, ::3], scale=40, color='k')
plt.plot((-25), (44.5), 'r.')
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.savefig(f'{year}_{days}d.png')
plt.show()
