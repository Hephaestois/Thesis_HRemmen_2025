# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Handle arguments
if len(sys.argv) != 5:
    print("Usage: python FVM[year].py <sim_days> <dx> <dy> <dt>")
    sys.exit(1)

simLengthDays = int(sys.argv[1])
dx = float(sys.argv[2])
dy = float(sys.argv[3])
dt = float(sys.argv[4])

# Other imports
from library.structures import Grid
from library.functions import progressBar, save_data
import numpy as np
import matplotlib.pyplot as plt
import math
from time import time
import netCDF4
import pickle
from matplotlib import cm
from matplotlib.colors import Normalize

#
### Start settings
#

### Related to constants
diffusionMatrix = [[0.00009, 0], [0, 0.00011]] #Converted to NParray later. Diffusion behaviour
advectionVector = [0.108, -0.345] #Converted to NP later. Only defines direction, length is set using advectionWeight (analog to swimspeed!!!)
km_travel_per_day = 2 # Daily swimming distance
advectionWeight = km_travel_per_day/100 
initialCondition = 'inflow' #'delta' or 'gauss'. See grid.ic for details, or manage manually using grid.addValue and grid.cti (coord. to index)

### Related to integration domain
# 2018-2024: lons are in *East
x_range = [331, 349]
y_range = [42, 47]
year = 2020 #For naming dataset, should only be changed between files.


# TODO: Change these to 2024
### Related to dataset time and VF
startTime_1 = 175_344      # This repr. 01-01-2024, Hours since 01-01-2000.
startTime_2 = 300_000      # a high enough number!
timeResolution = 24     # Hours between dataset snapshots. Intermediate timesteps use identical set.
endTime = startTime_1 + timeResolution * simLengthDays
quiver_step = int(np.floor(0.4/dx))

### Dataset url
url1 = 'https://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0/uv3z/2020' # No spatial resolution for the dataset is necessary; it is interpolated onto the simulation grid size.
### Start simulation related stuff

grid = Grid(x_range, y_range, dx ,dy)
grid.setDiffusionConstants(np.array(diffusionMatrix))
grid.setAdvectionConstant(advectionWeight*(np.array(advectionVector)/np.sqrt(np.sum(np.array(advectionVector)**2))))
grid.setTimestep(dt)

grid.precalculateDiffusiveOperator(type="Neumann", direction="Horizontal")
grid.precalculateDiffusiveOperator(type="Neumann", direction="Vertical")
grid.precalculateAdvectiveOperator()
grid.ic(initialCondition, 400)

#
### End simulation related stuff
#

#
### Start vectorfield data
#

dataset1 = netCDF4.Dataset(url1)
e = 1e-3 #Small offset for mask boundaries

# Original arrays
time_array_1 = dataset1.variables['time'][:]

lon_array = dataset1.variables['lon'][:]
lat_array = dataset1.variables['lat'][:]


# Time indices and values for timeset 1
time_mask_1 = (time_array_1 >= startTime_1) & (time_array_1 <= endTime)
time_idx_1 = np.where(time_mask_1)[0]
times_1 = time_array_1[time_idx_1]
startTimeIndex_1 = list(time_array_1).index(startTime_1)

# Longitude indices and values
lon_mask = (lon_array >= min(x_range)-e) & (lon_array <= max(x_range)+e)
lon_idx = np.where(lon_mask)[0]
longitudes = lon_array[lon_idx]

# Latitude indices and values
lat_mask = (lat_array >= min(y_range)-e) & (lat_array <= max(y_range)+e)
lat_idx = np.where(lat_mask)[0]
latitudes = lat_array[lat_idx]
grid.setLonLatVals(dataset1, lon_idx, lat_idx)

N_steps_per_day = int(1/dt)

#
### End vectorfield data
#

#
### Start main loop
#
metadata = {'dx': dx, 'dy': dx, 'dt': dt}
save_data(metadata, 'pde', year, simLengthDays, f'{dx}x{dy}_{dt}', 'metadata')

start_time = time()
for i in range(simLengthDays):
    if initialCondition == 'inflow':
        grid.addValue(grid.cti(335, 44.5), 2)
    
    simTime = startTime_1 + i*timeResolution #Hours since 2000
    simTimeIndex = np.searchsorted(times_1, simTime) + startTimeIndex_1 #To access dataset
    dataset = dataset1

    #To plot a quiver later
    vf_x, vf_y = grid.getVectorField(dataset, lon_idx, lat_idx, simTimeIndex) #At the start of every 24 hours.
    
    save_data([grid.getMatrix(), vf_x, vf_y], 'pde', year, simLengthDays, f'{dx}x{dy}_{dt}', i)
    
    for j in range(N_steps_per_day):
        grid.timeStep(diffusion=True, constantAdvection=True, VFAdvection=True)
        progressBar(i*N_steps_per_day + j, simLengthDays*N_steps_per_day-1, start_time, comment=grid.getTotalValue(), commentMessage='Mass')


save_data([grid.getMatrix(), vf_x, vf_y], 'pde', year, simLengthDays, f'{dx}x{dy}_{dt}', simLengthDays)


# print('Overflow Ratio:', grid.getOverflowRatio())
# print('Overflow through bottom:', grid.getOverflowBottom())

# masked_matrix = np.ma.masked_less(matrix, 0.01)

# # Create a colormap and set the "bad" (masked) color to white or gray
# cmap = cm.viridis.copy()
# cmap.set_bad(color='white')  # Or 'white'

# plt.figure(figsize=[8, 3], dpi=180)
# plt.title(f"Grid step {dx}x{dy}, dt={dt}. {simLengthDays} days simulation")
# # Use masked matrix and custom colormap
# plt.imshow(masked_matrix, origin='lower', extent=[-29, -11, 42, 47],
#            aspect=1, vmin=0.01, vmax=np.max(matrix), cmap=cmap)

# lon_grid, lat_grid = np.meshgrid(grid.x_s, grid.y_s)
# plt.quiver(lon_grid[::quiver_step, ::quiver_step], lat_grid[::quiver_step, ::quiver_step], vf_x[::quiver_step, ::quiver_step], vf_y[::quiver_step, ::quiver_step], scale=40, color='k')
# plt.plot((-25), (44.5), 'r.')
# plt.colorbar()
# plt.xlabel('x')
# plt.ylabel('y')
# plt.savefig(f'{year}_{simLengthDays}d.png')
# plt.show()


