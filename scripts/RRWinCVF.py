from library.agents import Walker
from library.functions import zipCoords, getVectorFieldFromExcel, progressBar
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
import netCDF4


### Simulation options
# High level stuff
N_swims = 40
swim_length = 600
startpos = np.array([-25.6, 44.4])
walk_opacity = 0.2

### Options
N_steps = 800
longitude_data_stepsize = 16 #Multiples of 0.04 degree
latitude_data_stepsize  = 8 #Multiples of 0.08 degree
delta = 8
simulationTimeIndex = 131496 #Moment at which this simulation is ran. This is time CONSTANT vector field.

### END options

start = time.time()
url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3'
dataset = netCDF4.Dataset(url)

lons_idx = range(1885,2113,longitude_data_stepsize)
lats_idx = range(2050,2176-delta,latitude_data_stepsize)
longitudes = dataset.variables['lon'][lons_idx] # Range -29.2, -11.28
latitudes = dataset.variables['lat'][lats_idx]  # Range 42.0, 46.48
water_u = dataset.variables['water_u'][list(dataset.variables['time'][:]).index(simulationTimeIndex), 0, lats_idx, lons_idx]
water_v = dataset.variables['water_v'][list(dataset.variables['time'][:]).index(simulationTimeIndex), 0, lats_idx, lons_idx]

# construct our VF snapshot
vectorfield = dict()
vectorfield['latitude'] = latitudes
vectorfield['longitude'] = longitudes
vectorfield['water_u'] = water_u
vectorfield['water_v'] = water_v


#Math ends here, only plotting below.
plt.figure(figsize=[10, 4], dpi=400)
plt.quiver(longitudes, latitudes, water_u, water_v, angles='xy', scale_units='xy', scale=2)
points = []


for i in range(N_swims):
    progressBar(i, N_swims-1, start)
    Tutel = Walker(
        init_position=startpos,
        horizontalStepSize=0.05, 
        verticalStepSize=0.05
        )
    locations = []
    for _ in range(swim_length):
        locations.append(Tutel.traverseVF(vectorfield, 1))
        
    plotvals = zipCoords(locations)
    points.append([plotvals[0][-1], plotvals[1][-1]])
    
    if walk_opacity == 0:
        continue
    
    for j in range(len(plotvals[0])-1):
        plt.plot(plotvals[0][j:j+2], plotvals[1][j:j+2], color='red', alpha=walk_opacity)
    
#plt.scatter(zipCoords(points)[1], zipCoords(points)[0], color='g', marker='.', zorder=10)        
plt.plot(startpos[0], startpos[1], color="k", marker='.')

end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.savefig('randomWalk.png')