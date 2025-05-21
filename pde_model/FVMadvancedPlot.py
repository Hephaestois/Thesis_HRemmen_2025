# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

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
diffusionMatrix = [[0.00456, 0], [0, 0.00544]] #Converted to NParray later. Diffusion behaviour
advectionVector = [0.108, -0.345] #Converted to NP later. Only defines direction, length is set using advectionWeight (analog to swimspeed!!!)
km_travel_per_day = 2 # Daily swimming distance
advectionWeight = km_travel_per_day/100 
initialCondition = 'inflow' #'delta' or 'gauss'. See grid.ic for details, or manage manually using grid.addValue and grid.cti (coord. to index)

### Related to integration domain
x_range = [-29, -11]
y_range = [42, 47]
dx = 0.1 # dx =/= dy is supported. Some stepsizes will cause an idx-oo-bounds. add small perturbation to stepsize or choose differently. 
dy = 0.1 # Ex: 0.01 breaks, 0.012 doesn't.
dt = 0.01 # timestep between dataset swapping. scale: day.
simLengthDays = 100

### Related to dataset time and VF
year = 2016
startTime = 140256      #Hours since 01-01-2000. This repr. 01-01-2016
timeResolution = 24     #Hours between dataset snapshots. Intermediate timesteps use identical set.
endTime = startTime + timeResolution * simLengthDays
quiver_step = int(np.floor(0.4/dx))

### Dataset url. 2 are needed as the simulation range crosses a time bound
url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3' # No spatial resolution for the dataset is necessary; it is interpolated onto the simulation grid size.
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

dataset = netCDF4.Dataset(url)
e = 1e-3 #Small offset for mask boundaries

# Original arrays
time_array = dataset.variables['time'][:]
lon_array = dataset.variables['lon'][:]
lat_array = dataset.variables['lat'][:]

# Time indices and values
time_mask = (time_array >= startTime) & (time_array <= endTime)
time_idx = np.where(time_mask)[0]
times = time_array[time_idx]
startTimeIndex = list(time_array).index(startTime)

# Longitude indices and values
lon_mask = (lon_array >= min(x_range)-e) & (lon_array <= max(x_range)+e)
lon_idx = np.where(lon_mask)[0]
longitudes = lon_array[lon_idx]

# Latitude indices and values
lat_mask = (lat_array >= min(y_range)-e) & (lat_array <= max(y_range)+e)
lat_idx = np.where(lat_mask)[0]
latitudes = lat_array[lat_idx]
grid.setLonLatVals(dataset, lon_idx, lat_idx)

N_steps_per_day = int(1/dt)

#
### End vectorfield data
#

#
### Start main loop
#

matrix=grid.getMatrix()
vf_x, vf_y = grid.getVectorField(dataset, lon_idx, lat_idx, 0) #At the start of every 24 hours.
save_data([matrix, vf_x, vf_y], 'pde', year, simLengthDays, f'{dx}x{dy}_{dt}', 0)

start_time = time()
for i in range(simLengthDays):
    if initialCondition == 'inflow':
        grid.addValue(grid.cti(-25, 44.5), 5)
    
    simTime = startTime + i*timeResolution #Hours since 2000
    simTimeIndex = np.searchsorted(times, simTime) + startTimeIndex #To access dataset
    
    #To plot a quiver later
    vf_x, vf_y = grid.getVectorField(dataset, lon_idx, lat_idx, simTimeIndex) #At the start of every 24 hours.
        
    for j in range(N_steps_per_day):
        grid.timeStep(diffusion=False, constantAdvection=True, VFAdvection=False)
        progressBar(i*N_steps_per_day + j, simLengthDays*N_steps_per_day-1, start_time, comment=grid.getTotalValue(), commentMessage='Mass')
    
    matrix = grid.getMatrix()
    save_data([matrix, vf_x, vf_y], 'pde', year, simLengthDays, f'{dx}x{dy}_{dt}', 0)


with open('matrix.pkl', 'wb') as f:
    pickle.dump(matrix, f)

print('Overflow Ratio:', grid.getOverflowRatio())
print('Overflow through bottom:', grid.getOverflowBottom())

masked_matrix = np.ma.masked_less(matrix, 0.01)

# Create a colormap and set the "bad" (masked) color to white or gray
cmap = cm.viridis.copy()
cmap.set_bad(color='white')  # Or 'white'

plt.figure(figsize=[8, 3], dpi=180)
plt.title(f"Grid step {dx}x{dy}, dt={dt}. {simLengthDays} days simulation")
# Use masked matrix and custom colormap
plt.imshow(masked_matrix, origin='lower', extent=[-29, -11, 42, 47],
           aspect=1, vmin=0.01, vmax=np.max(matrix), cmap=cmap)

lon_grid, lat_grid = np.meshgrid(grid.x_s, grid.y_s)
plt.quiver(lon_grid[::quiver_step, ::quiver_step], lat_grid[::quiver_step, ::quiver_step], vf_x[::quiver_step, ::quiver_step], vf_y[::quiver_step, ::quiver_step], scale=40, color='k')
plt.plot((-25), (44.5), 'r.')
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('densityplot.png')
plt.show()


