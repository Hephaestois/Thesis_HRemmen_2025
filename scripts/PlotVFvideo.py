import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import netCDF4
import numpy as np
from time import time

start = time()

# Dataset URL
url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3'
dataset = netCDF4.Dataset(url)

# Index ranges
lats_idx = range(2050, 2176, 2)
lons_idx = range(1885, 2113, 2)
time_idx = range(0, 60, 1)
#time_idx = range(1452, 4388, 4)

# Get coordinate grids
lats = dataset.variables['lat'][lats_idx]
lons = dataset.variables['lon'][lons_idx]
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Setup figure
fig, ax = plt.subplots(figsize=(10, 8))
quiver = ax.quiver(lon_grid, lat_grid, np.zeros_like(lon_grid), np.zeros_like(lat_grid),
                   angles='xy', scale_units='xy', scale=2, width=0.002)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Water Current Vectors')

# Update function
def update(frame):
    u = dataset.variables['water_u'][frame, 0, lats_idx, lons_idx]
    v = dataset.variables['water_v'][frame, 0, lats_idx, lons_idx]
    quiver.set_UVC(u, v)
    ax.set_title(f'Water Currents at Time Index: {frame}')
    print(f'frame {frame}')
    return quiver,

# Create animation
ani = FuncAnimation(fig, update, frames=time_idx, interval=50, blit=False)

# Save animation using FFMpegWriter
writer = FFMpegWriter(fps=15, metadata=dict(artist='HYCOM'), bitrate=1800)
ani.save('ocean_currents_animation.mp4', writer=writer, dpi=200)

print(f'Animation saved to ocean_currents_animation.mp4. Total time: {time() - start:.2f} seconds')
