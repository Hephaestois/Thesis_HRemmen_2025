import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import cm
from matplotlib.animation import FuncAnimation, FFMpegWriter

def load_day_data(day_index, data_dir):
    path = os.path.join(data_dir, f"day_{day_index:03}.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

def make_video(start_day=0, end_day=49, data_dir="simulation_output", output_file="simulation.mp4"):
    fig, ax = plt.subplots(figsize=[8, 3], dpi=180)
    cmap = cm.viridis.copy()
    cmap.set_bad(color='white')

    # Load one day for shape info
    sample = load_day_data(start_day, data_dir)
    im = ax.imshow(np.zeros_like(sample['matrix']), origin='lower',
                   extent=[-29, -11, 42, 47], aspect=1, cmap=cmap, vmin=0.01, vmax=1)
    qv = ax.quiver(sample['lon_grid'][::3, ::3], sample['lat_grid'][::3, ::3],
                   sample['vf_x'][::3, ::3], sample['vf_y'][::3, ::3], scale=4, color='k')
    
    red_dot, = ax.plot((-25), (44.5), 'r.')

    ax.set_title(f"Day {start_day}")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.colorbar(im, ax=ax, label="Value")

    def update(frame):
        data = load_day_data(frame, data_dir)
        matrix = data['matrix']
        masked_matrix = np.ma.masked_less(matrix, 0.01)
        im.set_data(masked_matrix)
        im.set_clim(vmin=0.01, vmax=np.max(matrix))
        
        qv.set_UVC(data['vf_x'][::3, ::3], data['vf_y'][::3, ::3])
        ax.set_title(f"Day {frame}")

    ani = FuncAnimation(fig, update, frames=range(start_day, end_day + 1), blit=False)

    writer = FFMpegWriter(fps=5, bitrate=1800)
    ani.save(output_file, writer=writer)
    print(f"Saved video to {output_file}")

if __name__ == "__main__":
    make_video()
