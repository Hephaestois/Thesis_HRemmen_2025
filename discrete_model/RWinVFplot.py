# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Other imports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from library.functions import progressBar, load_data
import pickle
from library.functions import zipCoords
from time import time

##For Viktoria: This function is slow as hell. Use at your own discretion. Takes data created by either RWinVF or RWinVF2km.

# === Toggle here ===
plot_paths = True         # Show/don't show turtle path lines
walk_opacity = 0.1       # Only effective if plot_paths = True

# # Load data
# with open('createdData.pkl', 'rb') as file:
#     paths, start_frames = pickle.load(file)
paths, start_frames = load_data('discrete', '2016', '100', '0.02x0.02', 'allpositions')

# Prepare figure
fig, ax = plt.subplots(figsize=[10, 4], dpi=150)
ax.set_xlim(-29, -11.5)
ax.set_ylim(41.5, 47)

# Preprocess paths
processed_paths = [zipCoords(path) for path in paths]
path_lengths = [len(p[0]) for p in processed_paths]
max_steps = max(start + len(p[0]) for p, start in zip(processed_paths, start_frames))

# Create plot elements
lines = []
dots = []
crosses = []
starts = []

for x, y in processed_paths:
    line, = ax.plot([], [], color='red', alpha=walk_opacity if plot_paths else 0.0)
    dot, = ax.plot([], [], 'go')    # green current dot
    cross, = ax.plot([], [], 'kx')  # black X at end
    start, = ax.plot(-25, 44.5, 'ko')  # black dot at start (static)
    lines.append(line)
    dots.append(dot)
    crosses.append(cross)
    starts.append(start)


startTime = time()
# Animation update function
def update(frame):
    progressBar(frame, max_steps-1, startTime)
    artists = []

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

    return artists

print("Starting animation...")
# Create animation
anim = FuncAnimation(fig, update, frames=max_steps, interval=100, blit=True)

# Save video
writer = FFMpegWriter(fps=10)
anim.save("randomWalkAnimation.mp4", writer=writer)
print('Finished')
