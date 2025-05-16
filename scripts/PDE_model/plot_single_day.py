import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import cm

def plot_single_day(day_index, data_dir="simulation_output", output_path=None):
    filepath = os.path.join(data_dir, f"day_{day_index:03}.pkl")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No data found for day {day_index} at {filepath}")
    
    with open(filepath, "rb") as f:
        data = pickle.load(f)
    
    matrix = data['matrix']
    vf_x = data['vf_x']
    vf_y = data['vf_y']
    lon_grid = data['lon_grid']
    lat_grid = data['lat_grid']

    # Mask values below 0.01
    masked_matrix = np.ma.masked_less(matrix, 0.01)

    cmap = cm.viridis.copy()
    cmap.set_bad(color='white')

    plt.figure(figsize=[8, 3], dpi=180)
    plt.title(f"Day {day_index}: Grid Plot")
    plt.imshow(masked_matrix, origin='lower', extent=[-29, -11, 42, 47],
               aspect=1, vmin=0.01, vmax=np.max(matrix), cmap=cmap)
    
    plt.quiver(lon_grid[::3, ::3], lat_grid[::3, ::3], vf_x[::3, ::3], vf_y[::3, ::3], scale=4, color='k')
    plt.plot((-25), (44.5), 'r.')
    plt.colorbar(label="Value")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    if output_path:
        plt.savefig(output_path, dpi=180)
        print(f"Saved plot to {output_path}")
    else:
        plt.show()

if __name__ == "__main__":
    plot_single_day(day_index=10)  # Change to any day index
