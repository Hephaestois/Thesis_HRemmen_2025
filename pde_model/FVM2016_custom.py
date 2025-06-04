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
x_range = [-29, -11]
y_range = [42, 47]
year = 2016 #For naming dataset, should only be changed between files.


### Related to dataset time and VF
startTime_1 = 140_256     # This repr. 01-01-2016, Hours since 01-01-2000. End at 30-04-2016
startTime_2 = 143_184     # This repr. 01-05-2016 (May)
startTime_3 = 149_808      # This repr. 01-02-2017 (Feb)

timeResolution = 24     # Hours between dataset snapshots. Intermediate timesteps use identical set.
endTime = startTime_1 + timeResolution * simLengthDays
quiver_step = int(np.floor(0.4/dx))

### Dataset url
url1 = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3' # No spatial resolution for the dataset is necessary; it is interpolated onto the simulation grid size.
url2 = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.2'
url3 = 'https://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_92.8'
### Start simulation related stuff

grid = Grid(x_range, y_range, dx ,dy)
grid.setDiffusionConstants(np.array(diffusionMatrix))
grid.setAdvectionConstant(advectionWeight*(np.array(advectionVector)))#/np.sqrt(np.sum(np.array(advectionVector)**2))))
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
dataset2 = netCDF4.Dataset(url2)
dataset3 = netCDF4.Dataset(url3)
e = 1e-3 #Small offset for mask boundaries

# Original arrays
time_array_1 = dataset1.variables['time'][:]
time_array_2 = dataset2.variables['time'][:]
time_array_3 = dataset3.variables['time'][:]


lon_array = dataset1.variables['lon'][:]
lat_array = dataset1.variables['lat'][:]

# Time indices and values for timeset 1
time_mask_1 = (time_array_1 >= startTime_1) & (time_array_1 <= endTime)
time_idx_1 = np.where(time_mask_1)[0]
times_1 = time_array_1[time_idx_1]
startTimeIndex_1 = list(time_array_1).index(startTime_1)

# Time indices for timeset 2
time_mask_2 = (time_array_2 >= startTime_2) & (time_array_2 <= endTime)
time_idx_2 = np.where(time_mask_2)[0]
times_2 = time_array_2[time_idx_2]
startTimeIndex_2 = list(time_array_2).index(startTime_2)

# Time indices for timeset 3
time_mask_3 = (time_array_3 >= startTime_3) & (time_array_3 <= endTime)
time_idx_3 = np.where(time_mask_3)[0]
times_3 = time_array_3[time_idx_3]
startTimeIndex_3 = list(time_array_3).index(startTime_3)

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
save_data(metadata, 'pde_onlyConstant', year, simLengthDays, f'{dx}x{dy}_{dt}', 'metadata')

start_time = time()
for i in range(simLengthDays):
    if initialCondition == 'inflow' and i<366:
        grid.addValue(grid.cti(-25, 44.5), 2)
    
    simTime = startTime_1 + i*timeResolution #Hours since 2000
    if simTime < startTime_2:
        simTimeIndex = np.searchsorted(times_1, simTime) + startTimeIndex_1
        dataset = dataset1
    elif simTime < startTime_3:
        simTimeIndex = np.searchsorted(times_2, simTime) + startTimeIndex_2
        dataset = dataset2
    else:
        simTimeIndex = np.searchsorted(times_3, simTime) + startTimeIndex_3
        dataset=dataset3
    
    #To plot a quiver later
    vf_x, vf_y = grid.getVectorField(dataset, lon_idx, lat_idx, simTimeIndex) #At the start of every 24 hours.
    save_data([grid.getMatrix(), vf_x, vf_y], 'pde_onlyConstant', year, simLengthDays, f'{dx}x{dy}_{dt}', i)

    for j in range(N_steps_per_day):
        grid.timeStep(diffusion=True, constantAdvection=True, VFAdvection=False)
        progressBar(i*N_steps_per_day + j, simLengthDays*N_steps_per_day-1, start_time, comment=grid.getTotalValue(), commentMessage='Mass')


save_data([grid.getMatrix(), vf_x, vf_y], 'pde_onlyConstant', year, simLengthDays, f'{dx}x{dy}_{dt}', simLengthDays)
