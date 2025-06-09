# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Other imports
from library.agents import Walker
from library.functions import zipCoords, progressBar
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
import netCDF4


### Simulation options
# High level stuff
# N_swims = 200
# swim_length = 1000
# startpos = np.array([-25, 44.5])
# walk_opacity = 0.0066

N_swims = 200
swim_length = 100
startpos = np.array([-25, 44.5])
walk_opacity = 0.0066

### Options
longitude_data_stepsize = 1 #Multiples of 0.04 degree
latitude_data_stepsize  = 1 #Multiples of 0.08 degree
delta = 0
simulationTimeIndex = 133893 #Moment at which this simulation is ran. This is time CONSTANT vector field.


### END options

start = time.time()
url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3' # No spatial resolution for the dataset is necessary; it is interpolated onto the simulation grid size.
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

label_fontsize = 12
tick_fontsize = 12

#Math ends here, only plotting below.
plt.figure(figsize=[10, 3.2], dpi=150)
quiver_step=6
plt.quiver(longitudes[::quiver_step], latitudes[::quiver_step], water_u[::quiver_step, ::quiver_step], water_v[::quiver_step, ::quiver_step], scale=40, color='k')

#plt.quiver(longitudes, latitudes, water_u, water_v, angles='xy', scale_units='xy', scale=2)
points = []


for i in range(N_swims):
    progressBar(i, N_swims-1, start)
    Tutel = Walker(
        init_position=startpos,
        #init_probs=(0.25,0.25,0.25,0.25),
        init_probs=(0.174468, 0.28168, 0.09942134, 0.4444274),
        horizontalStepSize=0.02, 
        verticalStepSize=0.02
        )
    locations = []
    
    for _ in range(swim_length):
        Tutel.probdistance = 0
        while Tutel.probdistance < 1:
            locations.append(Tutel.traverseVF(vectorfield, 1))
        
        
        
    plotvals = zipCoords(locations)
    points.append([plotvals[0][-1], plotvals[1][-1]])
    
    if walk_opacity == 0:
        continue
    
    for j in range(len(plotvals[0])-1):
        plt.plot(plotvals[0][j:j+2], plotvals[1][j:j+2], color='red', alpha=walk_opacity)

for point in points:
    plt.plot(point[0][-1], point[1][-1], 'wo', markersize=4, markeredgecolor='black')
    
#plt.scatter(zipCoords(points)[0], zipCoords(points)[1], color='g', marker='.')       
plt.tight_layout() 
plt.plot(startpos[0], startpos[1], color="k", marker='.')
plt.xlabel("Longitude ($\degree$E)", fontsize=label_fontsize)
plt.ylabel("Latitude ($\degree$N)", fontsize=label_fontsize)
plt.tick_params(labelsize=tick_fontsize)

end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.savefig('randomWalk.png', bbox_inches='tight')