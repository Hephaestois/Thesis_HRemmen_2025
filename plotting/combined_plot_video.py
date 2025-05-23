# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Other imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
from matplotlib import cm
from library.functions import load_data, progressBar, zipCoords
import time

# === Configuration ===
year = 2020
days = 100
fps = 10
vmin, vmax = 0, 0.5
matrix_cutoff = 0.02
density_resolution = '0.1x0.1_0.01'
walk_nperday = 2
output_filename = f'{year}_{days}d_combined.mp4'

# === Load metadata and data ===
metadata = load_data("pde", year, days, density_resolution, 'metadata')
dx, dy = metadata['dx'], float(metadata['dy'])

# Load random walk data
paths, start_frames = load_data('discrete', str(year), str(days), f'{walk_nperday}perday', 'allpositions')
processed_paths = [zipCoords(path) for path in paths]
path_lengths = [len(p[0]) for p in processed_paths]
max_steps = max(start + len(p[0]) for p, start in zip(processed_paths, start_frames))

# === Setup Figure ===
fig, ax = plt.subplots(figsize=[10, 4], dpi=150)
ax.set_xlim(360-29, 360-11.5)
ax.set_ylim(41.5, 47)

# Set up colormap for density field
cmap = cm.viridis.copy()
cmap.set_bad(color='white')

# === Prepare plot elements ===
# Density image (reused)
density_img = ax.imshow(np.zeros((10, 10)), origin='lower', extent=[360-29, 360-11, 42, 47],
                        aspect=1, vmin=vmin, vmax=vmax, cmap=cmap)

# Plot elements for each walker
dots = []
crosses = []
starts = []

for x, y in processed_paths:
    # Small white dot with black edge
    dot, = ax.plot([], [], marker='o', markerfacecolor='white', markeredgecolor='black', markersize=4, linestyle='None')
    cross, = ax.plot([], [], 'kx')  # Black 'X' for end
    start, = ax.plot(360-25, 44.5, 'ko')  # Static black dot at origin
    dots.append(dot)
    crosses.append(cross)
    starts.append(start)

start_time = time.time()

# === Animation update function ===
def update(frame):
    artists = []

    # Update density field
    matrix = load_data("pde", year, days, density_resolution, frame)[0]
    masked_matrix = np.ma.masked_less(matrix, matrix_cutoff)
    density_img.set_data(masked_matrix)
    artists.append(density_img)

    # Update walker positions
    for i, (x, y) in enumerate(processed_paths):
        start_frame = start_frames[i]
        plen = path_lengths[i]

        if frame < start_frame:
            dots[i].set_data([], [])
            crosses[i].set_data([], [])
        elif frame < start_frame + plen:
            idx = frame - start_frame
            dots[i].set_data(x[idx], y[idx])
            crosses[i].set_data([], [])
        else:
            dots[i].set_data([], [])
            crosses[i].set_data(x[-1], y[-1])

        artists.extend([dots[i], crosses[i], starts[i]])

    ax.set_title(f"Day {frame} | Grid step {dx}x{dy}")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.plot(360-25, 44.5, 'ro')  # Fixed red marker

    progressBar(frame, max_steps - 1, start_time)
    return artists

# === Run animation ===
print("Starting combined animation...")
ani = animation.FuncAnimation(fig, update, frames=max_steps, interval=1000 / fps, blit=True)
writer = FFMpegWriter(fps=fps)
ani.save(output_filename, writer=writer)
plt.close()
print("Animation saved:", output_filename)
