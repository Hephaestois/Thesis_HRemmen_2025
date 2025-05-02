import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from library.functions import progressBar
import pickle
from library.functions import zipCoords
from time import time

# === Toggle here ===
plot_paths = False         # ← Set to False to hide trajectory lines
walk_opacity = 0.01       # Only applies if plot_paths = True

# Load data
with open('createdData.pkl', 'rb') as file:
    paths = pickle.load(file)

# Prepare figure
fig, ax = plt.subplots(figsize=[10, 4], dpi=150)
ax.set_xlim(-29, -11.5)
ax.set_ylim(41.5, 47)

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
    line, = ax.plot([], [], color='red', alpha=walk_opacity if plot_paths else 0.0)
    dot, = ax.plot([], [], 'go')    # green current dot
    cross, = ax.plot([], [], 'kx')  # black X at end
    start, = ax.plot(-25.6, 44.4, 'ko')  # black dot at start (static)
    lines.append(line)
    dots.append(dot)
    crosses.append(cross)
    starts.append(start)


startTime = time()
# Animation update function
def update(frame):
    progressBar(frame, max_steps, startTime)
    for i, (x, y) in enumerate(processed_paths):
        plen = path_lengths[i]
        if frame < plen:
            if plot_paths:
                lines[i].set_data(x[:frame + 1], y[:frame + 1])
            dots[i].set_data(x[frame], y[frame])
            crosses[i].set_data([], [])
        else:
            if plot_paths:
                lines[i].set_data(x, y)
            dots[i].set_data([], [])
            crosses[i].set_data(x[-1], y[-1])
    return (dots + crosses + starts) if not plot_paths else (lines + dots + crosses + starts)

# Create animation
anim = FuncAnimation(fig, update, frames=max_steps, interval=20, blit=True)

# Save as video or gif
writer = FFMpegWriter(fps=50)
anim.save("randomWalkAnimation.mp4", writer=writer)
print('Finished')
