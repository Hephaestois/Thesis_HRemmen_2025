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

# Handle arguments
if len(sys.argv) != 9:
    print("Usage: python plot_video_fine.py <year> <ndays> <dx> <dy> <dt> <nperday> <offset> <mode>")
    sys.exit(1)

year = int(sys.argv[1])
days = int(sys.argv[2])
dx = float(sys.argv[3])
dy = float(sys.argv[4])
dt = float(sys.argv[5])
walk_nperday = int(sys.argv[6])
offset = int(sys.argv[7])
mode = sys.argv[8].lower()
assert mode in {"rw", "pde", "both"}, "mode must be one of: density, walkers, both"


# === Configuration ===
# days = simLengthDays

fps = 10
vmin, vmax = 0, 0.05
matrix_cutoff = 0.001
plot_paths = (mode == "rw")  # Only show red path lines in 'walkers' mode
density_resolution = f'{dx}x{dy}_{dt}'
output_filename = f'{year}_{days}d_{density_resolution}_combined.mp4'
y_min_display = 42.5
y_max_display = 46.5
label_fontsize = 12
tick_fontsize = 12
title_fontsize = 14
y_min = 42
y_max = 47
walk_opacity = 10/days
             
# === Load metadata and data ===
metadata = load_data("pde", year, days, density_resolution, 'metadata')
exceedsTop, exceedsBottom = load_data('discrete', f'{year}', f'{days}', f'{walk_nperday}perday', 'exceedTopBottom')
print(f'{year} Survival Ratio: ', exceedsBottom / (exceedsTop+exceedsBottom))


dx, dy = float(metadata['dx']), float(metadata['dy'])

# Load random walk data
paths, start_frames = load_data('discrete', year, days, f'{walk_nperday}perday', 'allpositions')
processed_paths = [zipCoords(path) for path in paths]
path_lengths = [len(p[0]) for p in processed_paths]
max_steps = max(start + len(p[0]) for p, start in zip(processed_paths, start_frames))

# === Setup Figure ===
fig, ax = plt.subplots(figsize=[10, 2.7778], dpi=150)
ax.set_xlim(offset-29, offset-11)
ax.set_ylim(42, 47)

# Set up colormap for density field
cmap = cm.viridis.copy()
cmap.set_bad(color='white')

# === Prepare plot elements ===
# Density image (reused)
if mode in {"pde", "both"}:
    density_img = ax.imshow(np.zeros((10, 10)), origin='lower',
                            extent=[offset - 29, offset - 11, y_min_display, y_max_display],
                            aspect=1, vmin=vmin, vmax=vmax, cmap=cmap)

# Plot elements for each walker
dots = []
crosses = []
starts = []
lines = []

for x, y in processed_paths:
    # Small white dot with black edge
    line, = ax.plot([], [], color='red', alpha=walk_opacity if plot_paths else 0.0)
    dot, = ax.plot([], [], marker='o', markerfacecolor='white', markeredgecolor='black', markersize=4, linestyle='None')
    cross, = ax.plot([], [], 'kx')  # Black 'X' for end
    start, = ax.plot(offset-25, 44.5, 'ko')  # Static black dot at origin
    dots.append(dot)
    lines.append(line)
    crosses.append(cross)
    starts.append(start)

start_time = time.time()

# === Animation update function ===
def update(frame):
    artists = []
    if mode in {"pde", "both"}:
        matrix = load_data("pde", year, days, density_resolution, frame)[0]
        ny = matrix.shape[0]
        dy = (y_max - y_min) / ny
        row_start = int((y_min_display - y_min) / dy)
        row_end = int((y_max_display - y_min) / dy)
        cropped_matrix = matrix[row_start:row_end, :]
        masked_matrix = np.ma.masked_less(cropped_matrix, matrix_cutoff)
        density_img.set_data(masked_matrix)
        artists.append(density_img)

    if mode in {"rw", "both"}:
        # Update walker positions
        for i, (x, y) in enumerate(processed_paths):
            start_frame = start_frames[i]
            plen = path_lengths[i]

            if frame < start_frame:
                # Turtle hasn't started yet
                if plot_paths:
                    lines[i].set_data([], [])
                dots[i].set_data([], [])
                crosses[i].set_data([], [])
            elif frame < start_frame + plen:
                idx = frame - start_frame
                if plot_paths:
                    lines[i].set_data(x[:idx + 1], y[:idx + 1])
                    artists.append(lines[i])
                dots[i].set_data(x[idx], y[idx])
                crosses[i].set_data([], [])
            else:
                if plot_paths:
                    lines[i].set_data(x, y)
                    artists.append(lines[i])
                dots[i].set_data([], [])
                crosses[i].set_data(x[-1], y[-1])

            artists.extend([dots[i], crosses[i], starts[i]])

    ax.set_title(f"Year {year}, day {frame}", fontsize=title_fontsize)
    ax.set_xlabel("Longitude ($\degree$E)", fontsize=label_fontsize)
    ax.set_ylabel("Latitude ($\degree$N)", fontsize=label_fontsize)
    ax.tick_params(labelsize=tick_fontsize)
    ax.plot(offset-25, 44.5, 'ro')  # Fixed red marker
    progressBar(frame, max_steps-1, start_time)
    return artists

# === Run animation ===
print("Starting combined animation...")
ani = animation.FuncAnimation(fig, update, frames=max_steps, interval=1000 / fps, blit=True)
writer = FFMpegWriter(fps=fps)
if mode == 'both':
    ani.save(f'videos/combined/{output_filename}', writer=writer)
    print("Animation saved:", output_filename)
if mode == 'rw':
    ani.save(f'videos/rw/{output_filename}', writer=writer)
    print("Animation saved:", output_filename)
if mode == 'pde':
    ani.save(f'videos/pde/{output_filename}', writer=writer)
    print("Animation saved:", output_filename)

plt.close()
