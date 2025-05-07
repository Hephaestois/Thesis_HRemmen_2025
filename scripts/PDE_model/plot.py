import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py

# Load data
with h5py.File("simulation_data.h5", "r") as f:
    frames = f["frames"][:]  # Load all at once

# Plot setup
fig, ax = plt.subplots()
img = ax.imshow(frames[0], cmap='viridis')

def update(i):
    img.set_data(frames[i])
    ax.set_title(f"Step {i}")
    return [img]

ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=50, blit=True)
ani.save("simulation_video.mp4", writer='ffmpeg')
