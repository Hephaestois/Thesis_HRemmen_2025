import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

import netCDF4
import numpy as np
from time import time

start = time()

# Dataset URL
url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3'
dataset = netCDF4.Dataset(url)
startTime_1 = 140256 #01-01-2016
endTime = 140256 + 24*50

# Index ranges
lats_idx = np.arange(2050, 2176, 2)
lons_idx = np.arange(1885, 2113, 2)
time_array_1 = dataset.variables['time'][:]
time_mask_1 = (time_array_1 >= startTime_1) & (time_array_1 <= endTime)
time_idx_1 = np.where(time_mask_1)[0]
times_1 = time_array_1[time_idx_1]
startTimeIndex_1 = list(time_array_1).index(startTime_1)

# Get coordinate grids
lats = dataset.variables['lat'][lats_idx]
lons = dataset.variables['lon'][lons_idx]
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Setup figure
fig, ax = plt.subplots(figsize=(10, 4))
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
ani = FuncAnimation(fig, update, frames=time_idx_1, interval=200, blit=False)

# Save animation using FFMpegWriter
writer = FFMpegWriter(fps=15, metadata=dict(artist='HYCOM'), bitrate=-1)
ani.save('ocean_currents_animation.mp4', writer=writer, dpi=600)

print(f'Animation saved to ocean_currents_animation.mp4. Total time: {time() - start:.2f} seconds')
