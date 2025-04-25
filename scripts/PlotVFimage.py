import matplotlib.pyplot as plt
import numpy as np
from time import time
import netCDF4

start = time()
url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3'
dataset = netCDF4.Dataset(url)

# Lat index range: 2050-2175
# Lon index range: 1885-2112
# Time index range: 1452-4388, stepsize 4
# Do not forget python's exclusive bounds!

# Access water_u, water_v: water_u[time, depth, lat, lon] slices
lats_idx = range(2050,2176,18)
lats = dataset.variables['lat'][lats_idx]
lons_idx = range(1885,2113,18)
lons = dataset.variables['lon'][lons_idx]
#time_idx = range(1452, 4388, 4)
#times = dataset.variables['time'][:]
time_plot_idx = 0 #Variable between 0, 4388. Notable 146 is 01-01-2014 + 200days (see KJP)

# Print a subset of the data
water_u = dataset.variables['water_u'][time_plot_idx, 0, lats_idx, lons_idx]
water_v = dataset.variables['water_v'][time_plot_idx, 0, lats_idx, lons_idx]

print(f'Elapsed time after reading data: {time()-start}')
# Create a plot
plt.figure(figsize=(6, 2))
plt.quiver(lons, lats, water_u, water_v, angles='xy', scale_units='xy', scale=1)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Water Vectors (water_u, water_v)')
print(f'Elapsed time after plotting: {time()-start}')
plt.show()

