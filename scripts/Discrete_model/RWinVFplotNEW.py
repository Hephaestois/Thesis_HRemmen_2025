import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from library.functions import progressBar
import pickle
from library.functions import zipCoords
from time import time
import numpy as np
from matplotlib import cm


##For Viktoria: This function is slow as hell. Use at your own discretion. Takes data created by either RWinVF or RWinVF2km.

# === Toggle here ===
plot_paths = True         # Show/don't show turtle path lines
walk_opacity = 0.01       # Only effective if plot_paths = True

# Load data
with open('createdData.pkl', 'rb') as file:
    paths, start_frames = pickle.load(file)

# Preprocess paths
processed_paths = [zipCoords(path) for path in paths]
path_lengths = [len(p[0]) for p in processed_paths]
max_steps = max(start + len(p[0]) for p, start in zip(processed_paths, start_frames))

print(processed_paths[0])

startTime = time()

cmap = cm.viridis.copy()
cmap.set_bad(color='white')  # Values exceeding lower bound are seethrough.


###
with open(f'2016_100d_matrix.pkl', 'rb') as f:
    matrix = pickle.load(f)

masked_matrix = np.ma.masked_less(matrix, 0.02) #5 times as much
###

plt.figure(figsize=[8, 3], dpi=180)
# Use masked matrix and custom colormap
plt.imshow(masked_matrix, origin='lower', extent=[-29, -11, 42, 47],
           aspect=1, vmin=0, vmax=0.5, cmap=cmap) #5 times as high

# lon_grid, lat_grid = np.meshgrid(grid.x_s, grid.y_s)
# plt.quiver(lon_grid[::3, ::3], lat_grid[::3, ::3], vf_x[::3, ::3], vf_y[::3, ::3], scale=40, color='k')
plt.plot((-25), (44.5), 'r.')
plt.colorbar()
for path in processed_paths:
    plt.plot((path[0][-1]), (path[1][-1]), 'g.')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig(f'randomWalk.png')
plt.show()
