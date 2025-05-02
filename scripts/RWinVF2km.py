from library.agents import Walker
from library.functions import zipCoords, getVectorFieldFromExcel
import matplotlib.pyplot as plt
import time
import numpy as np
import netCDF4
import pickle

### Simulation options
# High level stuff
N_tutels = 40
N_simulation_steps = 300 #dont go beyond 638 fr fr, exceeds dataset bound
N_steps_per_timestep = 5

# Turtle related stuff
startpos = np.array([-25.6, 44.4])
initial_probability = (0.25, 0.25, 0.25, 0.25) #lrud
weight_self = 0.5 # Contribution due to own movement
weight_VF = 0.5   # Contribution due to vector field
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
delta = 8                   #For correcting size mismatch

### Plotting options
walk_opacity = 0.2


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

for _ in range(N_tutels):
    tutel = Walker(
        init_position=startpos,
        init_probs = initial_probability,
        horizontalStepSize=horizontalStepSize, 
        verticalStepSize=verticalStepSize,
        weight_self = weight_self, 
        weight_VF = weight_VF 
        )
    Tutels.append(tutel)
    paths.append([])

done = 0
for simstep, t in enumerate(simulationTimes):
    # Searchsorted find the place t would be put to maintain order. 
    # So this is the closest value to t that is no larger than t.
    simulationTimeIndex = np.searchsorted(times, t)+startTimeIndex
    print(simstep)    
    vectorfield['water_u']=dataset.variables['water_u'][simulationTimeIndex, 0, lats_idx, lons_idx]
    vectorfield['water_v']=dataset.variables['water_v'][simulationTimeIndex, 0, lats_idx, lons_idx]
    
    for j in range(N_tutels):
        if done > N_tutels*N_steps_per_timestep: 
            break
            
        for _ in range(N_steps_per_timestep):
            if Tutels[j].finished:
                done += 1
                print(f'Skipped turtle {j} at timestep {simstep}')
                continue
            
            done = 0
            Tutels[j].traverseContVectorField(vectorfield, n=1)
            paths[j].append(Tutels[j].position)
    
    if done > N_tutels*N_steps_per_timestep:
        print(f'Exited at simstep {simstep} as all turtles were done.')
        break
    

# Save the data so we can do graphical stuff on it.
with open('createdData.pkl', 'wb') as file:
    pickle.dump(paths, file)

end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")