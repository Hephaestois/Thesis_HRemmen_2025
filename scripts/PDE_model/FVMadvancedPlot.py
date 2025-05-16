from library.structures import Grid
from library.functions import progressBar
import numpy as np
import matplotlib.pyplot as plt
import math
from time import time
import netCDF4
from matplotlib import cm
from matplotlib.colors import Normalize

### Related to constants
diffusionMatrix = [[0.00025, 0], [0, 0.00025]] #Is converted to NParray later.
advectionVector = [0.1, 0] #Converted to NP later. Constant behaviour.


### Related to integration domain
x_range = [-29, -11]
y_range = [42, 47]
dx = 0.1 # dx =/= dy is supported. Some stepsizes will cause an idx-oo-bounds. add small perturbation to stepsize or choose differently. 
dy = 0.1 # Ex: 0.01 breaks, 0.012 doesn't.
dt = 0.01 # timestep between dataset swapping. scale: day.


### Related to dataset time and VF
startTime = 131496      #Hours since 01-01-2000. This repr. 01-01-2015
timeResolution = 24     #Hours between dataset snapshots. Intermediate timesteps use identical set.
simLengthDays = 100
endTime = startTime + timeResolution * simLengthDays

url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3'
# No spatial resolution for the dataset is necessary; it is interpolated to fit to the grid size.

### Start simulation related stuff

grid = Grid(x_range, y_range, dx ,dy)
grid.setDiffusionConstants(np.array(diffusionMatrix))
grid.setAdvectionConstant(np.array(advectionVector))
grid.setTimestep(dt)

grid.precalculateDiffusiveOperator(type="Neumann", direction="Horizontal")
grid.precalculateDiffusiveOperator(type="Neumann", direction="Vertical")
grid.precalculateAdvectiveOperator()

# ## IC: Gaussian
# A = 1
# x0 = (-25)
# y0 = (44.5)
# sigma_x = 1
# sigma_y = 1

# for i in grid.x_idxs:
#     for j in grid.y_idxs:
#         x,y = grid.itc(j, i)
#         value = A * math.exp(-((x - x0)**2) / (2 * sigma_x**2) - ((y - y0)**2) / (2 * sigma_y**2))
#         grid.addValue(grid.cti(*grid.itc(j, i)), value)
# ## End IC

# ## IC: point mass


# ## End IC

dataset = netCDF4.Dataset(url)
# times = [j for j in [i for i in dataset.variables['time'][:] if i >= startTime] if j <= endTime]
# longitudes = [j for j in [i for i in dataset.variables['lon'][:] if i >= min(x_range)] if j <= max(x_range)]
# latitudes = [j for j in [i for i in dataset.variables['lat'][:] if i >= min(y_range)] if j <= max(y_range)]

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
lon_mask = (lon_array >= min(x_range)) & (lon_array <= max(x_range))
lon_idx = np.where(lon_mask)[0]
longitudes = lon_array[lon_idx]

# Latitude indices and values
lat_mask = (lat_array >= min(y_range)) & (lat_array <= max(y_range))
lat_idx = np.where(lat_mask)[0]
latitudes = lat_array[lat_idx]
grid.setLonLatVals(dataset, lon_idx, lat_idx)

N_steps_per_day = int(1/dt)
start_time = time()




for i in range(simLengthDays):
    grid.addValue(grid.cti(-25, 44.5), 5)
    
    simTime = startTime + i*timeResolution #Hours since 2000
    simTimeIndex = np.searchsorted(times, simTime) + startTimeIndex #To access dataset
    
    #To plot a quiver later
    vf_x, vf_y = grid.getVectorField(dataset, lon_idx, lat_idx, simTimeIndex) #At the start of every 24 hours.
    
    for j in range(N_steps_per_day):
        grid.timeStep(diffusion=False, constantAdvection=False, VFAdvection=True)
        progressBar(i*N_steps_per_day + j, simLengthDays*N_steps_per_day-1, start_time, comment=grid.getTotalValue(), commentMessage='Mass')


print('Overflow Ratio:', grid.getOverflowRatio())
print('Overflow through bottom:', grid.getOverflowBottom())

matrix = grid.getMatrix()
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
plt.quiver(lon_grid[::3, ::3], lat_grid[::3, ::3], vf_x[::3, ::3], vf_y[::3, ::3], scale=4, color='k')
plt.plot((-25), (44.5), 'r.')
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('densityplot.png')
plt.show()


