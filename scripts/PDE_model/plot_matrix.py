import numpy as np
from library.structures import Grid
import matplotlib.pyplot as plt
from matplotlib import cm
import pickle

with open('matrix.pkl', 'rb') as f:
    matrix = pickle.load(f)

dx, dy = 0.1, 0.1
dt = 0.01
simLengthDays = 100


masked_matrix = np.ma.masked_less(matrix, 0.004) #5 times as much

# Create a colormap and set the "bad" (masked) color to white or gray
cmap = cm.viridis.copy()
cmap.set_bad(color='white')  # Or 'white'

plt.figure(figsize=[8, 3], dpi=180)
plt.title(f"Grid step {dx}x{dy}, dt={dt}. {simLengthDays} days simulation")
# Use masked matrix and custom colormap
plt.imshow(masked_matrix, origin='lower', extent=[-29, -11, 42, 47],
           aspect=1, vmin=0, vmax=0.1, cmap=cmap) #5 times as high

# lon_grid, lat_grid = np.meshgrid(grid.x_s, grid.y_s)
# plt.quiver(lon_grid[::3, ::3], lat_grid[::3, ::3], vf_x[::3, ::3], vf_y[::3, ::3], scale=40, color='k')
plt.plot((-25), (44.5), 'r.')
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('densityplot.png')
plt.show()
