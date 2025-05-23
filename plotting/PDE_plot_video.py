# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Other imports
import numpy as np
from library.structures import Grid
from library.functions import load_data, progressBar
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import pickle

### === Options ===

year = 2020
days = 100
fps = 10
vmin, vmax = 0, 0.5
output_filename = f'{year}_{days}d.mp4'
matrix_cutoff = 0.02

### === End options ===

metadata = load_data("pde", year, days, '0.1x0.1_0.01', 'metadata')
matrix = load_data("pde", year, days, '0.1x0.1_0.01', 100)[0] #Contains the matrix and the vectorfield at each timestep!


dx, dy = metadata['dx'], float(metadata['dy'])
dt = 0.01
simLengthDays = days

masked_matrix = np.ma.masked_less(matrix, matrix_cutoff) #5 times as much

# Create a colormap and set the "bad" (masked) color to white or gray
cmap = cm.viridis.copy()
cmap.set_bad(color='white')  # Values exceeding lower bound are seethrough.

fig, ax = plt.subplots(figsize=[8, 3], dpi=180)
start = time.time()

def update(day):
    ax.clear()
    matrix = load_data("pde", year, days, '0.1x0.1_0.01', day)[0]
    masked_matrix = np.ma.masked_less(matrix, 0.02)
    im = ax.imshow(masked_matrix, origin='lower', extent=[-29, -11, 42, 47],
                   aspect=1, vmin=vmin, vmax=vmax, cmap=cmap)
    ax.plot((-25), (44.5), 'r.')
    ax.set_title(f"Day {day} | Grid step {dx}x{dy}, dt={dt}")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    progressBar(day, simLengthDays, start)
    return [im]

ani = animation.FuncAnimation(fig, update, frames=range(days + 1), blit=False)

ani.save(output_filename, fps=fps, dpi=180)
plt.close()