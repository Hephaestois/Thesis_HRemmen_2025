import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from library.functions import progressBar
import pickle
from library.functions import zipCoords
from time import time

walk_opacity = 0.2

# Load data
with open('createdData.pkl', 'rb') as file:
    paths = pickle.load(file)

# Prepare figure
fig, ax = plt.subplots(figsize=[10, 4], dpi=150)
ax.set_xlim(-29, -11.5) #-29 slightly smaller than original range, tutels dont go here
ax.set_ylim(41.5, 47)   #Slightly larger than the range, for clarity in plot.

# Preprocess paths
processed_paths = [zipCoords(path) for path in paths]
path_lengths = [len(p[0]) for p in processed_paths]
max_steps = max(path_lengths)

# Create plot elements
lines = []
dots = []
crosses = []
starts = []

for x, y in processed_paths:
    line, = ax.plot([], [], color='red', alpha=walk_opacity)
    dot, = ax.plot([], [], 'go')    # green current dot
    cross, = ax.plot([], [], 'kx')  # black X at end
    start, = ax.plot(-25.6, 44.4, 'ko')  # black dot at start (static)
    lines.append(line)
    dots.append(dot)
    crosses.append(cross)
    starts.append(start)

# Animation update function
def update(frame):
    progressBar(frame, max_steps)
    for i, (x, y) in enumerate(processed_paths):
        plen = path_lengths[i]
        if frame < plen:
            lines[i].set_data(x[:frame + 1], y[:frame + 1])
            dots[i].set_data(x[frame], y[frame])
            crosses[i].set_data([], [])
        else:
            lines[i].set_data(x, y)
            dots[i].set_data([], [])
            crosses[i].set_data(x[-1], y[-1])
    return lines + dots + crosses + starts

# Create animation
anim = FuncAnimation(fig, update, frames=max_steps, interval=20, blit=True)

# Save as video or gif
writer = FFMpegWriter(fps=50)
anim.save("randomWalkAnimation.mp4", writer=writer)
print('Finished')

