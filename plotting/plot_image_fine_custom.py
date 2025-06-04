import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

# === Local imports ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))
from library.functions import load_data, zipCoords

# === Argument Parsing ===
if len(sys.argv) != 10:
    print("Usage: python single_day_plot.py <year> <ndays> <dx> <dy> <dt> <nperday> <offset> <frame> <mode>")
    sys.exit(1)

year = int(sys.argv[1])
days = int(sys.argv[2])
dx = float(sys.argv[3])
dy = float(sys.argv[4])
dt = float(sys.argv[5])
walk_nperday = int(sys.argv[6])
offset = int(sys.argv[7])
frame = int(sys.argv[8])
mode = sys.argv[9].lower()

assert mode in {"rw", "pde", "both"}, "mode must be one of: density, walkers, both"
plot_paths = (mode == "rw")  # Only show red path lines in 'walkers' mode
walk_opacity = 10/frame  # Opacity of path lines

# === Setup ===
density_resolution = f'{dx}x{dy}_{dt}'
matrix_cutoff = 0.001
vmin, vmax = 0, 0.05

# === Load data ===
metadata = load_data("pde_onlyAdvection", year, days, density_resolution, 'metadata')
paths, start_frames = load_data('discrete', year, days, f'{walk_nperday}perday', 'allpositions')
processed_paths = [zipCoords(path) for path in paths]
filename = "figures/special/onlyAdvection.png"


# === Load matrix for the specific frame ===
matrix = load_data("pde", year, days, density_resolution, frame)[0]
y_min_display = 42.5
y_max_display = 46.5
label_fontsize = 12
tick_fontsize = 12
title_fontsize = 14

# === Crop matrix vertically ===
y_min = 42
y_max = 47
ny = matrix.shape[0]
dy = (y_max - y_min) / ny
row_start = int((y_min_display - y_min) / dy)
row_end = int((y_max_display - y_min) / dy)
cropped_matrix = matrix[row_start:row_end, :]
masked_matrix = np.ma.masked_less(cropped_matrix, matrix_cutoff)

# === Setup Plot ===
fig, ax = plt.subplots(figsize=[10, 3.2], dpi=150)
ax.set_xlim(offset - 29, offset - 11)
ax.set_ylim(42, 47)

cmap = cm.viridis.copy()
cmap.set_bad(color='white')

# === Colorbar setup ===

# === Plot density if requested ===
if mode in {"pde", "both"}:
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.1)

    density_img = ax.imshow(masked_matrix, origin='lower',
                            extent=[offset - 29, offset - 11, y_min_display, y_max_display],
                            aspect=1, vmin=vmin, vmax=vmax, cmap=cmap)
    cbar = fig.colorbar(density_img, cax=cax)
    cbar.ax.tick_params(labelsize=tick_fontsize)

# === Plot turtles if requested ===
if mode in {"rw", "both"}:
    for i, (x, y) in enumerate(processed_paths):
        start_frame = start_frames[i]
        plen = len(x)

        if start_frame <= frame < start_frame + plen:
            idx = frame - start_frame
            if plot_paths:
                ax.plot(x[:idx + 1], y[:idx + 1], color='red', alpha=walk_opacity)  # faded path
            ax.plot(x[idx], y[idx], 'wo', markersize=4, markeredgecolor='black')  # current walker
        elif frame >= start_frame + plen:
            if plot_paths:
                ax.plot(x, y, color='red', alpha=walk_opacity)
            ax.plot(x[-1], y[-1], 'kx')  # end marker

        ax.plot(offset - 25, 44.5, 'ko')  # origin

    # Fixed red marker
    ax.plot(offset - 25, 44.5, 'ro')

# === Final touches ===
ax.set_title(f"{year}, Day {frame}", fontsize=title_fontsize)
ax.set_xlabel("Longitude ($\degree$E)", fontsize=label_fontsize)
ax.set_ylabel("Latitude ($\degree$N)", fontsize=label_fontsize)
ax.tick_params(labelsize=tick_fontsize)

# === Save plot ===
plt.tight_layout()
# if mode == 'both':
#     plt.savefig(f"figures/combined/{year}day{frame}_{density_resolution}_{mode}.png", bbox_inches='tight')
# if mode == 'rw':
#     plt.savefig(f"figures/rw/{year}day{frame}_{density_resolution}_{mode}.png", bbox_inches='tight')
# if mode == 'pde':
#     plt.savefig(f"figures/pde/{year}day{frame}_{density_resolution}_{mode}.png", bbox_inches='tight')

plt.savefig(filename, bbox_inches='tight')

print(f'Created image {year}day{frame}_{density_resolution}_{mode}.png')
