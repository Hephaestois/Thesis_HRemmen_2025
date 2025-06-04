# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Other imports
from library.agents import Walker
from library.functions import zipCoords
import netCDF4
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np

### Options
N_steps = 800
longitude_data_stepsize = 1 #Multiples of 0.04 degree
latitude_data_stepsize  = 1 #Multiples of 0.08 degree
delta = 0
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

Tutel = Walker(init_position=np.array([-25.6, 44.4]), horizontalStepSize=0.02, verticalStepSize=0.02)

locations=[]
for _ in range(N_steps):
    locations.append(Tutel.traverseVF(vectorfield))

plotvals = zipCoords(locations)
plt.figure(dpi=600)
quiver_step=1
plt.quiver(longitudes[::quiver_step], latitudes[::quiver_step], water_u[::quiver_step, ::quiver_step], water_v[::quiver_step, ::quiver_step], scale=40, color='k')
for i in range(len(plotvals[0])-1):
    plt.plot(plotvals[0][i:i+2], plotvals[1][i:i+2], color='red', alpha=0.5)
#plt.plot(plotvals[0][0], plotvals[1][0], color="k", marker='.')


end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.savefig('randomWalk.png')