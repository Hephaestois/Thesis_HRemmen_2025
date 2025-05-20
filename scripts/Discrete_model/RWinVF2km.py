from library.agents import Walker
from library.functions import zipCoords, progressBar
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
import time
import numpy as np
import netCDF4
import pickle

### Simulation options
# High level stuff
# N_tutels = 40
N_simulation_steps = 50 # N days of swimming. Dont go beyond 638 fr fr, exceeds dataset bound. 
N_steps_per_timestep = 10 #Adds up to approx. 2km, but should get its own logic in the program because radians are not equidistant
N_released_per_day = 1   #Gamma=5 in Painter, amount of released tutels

# Turtle related stuff
startpos = np.array([-25.6, 44.4]) #lon(x), lat(y)
initial_probability = (0.174468, 0.28168, 0.09942134, 0.4444274) #lrud
horizontalStepSize = 0.02 # Turtle step size, in degrees lat/long
verticalStepSize = 0.02   # Turtle step size, in degrees lat/long

# Time / dataset related stuff
startTime = 131496 #01-01-2015
timeResolution = 24 # This is regardless of the multiples of 3 hours 
                    # the dataset works with. 
endTime = startTime + timeResolution*N_simulation_steps


# Spatial dataset related stuff. #lat and #long should be the same length, delta is used to accomodate for this.
longitude_data_stepsize = 8 #Multiples of 0.04 degree
latitude_data_stepsize  = 4 #Multiples of 0.08 degree
delta = 8                   #For correcting size mismatch in latitudes/longitudes.

### END of options

start = time.time()
url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3'
dataset = netCDF4.Dataset(url)

lons_idx = range(1885,2113,longitude_data_stepsize)
lats_idx = range(2050,2176-delta,latitude_data_stepsize)

# These three are pretty important, as they are used to precompute some stuff, best saved locally
longitudes = dataset.variables['lon'][lons_idx] # Range -29.2, -11.28
print(longitudes)
latitudes = dataset.variables['lat'][lats_idx]  # Range 42.0, 46.48
times = [j for j in [i for i in dataset.variables['time'][:] if i >= startTime] if j <= endTime]
simulationTimes = list(range(startTime, endTime, 24))
startTimeIndex = list(dataset.variables['time'][:]).index(startTime)

vectorfield = dict()
vectorfield['latitude'] = latitudes
vectorfield['longitude'] = longitudes

Tutels = []
paths = []
start_frames = []

for simstep, t in enumerate(simulationTimes):
    for _ in range(N_released_per_day):
        tutel = Walker(
            init_position=startpos,
            init_probs=initial_probability,
            horizontalStepSize=horizontalStepSize, 
            verticalStepSize=verticalStepSize
        )
        Tutels.append(tutel)
        paths.append([])
        start_frames.append(simstep * N_steps_per_timestep)  # Frame when this turtle starts walking

    progressBar(simstep, N_simulation_steps-1, start)    

    # Searchsorted finds the place t would be put to maintain order. 
    # So this is the closest value to t that is no larger than t.
    simulationTimeIndex = np.searchsorted(times, t)+startTimeIndex
    ### NON-linterp
    vectorfield['water_u']=dataset.variables['water_u'][simulationTimeIndex, 0, lats_idx, lons_idx]
    vectorfield['water_v']=dataset.variables['water_v'][simulationTimeIndex, 0, lats_idx, lons_idx]

    ### Linterp
    # # Make the water grid linearly interpolatable
    # u_grid = dataset.variables['water_u'][simulationTimeIndex, 0, lats_idx, lons_idx]  # shape (lat, lon)
    # v_grid = dataset.variables['water_v'][simulationTimeIndex, 0, lats_idx, lons_idx]  # shape (lat, lon)
    
    # # Interpolators assume input in the form (lat, lon)
    # u_interp = RegularGridInterpolator((lats_idx, lons_idx), u_grid, bounds_error=False, fill_value=None)
    # v_interp = RegularGridInterpolator((lats_idx, lons_idx), v_grid, bounds_error=False, fill_value=None)

    # # Now create a vector field dictionary with interpolators
    # vectorfield['water_u'] = u_interp
    # vectorfield['water_v'] = v_interp
    
    
    for j, tutel in enumerate(Tutels):
        if tutel.finished:
            continue

        for _ in range(N_steps_per_timestep):
            if tutel.finished:
                continue
            
            tutel.traverseVF(vectorfield, n=1)
            paths[j].append(tutel.position)
    

print('Writing data to storage...')
# Save the data so we can do graphical stuff on it.
with open('createdData.pkl', 'wb') as file:
    pickle.dump((paths, start_frames), file)

print("Done!")

end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")