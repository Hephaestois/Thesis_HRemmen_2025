from library.agents import Walker
from library.functions import zipCoords, getVectorFieldFromExcel, progressBar
import matplotlib.pyplot as plt
import time
import numpy as np
import netCDF4
import pickle

### Simulation options
# High level stuff
# N_tutels = 40
N_simulation_steps = 20 # N days of swimming. Dont go beyond 638 fr fr, exceeds dataset bound. 
N_steps_per_timestep = 5 #Adds up to approx. 2km, but should get its own logic in the program because radians are not equidistant
N_released_per_day = 1   #Gamma=5 in Painter, amount of released tutels

# Turtle related stuff
startpos = np.array([-25.6, 44.4])
initial_probability = (0.25, 0.25, 0.25, 0.25) #lrud
horizontalStepSize = 0.05 # Turtle step size, in degrees lat/long
verticalStepSize = 0.05   # Turtle step size, in degrees lat/long

# Time / dataset related stuff
startTime = 131496 #01-01-2015
timeResolution = 24 # This is regardless of the multiples of 3 hours 
                    # the dataset works with. 
endTime = startTime + timeResolution*N_simulation_steps


# Spatial dataset related stuff
longitude_data_stepsize = 16 #Multiples of 0.04 degree
latitude_data_stepsize  = 8 #Multiples of 0.08 degree
delta = 8                   #For correcting size mismatch in latitudes/longitudes.

### END of options

start = time.time()
url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3'
dataset = netCDF4.Dataset(url)

lons_idx = range(1885,2113,longitude_data_stepsize)
lats_idx = range(2050,2176-delta,latitude_data_stepsize)

# These three are pretty important, as they are used to precompute some stuff, best saved locally
longitudes = dataset.variables['lon'][lons_idx] # Range -29.2, -11.28
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

    # Searchsorted find the place t would be put to maintain order. 
    # So this is the closest value to t that is no larger than t.
    simulationTimeIndex = np.searchsorted(times, t)+startTimeIndex
    vectorfield['water_u']=dataset.variables['water_u'][simulationTimeIndex, 0, lats_idx, lons_idx]
    vectorfield['water_v']=dataset.variables['water_v'][simulationTimeIndex, 0, lats_idx, lons_idx]
    
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